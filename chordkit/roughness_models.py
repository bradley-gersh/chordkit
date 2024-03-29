import numpy as np
from hearing_models import cbw_volk, cbw_hutchinson
from pair_constants import SETHARES_CONSTANTS as sc, AUDITORY_CONSTANTS as ac, pair_volume, pair_distance
from chord_utils import MergedSpectrum, ChordSpectrum

# This file contains both the individual pairwise models used for assessing the
# roughness of partial pairs and the summing function that adds up all such
# pairwise contributions.

###################
# PAIRWISE MODELS #
###################

# Different pairwise roughness evaluation functions. Each has the same signature
# so that they can be called by the same line of code.

def helmholtz_roughness_pair(x_hz, *, x_p=1, ref_p=1, options={}):
    # Note that x_p and ref_p are now 1-indexed in the function call.

    # The following constants have not been given values by Helmholtz.
    # They are chosen here somewhat arbitrarily to make the graph resemble his.
    bPrime1 = 1
    bPrime2 = 1
    beta = 0.3 # Trial and error; Helmholtz doesn't specify

    # Take partial ref_p from the reference pitch
    ref_hz = options['ref'][ref_p - 1]

    delta = ((float(x_hz) / ref_hz) - 1) / 2
    theta = 15.0 / ref_hz

    s = 4 * bPrime1 * bPrime2 * (beta ** 2) / (beta ** 2 + (2 * np.pi * delta) ** 2)

    r = s * ((2 * theta * delta * x_p) ** 2) / ((theta ** 2 + (x_p * delta) ** 2) ** 2)

    return r

# Returns the value of the Sethares "sensory dissonance" (roughness)
# function at frequency x_hz with respect to ref_hz.
# Based on Sethares 1997, as implemented in Giordano 2015.
def sethares_roughness_pair(x_hz, ref_hz, v_x, v_ref, *, options = {
    'original': False,
    'amp_type': 'MIN',
    'cutoff': False,
}):
    s = sc['s_star'] / (sc['s1'] * min([x_hz, ref_hz]) + sc['s2'])

    if options['original'] == True:
        # This line not based on the Sethares 1993 paper, but on the implementation
        # on his website, https://sethares.engr.wisc.edu/comprog.html
        options['amp_type'] = 'MIN'

    v12 = pair_volume(v_x, v_ref, options['amp_type'])

    # Sethares' MATLAB implementation (but not the published paper)
    # scaling = 5
    
    # For agreement with Harrison and Pearce (2020), I am removing the
    # scaling factor.
    scaling = 1

    # The following scaling factor is introduced to ensure that the maximum
    # value obtained by the pairwise roughness function is approximately 1.
    # The numerator comes from Sethares' MATLAB implementation; the
    # denominator is my additional modification.
    # if options['original'] == False:
        # scaling = 5 / 0.8986

    distance = np.abs(x_hz - ref_hz)

    # Cutoff: Following Hutchinson and Knopoff 1978, cuts off the Sethares
    # roughness function at 1.2 CBW, which prevents too-remote partials from
    # contributing to the final score. (Check whether this also prevents drift
    # for larger intervals.)
    # Sethares' original does not use this cutoff.
    if options['cutoff'] == True:
        cbw_limit = 1.2 * cbw_volk(max[x_hz, ref_hz]) / 2
        if distance < ac['slow_beat_limit'] or distance >= cbw_limit:
            v12 = 0

    try:
        return v12 * scaling * (np.exp(-sc['a'] * s * distance) - np.exp(-sc['b'] * s * distance))
    except OverflowError:
        print(f"Overflow in computing roughness: a == {sc['a']}, b == {sc['b']}, s == {s}, distance == {distance}")


# Returns roughness contribution of two partials, based on an indicator
# function on the critical bandwidth, scaled to the amplitude of the partial.
def cbw_roughness_pair(x_hz, ref_hz, v_x, v_ref, options={ 'amp_type': 'MIN' }):
    cbw_limit = cbw_volk(max([x_hz, ref_hz])) / 2
    distance = pair_distance(x_hz, ref_hz)

    if distance >= 15 and distance < cbw_limit:
        return pair_volume(v_x, v_ref, options['amp_type'])
    else:
        return 0

