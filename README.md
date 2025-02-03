# pyLEX - SPICE STD-CELL ARCS EXTRACTOR (but in Python)

## Please, Cite the Paper

R. N. Wuerdig, V. H. Maciel, R. Reis and S. Bampi, "LEX - A Cell Switching Arcs Extractor: A Simple SPICE-Input Interface for Electrical Characterization," 2023 IEEE Computer Society Annual Symposium on VLSI (ISVLSI), Foz do Iguacu, Brazil, 2023, pp. 1-6, doi: 10.1109/ISVLSI59464.2023.10238671.

## About

This tool is ment to extract arcs from Pull-Down (PDN) and Pull-up Networks (PUN) while analysing a node-graph representation. This tool is part of a standard-cell characterization suite (FUTURE WORK).

## Installing Dependencies and Running

```
pip install networkx
pip install pyyaml
```


To run:

```
python3 main.py [-h/--help] for help
python3 main.py [-i/--input] <spice file>.sp
```

By running the spice_files/nand3.sp example the tool outputs:

```
~/pyLEX$ python3 main.py -i spice_files/nand2.sp
================================
██████╗ ██╗   ██╗██╗     ███████╗██╗  ██╗
██╔══██╗╚██╗ ██╔╝██║     ██╔════╝╚██╗██╔╝
██████╔╝ ╚████╔╝ ██║     █████╗   ╚███╔╝
██╔═══╝   ╚██╔╝  ██║     ██╔══╝   ██╔██╗
██║        ██║   ███████╗███████╗██╔╝ ██╗
╚═╝        ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝
================================
LOGICAL EXTRACTOR
================================
Processing File: spice_files/nand2.sp
---------------------------------------
PINOUT INFORMATION:
#IN pins: 2
A B

#OUT pins: 1
OUT
---------------------------------------
00| 1
10| 1
01| 1
11| 0
1 R  | Fall
R 1  | Fall
F 1  | Rise
1 F  | Rise
```


