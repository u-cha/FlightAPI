import typing
import exceptions
from application.application import Application
from errors import errors
from handler.iatacodevalidator import IATACodeValidator
from database.database_service import DataBaseService
from representation.representation import JsonRepresentation
from DTO import dto


class BaseHandler:
    def __init__(self, route, path_params=None, query_params=None):
        self.__data = ''
        self.__content_type = None
        self.__status = 200
        self.__route = route
        self.__path_params = path_params
        self.__query_params = query_params

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def route(self):
        return self.__route

    @route.setter
    def route(self, route):
        self.__route = route

    @property
    def content_type(self):
        return self.__content_type

    @content_type.setter
    def content_type(self, content_type):
        self.__content_type = content_type

    @property
    def query_params(self):
        return self.__query_params

    @query_params.setter
    def query_params(self, query_params):
        self.__query_params = query_params

    @property
    def path_params(self):
        return self.__path_params

    @path_params.setter
    def path_params(self, path_params):
        self.__path_params = path_params

    def get_data(self):
        return self

    def post_data(self):
        return self

    def patch_data(self):
        return self


class BadRouteHandler(BaseHandler):
    def __init__(self, route, *args):
        super().__init__(route)
        self.status = 404
        self.data = f'404 - {self.route} - route not served, pay attention to typos and slashes'


class AirportsHandler(BaseHandler):
    def __init__(self, route, path_params=None, query_params=None):
        super().__init__(route, path_params, query_params)

    def get_data(self):
        if len(self.path_params) == 0 and self.query_params is None:
            return self.get_all_airports()
        elif len(self.path_params) == 1 and self.query_params is None:
            airport_code = self.path_params[0]
            if not IATACodeValidator.airport_code_is_valid(airport_code):
                raise exceptions.RequestError
            else:
                return self.get_one_airport(airport_code)
        else:
            raise exceptions.RequestError

    def get_all_airports(self):
        airports_dto_list = Application.get_all_airports()
        self.data = JsonRepresentation.transform_airport_dto_list_to_json(airports_dto_list)
        return self

    def get_one_airport(self, airport_code):
        airport = Application.get_airport_by_code(airport_code)
        if not airport:
            raise exceptions.EntryNotFoundError
        self.data = JsonRepresentation.transform_airport_dto_to_json(airport)
        return self

    def validate_post_request(self):
        if (len(self.path_params) == 0
                and self.query_params is not None
                and 'code' in self.query_params
                and IATACodeValidator.airport_code_is_valid(self.query_params['code'])
                and 'name' in self.query_params
                and isinstance(self.query_params['name'], str)):
            return True
        return False

    def post_data(self):
        if not self.validate_post_request():
            raise exceptions.RequestError
        airport_code = self.query_params['code']
        airport_name = self.query_params['name']
        airport = Application.get_airport_by_code(airport_code)
        if airport:
            raise exceptions.EntryAlreadyExistsError
        else:
            airport = Application.post_airport(airport_code, airport_name)
        self.data = JsonRepresentation.transform_airport_dto_to_json(airport)
        return self


