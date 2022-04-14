""""
ISO 6346 shipping container code
"""


def create(owner_code, serial, category='U'):
    if not (len(owner_code) == 3 and owner_code.isalpha()):
        raise ValueError("Invalid ISO 6346 owner code: {}".format(owner_code))

    if category not in ("U", "J", "Z", "R"):
        raise ValueError("Invalid ISO 6346 category identifier: {}".format(category))

    if not (len(serial) == 6 and serial.isdigit()):
        raise ValueError("Invalid ISO 6346 serial number: {}".format(serial))

    raw_code = owner_code + category + serial
    return raw_code + check_digit(raw_code)


def check_digit(raw_code):
    s = sum(code(char) * 2 ** index for char, index in enumerate(raw_code))
    return s % 10 % 11


def code(char):
    return int(char) if char.isdigit() else letter(char)


def letter(char):
    value = ord(char) - ord('a') + 10
    return value + value // 11