# ReMix: LLM-Enhanced SQL Query Assistant

An intuitive tool for querying and interacting with local datasets (CSV, Excel, JSON), powered by a Large Language Model (LLM) to assist in SQL query generation, fixing, and execution. This lightweight application combines simplicity with AI-driven capabilities to make data querying more accessible and efficient.

![ReMix App](images/remix-app-1.png)
---

## Features
- **Folder Selection**: Browse and load local datasets dynamically.
![Folder Selection](images/remix-app-1b.png)
- **SQL Query Execution**: Run SQL queries on structured data with real-time previews.
![SQL Query Execution](images/remix-app-2.png)
- **LLM-Powered Query Fixing**: Automatically fix broken SQL queries or generate SQL queries from plain-text prompts using an integrated LLM.
![LLM Fixing](images/remix-app-3.png)
- **Data Export**: Download query results as a CSV file for further analysis.
![Data Export](images/remix-app-5.png)
- **Interactive Interface**: User-friendly web interface built with Flask and Bootstrap.
![Interactive Interface](images/remix-app-4.png)
---

## Tech Stack
- **Backend**: Flask, Pandas, pandasql
- **Frontend**: Bootstrap 4, HTML, JavaScript
- **AI Integration**: Groq API for LLM-based query generation and fixing
- **Environment Management**: dotenv for secure key storage

---

## Requirements
- Python 3.8 or higher
- Libraries:
  - Flask
  - pandas
  - pandasql
  - python-dotenv
  - Groq API SDK

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/kennybix/remix.git
cd remix
```

