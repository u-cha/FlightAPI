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
    def get_airport_by_code(code: str) -> DTO.AirportDTO:
        database_service = DBS.DataBaseService('../database/airports.sqlite3')
        airport = database_service.get_one_entry_from_table_by_code('Airports', code)
        airport_dto = DTO.AirportDTO(**airport)
        return airport_dto

    @staticmethod
    def get_airport_by_id(id_param: (str, int)) -> (DTO.AirportDTO, None):
        database_service = DBS.DataBaseService('../database/airports.sqlite3')
        airport = database_service.get_one_entry_from_table_by_id('Airports', id_param)
        if airport:
            return DTO.AirportDTO(**airport)
        return None


if __name__ == '__main__':
    for i in range(-11, 10):
        airport = Application.get_airport_by_id(i)
        if airport:
            print(airport.name)




