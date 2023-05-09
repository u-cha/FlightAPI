import typing
import database.database_service as DBS
import DTO.dto as DTO


class Application:
    @staticmethod
    def get_all_airports() -> typing.List[DTO.AirportDTO]:
        database_service = DBS.DataBaseService('../database/airports.sqlite3')
        all_airports_list = database_service.get_all_entries_from_table('Airports')
        all_airports_DTOs_list = [DTO.AirportDTO(**entry) for entry in all_airports_list]
        return all_airports_DTOs_list

    @staticmethod
    def get_airport_by_code(code: str) -> (DTO.AirportDTO, None):
        database_service = DBS.DataBaseService('../database/airports.sqlite3')
        airport = database_service.get_one_entry_from_table_by_code('Airports', code)
        if airport:
            return DTO.AirportDTO(**airport)
        return None

    @staticmethod
    def get_airport_id_by_code(code: str) -> (int, None):
        database_service = DBS.DataBaseService('../database/airports.sqlite3')
        airport = database_service.get_one_entry_from_table_by_code('Airports', code)
        if airport:
            return DTO.AirportDTO(**airport).id
        return None

    @staticmethod
    def get_airport_by_id(id_param: (str, int)) -> (DTO.AirportDTO, None):
        database_service = DBS.DataBaseService('../database/airports.sqlite3')
        airport = database_service.get_one_entry_from_table_by_id('Airports', id_param)
        if airport:
            return DTO.AirportDTO(**airport)
        return None

    @staticmethod
    def get_all_airlines() -> typing.List[DTO.AirlineDTO]:
        database_service = DBS.DataBaseService('../database/airports.sqlite3')
        all_airlines_list = database_service.get_all_entries_from_table('Airlines')
        all_airlines_DTOs_list = [DTO.AirlineDTO(**entry) for entry in all_airlines_list]
        return all_airlines_DTOs_list

    @staticmethod
    def get_airline_by_code(code: str) -> (DTO.AirlineDTO, None):
        database_service = DBS.DataBaseService('../database/airports.sqlite3')
        airline = database_service.get_one_entry_from_table_by_code('Airlines', code)
        if airline:
            return DTO.AirlineDTO(**airline)
        return None

    @staticmethod
    def get_airline_id_by_code(code: str) -> (int, None):
        database_service = DBS.DataBaseService('../database/airports.sqlite3')
        airline = database_service.get_one_entry_from_table_by_code('Airlines', code)
        if airline:
            return DTO.AirlineDTO(**airline).id
        return None

    @staticmethod
    def get_airline_by_id(id_param: (str, int)) -> (DTO.AirlineDTO, None):
        database_service = DBS.DataBaseService('../database/airports.sqlite3')
        airline = database_service.get_one_entry_from_table_by_id('Airlines', id_param)
        if airline:
            return DTO.AirlineDTO(**airline)
        return None

if __name__ == '__main__':

    airline = Application.get_airline_by_id(810)
    print(airline.name)





