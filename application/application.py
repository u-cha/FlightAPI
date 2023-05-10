import typing

import DTO.dto
import database.database_service as dbs
import DTO.dto as dto
import exceptions


class Application:
    @staticmethod
    def get_all_airports() -> typing.List[dto.AirportDTO]:
        database_service = dbs.DataBaseService('../database/airports.sqlite3')
        all_airports_list = database_service.get_all_entries_from_table('Airports')
        all_airports_dtos_list = [dto.AirportDTO(**entry) for entry in all_airports_list]
        return all_airports_dtos_list

    @staticmethod
    def get_airport_by_code(code: str) -> (dto.AirportDTO, None):
        database_service = dbs.DataBaseService('../database/airports.sqlite3')
        airport = database_service.get_one_entry_from_table_by_code('Airports', code)
        if airport:
            return dto.AirportDTO(**airport)
        return None

    @staticmethod
    def get_airport_id_by_code(code: str) -> (int, None):
        database_service = dbs.DataBaseService('../database/airports.sqlite3')
        airport = database_service.get_one_entry_from_table_by_code('Airports', code)
        if airport:
            return dto.AirportDTO(**airport).id
        return None

    @staticmethod
    def get_airport_by_id(id_param: (str, int)) -> (dto.AirportDTO, None):
        database_service = dbs.DataBaseService('../database/airports.sqlite3')
        airport = database_service.get_one_entry_from_table_by_id('Airports', id_param)
        if airport:
            return dto.AirportDTO(**airport)
        return None

    @staticmethod
    def get_all_airlines() -> typing.List[dto.AirlineDTO]:
        database_service = dbs.DataBaseService('../database/airports.sqlite3')
        all_airlines_list = database_service.get_all_entries_from_table('Airlines')
        all_airlines_dtos_list = [dto.AirlineDTO(**entry) for entry in all_airlines_list]
        return all_airlines_dtos_list

    @staticmethod
    def get_airline_by_code(code: str) -> (dto.AirlineDTO, None):
        database_service = dbs.DataBaseService('../database/airports.sqlite3')
        airline = database_service.get_one_entry_from_table_by_code('Airlines', code)
        if airline:
            return dto.AirlineDTO(**airline)
        return None

    @staticmethod
    def get_airline_id_by_code(code: str) -> (int, None):
        database_service = dbs.DataBaseService('../database/airports.sqlite3')
        airline = database_service.get_one_entry_from_table_by_code('Airlines', code)
        if airline:
            return dto.AirlineDTO(**airline).id
        return None

    @staticmethod
    def get_airline_by_id(id_param: (str, int)) -> (dto.AirlineDTO, None):
        database_service = dbs.DataBaseService('../database/airports.sqlite3')
        airline = database_service.get_one_entry_from_table_by_id('Airlines', id_param)
        if airline:
            return dto.AirlineDTO(**airline)
        return None

    @classmethod
    def get_all_flights(cls) -> typing.List[dto.FlightDTO]:
        database_service = dbs.DataBaseService('../database/airports.sqlite3')
        all_flights_list = database_service.get_all_entries_from_table('Flights')
        all_flights_dtos_list = []
        for entry in all_flights_list:
            flight = dto.FlightDTO(entry['id'],
                                   cls.get_airport_by_id(entry['from_airport_id']),
                                   cls.get_airport_by_id(entry['to_airport_id']),
                                   cls.get_airline_by_id(entry['airline_id']),
                                   entry['price'])
            all_flights_dtos_list.append(flight)
        return all_flights_dtos_list

    def get_flight_by_from_to_airline(self,
                                      from_airport_code: str,
                                      to_airport_code: str,
                                      airline_code: str) -> dto.FlightDTO:
        database_service = dbs.DataBaseService('../database/airports.sqlite3')
        from_airport_id = self.get_airport_id_by_code(from_airport_code)
        to_airport_id = self.get_airport_id_by_code(to_airport_code)
        airline_id = self.get_airline_id_by_code(airline_code)
        if not all((from_airport_id, to_airport_id, airline_id)):
            raise exceptions.EntryNotFoundError
        else:
            try:
                flight = database_service.get_entries_by_kwargs('Flights',
                                                                from_airport_id=from_airport_id,
                                                                to_airport_id=to_airport_id,
                                                                airline_id=airline_id)[0]
            except IndexError:
                return None
            flight_dto = dto.FlightDTO(flight['id'],
                                       self.get_airport_by_id(flight['from_airport_id']),
                                       self.get_airport_by_id(flight['to_airport_id']),
                                       self.get_airline_by_id(flight['airline_id']),
                                       flight['price'])
            return flight_dto

    def get_flights_by_from(self, from_airport_code: str) -> typing.List[dto.FlightDTO]:
        database_service = dbs.DataBaseService('../database/airports.sqlite3')
        from_airport_id = self.get_airport_id_by_code(from_airport_code)
        if not from_airport_id:
            raise exceptions.EntryNotFoundError
        else:
            flights_list = database_service.get_entries_by_kwargs('Flights',
                                                                  from_airport_id=from_airport_id)

            flight_dtos_list = []
            for flight in flights_list:
                flight_dto = dto.FlightDTO(flight['id'],
                                           self.get_airport_by_id(flight['from_airport_id']),
                                           self.get_airport_by_id(flight['to_airport_id']),
                                           self.get_airline_by_id(flight['airline_id']),
                                           flight['price'])
                flight_dtos_list.append(flight_dto)
            return flight_dtos_list

    def get_flights_by_to(self, to_airport_code: str) -> typing.List[dto.FlightDTO]:
        database_service = dbs.DataBaseService('../database/airports.sqlite3')
        to_airport_id = self.get_airport_id_by_code(to_airport_code)
        if not to_airport_id:
            raise exceptions.EntryNotFoundError
        else:
            flights_list = database_service.get_entries_by_kwargs('Flights',
                                                                  to_airport_id=to_airport_id)

            flight_dtos_list = []
            for flight in flights_list:
                flight_dto = dto.FlightDTO(flight['id'],
                                           self.get_airport_by_id(flight['from_airport_id']),
                                           self.get_airport_by_id(flight['to_airport_id']),
                                           self.get_airline_by_id(flight['airline_id']),
                                           flight['price'])
                flight_dtos_list.append(flight_dto)
            return flight_dtos_list

    def get_flights_by_from_to(self, from_airport_code: str, to_airport_code: str) -> typing.List[dto.FlightDTO]:
        database_service = dbs.DataBaseService('../database/airports.sqlite3')
        from_airport_id = self.get_airport_id_by_code(from_airport_code)
        to_airport_id = self.get_airport_id_by_code(to_airport_code)
        if not all((from_airport_id, to_airport_id)):
            raise exceptions.EntryNotFoundError
        else:
            flights_list = database_service.get_entries_by_kwargs('Flights',
                                                                  from_airport_id=from_airport_id,
                                                                  to_airport_id=to_airport_id)

            flight_dtos_list = []
            for flight in flights_list:
                flight_dto = dto.FlightDTO(flight['id'],
                                           self.get_airport_by_id(flight['from_airport_id']),
                                           self.get_airport_by_id(flight['to_airport_id']),
                                           self.get_airline_by_id(flight['airline_id']),
                                           flight['price'])
                flight_dtos_list.append(flight_dto)
            return flight_dtos_list

    def get_flights_by_airline(self, airline_code: str) -> typing.List[dto.FlightDTO]:
        database_service = dbs.DataBaseService('../database/airports.sqlite3')
        airline_id = self.get_airline_id_by_code(airline_code)
        if not airline_id:
            raise exceptions.EntryNotFoundError
        else:
            flights_list = database_service.get_entries_by_kwargs('Flights',
                                                                  airline_id=airline_id)

            flight_dtos_list = []
            for flight in flights_list:
                flight_dto = dto.FlightDTO(flight['id'],
                                           self.get_airport_by_id(flight['from_airport_id']),
                                           self.get_airport_by_id(flight['to_airport_id']),
                                           self.get_airline_by_id(flight['airline_id']),
                                           flight['price'])
                flight_dtos_list.append(flight_dto)
            return flight_dtos_list

    @classmethod
    def post_airport(cls, code: str = None, name: str = None) -> (dto.AirportDTO, None):
        if code and name:
            airport = cls.get_airport_by_code(code)
            if airport:
                raise exceptions.EntryAlreadyExistsError
            else:
                db_service = dbs.DataBaseService('../database/airports.sqlite3')
                db_service.insert_one_entry_into_table('Airports', code=code, name=name)
                return cls.get_airport_by_code(code)
        else:
            raise exceptions.MissingParams

    @classmethod
    def post_airline(cls, code: str = None, name: str = None) -> (dto.AirlineDTO, None):
        if code and name:
            airline = cls.get_airline_by_code(code)
            if airline:
                raise exceptions.EntryAlreadyExistsError
            else:
                db_service = dbs.DataBaseService('../database/airports.sqlite3')
                db_service.insert_one_entry_into_table('Airlines', code=code, name=name)
                return cls.get_airline_by_code(code)
        else:
            raise exceptions.MissingParams

    @classmethod
    def post_flight(cls,
                    from_airport_code: str = None, to_airport_code: str = None,
                    airline_code: str = None, price: int = None) -> DTO.dto.FlightDTO:
        if not all((from_airport_code, to_airport_code, airline_code, price)):
            raise exceptions.MissingParams
        try:
            flight = cls().get_flight_by_from_to_airline(from_airport_code, to_airport_code, airline_code)
        except exceptions.EntryNotFoundError:
            raise exceptions.MissingParams
        if flight:
            raise exceptions.EntryAlreadyExistsError
        else:
            db_service = dbs.DataBaseService('../database/airports.sqlite3')
            from_airport_id = cls.get_airport_id_by_code(from_airport_code)
            to_airport_id = cls.get_airport_id_by_code(to_airport_code)
            airline_id = cls.get_airline_id_by_code(airline_code)
            db_service.insert_one_entry_into_table('Flights',
                                                   from_airport_id=from_airport_id,
                                                   to_airport_id=to_airport_id,
                                                   airline_id=airline_id,
                                                   price=price)
            return cls().get_flight_by_from_to_airline(from_airport_code, to_airport_code, airline_code)

    def patch_flight(self,
                     from_airport_code: str, to_airport_code: str,
                     airline_code: str, price: int):
        if not all((from_airport_code, to_airport_code, airline_code, price)):
            raise exceptions.MissingParams
        flight = self.get_flight_by_from_to_airline(from_airport_code, to_airport_code, airline_code)
        if flight:
            from_airport_id = self.get_airport_id_by_code(from_airport_code)
            to_airport_id = self.get_airport_id_by_code(to_airport_code)
            airline_id = self.get_airline_id_by_code(airline_code)
            db_service = dbs.DataBaseService('../database/airports.sqlite3')
            db_service.update_one_entry_in_table('Flights',
                                                 dict(price=price),
                                                 dict(from_airport_id=from_airport_id,
                                                      to_airport_id=to_airport_id,
                                                      airline_id=airline_id))
            return self.get_flight_by_from_to_airline(from_airport_code, to_airport_code, airline_code)


if __name__ == '__main__':
    resp = Application().patch_flight('OLZ', 'FVM', '4B', 10100)
    print(resp.price, resp.airline.code)