import numpy as np
import chordkit.chord_utils as cu

default_timbre = cu.default_timbre
default_fund = cu.default_fund
default_chord_struct = [0]
default_chord = cu.make_chord(default_chord_struct)
default_chord_struct_type = 'ST-DIFF'
default_function_type = 'SETHARES'
default_chord_domain = np.linspace(0, 12, num=1000)
