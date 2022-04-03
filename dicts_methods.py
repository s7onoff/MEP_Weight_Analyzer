def find_text_inclusion_in_dict(element: str, dictionary: dict, default_value):
    keys = dictionary.keys()
    for key in keys:
        if str(key).__contains__(element):
            return dictionary[key]
        else:
            return default_value


def find_by_ceil_in_dict(element: float, dictionary: dict) -> dict:
    if max(dictionary.keys()) >= element:
        return dictionary[max(dictionary.keys(), key=lambda key: (key - element) >= 0)]
    else:
        return dictionary[max(dictionary.keys())]
