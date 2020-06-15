def id_sort(to_sort):
    return to_sort['id']

def remove_underscore(dict):
    dict['id'] = dict.pop('_id')
    return dict
