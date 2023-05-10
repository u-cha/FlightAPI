from errors import errors
from handler.iatacodevalidator import IATACodeValidator
from database.database_service import DataBaseService
from DTO import dto


class BaseHandler:
    def __init__(self, route, path_params=None, query_params=None):
        self.__data = None
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

    def get_data(self, table_name, data_object, **kwargs):
        dba_agent = DataBaseService('./database/airports.sqlite3')
        if not self.path_params:
            dba_agent.get_entries_by_kwargs(table_name)
            self.error = dba_agent.__error
            if not self.error and dba_agent.__data:
                content = dba_agent.__data['content']
                if len(content) == 0:
                    self.error = errors.errors_and_statuses['db entry not found']
                    self.data = self.error['message']
                if len(content) >= 1:
                    self.data = '[' + ', '.join([data_object(*entry).jsonize() for entry in content]) + ']'

        else:
            dba_agent.get_entries_by_kwargs(table_name, code=self.path_params[0])
            self.error = dba_agent.__error
            if not self.error and dba_agent.__data:
                content = dba_agent.__data['content']
                if len(content) == 0:
                    self.error = errors.errors_and_statuses['db entry not found']
                    self.data = self.error['message']
                if len(content) == 1:
                    self.data = data_object(*content[0]).jsonize()
        return self

    def post_data(self, *args, **kwargs):
        if self.error:
            return None

    def patch_data(self, *args, **kwargs):
        if self.error:
            return None

    def update_status(self):
        if self.error:
            self.status = self.error.get('status', None)
            if not self.status:
                self.status = 666

    def update_content_type(self):
        if self.error:
            self.content_type = 'text/html'
        else:
            self.content_type = 'application/json'

    def perform(self, function):
        request_is_valid = self.validate_request(function)
        if request_is_valid:
            getattr(self, function)()
        else:
            self.error = errors.errors_and_statuses['incorrect param(s)']
            self.data = self.error['message']

        self.update_status()
        self.update_content_type()

    def validate_request(self, function):
        if function == 'get_data':
            return self.validate_get_request()
        if function == 'post_data':
            return self.validate_post_request()
        self.error = errors.errors_and_statuses['incorrect param(s)']
        return False

    def validate_get_request(self):
        pass

    def validate_post_request(self):
        pass


class BadRouteHandler(BaseHandler):
    def __init__(self, route, *args):
        super().__init__(route)
        self.status = 404
        self.data = f'404 - {self.route} - route not served, pay attention to typos and slashes'

    def perform(self, function):
        pass


class AirportsHandler(BaseHandler):
    def __init__(self, route, path_params=None, query_params=None):
        super().__init__(route, path_params, query_params)
        self.data = route

    def validate_get_request(self):
        if len(self.path_params) == 0 and self.query_params is None:
            return True
        if (len(self.path_params) == 1
                and IATACodeValidator.airport_code_is_valid(self.path_params[0])):
            return True
        return False

    def validate_post_request(self):
        if (len(self.path_params) == 0
                and self.query_params is not None
                and 'code' in self.query_params
                and IATACodeValidator.airport_code_is_valid(self.query_params['code'])
                and 'name' in self.query_params
                and isinstance(self.query_params['name'], str)):
            return True
        return False

    def get_data(self, **kwargs):
        if self.path_params:
            return super().get_data('Airports', dto.AirportDTO, code=self.path_params[0])
        return super().get_data('Airports', dto.AirportDTO)

    def post_data(self):
        dba_agent = DataBaseService('./database/airports.sqlite3')
        dba_agent.get_entries_by_kwargs('Airports', code=self.query_params['code'])
        self.error = dba_agent.__error
        if not self.error and dba_agent.__data:
            content = dba_agent.__data['content']
            if len(content) > 0:
                self.error = errors.errors_and_statuses['db entry exists']
                self.data = self.error['message']
                return self
            if len(content) == 0:
                dba_agent.insert_one_entry_into_table('Airports', code=self.query_params['code'],
                                                      name=self.query_params['name'])
                self.error = dba_agent.__error
                if not self.error:
                    self.get_data()
                    if not self.error:
                        self.data = dto.AirportDTO(*dba_agent.__data['content'][0]).jsonize()
        return self


