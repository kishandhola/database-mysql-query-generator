import mysql.connector
import os

# Gather database connection details from the user
host = input("Enter database host: ")
user = input("Enter database root: ")
password = input("Enter database password: ")
database = input("Enter database database name: ")

# Connect to the database using provided details
db = mysql.connector.connect(host=host, user=user, password=password, database=database)
cursor = db.cursor()
cursor.execute("SHOW TABLES")
all_tables = cursor.fetchall()

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

# Ensure the database folder exists
create_folder_if_not_exists(database)

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

# Iterate through each table and generate SQL queries
for table_name in all_tables:
    t_name = table_name[0]
    cursor.execute(f"SHOW COLUMNS FROM {t_name}")
    all_columns = cursor.fetchall()

    # Construct field names part of the query
    field_names = ", ".join([field[0] for field in all_columns])

    # Construct values part of the query
    value_strs = []
    for field in all_columns:
        field_name, field_type = field[0], field[1]
        if requires_quotes(field_type):
            value_strs.append("'`${" + field_name + "}`'")
        else:
            value_strs.append("`${" + field_name + "}`")

    value_part = ", ".join(value_strs)

    # Construct the final insert query
    insert_query = f"INSERT INTO {t_name} ({field_names}) VALUES ({value_part});"
    print(insert_query)

    # Construct set part of the update query
    set_parts = []
    primary_field = get_primary_key(t_name)
    for field in all_columns:
        field_name, field_type = field[0], field[1]
        if field_name != primary_field:
            if requires_quotes(field_type):
                set_parts.append(f"{field_name} = '`${{{field_name}}}`'")
            else:
                set_parts.append(f"{field_name} = `${{{field_name}}}`")

    set_part = ", ".join(set_parts)
    condition = f"{primary_field} = `${{{primary_field}}}`"

    # Construct the final update query
    update_query = f"UPDATE {t_name} SET {set_part} WHERE {condition};"
    print(update_query)

    # Construct the final delete query
    delete_query = f"DELETE FROM {t_name} WHERE {condition};"
    print(delete_query)

    # Construct the final select all fields query
    select_all_field_query = f"SELECT * FROM {t_name} WHERE {condition};"
    print(select_all_field_query)

    # Construct the final select specific fields query
    select_specific_field_query = (
        "SELECT {fields} FROM {t_name} WHERE {condition};".format(
            fields=", ".join([field[0] for field in all_columns]),
            t_name=t_name,
            condition=condition
        )
    )
    
    # Write all queries to a text file within the database folder
    with open(f'{database}/{t_name}.txt', 'w') as file:
        file.write(
            "Insert Query\n" + insert_query + "\n\n\n" +
            "Update Query\n" + update_query + "\n\n\n" +
            "Delete Query\n" + delete_query + "\n\n\n" +
            "Select All Field Query\n" + select_all_field_query + "\n\n\n" +
            "Select Specific Field Query\n" + select_specific_field_query
        )

    print("----------------------------------------------------------------------------")
