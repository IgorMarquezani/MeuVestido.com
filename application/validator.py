import re


class Validator():
    def validate_name(self, name: str) -> bool:
        return len(name) > 1 and len(name) < 56

    def validate_email(self, email: str) -> bool:
        regex = r"^[\w]+@([\w]+\.)+[\w]{2,4}$"

        if not re.fullmatch(regex, email):
            return False

        return True

    def validate_passwd(self, passwd: str) -> bool:
        upper, numeric, special = [False, False, False]

        for c in passwd:
            if c.isupper():
                upper = True
            if c.isnumeric():
                numeric = True

            ascii = ord(c)

            if ascii >= 33 and ascii <= 47:
                special = True
            if ascii >= 58 and ascii <= 64:
                special = True
            if ascii >= 91 and ascii <= 96:
                special = True
            if ascii >= 123 and ascii <= 126:
                special = True

        return upper and numeric and special and len(passwd) > 7
