import numpy as np
from hearing_models import cbw_volk as cbw, bark_zwicker as bar
from pair_constants import SETHARES_CONSTANTS as sc, AUDITORY_CONSTANTS as ac, pair_volume, pair_distance
from chord_utils import MergedSpectrum

# Returns overlap contribution of two partials, based on an indicator
# function on the overlap zone, scaled to the amplitude of the partial.
# This is called "cbw" because it pairs with the pair-roughness function that
# uses an indicator function on the critical bandwidth, but the CBW is not used.
def cbw_overlap_pair(x_hz, ref_hz, v_x, v_ref, options={
    'amp_type': 'MIN'
}):
    distance = pair_distance(x_hz, ref_hz)

    if distance < ac['slow_beat_limit']:
        return pair_volume(v_x, v_ref, options['amp_type'])
    else:
        return 0

# Uses a bump function from a cosine wave to measure overlap
def cos_overlap_pair(x_hz, ref_hz, v_x, v_ref, options={
    'amp_type': 'MIN'
}):
    distance = pair_distance(x_hz, ref_hz)
    flat = cbw_overlap_pair(x_hz, ref_hz, v_x, v_ref, options)

    return flat * 0.5 * (1 + np.cos(np.pi * distance/ac['slow_beat_limit']))

# An imitation of the Sethares (1993) roughness function, but for overlap,
# using a bell-like function
def bell_overlap_pair(x_hz, ref_hz, v_x, v_ref, options={
    'amp_type': 'MIN',
    'K': -2.374,
    'cutoff': False
}):
    s = sc['s_star'] / (sc['s1'] * min([x_hz, ref_hz]) + sc['s2'])
    v12 = pair_volume(v_x, v_ref, options['amp_type'])

    # The following scaling factor is introduced to ensure that the maximum
    # value obtained by the pairwise roughness function is approximately 1.
    # 'K' can be overriden in the options dictionary
    K = -2.374
    if 'K' in options:
        K = options['K']

    distance = pair_distance(x_hz, ref_hz)

    # Cutoff: Following Hutchinson and Knopoff 1978, cuts off the overlap
    # function at 1.2 CBW, which prevents too-remote partials from
    # contributing to the final score.
    if options['cutoff'] == True:
        cbw_limit = 1.2 * cbw(max[x_hz, ref_hz]) / 2
        if distance < ac['slow_beat_limit'] or distance >= cbw_limit:
            v12 = 0

    try:
        return v12 * np.exp(K * sc['b'] * s * distance)
    except OverflowError:
        print(f'Overflow in computing overlap: b == {sc["b"]}, s == {s}, distance == {distance}')

###################
# SUMMATION MODEL #
###################

# The following function is based on Sethares' 1993 model, adapted for summing
# pairwise overlap functions.
def overlap_complex(
    spectrum: MergedSpectrum,
    function_type: str = 'BELL',
    overlap_limit: float = 0.1,
    *,
    options={
        'amp_type': 'MIN',
        'cutoff': False,
        'original': False,
        'show_partials': False
    }
):
    n = len(spectrum.partials['hz'])
    overlap_partials = []
    overlap_vals = np.zeros((n, n))

    if function_type.upper() == 'BELL':
        pair_assess = bell_overlap_pair
    elif function_type.upper() == 'CBW':
        pair_assess = cbw_overlap_pair
    elif function_type.upper() == 'COS':
        pair_assess = cos_overlap_pair
    else:
        raise ValueError(f'Invalid assessment function type: {function_type.upper()}')

    # Assess all pairs for overlap
    for i in range(n - 1):
        for j in range(i + 1, n):
            overlap_vals[i][j] = pair_assess(
                spectrum.partials['hz'][i],
                spectrum.partials['hz'][j],
                spectrum.partials['amp'][i],
                spectrum.partials['amp'][j],
                options=options
            )
        if options['show_partials'] == True and overlap_vals[i][j] > overlap_limit:
            overlap_partials.append((i, j))

    if options['show_partials']:
        return {
            'overlap': np.sum(overlap_vals),
            'overlap_partials': overlap_partials
        }

    return np.sum(overlap_vals)
