import re
import transistor
import subcircuit
import yaml


def is_vdd_pin(pin, yaml_file):
    for vdd_name in yaml_file['VDD']:
        if (vdd_name.lower() == pin.lower()):
            return True
    return False


def is_gnd_pin(pin, yaml_file):
    for gnd_name in yaml_file['GND']:
        if (gnd_name.lower() == pin.lower()):
            return True
    return False


def is_pmos(device_name, yaml_file):
    for pmos_name in yaml_file['PMOS']:
        if (pmos_name.lower() == device_name.lower()):
            return True
    return False


def is_nmos(device_name, yaml_file):
    for nmos_name in yaml_file['NMOS']:
        if (nmos_name.lower() == device_name.lower()):
            return True
    return False


def find_common_nets(PDN, PUN):
    common_nets = []
    for tn in PDN:
        for tp in PUN:
            if (tn.get_source() == tp.get_source()) or (tn.get_source() == tp.get_drain()):
                if not (tn.get_source() in common_nets):
                    common_nets.append(tn.get_source())
            elif (tn.get_drain() == tp.get_source()) or (tn.get_drain() == tp.get_drain()):
                if not (tn.get_drain() in common_nets):
                    common_nets.append(tn.get_drain())
    return common_nets


def in_or_out(io_pins, CNS):
    o_pins = []
    i_pins = []
    for pin in io_pins:
        if pin in CNS:
            o_pins.append(pin)
            CNS.remove(pin)
        else:
            i_pins.append(pin)
    return [i_pins, o_pins]


def parse_spice(file):
    # Start Variables -----------------------
    PDN = []  # Start List for N Transistors
    PUN = []  # Start List for P Transistors
    vdd_pins = []  # List for the Pins
    gnd_pins = []  # List for the Pins
    io_pins = []  # List for the Pins
    subcircuit_name = ""
    header = ""
    f = open(file, "r")
    yaml_file = yaml.safe_load(open("pdk_config.yml"))

    line_count = 1
    for line in f:
        newline = line.rstrip('\n')
        # Check if the line is either a subcircuit definition line or a device line
        if (".subckt" in newline.lower()):
            # print("**subcircuit line**")
            tokenized_string = newline.split()
            header = " ".join(tokenized_string[2:])
            subcircuit_name = tokenized_string[1]
            for token in tokenized_string[2:]:
                if is_vdd_pin(token, yaml_file):
                    vdd_pins.append(token)
                elif is_gnd_pin(token, yaml_file):
                    gnd_pins.append(token)
                else:
                    io_pins.append(token)

        elif (("m" in newline.lower()) or ("x" in newline.lower())):
            # print("**device line**")
            tokenized_string = newline.split()
            name = tokenized_string[0]
            source = tokenized_string[1]
            gate = tokenized_string[2]
            drain = tokenized_string[3]
            bulk = tokenized_string[4]
            device_type = tokenized_string[5]
            wsize = re.findall('[Ww]=[0-9Ee]*.[0-9Ee]*[\-+0-9]*', newline)
            if (wsize):
                wsize = wsize[0].replace('w=', '')
                wsize = wsize.replace('W=', '')
                wsize = wsize.replace('m', 'e-03')
                wsize = wsize.replace('u', 'e-06')
                wsize = wsize.replace('n', 'e-09')
                wsize = float(wsize)
                # print("W Size:", wsize)
            else:
                wsize = 1e-6
                print("pattern not found W size on line {line_count}")

            lsize = re.findall('[Ll]=[0-9Ee]*.[0-9Ee]*[\-+0-9]*', newline)
            if (lsize):
                lsize = lsize[0].replace('l=', '')
                lsize = lsize.replace('L=', '')
                lsize = lsize.replace('m', 'e-03')
                lsize = lsize.replace('u', 'e-06')
                lsize = lsize.replace('n', 'e-09')
                lsize = float(lsize)
                # print("L Size:", lsize)
            else:
                lsize = 180e-9
                print("pattern not found L Size on line {line_count}")

            fingers = re.findall('nf=[0-9]*', newline.lower())
            if (fingers):
                fingers = fingers.replace('nf=', '')
                fingers = fingers.replace('NF=', '')
                fingers = int(fingers)
                # print("Fingers:", fingers)
            else:
                print(
                    f'pattern not found: Number of Fingers on line {line_count}')
                fingers = 1
            if is_pmos(device_type, yaml_file):
                mos = transistor.Transistor(
                    name, source, gate, drain, bulk, "PMOS", wsize, fingers, lsize)
                PUN.append(mos)
            elif is_nmos(device_type, yaml_file):
                mos = transistor.Transistor(
                    name, source, gate, drain, bulk, "NMOS", wsize, fingers, lsize)
                PDN.append(mos)
            else:
                print(
                    f'Device not found in device list:{device_type} on line {line_count} \n Update YAML file')
        line_count = line_count + 1
    f.close()
    # FIND COMMON NETS BETWEEN THE PDN AND PUN
    CNS = find_common_nets(PDN, PUN)
    # DISTRIBUTE PINS
    i_pins, o_pins = in_or_out(io_pins, CNS.copy())
    # RETURN THE SUBCIRCUIT
    return subcircuit.Subcircuit(subcircuit_name, PDN, PUN, i_pins, o_pins, vdd_pins, gnd_pins, CNS, path=file, header=header)
