from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
import os
# from data_system import DataSystem, load_data_from_folder, process_data  # Corrected imports
from data_system import DataSystem, process_data  # Corrected imports

from groq import Groq  # Import Groq client
from werkzeug.utils import secure_filename
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize the Groq client with your API key
client = Groq(api_key=GROQ_API_KEY)  # Replace with your actual Groq API key

app = Flask(__name__)
app.secret_key = "supersecretkey"
data_system = None
folder_path = None
query_result = None

@app.route('/open_folder_dialog', methods=['GET'])
def open_folder_dialog():
    """Handle the request to open the folder selection dialog."""
    try:
        folder_path = filedialog.askdirectory()  # Open the folder dialog
        if folder_path:
            return jsonify({'folder_path': folder_path})
        else:
            return jsonify({'error': 'No folder selected.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    global data_system, folder_path, query_result

    files = []
    preview_data = None
    sql_query = request.form.get('sql_query', '')  # Preserve the query
    preview_count = request.form.get('preview_count', '10')  # Preserve preview count
    result_message = None

    if request.method == 'POST':
        # Handle Folder Browsing
        if 'folder_path' in request.form:
            folder_path = request.form['folder_path']
            if folder_path:
                try:
                    files = os.listdir(folder_path)
                    data_system = DataSystem(folder_path)  # Initialize DataSystem with folder path
                except Exception as e:
                    flash(f"Error initializing DataSystem: {str(e)}", 'error')
                    return render_template('index.html', files=[], folder_path=folder_path)

            else:
                flash("No folder selected.", 'error')

        # Handle SQL Query Execution
        elif 'query' in request.form:
            query = request.form['sql_query']
            preview_count = int(request.form.get('preview_count', 10))

            if data_system:
                try:
                    query_result = data_system.query_pds(query)  # Execute the query
                    preview_data = process_data(query_result).head(preview_count).to_html(classes='table table-striped')
                except Exception as e:
                    flash(f"Error executing query: {str(e)}", 'error')

        # Handle SQL Query Fix using Groq API
        elif 'fix_query' in request.form:
            user_input = request.form['hidden_sql_query']
            fixed_query, result_message = fix_query_using_groq(user_input)
            flash(result_message)
            return render_template('index.html', files=files, folder_path=folder_path, sql_query=fixed_query)

        # Handle CSV Download
        elif 'download_csv' in request.form:
            if query_result is not None:
                return download_csv()
            else:
                flash("No query result available to download.", 'error')

    # return render_template('index.html', files=files, folder_path=folder_path,
    #                        preview_count=request.form.get('preview_count', '10'), preview_data=preview_data)
    return render_template('index.html', files=files, folder_path=folder_path, 
                           sql_query=sql_query, preview_count=preview_count, preview_data=preview_data)

@app.route('/download', methods=['GET', 'POST'])
def download_csv():
    """Download the query result as a CSV file."""
    if query_result is not None:
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the main Tk window

            save_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )

            if save_path:
                query_result.to_csv(save_path, index=False)
                flash("Query result downloaded successfully.", 'success')
            else:
                flash("Download cancelled.", 'warning')

        except Exception as e:
            flash(f"Error during download: {str(e)}", 'error')

    else:
        flash("No query result available to download.", 'error')

    return redirect(url_for('index'))

def fix_query_using_groq(user_input):
    """
    Use the Groq API to fix the SQL query or generate a new one.
    """
    try:
        # Create a completion request with the user prompt or SQL code
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior data engineer. Your job is to either "
                        "fix the provided SQL query or generate a new SQL query "
                        "based on the user's prompt. Only return the SQL code, "
                        "without any additional explanation or comments."
                    )
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            temperature=0.7,
            max_tokens=512,
            top_p=1,
            stream=False,
            stop=None,
        )

        # Extract the SQL response from Groq
        fixed_query = completion.choices[0].message.content
        return fixed_query, "Query Fixed"
    except Exception as e:
        return user_input, f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
