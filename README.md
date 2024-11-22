# StackExchange XML data to Postgres

This project processes large XML data dumps from StackExchange and imports them into a PostgreSQL database. The data is parsed from XML files and mapped to specific database tables based on predefined schemas.

- Database Schema: The script automatically matches the XML data to the corresponding PostgreSQL table columns.
- This project uses the SQL structure provided in the repository [stackexchange-dump-to-postgres](https://github.com/Networks-Learning/stackexchange-dump-to-postgres) as a foundation. Some updates have been made to adapt the schema to the current StackExchange data format.


## Prerequisites

1. **Python 3.9 or later**: Make sure Python is installed on your system.
2. **PostgreSQL**: Ensure you have a running PostgreSQL instance.

## Setup Instructions
### 1. Create a PostgreSQL Database
- Log into your PostgreSQL server:
  ``` console
  psql -U your_username
  ```
- Create a new database:
   ```sql
    CREATE DATABASE dbname;
   ```        
### 2. Configure the Environment Variables
Create a .env file in the project root directory and fill in the database connection details   
```make
DATABASE=dbname
HOST=localhost
PORT=5432
USER=your_username
PASS=your_password
```
### 3. Download and Extract the StackExchange Dump
- Download the XML data dump from the official StackExchange archive: https://ia600508.us.archive.org/30/items/stackexchange/
- Extract the downloaded files into the xml/ folder located in the root of this project.

### 4. Install Python Dependencies
- Install the required Python libraries using dependencies.txt

``` console
$ pip install -r dependencies.txt
```
5. Run the Import Script
- Execute the main script to process the XML and populate the database:
```bash
python main.py
```

