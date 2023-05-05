class IATACodeValidator:

    @staticmethod
    def airport_code_is_valid(airport_code):
        if (
            isinstance(airport_code, str) and
            len(airport_code) == 3 and
            airport_code.isalpha()
        ):
            return True
        return False

    @staticmethod
    def airline_code_is_valid(airline_code):
        if (
                isinstance(airline_code, str) and
                len(airline_code) == 2 and
                airline_code.isalnum()
        ):
            return True
        return False
