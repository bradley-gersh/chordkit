import numpy as np
from chord_utils import Timbre, ChordSpectrum, TransposeDomain

###########
# TIMBRES #
###########
# 7 partials, amplitude of p is 0.88^(p-1). From Sethares 1993, Fig. 2.
sethares_timbre = Timbre(range(1, 8), [0.88 ** p for p in range(0, 7)])

# 12 partials, amplitude of p is 0.88^(p-1). Based on Sethares 1993, Fig. 2.
sethares_timbre_12 = Timbre(range(1, 13), [0.88 ** p for p in range(0, 12)])

# 1 partial, amplitude 1
sine_tone = Timbre([1], [1])

# 12 partials, amplitude of p is 1/p
basic_saw_12 = Timbre(range(1, 13), [1/p for p in range(1, 13)])


###############
# FREQUENCIES #
###############
a4 = 440.0
a3 = 220.0
c4 = 261.6255653005986

# Hz value for C(-1). Choosing this as the 'fundamental' allows MIDI numbers
# to be used for specifying chords.
midi_zero = 8.175798915643707

##################
# DEFAULT VALUES #
##################
default_timbre = sethares_timbre_12
default_fund = a3
default_chord = ChordSpectrum([0], 'ST_DIFF')
default_T = TransposeDomain(-0.5, 12.5, 1301, 'ST_DIFF')
default_overlap_function_type = 'BELL'
default_roughness_function_type = 'SETHARES'
