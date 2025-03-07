COLORS = {
    'blue': '\033[34m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'red': '\033[31m',
    'purple': '\033[35m',
    'end': '\033[0m'  
}

def model_layout():
    print(f"{COLORS['yellow']}..{COLORS['end']}")
    print(f"{COLORS['green']}├──{COLORS['end']} Project_Name")
    print(f"{COLORS['red']}│   ├──{COLORS['end']} DataSet")
    print(f"{COLORS['blue']}│   │   ├──{COLORS['end']} Training_Data")
    print(f"{COLORS['purple']}│   │   │   ├──{COLORS['end']} Class_Name_A")
    print(f"{COLORS['yellow']}│   │   │   ├──{COLORS['end']} Classes_Name_B")
    print(f"{COLORS['green']}│   │   │   └──{COLORS['end']} Classes_Name_etc...")
    print(f"{COLORS['red']}│   │   ├──{COLORS['end']} Validation_Data")
    print(f"{COLORS['blue']}│   │   │   ├──{COLORS['end']} Class_Name_A")
    print(f"{COLORS['purple']}│   │   │   ├──{COLORS['end']} Classes_Name_B")
    print(f"{COLORS['yellow']}│   │   │   └──{COLORS['end']} Classes_Name_etc...")
    print(f"{COLORS['green']}│   └──{COLORS['end']} model.h5")
    print('-----------------------------------')
    print('                           -capchan')

def neural_network():
    print('')
    print("  Input Layer          Hidden Layer     Output Layer\n")
    print(f"{COLORS['green']}   o - o - o          o - o - o - o           o - o\n{COLORS['end']}")
    print(f"{COLORS['red']}   \\   |   /            \\   |   /               |{COLORS['end']}")
    print(f"{COLORS['blue']}    o  o  o             o - o - o               o{COLORS['end']}")
    print(f"{COLORS['purple']}   /   |   \\            /   |   \\               |\n{COLORS['end']}")
    print(f"{COLORS['yellow']}   o - o - o          o - o - o - o           o - o{COLORS['end']}")
    print('---------------------------------------------------')
    print('                                           -capchan')

def weights_biases():
    print('')
    print("    Inputs (x1, x2, ..., xn)")
    print(f"{COLORS['green']}          |{COLORS['end']}")
    print(f"{COLORS['red']}          |{COLORS['end']}")
    print(f"{COLORS['blue']}    O-----|----{COLORS['end']}[Weighted Sum]{COLORS['blue']}---->{COLORS['end']}[Activation]{COLORS['blue']}----> Outputs")
    print(f"{COLORS['purple']}          |                     /{COLORS['end']}")
    print(f"{COLORS['yellow']}          |                    /{COLORS['end']}")
    print(f"{COLORS['end']}         [Bias]{COLORS['green']}---------------/{COLORS['end']}")
    print('-----------------------------------------------------------')
    print('                                                   -capchan')

def RS_function():
    print('')
    print("       Sigmoid                ReLU\n")
    print(f"{COLORS['green']}  Y                    Y{COLORS['end']}")
    print(f"{COLORS['red']}  |         ._/        |    /{COLORS['end']}")
    print(f"{COLORS['blue']}  |      ._/           |   /{COLORS['end']}")
    print(f"{COLORS['purple']}  |   ._/              |  /{COLORS['end']}")
    print(f"{COLORS['yellow']}  | _/                 | /{COLORS['end']}")
    print(f"{COLORS['green']}  |/______________ X   |/______________ X{COLORS['end']}")
    print('-----------------------------------------')
    print('                                 -capchan')
