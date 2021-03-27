import pandas as pd
import numpy as np

def make_timbre(fund_multiple: list or range, amps: list = 1):
    timbre = pd.DataFrame({
        'fund_multiple': list(fund_multiple),
        'amps': np.ones_like(fund_multiple)
    })

    if amps != 1:
        timbre['amps'] = amps

    return timbre

def make_chord(timbre: pd.DataFrame, fund_hz: float, chord_struct: list, chord_struct_type: str = 'ST_DIFF'):
    chord = pd.DataFrame();

    # Reference tone for generating chord
    ref_tone = timbre.copy();
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
    for idx, note in enumerate(chord_struct):
        new_note = ref_tone.copy()
        new_note['hz'] = new_note_hz(note)
        new_note['note_id'] = idx
        chord = chord.append(new_note, ignore_index = True)

    return chord.reindex(['hz', 'amps', 'note_id', 'fund_multiple'], axis=1).sort_values(by = 'hz')
