from http.server import HTTPServer
import logging
from server.server import Server

logging.basicConfig(filename='flight_service.log', encoding='utf-8', filemode='w', level=logging.DEBUG)

server = HTTPServer(('127.0.0.1', 8080), Server)

if __name__ == '__main__':
    server.serve_forever()
