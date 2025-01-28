import subcircuit
import transistor
import parse_spice
import yaml
import misc


def is_pg_pin(pin):
    yaml_file = yaml.safe_load(open("pdk_config.yml"))
    if (parse_spice.is_vdd_pin(pin, yaml_file) or parse_spice.is_gnd_pin(pin, yaml_file)):
        return True
    else:
        return False


def check_common_net(t1, CN):
    if (t1.get_source() == CN) or (t1.get_drain() == CN):
        return True
    else:
        return False


def check_parallel(t1, t2):
    if (((t1.get_source() == t2.get_source()) and (t1.get_drain() == t2.get_drain())) or ((t1.get_drain() == t2.get_source()) and (t1.get_source() == t2.get_drain()))):
        return True
    else:
        return False


def check_series(t1, t2):
    a_src = t1.get_source()
    b_src = t2.get_source()
    a_dra = t1.get_drain()
    b_dra = t2.get_drain()
    if (((a_src == b_src) & (not (is_pg_pin(a_src))) & (a_dra != b_dra)) |
        ((a_src == b_dra) & (not (is_pg_pin(a_src))) & (a_dra != b_src)) |
        ((a_dra == b_src) & (not (is_pg_pin(a_dra))) & (a_src != b_dra)) |
            ((a_dra == b_dra) & (not (is_pg_pin(a_dra))) & (a_src != a_src))):
        return True
    else:
        return False


def merge_parallel(t1, t2):
    ttype = t1.get_ttype()
    bulk = t1.get_bulk()
    source = t1.get_source()
    drain = t1.get_drain()
    fingers = 0
    diff_width = 0.0
    gate_lenght = 0.0
    stack = t1.get_stack()
    alias = f'({t1.get_gate()}'
    if (t1.get_ttype() == "PMOS"):
        alias = alias + "*"
    else:
        alias = alias + "+"
    alias = alias + t2.get_gate() + ")"
    merged_transistor = transistor.Transistor(
        alias, source, alias, drain, bulk, ttype, diff_width, fingers, gate_lenght)
    return merged_transistor


def merge_series(t1, t2):
    ttype = t1.get_ttype()
    bulk = t1.get_bulk()
    fingers = 0
    diff_width = 0.0
    gate_lenght = 0.0
    stack = t1.get_stack() + t2.get_stack()
    alias = f'({t1.get_gate()}'
    if (t1.get_ttype() == "PMOS"):
        alias = alias + "+"
    else:
        alias = alias + "*"
    alias = alias + t2.get_gate() + ")"

    a_src = t1.get_source()
    b_src = t2.get_source()
    a_dra = t1.get_drain()
    b_dra = t2.get_drain()
    if (a_src == b_src):
        source = a_dra
        drain = b_dra
    elif (a_src == b_dra):
        source = b_src
        drain = a_dra
    elif (a_dra == b_src):
        source = a_src
        drain = b_dra
    else:
        source = a_src
        drain = b_src

    merged_transistor = transistor.Transistor(
        alias, source, alias, drain, bulk, ttype, diff_width, fingers, gate_lenght)
    return merged_transistor


def collapse_parallel(PDX, CNS):
    for i in range(0, len(PDX)-1):
        t1 = PDX[i]
        for j in range(i+1, len(PDX)):
            t2 = PDX[j]
            if (check_parallel(t1, t2)):
                merged_transistor = merge_parallel(t1, t2)
                PDX.append(merged_transistor)
                PDX.remove(t1)
                PDX.remove(t2)
                if (len(PDX) == len(CNS)):
                    return PDX
                else:
                    return collapse_parallel(PDX, CNS)
    return PDX


def collapse_series(PDX, CNS):
    for i in range(0, len(PDX)-1):
        t1 = PDX[i]
        for j in range(i+1, len(PDX)):
            t2 = PDX[j]
            if (check_series(t1, t2)):
                merged_transistor = merge_series(t1, t2)
                PDX.append(merged_transistor)
                PDX.remove(t1)
                PDX.remove(t2)
                if (len(PDX) == len(CNS)):
                    return PDX
                else:
                    return collapse_series(PDX, CNS)
    return PDX


def solve_boolean_expression(expression):
    if (len(expression) > 1):
        expression = expression.replace('0+0', '0')
        expression = expression.replace('0+1', '1')
        expression = expression.replace('1+0', '1')
        expression = expression.replace('1+1', '1')

        expression = expression.replace('0*0', '0')
        expression = expression.replace('0*1', '0')
        expression = expression.replace('1*0', '0')
        expression = expression.replace('1*1', '1')

        expression = expression.replace('!1', '0')
        expression = expression.replace('!(1)', '0')
        expression = expression.replace('!0', '1')
        expression = expression.replace('!(0)', '1')
        expression = expression.replace('(0)', '0')
        expression = expression.replace('(1)', '1')
        return solve_boolean_expression(expression)
    else:
        return int(expression)


