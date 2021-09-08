import math
import pandas as pd
import numpy as np
from hearing_models import cbw_volk as cbw, bark_zwicker as bark
from pair_constants import SETHARES_CONSTANTS as sc, AUDITORY_CONSTANTS as ac, pair_volume, pair_distance
from chord_utils import MergedSpectrum
from matplotlib import pyplot as plt

# This file contains both the individual pairwise models used for assessing the
# roughness of partial pairs and the summing function that adds up all such
# pairwise contributions.

###################
# PAIRWISE MODELS #
###################

# Different pairwise roughness evaluation functions. Each has the same signature
# so that they can be called by the same line of code.

def helmholtz_roughness_pair(x_hz, ref_hz, v_x, v_ref, *, p=1, options={}):

    # The following constants have not been given values by Helmholtz.
    # They are chosen here somewhat arbitrarily to make the graph resemble his.
    bPrime1 = 1
    bPrime2 = 1
    beta = 0.01
    # print(options)
    true_ref = options['ref'][0]

    if ref_hz != true_ref:
        temp = x_hz
        x_hz = ref_hz
        ref_hz = temp

    delta = ((float(x_hz) / ref_hz) - 1) / 2
    theta = 15.0 / true_ref

    s = 4 * bPrime1 * bPrime2 * (beta ** 2) / (beta ** 2 + (2 * np.pi * delta) ** 2)

    r = s * ((2 * theta * delta * p) ** 2) / ((theta ** 2 + (p * delta) ** 2) ** 2)

    return r

# Returns the value of the Sethares "sensory dissonance" (roughness)
# function at frequency x_hz with respect to ref_hz.
# Based on Sethares 1997, as implemented in Giordano 2015.
def sethares_roughness_pair(x_hz, ref_hz, v_x, v_ref, *, amp_type='MIN', cutoff=False, options = {
    'original': False
}):
    s = sc['s_star'] / (sc['s1'] * min([x_hz, ref_hz]) + sc['s2'])
    v12 = pair_volume(v_x, v_ref, amp_type)

    # The following scaling factor is introduced to ensure that the maximum
    # value obtained by the pairwise roughness function is approximately 1.
    # The numerator comes from Sethares' MATLAB implementation; the
    # denominator is my additional modification.
    scaling = 5 / 0.8986

    distance = pair_distance(x_hz, ref_hz)

    # Cutoff: Following Hutchinson and Knopoff 1978, cuts off the Sethares
    # roughness function at 1.2 CBW, which prevents too-remote partials from
    # contributing to the final score. (Check whether this also prevents drift
    # for larger intervals.)
    # Sethares' original does not use this cutoff.
    if cutoff:
        cbw_limit = 1.2 * cbw(max[x_hz, ref_hz]) / 2
        if distance < ac['slow_beat_limit'] or distance >= cbw_limit:
            v12 = 0

    # Sethares' MATLAB implementation (but not the published paper)
    if options['original']:
        scaling = 5

    try:
        return v12 * scaling * (math.exp(-sc['a'] * s * distance) - math.exp(-sc['b'] * s * distance))
    except OverflowError:
        print(f"Overflow in computing roughness: a == {sc['a']}, b == {sc['b']}, s == {s}, distance == {distance}")


# Returns roughness contribution of two partials, based on an indicator
# function on the critical bandwidth, scaled to the amplitude of the partial.
def cbw_roughness_pair(x_hz, ref_hz, v_x, v_ref, options={ 'amp_type': 'MIN' }):
    cbw_limit = cbw(max([x_hz, ref_hz])) / 2
    distance = pair_distance(x_hz, ref_hz)

    if distance >= 15 and distance < cbw_limit:
        return pair_volume(v_x, v_ref, options['amp_type'])
    else:
        return 0

# From Bigand, Parncutt, and Lerdahl 1996. Note that the volumes are not used
def parncutt_roughness_pair(x_hz, ref_hz, v_x, v_ref, options = {}):
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

###################
# SUMMATION MODEL #
###################

# The following function is based on Sethares' 1993 model, which linearly sums
# all pairwise contributions to roughness. It can use any of the other
# pairwise roughness evaluation functions.
def roughness_complex(
    spectrum: MergedSpectrum,
    function_type: str = 'SETHARES',
    amp_type: str = 'MIN',
    cutoff: bool = False,
    rough_limit: float = 0.1,
    *,
    options={
        'original': False
    }
):
    n = len(spectrum.partials['hz'])
    rough_partials = []
    rough_vals = np.zeros((n, n))

    if function_type.upper() == 'SETHARES':
        pair_assess = sethares_roughness_pair
    elif function_type.upper() == 'CBW':
        pair_assess = cbw_roughness_pair
    elif function_type.upper() == 'PARNCUTT':
        pair_assess = parncutt_roughness_pair
    elif function_type.upper() == 'HELMHOLTZ':
        pair_assess = helmholtz_roughness_pair

    # Assess all pairs for roughness
    for i in range(n - 1):
        for j in range(i + 1, n):
            rough_vals[i][j] = pair_assess(
                spectrum.partials['hz'][i],
                spectrum.partials['hz'][j],
                spectrum.partials['amp'][i],
                spectrum.partials['amp'][j],
                options=options
            )
            if rough_vals[i][j] > rough_limit:
                rough_partials.append((i, j))

    return {
        'roughness': np.sum(rough_vals),
        'rough_partials': rough_partials
    }
