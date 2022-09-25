def remove_prefix(text: str, prefix: str):
    if prefix and text.startswith(prefix):
        return text[len(prefix):]
    return text
