import pandas as pd
import argparse
import misc
import parse_spice
import net_processing


def main():
    description = "pyLEX - SPICE STD-CELL ARCS EXTRACTOR"
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--input", nargs='+', type=str, default=0, help="Input Spice file", required=True)
    args = parser.parse_args()
    # config = vars(args)
    # print(config)
    file = args.input[0]
    misc.print_gmelogo()
    print(f'Processing File: {file}\n')
    # parse SPICE description
    subckt = parse_spice.parse_spice(file)

    print("---------------------------------------")
    print("PINOUT INFORMATION:")
    print(f'#IN pins: {len(subckt.get_i_pins())}')
    for pin in subckt.get_i_pins():
        print(pin, end=" ")
    print(f'\n\n#OUT pins: {len(subckt.get_o_pins())}')
    for pin in subckt.get_o_pins():
        print(pin, end=" ")
    print("\n---------------------------------------")

    subckt.set_boolean_expression(net_processing.retrieve_expression(subckt))
    subckt.set_truth_table(net_processing.return_truth_table(subckt))
    subckt.set_arcs(net_processing.find_arcs(subckt))


main()
# try:
#     main()
# except:
#     print("ERROR")
