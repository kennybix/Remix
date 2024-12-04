import pandas as pd
import pandasql as psql
import os


class DataSystem:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.datasets = {}
        self.load_datasets()

    def load_datasets(self):
        # Load all datasets in the folder
        for file_name in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, file_name)
            if os.path.isfile(file_path):
                file_extension = file_name.split('.')[-1].lower()
                dataset_name = file_name.split('.')[0]
                try:
                    if file_extension == 'csv':
                        self.datasets[dataset_name] = pd.read_csv(file_path)
                    elif file_extension in ['xls', 'xlsx']:
                        self.datasets[dataset_name] = pd.read_excel(file_path)
                    elif file_extension == 'json':
                        self.datasets[dataset_name] = pd.read_json(file_path)
                except Exception as e:
                    print(f"Error loading {file_name}: {e}")

    def query_pds(self, query):
        # Execute SQL query on the datasets available in the folder
        return psql.sqldf(query, {**locals(), **self.datasets})

def process_data(data):
    """Generate a summary of the DataFrame."""
    try:
        return data#.describe()
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        return pd.DataFrame({'Error': [str(e)]})