class FlightsHandler(BaseHandler):
    def __init__(self, route, path_params=None, query_params=None):
        super().__init__(route, path_params, query_params)
        self.data = route

    def validate_request(self, function):
        if function == 'get_data':
            if len(self.path_params) == 0 and self.query_params is None:
                return True
        if function in ('get_data', 'post_data'):
            if (len(self.path_params) == 0
                    and 'from_airport_code' in self.query_params
                    and IATACodeValidator.airport_code_is_valid(self.query_params['from_airport_code'])
                    and 'to_airport_code' in self.query_params
                    and IATACodeValidator.airport_code_is_valid(self.query_params['to_airport_code'])
                    and 'airline' in self.query_params
                    and IATACodeValidator.airline_code_is_valid(self.query_params['airline'])):
                if function == 'get_data':
                    return True
                if (function == 'post_data'
                        and 'price' in self.query_params
                        and self.query_params['price'].count('.') <= 1
                        and self.query_params['price'].replace('.', '').isnumeric()):
                    return True
        if function == 'get_data':
            if (len(self.path_params) == 0
                    and (
                            ('from_airport_code' in self.query_params
                             and IATACodeValidator.airport_code_is_valid(self.query_params['from_airport_code'])) or
                            ('to_airport_code' in self.query_params
                             and IATACodeValidator.airport_code_is_valid(self.query_params['to_airport_code'])) or
                            ('airline' in self.query_params
                             and IATACodeValidator.airline_code_is_valid(self.query_params['airline'])))):
                return True

        if function == 'patch_data':
            path_params = self.path_params
            if (len(path_params) == 1
                    and len(path_params[0]) == 8
                    and path_params[0].isalpha()
                    and IATACodeValidator.airport_code_is_valid(path_params[0][:3])
                    and IATACodeValidator.airport_code_is_valid(path_params[0][3:6])
                    and IATACodeValidator.airline_code_is_valid(path_params[0][6:])):
                return True

        self.error = errors.errors_and_statuses['incorrect param(s)']
        return False

    def get_data(self, **kwargs):
        dba_agent = DataBaseService('./database/airports.sqlite3')

        if not self.path_params:
            if self.query_params:
                from_airport_code = self.query_params.get('from_airport_code')
                to_airport_code = self.query_params.get('to_airport_code')
                airline_code = self.query_params.get('airline')
                if from_airport_code:
                    response = dba_agent.get_entries_by_kwargs('Airports', code=from_airport_code).__data
                    from_airport_id = int(dict(zip(response['description'], response['content'][0]))['id'])
                if to_airport_code:
                    response = dba_agent.get_entries_by_kwargs('Airports', code=to_airport_code).__data
                    to_airport_id = int(dict(zip(response['description'], response['content'][0]))['id'])
                if airline_code:
                    response = dba_agent.get_entries_by_kwargs('Airlines', code=airline_code).__data
                    airline_id = int(dict(zip(response['description'], response['content'][0]))['id'])

                if from_airport_code and to_airport_code and airline_code:
                    dba_agent.get_entries_by_kwargs('Flights', from_airport_id=from_airport_id,
                                                      to_airport_id=to_airport_id, airline_id=airline_id)

                elif from_airport_code and to_airport_code:
                    dba_agent.get_entries_by_kwargs('Flights', from_airport_id=from_airport_id,
                                                      to_airport_id=to_airport_id)

                elif from_airport_code:
                    dba_agent.get_entries_by_kwargs('Flights', from_airport_id=from_airport_id)

                elif to_airport_code:
                    dba_agent.get_entries_by_kwargs('Flights', to_airport_id=to_airport_id)

                elif airline_id:
                    dba_agent.get_entries_by_kwargs('Flights', airline_id=airline_id)
            else:
                dba_agent.get_entries_by_kwargs('Flights')

            self.error = dba_agent.__error
            if not self.error and dba_agent.__data:
                content = dba_agent.__data['content']
                description = dba_agent.__data['description']
                if len(content) == 0:
                    self.error = errors.errors_and_statuses['db entry not found']
                    self.data = self.error['message']
                if len(content) >= 1:

                    flights = []
                    for db_entry in content:
                        response_entry = dict(zip(description, db_entry))

                        from_airport, to_airport, airline = (
                            response_entry.pop('from_airport_id'),
                            response_entry.pop('to_airport_id'),
                            response_entry.pop('airline_id')
                        )

                        response_entry['from_airport'] = dto.AirportDTO(*dba_agent.__get_entries_by_kwargs(
                            'Airports', id=from_airport).__data['content'][0])
                        response_entry['to_airport'] = dto.AirportDTO(*dba_agent.__get_entries_by_kwargs(
                            'Airports', id=to_airport).__data['content'][0])
                        response_entry['airline'] = dto.AirlineDTO(*dba_agent.__get_entries_by_kwargs(
                            'Airlines', id=airline).__data['content'][0])
                        flight = dto.FlightDTO(**dict(response_entry.items()))
                        flights.append(flight.jsonize())
                    response = f"[{', '.join(flights)}]"
                    self.data = response

        return self

    def post_data(self, *args, **kwargs):
        from_airport_code = self.query_params['from_airport_code']
        to_airport_code = self.query_params['to_airport_code']
        airline_code = self.query_params['airline']

        dba = DataBaseService('../database/airports.sqlite3')
        response = dba.get_entries_by_kwargs('Flights', code=from_airport_code).__data
        from_airport_id = int(dict(zip(response['description'], response['content'][0]))['id'])

        response = dba.get_entries_by_kwargs('Flights', code=to_airport_code).__data
        to_airport_id = int(dict(zip(response['description'], response['content'][0]))['id'])

        response = dba.get_entries_by_kwargs('Flights', code=airline_code).__data
        airline_id = int(dict(zip(response['description'], response['content'][0]))['id'])


