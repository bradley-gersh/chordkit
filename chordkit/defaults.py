from chordkit.chord_utils import Timbre, ChordSpectrum, TransposeDomain

###########
# TIMBRES #
###########
# With 7 partials, used in Sethares 1993, Fig. 2.
class SetharesTimbre(Timbre):
    def __init__(self, partials=7):
        Timbre.__init__(self, range(1, partials + 1), [0.88 ** p for p in range(0, partials)])

class SineTimbre(Timbre):
    def __init__(self):
        Timbre.__init__(self, [1], 1)

class FlatSawTimbre(Timbre):
    def __init__(self, partials=12):
        Timbre.__init__(self, range(1, partials + 1), 1)

class FilteredSawTimbre(Timbre):
    def __init__(self, partials=12):
        Timbre.__init__(self, range(1, partials + 1), [1/p for p in range(1, partials + 1)])

class DefaultTimbre(SetharesTimbre):
    def __init__(self):
        SetharesTimbre.__init__(self, 12)


###############
# FREQUENCIES #
###############
a4 = 440.0
a3 = 220.0
c4 = 261.6255653005986
d4 = 293.6647679174076

# Hz value for C(-1). Choosing this as the 'fundamental' allows MIDI numbers
# to be used for specifying chords.
midi_zero = 8.175798915643707

default_fund = a3

#########################
# TRANSPOSITION DOMAINS #
#########################
# These are not generally modified over the course of the computations,
# so we can keep referencing these same objects in memory

one_octave = TransposeDomain(-0.5, 12.5, 1301, 'ST_DIFF')
two_octaves = TransposeDomain(-0.5, 24.5, 2501, 'ST_DIFF')
two_octaves_symm = TransposeDomain(-12.5, 12.5, 2501, 'ST_DIFF')

default_transpose_domain = one_octave

###############
# CHORD TYPES #
###############
class SineTone(ChordSpectrum):
    def __init__(self, fund=default_fund):
        ChordSpectrum.__init__(self, [0], 'ST_DIFF', timbre=SineTimbre(), fund_hz=fund)

class SetharesTone(ChordSpectrum):
    def __init__(self, partials=7, fund=default_fund):
        ChordSpectrum.__init__(self, [0], 'ST_DIFF', timbre=SetharesTimbre(partials), fund_hz=fund)

class FlatSawTone(ChordSpectrum):
    def __init__(self, partials=12, fund=default_fund):
        ChordSpectrum.__init__(self, [0], 'ST_DIFF', timbre=FlatSawTimbre(partials), fund_hz=fund)

class FilteredSawTone(ChordSpectrum):
    def __init__(self, partials=12, fund=default_fund):
        ChordSpectrum.__init__(self, [0], 'ST_DIFF', timbre=FilteredSawTimbre(partials), fund_hz=fund)

class SetharesMajTriad(ChordSpectrum):
    def __init__(self, partials=12, fund=default_fund):
        ChordSpectrum.__init__(self, [0, 4, 7], 'ST_DIFF', timbre=SetharesTimbre(partials), fund_hz=fund)

default_chord = SetharesTone(1)

#####################
# RELATION DEFAULTS #
#####################
default_overlap_function_type = 'BELL'
default_roughness_function_type = 'SETHARES'
