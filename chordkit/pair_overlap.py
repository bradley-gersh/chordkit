import math
from chordkit.hearing_models import cbw_volk as cbw, bark_zwicker as bar
from chordkit.pair_constants import SETHARES_CONSTANTS as sc, AUDITORY_CONSTANTS as ac, pair_volume, pair_distance

# Returns overlap contribution of two partials, based on an indicator
# function on the critical bandwidth, scaled to the amplitude of the partial.
def cbw_overlap(x_hz, ref_hz, v_x, v_ref, amp_type='MIN'):
    cbw_limit = cbw(max([x_hz, ref_hz])) / 2
    distance = pair_distance(x_hz, ref_hz)

    if distance < ac.slow_beat_limit:
        return pair_volume(v_x, v_ref, amp_type)
    else:
        return 0

# Uses a bump function from a cosine wave to measure overlap
def cos_overlap(x_hz, ref_hz, v_x, v_ref, amp_type='MIN'):
    distance = pair_distance(x_hz, ref_hz)
    flat = cbw_overlap(x_hz, ref_hz, v_x, v_ref, amp_type)

    return flat * 0.5 * (1 + math.cos(math.pi * distance/ac.slow_beat_limit))

# An imitation of the Sethares (1993) roughness function, but for overlap
def sethares_like_overlap(x_hz, ref_hz, v_x, v_ref, amp_type='MIN', cutoff=False):
    s = sc.s_star / (sc.s1 * min([x_hz, ref_hz]) + sc.s2)
    v12 = pair_volume(v_x, v_ref, amp_type)

    # The following scaling factor is introduced to ensure that the maximum
    # value obtained by the pairwise roughness function is approximately 1.
    scaling = -2.374

    distance = pair_distance(x_hz, ref_hz)

    # Cutoff: Following Hutchinson and Knopoff 1978, cuts off the overlap
    # function at 1.2 CBW, which prevents too-remote partials from
    # contributing to the final score.
    if cutoff:
        cbw_limit = 1.2 * cbw(max[x_hz, ref_hz]) / 2
        if distance < ac.slow_beat_limit or distance >= cbw_limit:
            v12 = 0

    try:
        return v12 * math.exp(scaling * sc.b * s * distance)
    except OverflowError:
        print(f'Overflow in computing overlap: b == {sc.b}, s == {s}, distance == {distance}')
