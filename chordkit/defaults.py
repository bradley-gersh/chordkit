import numpy as np
import chord_utils as cu

# Timbres
default_timbre = cu.basic_saw_timbre
sethares_timbre = cu.sethares_timbre
sine_tone = cu.sine_tone

# Frequencies
default_fund = cu.default_fund
a4 = 440.0
a3 = 220.0
c4 = 261.6255653005986

# Chord structures
default_chord_struct = [0]
default_chord = cu.ChordSpectrum(default_chord_struct)
default_chord_struct_type = 'ST-DIFF'
default_function_type = 'SETHARES'
default_transpose_domain = cu.TransposeDomain(0, 12, 100, 'ST_DIFF')
