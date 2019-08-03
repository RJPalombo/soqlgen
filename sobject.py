class SObject:
    def __init__(self, label, apiname):
        self.label = label
        self.apiname = apiname
        self.fields = []

    def add_field(self, field):
        self.fields.append(field)


class Field:
    def __init__(self, label, apiname, datatype, custom):
        self.label = label
        self.apiname = apiname
        self.datatype = datatype
        self.custom = custom
