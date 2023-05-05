from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
import logging
import handler.handler as handlers

from server.path_processor import PathProcessor
import server.routes as routes


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        handler = self.__assign_handler_by_path()
        handler.perform('get_data')
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
        route = PathProcessor.determine_route(self.path)
        path_params = PathProcessor.determine_path_params(self.path)
        query_params = PathProcessor.determine_query_params(self.path)
        if route in routes.routes_and_handlers:
            handler = getattr(handlers, routes.routes_and_handlers[route])(route, path_params, query_params)
        else:
            handler = handlers.BadRouteHandler(route)
        return handler

    def __respond(self, handler):
        self.send_response(handler.status)
        self.send_header('Content-type', handler.content_type)
        self.end_headers()
        self.wfile.write(bytes(str(handler.__data), encoding='utf-8'))

