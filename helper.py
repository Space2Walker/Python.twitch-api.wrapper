# helper Module
from urllib.parse import urlencode


# get the kwargs keys and iterate
def kwargs_to_query(kwargs):
    req = ""
    for e in kwargs:
        if isinstance(kwargs[e], list):
            kwargs[e] = list(map(str, kwargs[e]))

        else:
            kwargs[e] = str(kwargs[e])

    for key in kwargs.keys():
        ''' goes over the list of values per key and makes a string 
        user_login=gronkh&user_login=lastmiles&user_id=49112900&
        where user_login is the key and "gronkh" and "lastmiles" are the values in the list of that key
        '''
        if isinstance(kwargs[key], list):
            for val in kwargs[key]:
                tes = urlencode({key: val})
                req = req + tes + '&'

        else:
            tes = urlencode({key: kwargs[key]})
            req = req + tes + '&'
    return req[:-1]