def return_truth_table(subckt):
    expression = subckt.get_boolean_expression()
    inputs = subckt.get_i_pins()
    output = subckt.get_o_pins()
    size = 1 << len(inputs)
    truth_table = [None]*size
    counter = 0
    amount_of_inputs = pow(2, len(inputs))
    while counter < amount_of_inputs:
        local_expression = expression
        pins = ""
        for pin in range(0, len(inputs)):
            teste = (counter >> pin) & 1
            pins = pins + str(teste)
            local_expression = local_expression.replace(
                str(inputs[pin]), str(teste))
            print(teste, end="")
        if solve_boolean_expression(local_expression) == 1:
            truth_table[int(pins, 2)] = 1
            print("| 1")
        else:
            truth_table[int(pins, 2)] = 0
            print("| 0")
        counter = counter + 1
    return truth_table


def find_arcs(subckt):
    truth_table = subckt.get_truth_table()
    inputs = subckt.get_i_pins()
    maxval = 1 << len(inputs)
    arcs = []
    values = [None]*len(inputs)
    for i in range(0, maxval):
        t = i
        j = 0
        for c in inputs:
            values[j] = str(t & 1)
            t >>= 1
            j = j + 1
        # print(values)
        source = ""
        source = source.join(values)
        # print(source)
        source_result = truth_table[int(source, 2)]
        k = 0
        for c in inputs:
            t = i ^ (1 << k)
            l = 0
            for d in inputs:
                values[l] = str(t & 1)
                t >>= 1
                l = l + 1
            destiny = ""
            destiny = destiny.join(values)
            destiny_result = truth_table[int(destiny, 2)]
            if source_result != destiny_result:
                # print(f'source:{source} destiny:{destiny}')
                counter = 0
                arc = ""
                for c1 in inputs:
                    if (c1 == c):
                        if (int(source[k]) == 1):
                            print("F", end="")
                            arc = arc + "F"
                        else:
                            print("R", end="")
                            arc = arc + "R"
                    else:
                        print(values[counter], end="")
                        if (values[counter] == 1):
                            arc = arc + str(1)
                        else:
                            arc = arc + str(0)
                    counter = counter + 1
                    print(" ", end="")
                print(" | ", end="")
                if (destiny_result == 0):
                    print("Fall", end="")
                    arc = arc + "F"
                else:
                    print("Rise", end="")
                    arc = arc + "R"
                arcs.append(arc)
                print("")
            k = k + 1
    return arcs


def retrieve_expression_for_net(PDX, CNS):
    it_count = 0
    expressions = []
    while ((len(PDX) > len(CNS)) and (it_count < 1000)):
        # misc.print_net(PDX)
        PDX = collapse_parallel(PDX.copy(), CNS.copy())
        if (len(PDX) == len(CNS)):
            break
        else:
            PDX = collapse_series(PDX.copy(), CNS.copy())
        it_count = it_count + 1
    # misc.print_net(PDX)
    for CN in CNS:
        for transistor in PDX:
            if check_common_net(transistor, CN):
                transistor.set_name(transistor.get_gate())
                expressions.append([CN, transistor.get_name()])
    return expressions


def flatten_expression(expressions):
    for cn, expression in expressions:
        for cn2, expression2 in expressions:
            if cn in expression2:
                expression2 = expression2.replace(cn, expression)
                expressions.remove(expression)
    return expressions[0]


def retrieve_expression(subckt):
    temp_subckt = subckt
    merged_expressions = []
    PDN_EXPRESSIONS = retrieve_expression_for_net(
        temp_subckt.get_PDN().copy(), temp_subckt.get_CNS())
    PUN_EXPRESSIONS = retrieve_expression_for_net(
        temp_subckt.get_PUN().copy(), temp_subckt.get_CNS())
    for CNN, TEMP_EXPRESSION in PDN_EXPRESSIONS:
        for CNP, TEMP_EXPRESSIONP in PUN_EXPRESSIONS:
            if (CNN == CNP):
                merged_expressions.append([
                    CNN, f'!({TEMP_EXPRESSION})*!({TEMP_EXPRESSIONP})'])
    cn, expression = flatten_expression(merged_expressions)
    subckt.set_boolean_expression(expression)
    return subckt.get_boolean_expression()
