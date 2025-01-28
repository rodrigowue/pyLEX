import transistor


class Subcircuit:
    def __init__(self, name, PDN, PUN, i_pins, o_pins, vdd_pins, vss_pins, CNS, expressions=[], boolean_expression="", truth_table=([]), arcs=([]), path="", header="", sim_files=[]):
        self.name = name
        self.PDN = PDN
        self.PUN = PUN
        self.i_pins = i_pins
        self.o_pins = o_pins
        self.vdd_pins = vdd_pins
        self.vss_pins = vss_pins
        self.CNS = CNS
        self.expressions = expressions
        self.boolean_expression = boolean_expression
        self.truth_table = truth_table
        self.arcs = arcs
        self.path = path
        self.header = header
        self.sim_files = sim_files

    # ===============================================
    # Methods for Attribute Manipulation
    # ===============================================

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_PDN(self):
        return self.PDN

    def set_PDN(self, PDN):
        self.PDN = PDN

    def get_PUN(self):
        return self.PUN

    def set_PUN(self, PUN):
        self.PUN = PUN

    def set_arcs(self, arcs):
        self.arcs = arcs

    def get_arcs(self):
        return self.arcs

    def get_boolean_expression(self):
        return self.boolean_expression

    def set_boolean_expression(self, boolean_expression):
        self.boolean_expression = boolean_expression

    def get_i_pins(self):
        return self.i_pins

    def set_i_pins(self, i_pins):
        self.i_pins = i_pins

    def get_o_pins(self):
        return self.o_pins

    def set_o_pins(self, o_pins):
        self.o_pins = o_pins

    def get_vdd_pins(self):
        return self.vdd_pins

    def set_vdd_pins(self, vdd_pins):
        self.vdd_pins = vdd_pins

    def get_vss_pins(self):
        return self.vss_pins

    def set_vss_pins(self, vss_pins):
        self.vss_pins = vss_pins

    def get_CNS(self):
        return self.CNS

    def set_CNS(self, CNS):
        self.CNS = CNS

    def add_expression(self, CN, expression):
        self.expressions.append({CN, expression})

    def set_truth_table(self, truth_table):
        self.truth_table = truth_table

    def get_truth_table(self):
        return self.truth_table

    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = path

    def get_header(self):
        return self.header

    def set_header(self, header):
        self.header = header

    def get_sim_files(self):
        return self.sim_files

    def set_sim_files(self, sim_files):
        self.sim_files = sim_files
