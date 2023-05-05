errors_and_statuses = {
    'db error': {
        'message': 'An error occurred while accessing database',
        'status': 500
    },
    'incorrect param(s)': {
        'message': 'Request is missing one or more parameters (or parameter(s) is/are incorrect)',
        'status': 400
    },
    'db entry not found': {
        'message': 'Entry not found in database',
        'status': 404
    },
    'db entry exists': {
        'message': 'Entry with such parameter(s) already exists in database',
        'status': 409
    },
    'flight route not found': {
        'message': 'Requested flight route not found in database',
        'status': 404
    }


}