# From Hutchinson and Knopoff 1978 and Bigand, Parncutt, and Lerdahl 1996.
def parncutt_roughness_pair(x_hz, ref_hz, v_x, v_ref, options = {}):
    # Parameters asserted in BPL 1996 paper
    max_distance = 1.2
    a = 0.25
    i_factor = 2

    freq_difference = abs(x_hz - ref_hz)
    freq_avg = (x_hz + ref_hz) / 2
    freq_avg_cbw = cbw_hutchinson(freq_avg)
    distance = freq_difference / freq_avg_cbw

    # Volume scaling (cf. Hutchinson and Knopoff 1978, 3)
    amp = v_x * v_ref
    
    if distance <= max_distance:
        return amp * (((np.exp(1)/a) * distance * np.exp(-distance / a)) ** i_factor)
    else:
        return 0

###################
# SUMMATION MODEL #
###################

# The following function is based on Sethares' 1993 model, which linearly sums
# all pairwise contributions to roughness. It can use any of the other
# pairwise roughness evaluation functions.
def roughness_complex(
    spectrum: MergedSpectrum or ChordSpectrum,
    function_type: str = 'SETHARES',
    rough_limit: float = 0.1,
    *,
    options={
        'amp_type': 'MIN',
        'cutoff': False,
        'original': False,
        'show_partials': False
    }
):
    n = len(spectrum.partials['hz'])
    rough_partials = []
    rough_vals = np.zeros((n, n))

    if function_type.upper() == 'SETHARES':
        pair_assess = sethares_roughness_pair
        denom = 1
    elif function_type.upper() == 'CBW':
        pair_assess = cbw_roughness_pair
        denom = 1
    elif function_type.upper() == 'PARNCUTT':
        pair_assess = parncutt_roughness_pair
        # Hutchinson and Knopoff (1979, 6) use a single scaling
        # denominator across the entire sum.
        denom = np.sum(spectrum.partials['amp'] ** 2)
    elif function_type.upper() == 'HELMHOLTZ':
        pair_assess = helmholtz_roughness_pair
        denom = 1
    else:
        raise ValueError(f'Invalid assessment function type: {function_type.upper()}')

    # Assess all pairs for roughness

    # Helmholtz's function works differently from the others.
    # In this case, `spectrum` is NOT a composite spectrum of the whole chord:
    # It contains exactly one pitch, which varies by transposition.
    # The second, reference pitch is stored under options['ref'] and is fixed.
    # This method will not work for cardinality > 2.
    if function_type.upper() == 'HELMHOLTZ':
        m = len(spectrum.partials['hz'])
        n = len(options['ref'])
        for i in range(m):
            for j in range(n):
                rough_vals[i][j] = helmholtz_roughness_pair(
                    spectrum.partials['hz'][i],
                    x_p=i + 1, # p is 1-indexed
                    ref_p=j + 1,
                    options=options
                )
                if options['show_partials'] == True and rough_vals[i][j] > rough_limit:
                    rough_partials.append((i, j))

    # Pairwise evaluations, as used by Hutchinson/Knopoff, Sethares, Parncutt)
    else:
        for i in range(n - 1):
            for j in range(i + 1, n):
                rough_vals[i][j] = pair_assess(
                    spectrum.partials['hz'][i],
                    spectrum.partials['hz'][j],
                    spectrum.partials['amp'][i],
                    spectrum.partials['amp'][j],
                    options=options
                )
                if options['show_partials'] == True and rough_vals[i][j] > rough_limit:
                    rough_partials.append((i, j))

    if options['show_partials']:
        return {
            'roughness': np.sum(rough_vals),
            'rough_partials': rough_partials
        }
    
    return np.sum(rough_vals) / denom
