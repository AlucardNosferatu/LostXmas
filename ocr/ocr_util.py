def starts_with_strs(line, prefixes):
    for prefix in prefixes:
        if line.startswith(prefix):
            return True
    return False


def ends_with_strs(line, postfixes):
    for postfix in postfixes:
        if line.endswith(postfix):
            return True
    return False
