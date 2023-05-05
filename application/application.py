import database.database_service as DBS
import DTO.dto as DTO


class Application:
    @staticmethod
    def get_all_airports():
        database_service = DBS.DataBaseService('../database/airports.sqlite3')
        all_airports_list = database_service.get_all_entries_from_table('Airports')
        all_airports_DTOs_list = [DTO.AirportDTO(**entry) for entry in all_airports_list]
        return all_airports_DTOs_list


if __name__ == '__main__':
    all_airports = Application.get_all_airports()
    for airport in all_airports:
        print(airport.id, airport.name, airport.code)




