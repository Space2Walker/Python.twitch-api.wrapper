# helper Module
from urllib.parse import urlencode


def kwargs_to_query(kwargs):
    """ goes over kwargs and makes a string
    key1=value1&key1=value2&key2=value
    auto converts input from str, int and list of str and int
    """
    request = ""

    for key, value in kwargs.items():
        # check if type is unsupported and raise
        if isinstance(value, (float, dict, complex, bool)):
            raise TypeError(f'{type(value)} Not Supported')
        # check if negative int and raise
        if isinstance(value, int):
            if value < 0:
                raise ValueError("Negative Values aren't Supported")

        # check if list
        if isinstance(value, list):
            # iterate over list values and combine with key to request string
            for val in value:
                # check if type is unsupported and raise
                if isinstance(val, (float, dict, complex, bool)):
                    raise TypeError(f'{type(val)} Not Supported')
                # check if negative int and raise
                if isinstance(val, int):
                    if val < 0:
                        raise ValueError("Negative Values aren't Supported")

                val = str(val)
                request = request + urlencode({key: val}) + '&'

        else:
            # if not list make request string from values and key
            request = request + urlencode({key: str(value)}) + '&'

    # return without last &
    return request[:-1]
