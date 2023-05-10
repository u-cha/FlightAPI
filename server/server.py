from http.server import BaseHTTPRequestHandler
import handler.handler as handlers

from server.path_processor import PathProcessor
from server.routes import routes_and_handlers_dict


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        handler = self.__assign_handler_by_path()
        self.__perform(handler.get_data)
        self.__respond(handler)

    def do_POST(self):
        handler = self.__assign_handler_by_path()
        handler.perform('post_data')
        self.__respond(handler)

    def do_PATCH(self):
        handler = self.__assign_handler_by_path()
        handler.perform('patch_data')
        self.__respond(handler)

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

    def __respond(self, handler):
        self.send_response(handler.status)
        self.send_header('Content-type', handler.content_type)
        self.end_headers()
        self.wfile.write(bytes(str(handler.__data), encoding='utf-8'))
