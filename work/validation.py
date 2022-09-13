import re

from validator.rules_src import Rule

from work.toolbox import clean_allspace


class phoneRule(Rule):
    regex = re.compile(r"""([+]\d+|0)\d{9,}""")  # chaines commençant par b ou B

    def __init__(self):
        super(phoneRule, self).__init__()
        self.error_message = "Téléphone non valide"

    def check(self, txt):
        if txt:
            txt = clean_allspace(txt)
            return self.regex.match(txt) is not None
        return True



class urlRule(Rule):
    regex = re.compile(r"""^(?i)(?P<proto>(http(s)?))(://)(?P<hostname>[\w.-]+)(/(?P<path>.*))?$""")

    def __init__(self):
        super(urlRule, self).__init__()
        self.error_message = "URL non valide"

    def check(self, txt):
        if txt:
            txt = clean_allspace(txt)
            return self.regex.match(txt.lower()) is not None
        else:
            return True



class emailRule(Rule):
    regex = re.compile(r"""([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+""")
    def __init__(self):
        super(emailRule, self).__init__()
        self.error_message = "Email non valide"

    def check(self, txt):
        return self.regex.match(txt) is not None

