# helper Module
from urllib.parse import urlencode


def kwargs_to_query(kwargs):
    request = ""

    for key, value in kwargs.items():
        ''' goes over kwargs and makes a string 
        key1=value&key1=value&key2=value
        auto converts input from str, int and list of str and int
        '''
        # check if list
        if isinstance(value, list):
            # convert list values to string
            value = list(map(str, value))

            # iterate over list values and combine with key to request string
            for val in value:
                request = request + urlencode({key: val}) + '&'
        else:
            # convert kwarg values to string
            value = str(value)

            # if not list make request string from values and key
            request = request + urlencode({key: value}) + '&'

    # return without last &
    return request[:-1]