class AirlinesHandler(BaseHandler):
    def __init__(self, route, path_params=None, query_params=None):
        super().__init__(route, path_params, query_params)
        self.data = route

    def validate_get_request(self):
        if len(self.path_params) == 0 and self.query_params is None:
            return True
        if (len(self.path_params) == 1
                and IATACodeValidator.airline_code_is_valid(self.path_params[0])):
            return True
        return False

    def validate_post_request(self):
        if (len(self.path_params) == 0
                and self.query_params is not None
                and 'code' in self.query_params
                and IATACodeValidator.airline_code_is_valid(self.query_params['code'])
                and 'name' in self.query_params
                and isinstance(self.query_params['name'], str)):
            return True
        self.error = errors.errors_and_statuses['incorrect param(s)']
        return False

    def get_data(self, **kwargs):
        if self.path_params:
            return super().get_data('Airlines', dto.AirlineDTO, code=self.path_params[0])
        return super().get_data('Airlines', dto.AirlineDTO)

    def post_data(self):
        dba_agent = DataBaseService('./database/airports.sqlite3')
        dba_agent.get_entries_by_kwargs('Airlines', code=self.query_params['code'])
        self.error = dba_agent.__error
        if not self.error and dba_agent.__data:
            content = dba_agent.__data['content']
            if len(content) > 0:
                self.error = errors.errors_and_statuses['db entry exists']
                self.data = self.error['message']
                return self
            if len(content) == 0:
                dba_agent.insert_one_entry_into_table('Airlines', code=self.query_params['code'],
                                                  name=self.query_params['name'])
                self.error = dba_agent.__error
                if not self.error:
                    self.get_data()
                    if not self.error:
                        self.data = dto.AirlineDTO(*dba_agent.__data['content'][0]).jsonize()
        return self


class RoutesHandler(BaseHandler):
    def __init__(self, route, path_params=None, query_params=None):
        super().__init__(route, path_params, query_params)
        self.data = route

    def validate_request(self, function):
        if function == 'get_data':
            if (len(self.path_params) == 2
                    and all([IATACodeValidator.airport_code_is_valid(path_param) for path_param in self.path_params])
                    and self.query_params.get('max_stops')
                    and self.query_params['max_stops'].isnumeric()
                    and 0 <= int(self.query_params['max_stops']) <= 2):
                return True
        self.error = errors.errors_and_statuses['incorrect param(s)']
        return False

    def get_data(self, **kwargs):
        dba_agent = DataBaseService('./database/airports.sqlite3')
        num_stops = self.query_params.get('max_stops')
        from_airport_code = self.path_params[0]
        to_airport_code = self.path_params[1]

        response = dba_agent.get_entries_by_kwargs('Airports', code=from_airport_code).__data
        from_airport_id = int(dict(zip(response['description'], response['content'][0]))['id'])

        response = dba_agent.get_entries_by_kwargs('Airports', code=to_airport_code).__data
        to_airport_id = int(dict(zip(response['description'], response['content'][0]))['id'])

        if num_stops == 0:
            dba_agent.get_entries_by_kwargs('Flights', from_airport_id=from_airport_id,
                                              to_airport_id=to_airport_id)

        self.error = dba_agent.__error
        if not self.error and dba_agent.__data:
            content = dba_agent.__data['content']
            description = dba_agent.__data['description']
            if len(content) == 0:
                self.error = errors.errors_and_statuses['flight route not found']
                self.data = self.error['message']
            if len(content) >= 1:

                routes = []
                for db_entry in content:
                    response_entry = dict(zip(description, db_entry))

                    from_airport, to_airport, airline = (
                        response_entry.pop('from_airport_id'),
                        response_entry.pop('to_airport_id'),
                        response_entry.pop('airline_id')
                    )

                    response_entry['from_airport'] = dto.AirportDTO(*dba_agent.get_entries_by_kwargs(
                        'Airports', id=from_airport).__data['content'][0])
                    response_entry['to_airport'] = dto.AirportDTO(*dba_agent.get_entries_by_kwargs(
                        'Airports', id=to_airport).__data['content'][0])
                    response_entry['airline'] = dto.AirlineDTO(*dba_agent.get_entries_by_kwargs(
                        'Airlines', id=airline).__data['content'][0])
                    flight = dto.FlightDTO(**dict(response_entry.items()))
                    routes.append(flight.jsonize())
                response = f"[{', '.join(routes)}]"
                self.data = response
        return self
