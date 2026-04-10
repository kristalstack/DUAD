def sort_hyphen_string(s):
    words = s.split("-")   # convert string to list
    words.sort()           # sort alphabetically
    return "-".join(words) # convert back to string