class FlightsHandler(BaseHandler):
    def __init__(self, route, path_params=None, query_params=None):
        super().__init__(route, path_params, query_params)

    def patch_data(self):
        if self.validate_patch_request():
            from_airport_code = self.path_params[0][:3]
            to_airport_code = self.path_params[0][3:6]
            airline_code = self.path_params[0][6:]
            flight = self.get_one_flight(from_airport_code, to_airport_code, airline_code)
            if not flight:
                raise exceptions.EntryNotFoundError
            else:
                price = self.query_params.get('price')
                flight_dto = Application().patch_flight(from_airport_code, to_airport_code, airline_code, price)
                self.data = JsonRepresentation.transform_flight_dto_to_json(flight_dto)
                return self
        else:
            raise exceptions.RequestError

    def get_data(self):
        if len(self.path_params) != 0:
            raise exceptions.RequestError
        if self.query_params is None:
            return self.get_all_flights()
        if self.query_params:
            if self.validate_exact_search():
                return self.get_one_flight()
            if self.validate_from_to_search():
                return self.get_from_to_flights()
            if self.validate_from_search():
                return self.get_from_flights()
            if self.validate_to_search():
                return self.get_to_flights()
            if self.validate_airline_search():
                return self.get_airline_flights()
            else:
                raise exceptions.RequestError

    def validate_exact_search(self):
        if (IATACodeValidator.airport_code_is_valid(self.query_params.get('from_airport_code', None)) and
                IATACodeValidator.airport_code_is_valid(self.query_params.get('to_airport_code', None)) and
                IATACodeValidator.airline_code_is_valid(self.query_params.get('airline', None))):
            return True
        return False

    def validate_price(self, price):
        a = bool(price.count('.') <= 1)
        b = bool(price.replace('.', '').isnumeric())
        return a and b

    def post_data(self):
        if len(self.path_params) != 0:
            raise exceptions.RequestError
        if not self.validate_exact_search():
            raise exceptions.RequestError
        price = self.query_params.get('price', None)
        if not price or not self.validate_price(price):
            raise exceptions.RequestError
        from_airport_code = self.query_params.get('from_airport_code')
        to_airport_code = self.query_params.get('to_airport_code')
        airline_code = self.query_params.get('airline')
        flight = Application().get_flight_by_from_to_airline(from_airport_code, to_airport_code, airline_code)
        if flight:
            raise exceptions.EntryAlreadyExistsError
        else:
            flight = Application.post_flight(from_airport_code, to_airport_code, airline_code, price)
            self.data = JsonRepresentation.transform_flight_dto_to_json(flight)
        return self

    def get_all_flights(self):
        flights_dto_list = Application.get_all_flights()
        self.data = JsonRepresentation.transform_flight_dto_list_to_json(flights_dto_list)
        return self

    def get_one_flight(self, from_airport_code=None, to_airport_code=None, airline_code=None):
        if not from_airport_code:
            from_airport_code = self.query_params.get('from_airport_code')
        if not to_airport_code:
            to_airport_code = self.query_params.get('to_airport_code')
        if not airline_code:
            airline_code = self.query_params.get('airline')
        flight_dto = Application().get_flight_by_from_to_airline(from_airport_code, to_airport_code, airline_code)
        if not flight_dto:
            raise exceptions.EntryNotFoundError
        self.data = JsonRepresentation.transform_flight_dto_to_json(flight_dto)
        return self

    def validate_from_to_search(self):
        if (IATACodeValidator.airport_code_is_valid(self.query_params.get('from_airport_code', None)) and
                IATACodeValidator.airport_code_is_valid(self.query_params.get('to_airport_code', None))):
            return True
        return False

    def get_from_to_flights(self):
        from_airport_code = self.query_params.get('from_airport_code')
        to_airport_code = self.query_params.get('to_airport_code')
        flight_dto_list = Application().get_flights_by_from_to(from_airport_code, to_airport_code)
        self.data = JsonRepresentation.transform_flight_dto_list_to_json(flight_dto_list)
        return self

    def validate_from_search(self):
        if IATACodeValidator.airport_code_is_valid(self.query_params.get('from_airport_code', None)):
            return True
        return False

    def validate_to_search(self):
        if IATACodeValidator.airport_code_is_valid(self.query_params.get('to_airport_code', None)):
            return True
        return False

    def validate_airline_search(self):
        if IATACodeValidator.airline_code_is_valid(self.query_params.get('airline', None)):
            return True
        return False

    def get_from_flights(self):
        from_airport_code = self.query_params.get('from_airport_code')
        flight_dto_list = Application().get_flights_by_from(from_airport_code)
        self.data = JsonRepresentation.transform_flight_dto_list_to_json(flight_dto_list)
        return self

    def get_to_flights(self):
        to_airport_code = self.query_params.get('to_airport_code')
        flight_dto_list = Application().get_flights_by_to(to_airport_code)
        self.data = JsonRepresentation.transform_flight_dto_list_to_json(flight_dto_list)
        return self

    def get_airline_flights(self):
        airline_code = self.query_params.get('airline')
        flight_dto_list = Application().get_flights_by_airline(airline_code)
        self.data = JsonRepresentation.transform_flight_dto_list_to_json(flight_dto_list)
        return self

    def validate_patch_request(self):
        path_params = self.path_params
        if not self.query_params:
            return False
        price = self.query_params.get('price', None)
        if (len(path_params) == 1
                and len(path_params[0]) == 8
                and path_params[0].isalnum()
                and IATACodeValidator.airport_code_is_valid(path_params[0][:3])
                and IATACodeValidator.airport_code_is_valid(path_params[0][3:6])
                and IATACodeValidator.airline_code_is_valid(path_params[0][6:])
                and self.validate_price(price)):
            return True
        return False


