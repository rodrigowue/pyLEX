class Transistor:
    def __init__(self, name, source, gate, drain, bulk, ttype, wsize, fingers, lsize):
        self.name = name
        self.source = source
        self.gate = gate
        self.drain = drain
        self.bulk = bulk
        self.ttype = ttype
        self.wsize = wsize
        self.fingers = fingers
        self.lsize = lsize
        self.stack = 1
    # ===============================================
    # Methods for Attribute Manipulation
    # ===============================================

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_source(self):
        return self.source

    def set_source(self, source):
        self.source = source

    def get_gate(self):
        return self.gate

    def set_gate(self, gate):
        self.gate = gate

    def get_drain(self):
        return self.drain

    def set_drain(self, drain):
        self.drain = drain

    def get_bulk(self):
        return self.bulk

    def set_bulk(self, bulk):
        self.bulk = bulk

    def get_ttype(self):
        return self.ttype

    def set_ttype(self, ttype):
        self.ttype = ttype

    def get_wsize(self):
        return self.wsize

    def set_wsize(self, wsize):
        self.wsize = wsize

    def get_fingers(self):
        return self.fingers

    def set_fingers(self, fingers):
        self.fingers = fingers

    def get_lsize(self):
        return self.lsize

    def set_lsize(self, lsize):
        self.lsize = lsize

    def get_stack(self):
        return self.stack

    def set_stack(self, stack):
        self.stack = stack
