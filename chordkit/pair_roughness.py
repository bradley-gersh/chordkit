import math
from chordkit.hearing_models import cbw_volk as cbw, bark_zwicker as bark

# Volume scale
def vol_scale(v_x, v_ref, amp_type='MIN'):
    if amp_type in ['PROD', 'PRODUCT']:
        return v_x * v_ref
    else:
        return min([v_x, v_ref])

# Returns the value of the Sethares "sensory dissonance" (roughness)
# function at frequency x_hz with respect to ref_hz.
# Based on Sethares 1997, as implemented in Giordano 2015.
def sethares_roughness(x_hz, ref_hz, v_x, v_ref, amp_type='MIN', cutoff=False, original=False):
    # Parameters fit by Sethares 1993. Reformulated version from Giordano 2015.
    a = 3.51 # From http://sethares.engr.wisc.edu/comprog.html; paper has 3.
    b = 5.75
    s_star = 0.24
    s1 = 0.0207 # From http://sethares.engr.wisc.edu/comprog.html; paper has 0.021
    s2 = 18.96 # From http://sethares.engr.wisc.edu/comprog.html; paper has 19
    s = s_star / (s1 * min([x_hz, ref_hz]) + s2)
    v12 = vol_scale(v_x, v_ref, amp_type)

    # The following scaling factor is introduced to ensure that the maximum
    # value obtained by the pairwise roughness function is approximately 1.
    # The numerator comes from Sethares' MATLAB implementation; the
    # denominator is my additional modification.
    scaling = 5 / 0.8986

    distance = abs(x_hz - ref_hz)

    # Cutoff: Following Hutchinson and Knopoff 1978, cuts off the Sethares
    # roughness function at 1.2 CBW, which prevents too-remote partials from
    # contributing to the final score. (Check whether this also prevents drift
    # for larger intervals.)
    if cutoff:
        cbw_limit = 1.2 * cbw(max[x_hz, ref_hz]) / 2
        if distance < 15 or distance >= cbw_limit:
            scaling = 0

    # Sethares' MATLAB implementation (but not the published paper)
    if original:
        scaling = 5

    try:
        return v12 * scaling * (math.exp(-a*s*distance) - math.exp(-b*s*distance))
    except OverflowError:
        print(f'Overflow in computing roughness: a == {a}, b == {b}, s == {s}, distance == {distance}')


# Returns roughness contribution of two partials, based on an indicator
# function on the critical bandwidth, scaled to the amplitude of the partial.
def cbw_roughness(x_hz, ref_hz, v_x, v_ref, amp_type='MIN'):
    cbw_limit = cbw(max([x_hz, ref_hz])) / 2
    distance = abs(x_hz - ref_hz)

    if distance >= 15 and distance < cbw_limit:
        return vol_scale(v_x, v_ref, amp_type)
    else:
        return 0

# From Bigand, Parncutt, and Lerdahl 1996.
def parncutt_roughness(x_hz, ref_hz):
    # Parameters asserted in BPL 1996 paper
    a = 0.25
    i_factor = 2

    x_bark = bark(x_hz)
    ref_bark = bark(ref_hz)
    distance = abs(x_bark - ref_bark)

    if distance < 1.2:
        return ((math.exp(1)/a) * distance * math.exp(-distance / a)) ** i_factor
    else:
        return 0