class AirlinesHandler(BaseHandler):
    def __init__(self, route, path_params=None, query_params=None):
        super().__init__(route, path_params, query_params)

    def validate_post_request(self):
        if (len(self.path_params) == 0
                and self.query_params is not None
                and 'code' in self.query_params
                and IATACodeValidator.airline_code_is_valid(self.query_params['code'])
                and 'name' in self.query_params
                and isinstance(self.query_params['name'], str)):
            return True
        return False

    def get_data(self):
        if len(self.path_params) == 0 and self.query_params is None:
            return self.get_all_airlines()
        elif len(self.path_params) == 1 and self.query_params is None:
            airline_code = self.path_params[0]
            if not IATACodeValidator.airline_code_is_valid(airline_code):
                raise exceptions.RequestError
            else:
                return self.get_one_airline(airline_code)
        else:
            raise exceptions.RequestError

    def get_all_airlines(self):
        airlines_dto_list = Application.get_all_airlines()
        self.data = JsonRepresentation.transform_airline_dto_list_to_json(airlines_dto_list)
        return self

    def get_one_airline(self, airline_code):
        airline = Application.get_airline_by_code(airline_code)
        if not airline:
            raise exceptions.EntryNotFoundError
        self.data = JsonRepresentation.transform_airline_dto_to_json(airline)
        return self

    def post_data(self):
        if not self.validate_post_request():
            raise exceptions.RequestError
        airline_code = self.query_params['code']
        airline_name = self.query_params['name']
        airline = Application.get_airline_by_code(airline_code)
        if airline:
            raise exceptions.EntryAlreadyExistsError
        else:
            airline = Application.post_airline(airline_code, airline_name)
        self.data = JsonRepresentation.transform_airline_dto_to_json(airline)
        return self


class RoutesHandler(BaseHandler):
    def __init__(self, route, path_params=None, query_params=None):
        super().__init__(route, path_params, query_params)
        self.data = route

    def validate_get_request(self):
        if (len(self.path_params) == 2
                and all([IATACodeValidator.airport_code_is_valid(path_param) for path_param in self.path_params])
                and self.query_params.get('max_stops')
                and self.query_params['max_stops'].isnumeric()
                and 0 <= int(self.query_params['max_stops']) <= 2):
            return True
        return False

    def get_data(self):
        if self.validate_get_request():
            max_stops = int(self.query_params.get('max_stops'))
            if max_stops == 0:
                return self.get_zero_stops_route()
            elif max_stops == 1:
                return self.get_one_stop_route()
            elif max_stops == 2:
                return self.get_two_stops_route()
        else:
            raise exceptions.RequestError

    def get_zero_stops_route(self):
        routes_dto_list = self.__get_zero_stops_routes_dto_list()
        self.data = JsonRepresentation.transform_route_dto_list_to_json(routes_dto_list)
        return self

    def get_one_stop_route(self):
        zero_stops_routes_dto_list = self.__get_zero_stops_routes_dto_list()
        one_stop_routes_dto_list = self.__get_one_stop_routes_dto_list()
        total_dto_list = zero_stops_routes_dto_list + one_stop_routes_dto_list
        self.data = JsonRepresentation.transform_route_dto_list_to_json(total_dto_list)
        return self

    def __get_zero_stops_routes_dto_list(self) -> typing.List[dto.RouteDTO]:
        num_stops = 0
        from_airport_code = self.query_params['from_airport_code'] = self.path_params[0]
        to_airport_code = self.query_params['to_airport_code'] = self.path_params[1]
        flight_dto_list = Application().get_flights_by_from_to(from_airport_code, to_airport_code)
        routes_dto_list = [dto.RouteDTO(num_stops, [flight_dto]) for flight_dto in flight_dto_list]
        return routes_dto_list

    def __get_one_stop_routes_dto_list(self) -> typing.List[dto.RouteDTO]:
        num_stops = 1
        from_airport_code = self.query_params['from_airport_code'] = self.path_params[0]
        to_airport_code = self.query_params['to_airport_code'] = self.path_params[1]
        flight_dto_list = Application().get_flights_by_from_to_with_one_stop(from_airport_code,
                                                                             to_airport_code)
        routes_dto_list = [dto.RouteDTO(num_stops, flight_list) for flight_list in flight_dto_list]
        return routes_dto_list

    def get_two_stops_route(self):
        zero_stops_routes_dto_list = self.__get_zero_stops_routes_dto_list()
        one_stop_routes_dto_list = self.__get_one_stop_routes_dto_list()
        two_stops_routes_dto_list = self.__get_two_stops_routes_dto_list()
        total_dto_list = zero_stops_routes_dto_list + one_stop_routes_dto_list + two_stops_routes_dto_list
        self.data = JsonRepresentation.transform_route_dto_list_to_json(total_dto_list)
        return self

    def __get_two_stops_routes_dto_list(self):
        num_stops = 2
        from_airport_code = self.query_params['from_airport_code'] = self.path_params[0]
        to_airport_code = self.query_params['to_airport_code'] = self.path_params[1]
        flight_dto_list = Application().get_flights_by_from_to_with_two_stops(from_airport_code,
                                                                             to_airport_code)
        routes_dto_list = [dto.RouteDTO(num_stops, flight_list) for flight_list in flight_dto_list]
        return routes_dto_list
