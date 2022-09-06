import re

from validator.rules_src import Rule


class PhoneRule(Rule):
    regex = re.compile(r"([+]\d+|0)\d{9,}")  # chaines commençant par b ou B

    def __init__(self):
        super(PhoneRule, self).__init__()
        self.error_message = "Téléphone non valide"

    def check(self, txt):
        if txt:
            return self.regex.match(txt) is not None
        return True



class UrlRule(Rule):
    regex = re.compile(r"""^(?i)(?P<proto>(http(s)?))(://)(?P<hostname>[\w.-]+)(/(?P<path>.*))?$""")

    def __init__(self):
        super(UrlRule, self).__init__()
        self.error_message = "URL non valide"

    def check(self, txt):
        if txt:
            return self.regex.match(txt) is not None
        else:
            return True

