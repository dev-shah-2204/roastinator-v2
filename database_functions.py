"""
Common functions that will be used in many files
"""

def fetch_all(cursor, table):
    cursor.execute(f"SELECT * FROM {table}")
    return cursor

def fetch_specific(cursor, table, item_name, item_specifics):
    cursor.execute(f"SELECT * FROM {table} where {item_name} = '{item_specifics}'")
    return cursor
