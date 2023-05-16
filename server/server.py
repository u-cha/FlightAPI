from http.server import BaseHTTPRequestHandler
import handler.handler as handlers
import exceptions
from server.path_processor import PathProcessor
from server.routes import routes_and_handlers_dict


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        handler = self.__assign_handler_by_path()
        self.__perform(handler.get_data)

    def do_POST(self):
        handler = self.__assign_handler_by_path()
        self.__perform(handler.post_data)

    def do_PATCH(self):
        handler = self.__assign_handler_by_path()
        self.__perform(handler.patch_data)

    def __assign_handler_by_path(self):
        route, path_params, query_params = self.__decompose_path()
        handler_name = routes_and_handlers_dict.get(route, None)
        if handler_name:
            handler = getattr(handlers, handler_name)(route, path_params, query_params)
        else:
            handler = handlers.BadRouteHandler(route)
        return handler

    def __decompose_path(self) -> tuple:
        route = PathProcessor.determine_route(self.path)
        path_params = PathProcessor.determine_path_params(self.path)
        query_params = PathProcessor.determine_query_params(self.path)
        return route, path_params, query_params

    def __perform(self, handler_function):
        try:
            response = handler_function()
            self.__respond(response.status, response.data, json=True)
        except exceptions.DataBaseError:
            self.__respond(500, 'A DB Error occurred')
        except exceptions.RequestError:
            self.__respond(400, 'Incorrect request')
        except exceptions.EntryNotFoundError:
            self.__respond(404, 'Entry not found')
        except exceptions.EntryAlreadyExistsError:
            self.__respond(409, 'Entry already exists')

    def __respond(self, status_code: int, server_message: str, json=False) -> None:
        self.send_response(status_code)
        content_type = 'application/json' if json else 'text/plain'
        self.send_header('Content-type', content_type)
        self.end_headers()
        self.wfile.write(bytes(server_message, encoding='utf-8'))
