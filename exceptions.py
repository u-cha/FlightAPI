class DataBaseError(Exception):
    """Marks DataBase manipulation errors including SQLite Errors
    (bad SQL syntax, unavailable tables) """

    def __init__(self, error_type, error_description):
        super().__init__(self)
        self.error_type = error_type
        self.description = error_description


class EntryAlreadyExistsError(Exception):
    """Marks the situation when trying to INSERT an entry that already exists in Database"""


class MissingParams(Exception):
    """Marks the situation when one or more parameters are missing"""


class EntryNotFoundError(Exception):
    """Marks the situation when entry with provided parameters  was not found in database"""


class RequestError(Exception):
    pass
