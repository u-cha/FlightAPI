import sqlite3


class DataBaseService:
    def __init__(self, db_address):
        self.__db_address = db_address
        self.__error = None
        self.__data = None

    @property
    def db_address(self):
        return self.__db_address

    @property
    def error(self):
        return self.__error

    @property
    def data(self):
        return self.__data

    def __manipulate_database(self, sql_query, params=None):
        try:
            with sqlite3.connect(self.__db_address) as db_connection:
                db_cursor = db_connection.cursor()
                if params:
                    db_cursor.execute(sql_query, params)
                    db_connection.commit()
                else:
                    db_cursor.execute(sql_query)
                    db_connection.commit()
        except sqlite3.Error as error:
            self.__error = error
        finally:
            if not self.__error:
                self.__data = db_cursor
            return self

    def get_all_entries_from_table(self, table_name):
        sql_query = f'SELECT * FROM {table_name}'
        return self.__manipulate_database(sql_query)

    def get_entries_by_kwargs(self, table_name, **kwargs):
        if kwargs:
            search_params = ' AND '.join([f'{key}="{kwargs[key]}"' for key in kwargs])
            sql_query = f'SELECT * FROM {table_name} WHERE {search_params}'
        else:
            sql_query = f'SELECT * FROM {table_name}'
        return self.__manipulate_database(sql_query)

    def insert_entry_into_table(self, table_name, **kwargs):
        column_names = tuple(kwargs.keys())
        params = tuple(kwargs.values())
        sql_query = f'INSERT INTO {table_name} {column_names} VALUES {params}'
        self.__manipulate_database(sql_query)
        return self.get_entries_by_kwargs(table_name, **kwargs)
