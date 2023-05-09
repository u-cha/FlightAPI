import typing
import database.database_service as DBS
import DTO.dto as DTO
import exceptions


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

    @classmethod
    def get_all_flights(cls) -> typing.List[DTO.FlightDTO]:
        database_service = DBS.DataBaseService('../database/airports.sqlite3')
        all_flights_list = database_service.get_all_entries_from_table('Flights')
        all_flights_DTOs_list = []
        for entry in all_flights_list:
            flight = DTO.FlightDTO(entry['id'],
                                   cls.get_airport_by_id(entry['from_airport_id']),
                                   cls.get_airport_by_id(entry['to_airport_id']),
                                   cls.get_airline_by_id(entry['airline_id']),
                                   entry['price'])
            all_flights_DTOs_list.append(flight)
        return all_flights_DTOs_list

    @classmethod
    def post_airport(cls, code: str = None, name: str = None) -> (DTO.AirportDTO, None):
        if code and name:
            airport = cls.get_airport_by_code(code)
            if airport:
                raise exceptions.EntryAlreadyExistsError
            else:
                dbs = DBS.DataBaseService('../database/airports.sqlite3')
                dbs.insert_one_entry_into_table('Airports', code=code, name=name)
                return cls.get_airport_by_code(code)
        else:
            raise exceptions.MissingParams

    @classmethod
    def post_airline(cls, code: str = None, name: str = None) -> (DTO.AirlineDTO, None):
        if code and name:
            airline = cls.get_airline_by_code(code)
            if airline:
                raise exceptions.EntryAlreadyExistsError
            else:
                dbs = DBS.DataBaseService('../database/airports.sqlite3')
                dbs.insert_one_entry_into_table('Airlines', code=code, name=name)
                return cls.get_airline_by_code(code)
        else:
            raise exceptions.MissingParams



if __name__ == '__main__':

    airline = Application.post_airline(code='Z1', name='Austrania')
    if airline:
        print(airline.name, airline.code, airline.id)







