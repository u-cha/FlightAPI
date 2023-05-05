import json
from typing import List


class DTO:
    def jsonize(self):
        json_obj = json.dumps(self.__dict__)
        return json_obj


class AirportDTO(DTO):
    def __init__(self, id, code, name):
        self.id = id
        self.code = code
        self.name = name


class AirlineDTO(DTO):
    def __init__(self, id, code, name):
        self.id = id
        self.code = code
        self.name = name


class FlightDTO(DTO):
    def __init__(self, id, from_airport: AirportDTO, to_airport: AirportDTO, airline: AirlineDTO, price):
        self.id = id
        self.from_airport = from_airport
        self.to_airport = to_airport
        self.airline = airline
        self.price = price

    def jsonize(self):
        self.from_airport = self.from_airport.__dict__
        self.to_airport = self.to_airport.__dict__
        self.airline = self.airline.__dict__
        json_obj = json.dumps(self.__dict__)
        return json_obj


class RouteDTO(DTO):
    def __init__(self, num_stops, flights: List[DTO]):
        self.id = id
        self.from_airport = from_airport
        self.to_airport = to_airport
        self.airline = airline
        self.price = price