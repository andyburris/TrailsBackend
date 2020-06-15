def id_sort(to_sort):
    return to_sort['_id']

def remove_underscore(dict):
    id = dict['_id']
    dict.remove('_id')
    dict['id'] = id
