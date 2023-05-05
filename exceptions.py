class DataBaseError(Exception):
    """Marks all DataBase errors including SQLite Errors
    (bad SQL queries, unavailable tables, UNIQUE constraint breaches, etc..."""