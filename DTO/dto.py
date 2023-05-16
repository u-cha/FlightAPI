import json
from typing import List


class DTO:
    def jsonize(self):
        json_obj = json.dumps(self.__dict__)
        return json_obj


class AirportDTO(DTO):
    def __init__(self, id: (int, str), code: str, name: str):
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

class RouteDTO(DTO):
    def __init__(self, num_stops, flights: List[FlightDTO]):
        self.num_stops = num_stops
        self.flights = flights
        self.total_price = self.__calculate_total_price()

    def __calculate_total_price(self):
        total_price = 0
        for flight in self.flights:
            total_price += flight.price
        return total_price
