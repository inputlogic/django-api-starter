# d1 is original definition, d2 is incoming data
def same_keys(d1, d2):
    if d1.keys() != d2.keys():
        return False
    for k in d1.keys():
        if not isinstance(d1[k], type(d2[k])):
            return False
        if type(d1[k]) == dict and not same_keys(d1[k], d2[k]):
            return False
        if type(d1[k]) == list:
            for d in d2[k]:
                if not same_keys(d1[k][0], d):
                    return False
    return True
