# Constants and functions shared between pairwise function assessing overlap and roughness of partials

# Parameters fit by Sethares 1993. Reformulated version from Giordano 2015.
SETHARES_CONSTANTS = {
    'a': 3.51, # From http://sethares.engr.wisc.edu/comprog.html; paper has 3.
    'b': 5.75,
    's_star': 0.24,
    's1': 0.0207, # From http://sethares.engr.wisc.edu/comprog.html; paper has 0.021
    's2': 18.96 # From http://sethares.engr.wisc.edu/comprog.html; paper has 19
}

AUDITORY_CONSTANTS = {
    'slow_beat_limit': 15, # +/- Hz limit for zone where two sine waves create sensation of slow beats
    'midi_zero': 8.175798915643707 # Hz value for C(-1). Choosing this as the 'fundamental' allows MIDI numbers
                                  # to be used for specifying chords
}

# Volume scale
def pair_volume(v_x, v_ref, amp_type='MIN'):
    if amp_type in ['PROD', 'PRODUCT']:
        return v_x * v_ref
    else:
        return min([v_x, v_ref])

def pair_distance(a_hz, b_hz):
    return abs(a_hz - b_hz)
