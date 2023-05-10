from urllib.parse import urlparse


class PathProcessor:

    @staticmethod
    def determine_route(request_path: str) -> str:
        path = urlparse(request_path).path
        split_path = path.split('/')
        if len(split_path) == 2:
            route = split_path[1]
        else:
            route = split_path[1] + '/'
        return route

    @staticmethod
    def determine_path_params(request_path: str) -> tuple:
        path = urlparse(request_path).path
        path_params = tuple(path.split('/')[2:])
        return path_params

    @staticmethod
    def determine_query_params(request_path: str) -> (dict, None):
        query = urlparse(request_path).query
        try:
            query_params = {pair.split('=')[0]: pair.split('=')[1] for pair in query.split('&')}
        except IndexError:
            return None
        return query_params
