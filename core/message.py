from starlette import status



class ErrorKey:
    status_code = 'status_code'
    message = 'message'
    code = 'code'


class ErrorMessage:
    SERVER_ERROR = {
        ErrorKey.status_code: status.HTTP_500_INTERNAL_SERVER_ERROR,
        ErrorKey.code: 1000,
        ErrorKey.message: 'An error occurred, please try again'
    }

    NOT_FOUND = {
        ErrorKey.status_code: status.HTTP_404_NOT_FOUND,
        ErrorKey.code: 1001,
        ErrorKey.message: 'Not found'
    }


