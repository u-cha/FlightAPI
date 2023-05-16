import typing
import json

import DTO.dto as dto


class JsonRepresentation:

    @staticmethod
    def transform_airport_dto_to_json(airport_dto: dto.AirportDTO) -> str:
        return json.dumps(airport_dto.__dict__, indent=2)

    @staticmethod
    def transform_airport_dto_list_to_json(airport_dto_list: typing.List[dto.AirportDTO]) -> str:
        result_json = '[' + \
                      ', '.join([JsonRepresentation.transform_airport_dto_to_json(airport_dto)
                                 for airport_dto in airport_dto_list]) + ']'
        return result_json

    @staticmethod
    def transform_airline_dto_to_json(airline_dto: dto.AirlineDTO) -> str:
        return json.dumps(airline_dto.__dict__, indent=2)

    @staticmethod
    def transform_airline_dto_list_to_json(airline_dto_list: typing.List[dto.AirlineDTO]) -> str:
        result_json = '[' + \
                      ', '.join([JsonRepresentation.transform_airline_dto_to_json(airline_dto)
                                 for airline_dto in airline_dto_list]) + ']'
        return result_json

    @staticmethod
    def transform_flight_dto_list_to_json(flight_dto_list: typing.List[dto.FlightDTO]) -> str:
        result_json = '[' + \
                      ', '.join([JsonRepresentation.transform_flight_dto_to_json(flight_dto)
                                 for flight_dto in flight_dto_list]) + ']'
        return result_json

    @staticmethod
    def transform_flight_dto_to_json(flight_dto: dto.FlightDTO) -> str:
        flight_dto.to_airport = flight_dto.to_airport.__dict__
        flight_dto.from_airport = flight_dto.from_airport.__dict__
        flight_dto.airline = flight_dto.airline.__dict__
        return json.dumps(flight_dto.__dict__)

    @staticmethod
    def transform_route_dto_list_to_json(route_dto_list: typing.List[dto.RouteDTO]) -> str:
        result_json = []
        for route_dto in route_dto_list:

            for flight_dto in route_dto.flights:
                flight_dto.to_airport = flight_dto.to_airport.__dict__
                flight_dto.from_airport = flight_dto.from_airport.__dict__
                flight_dto.airline = flight_dto.airline.__dict__
            route_dto.flights = [flight.__dict__ for flight in route_dto.flights]
            result_json.append(route_dto.__dict__)
        result_json = json.dumps(result_json)
        return result_json
