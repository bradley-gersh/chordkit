import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Sample usage: make_timbre(range(1, 13))
def make_timbre(fund_multiple: list or range, amp: list = 1):
    timbre = pd.DataFrame({
        'fund_multiple': list(fund_multiple),
        'amp': np.ones_like(fund_multiple)
    })

    if amp != 1:
        timbre['amp'] = amp

    return timbre

default_timbre = make_timbre(range(1, 13), [1/n for n in range(1, 13)])
default_fund = 220

# Sample usage: make_chord([0, 4, 7])
def make_chord(
    chord_struct: list,
    chord_struct_type: str = 'ST_DIFF',
    *,
    timbre: pd.DataFrame = default_timbre,
    fund_hz: float = default_fund
):
    chord = pd.DataFrame()

    # Reference tone for generating chord
    ref_tone = timbre.copy()
    ref_tone['hz'] = ref_tone['fund_multiple']
    if fund_hz > 0:
        ref_tone['hz'] *= fund_hz

    # Generate a new note for the chord, based on the chord_struct_type
    def new_note_hz(note):
        # chord_struct defines intervals by semitone difference
        if chord_struct_type == 'ST_DIFF':
            return 2**(note/12) * ref_tone['hz']
        # chord_struct defines intervals by frequency scaling (ratios)
        elif chord_struct_type == 'SCALE_FACTOR':
            return note * ref_tone['hz']
        # chord_struct defines intervals by absolute Hz difference
        # NB: This is still assuming that the timbre describes each tone by
        # multiples of that tone's fundamental.
        elif chord_struct_type == 'HZ_SHIFT':
            return note + ref_tone['hz']
        else:
            raise ValueError('invalid chord structure type')

    # Generate chord from reference tone and chord structure
    for (idx, note) in enumerate(chord_struct):
        new_note = ref_tone.copy()
        new_note['hz'] = new_note_hz(note)
        new_note['note_id'] = idx
        chord = chord.append(new_note, ignore_index = True)

    return chord.reindex(['hz', 'amp', 'note_id', 'fund_multiple'], axis=1).sort_values(by = 'hz', ignore_index = True)

# The following only returns the updated frequencies from sliding a chord, which
# is more efficient than creating a new chord data frame each time.
def slide_timbre(position, timbre, *, chord_struct_type, fund_hz = 220):
    if chord_struct_type.upper() == 'ST_DIFF':
        return 2 ** (position / 12) * timbre['fund_multiple']
    elif chord_struct_type.upper() == 'SCALE_FACTOR':
        return position * timbre['fund_multiple']
    elif chord_struct_type.upper() == 'HZ_SHIFT':
        return fund_hz * timbre['fund_multiple'] + position
    else:
        raise ValueError('invalid chord structure type')

def plot_chord(chord: pd.DataFrame):
    plt.stem(chord['hz'], chord['amp'])
    plt.show()

def plot_line(series):
    plt.plot(series)
    plt.show()
