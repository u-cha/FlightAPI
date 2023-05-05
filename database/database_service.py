import sqlite3
import exceptions
from typing import List


class DataBaseService:
    def __init__(self, db_address):
        self.__db_address = db_address

    @property
    def db_address(self):
        return self.__db_address

    def __manipulate_database(self, sql_query: str, params: tuple = None) -> sqlite3.Cursor:
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
            raise exceptions.DataBaseError from error
        return db_cursor

    def get_all_entries_from_table(self, table_name: str) -> List[dict]:
        sql_query = f'SELECT * FROM {table_name}'
        try:
            query_result = self.__manipulate_database(sql_query)
        except exceptions.DataBaseError as error:
            raise exceptions.DataBaseError from error
        entries_list = self.__convert_cursor_to_dict_list(query_result)
        return entries_list

    @staticmethod
    def __convert_cursor_to_dict_list(cursor: sqlite3.Cursor) -> List[dict]:
        description = tuple(column[0] for column in cursor.description)
        result = [dict(zip(description, entry)) for entry in cursor.fetchall()]
        return result

    def __get_entries_by_kwargs(self, table_name, **kwargs):
        if kwargs:
            search_params = ' AND '.join([f'{key}="{kwargs[key]}"' for key in kwargs])
            sql_query = f'SELECT * FROM {table_name} WHERE {search_params}'
        else:
            sql_query = f'SELECT * FROM {table_name}'
        return self.__manipulate_database(sql_query)

    def get_entry_from_table_by_id(self, table_name, id_parameter):
        return self.__get_entries_by_kwargs(table_name, id=id_parameter)

    def insert_entry_into_table(self, table_name, **kwargs):
        column_names = tuple(kwargs.keys())
        params = tuple(kwargs.values())
        sql_query = f'INSERT INTO {table_name} {column_names} VALUES {params}'
        self.__manipulate_database(sql_query)
        return self.__get_entries_by_kwargs(table_name, **kwargs)


if __name__ == '__main__':
    dbs = DataBaseService('airports.sqlite3')
    result = dbs.get_all_entries_from_table('Airports')
    print(result)