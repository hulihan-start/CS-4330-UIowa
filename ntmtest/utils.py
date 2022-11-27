from frozendict import frozendict


def freezeValue(value):
    """
    A helper function to convert the given value / structure into a fully
    immutable one by recursively processing said structure and any of its
    members, freezing them as well
    """
    if isinstance(value, list):
        return tuple(freezeValue(element) for element in value)
    if isinstance(value, set):
        return frozenset(freezeValue(element) for element in value)
    elif isinstance(value, dict):
        return frozendict({
            dict_key: freezeValue(dict_value)
            for dict_key, dict_value in value.items()
        })
    else:
        return value