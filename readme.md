# Database Query Generator

This Python program connects to a MySQL database, retrieves metadata
about the tables and columns, and generates various SQL queries for each
table. The queries include `INSERT`, `UPDATE`, `DELETE`, and `SELECT`
statements. The generated queries are saved into text files within a
folder named after the database.

## Table of Contents

-   [Features](#features)
-   [Requirements](#requirements)
-   [Installation](#installation)
-   [Usage](#usage)
-   [Functions](#functions)
    -   [create_folder_if_not_exists](#create_folder_if_not_exists)
    -   [requires_quotes](#requires_quotes)
    -   [get_primary_key](#get_primary_key)
-   [Generating Queries](#generating-queries)
-   [File Structure](#file-structure)
-   [Examples](#examples)
-   [License](#license)

## Features

-   Connects to a MySQL database using user-provided credentials.
-   Automatically creates a folder for the database if it doesn't exist.
-   Retrieves metadata about all tables and columns in the database.
-   Generates `INSERT`, `UPDATE`, `DELETE`, and `SELECT` SQL queries for
    each table.
-   Saves the generated queries into text files, one for each table.

## Requirements

-   Python 3.x
-   `mysql-connector-python` package for connecting to the MySQL
    database.

## Installation

1.  **Clone the repository**:

        git clone https://github.com/kishandhola/database-query-generator.git
        cd database-query-generator

2.  **Install the required packages**:

        pip install mysql-connector-python

## Usage

1.  **Run the script**:

        python generate_sql_queries.py

2.  **Provide the required database credentials** when prompted:

    -   **Host**: The hostname or IP address of the MySQL server.
    -   **User**: The username to connect to the MySQL server.
    -   **Password**: The password for the MySQL user.
    -   **Database**: The name of the database to generate queries for.

3.  **Check the generated files**: The queries will be saved in a folder
    named after your database.

## Functions

### create_folder_if_not_exists

    def create_folder_if_not_exists(folder_path):
        """
        Create a folder if it does not exist.

        Parameters:
            folder_path (str): The path of the folder to create.
        """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder '{folder_path}' created.")
        else:
            print(f"Folder '{folder_path}' already exists.")

This function ensures that a folder exists at the specified path. If the
folder does not exist, it creates it.

### requires_quotes

    def requires_quotes(data_type):
        """
        Check if a given data type requires quotes.

        Parameters:
            data_type (str): The data type to check.

        Returns:
            bool: True if the data type requires quotes, False otherwise.
        """
        need_quotes = {
            'varchar': True,
            'text': True,
            'char': True,
            'datetime': True,
            'timestamp': True,
            'date': True,
            'int': False,
            'bigint': False,
            'float': False,
            'double': False
        }
        
        for key in need_quotes:
            if key in data_type:
                return need_quotes[key]
        return False

This function checks if a given data type requires quotes in SQL
statements. For example, string types like `varchar` and `text` require
quotes, while numeric types like `int` and `float` do not.

### get_primary_key

    def get_primary_key(table_name):
        """
        Get the primary key of a table.

        Parameters:
            table_name (str): The name of the table.

        Returns:
            str: The name of the primary key column.
        """
        cursor.execute(f"SHOW KEYS FROM {table_name} WHERE Key_name = 'PRIMARY'")
        primary_key = cursor.fetchall()
        return primary_key[0][4]

This function retrieves the primary key column of a given table. It
executes a SQL query to get the primary key information from the table
metadata.

## Generating Queries

The main script iterates through each table in the database, retrieves
metadata about the columns, and generates the following SQL queries:

-   **INSERT Query**:

        INSERT INTO table_name (column1, column2, ...) VALUES (${column1}, ${column2}, ...);

-   **UPDATE Query**:

        UPDATE table_name SET column1 = ${column1}, column2 = ${column2}, ... WHERE primary_key = ${primary_key};

-   **DELETE Query**:

        DELETE FROM table_name WHERE primary_key = ${primary_key};

-   **SELECT All Fields Query**:

        SELECT * FROM table_name WHERE primary_key = ${primary_key};

-   **SELECT Specific Fields Query**:

        SELECT column1, column2, ... FROM table_name WHERE primary_key = ${primary_key};

## File Structure

The generated files will be organized in the following structure:

    database-query-generator/
    ├── database_name/
    │   ├── table1.txt
    │   ├── table2.txt
    │   └── ...
    └── generate_queries.py

Each text file will contain the generated SQL queries for a specific
table.

## Examples

### Example Database

Consider a database named `example_db` with two tables: `users` and
`orders`.

#### `users` Table

| id  | name  | email          |
|-----|-------|----------------|
| 1   | Alice | alice@mail.com |
| 2   | Bob   | bob@mail.com   |

#### `orders` Table

| order_id | user_id | amount |
|----------|---------|--------|
| 1        | 1       | 100.50 |
| 2        | 2       | 200.00 |

### Generated Queries

For the `users` table, the generated queries would look like this:

**`example_db/users.txt`**:

    Insert Query
    INSERT INTO users (id, name, email) VALUES (${id}, '${name}', '${email}');

    Update Query
    UPDATE users SET name = '${name}', email = '${email}' WHERE id = ${id};

    Delete Query
    DELETE FROM users WHERE id = ${id};

    Select All Field Query
    SELECT * FROM users WHERE id = ${id};

    Select Specific Field Query
    SELECT id, name, email FROM users WHERE id = ${id};

For the `orders` table, the generated queries would look like this:

**`example_db/orders.txt`**:

    Insert Query
    INSERT INTO orders (order_id, user_id, amount) VALUES (${order_id}, ${user_id}, ${amount});

    Update Query
    UPDATE orders SET user_id = ${user_id}, amount = ${amount} WHERE order_id = ${order_id};

    Delete Query
    DELETE FROM orders WHERE order_id = ${order_id};

    Select All Field Query
    SELECT * FROM orders WHERE order_id = ${order_id};

    Select Specific Field Query
    SELECT order_id, user_id, amount FROM orders WHERE order_id = ${order_id};

## License

This project is licensed under the MIT License. See the LICENSE file for
more details.
