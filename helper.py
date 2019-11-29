# helper Module
from urllib.parse import urlencode


def kwargs_to_query(kwargs):
    request = ""

    for key, value in kwargs.items():
        ''' goes over kwargs and makes a string 
        key1=value&key1=value&key2=value
        auto converts input from str, int and list of str and int
        '''
        # check is float and raise
        if isinstance(value, (float, dict)):
            raise Exception(f'{type(value)}Not Supported')

        # check if list
        if isinstance(value, list):
            # iterate over list values and combine with key to request string
            for val in value:
                # check is float and raise
                if isinstance(val, (float, dict)):
                    raise Exception(f'{type(val)}Not Supported')

                val = str(val)
                request = request + urlencode({key: val}) + '&'

        else:
            # if not list make request string from values and key
            request = request + urlencode({key: str(value)}) + '&'

    # return without last &
    return request[:-1]
