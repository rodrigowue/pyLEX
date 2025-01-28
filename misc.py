from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas as pd
# import seaborn as sns
import subcircuit
import networkx as nx


def print_subckt_ng(subckt):
    # ===========================================================================
    # Creates Networkx Node Graph and Include Nodes
    # ===========================================================================
    G = nx.Graph()  # Creates an graph called G
    color_map = []  # list that will define node colors
    node_size = []  # list that will define node sizes
    # -----------------------------------------
    # Searches Nodes and Color them
    # -----------------------------------------
    for vddpin in subckt.get_vdd_pins():
        G.add_node(vddpin)  # create vdd node
        color_map.append('green')
        node_size.append(2000)

    for gndpin in subckt.get_vss_pins():
        G.add_node(gndpin)  # create gnd node
        color_map.append('green')
        node_size.append(2000)

    for outpin in subckt.get_o_pins():
        G.add_node(outpin)
        color_map.append('magenta')
        node_size.append(1000)
    for n in subckt.get_PUN():
        G.add_node(n.get_name())
        color_map.append('red')
        node_size.append(500)
    for n in subckt.get_PDN():
        G.add_node(n.get_name())
        color_map.append('blue')
        node_size.append(500)
    for n in subckt.get_PUN():
        G.add_edge(n.get_name(), n.get_source())
        color_map.append('yellow')
        node_size.append(100)
        G.add_edge(n.get_name(), n.get_drain())
        color_map.append('yellow')
        node_size.append(100)
    for n in subckt.get_PDN():
        G.add_edge(n.get_name(), n.get_source())
        color_map.append('yellow')
        node_size.append(100)
        G.add_edge(n.get_name(), n.get_drain())
        color_map.append('yellow')
        node_size.append(100)
    nx.draw(G, node_size=node_size, node_color=color_map, with_labels=True)
    plt.show()


def print_net(net):
    # ===========================================================================
    # Creates Networkx Node Graph and Include Nodes
    # ===========================================================================
    G = nx.Graph()  # Creates an graph called G
    color_map = []  # list that will define node colors
    node_size = []  # list that will define node sizes
    # -----------------------------------------
    # Searches Nodes and Color them
    # -----------------------------------------
    for n in net:
        G.add_node(n.get_name())
        color_map.append('red')
        node_size.append(500)
    for n in net:
        G.add_edge(n.get_name(), n.get_source())
        color_map.append('yellow')
        node_size.append(100)
        G.add_edge(n.get_name(), n.get_drain())
        color_map.append('yellow')
        node_size.append(100)
    nx.draw(G)
    plt.show()


def print_gmelogo():
    print("================================")
    print("\033[37;41m██████╗ ██╗   ██╗██╗     ███████╗██╗  ██╗\033[0m")
    print("\033[37;41m██╔══██╗╚██╗ ██╔╝██║     ██╔════╝╚██╗██╔╝\033[0m")
    print("\033[37;41m██████╔╝ ╚████╔╝ ██║     █████╗   ╚███╔╝ \033[0m")
    print("\033[37;41m██╔═══╝   ╚██╔╝  ██║     ██╔══╝   ██╔██╗ \033[0m")
    print("\033[37;41m██║        ██║   ███████╗███████╗██╔╝ ██╗\033[0m")
    print("\033[37;41m╚═╝        ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝\033[0m")
    print("================================")
    print("LOGICAL EXTRACTOR")
    print("================================")
    