import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

###########
# CLASSES #
###########
class Timbre:
    def __init__(self, fund_multiple: list or range, amp: list = 1):
        self.partials = pd.DataFrame({
            'fund_multiple': list(fund_multiple),
            'amp': np.ones_like(fund_multiple)
        })

        if amp != 1:
            self.partials['amp'] = amp

    def copy(self):
        return Timbre(self.fund_multiple, self.amp)

default_timbre = Timbre(range(1, 13), [1/n for n in range(1, 13)])
default_fund = 220

class Spectrum:
    def __init__(self, timbre: Timbre, fund_hz: float = default_fund):
        self.partials = timbre.copy()
        self.fund_hz = fund_hz
        self.partials['hz'] = self.partials['fund_multiple']
        if fund_hz > 0:
            self.partials['hz'] *= fund_hz

class ChordSpectrum:
    def __init__(
        self,
        chord_struct: list,
        chord_struct_type: str = 'ST_DIFF',
        *,
        timbre: Timbre = default_timbre,
        fund_hz: float = default_fund
    ):
        self.partials = pd.DataFrame()
        self.struct = chord_struct
        self.struct_type = chord_struct_type
        self.timbre = timbre
        self.fund_hz = fund_hz
        self.ref_tone = Spectrum(timbre, fund_hz)

        # Generate chord from reference tone and chord structure
        for (idx, note) in enumerate(chord_struct):
            new_tone = Spectrum(timbre, fund_hz)
            new_tone.partials['hz'] = self.add_note_hz(note)
            new_tone.partials['note_id'] = idx
            self.partials = self.partials.append(new_tone.partials, ignore_index = True)

        self.partials = self.partials.reindex(['hz', 'amp', 'note_id', 'fund_multiple'], axis=1).sort_values(by = 'hz', ignore_index = True)

    # Generate a new note for the chord, based on the chord_struct_type
    def add_note_hz(self, note_hz):
        # chord_struct defines intervals by semitone difference
        if self.struct_type == 'ST_DIFF':
            return 2 ** (note_hz / 12) * self.ref_tone.partials['hz']
        # chord_struct defines intervals by frequency scaling (ratios)
        elif self.struct_type == 'SCALE_FACTOR':
            return note_hz * self.ref_tone.partials['hz']
        # chord_struct defines intervals by absolute Hz difference
        # NB: This is still assuming that the timbre describes each tone by
        # multiples of that tone's fundamental.
        elif self.struct_type == 'HZ_SHIFT':
            return note_hz + self.ref_tone.partials['hz']
        else:
            raise ValueError('invalid chord structure type')

    # Update chord's frequency table to reflect a transposition
    def transpose(self, position: float, position_type: str):
        if position_type.upper() != self.struct_type.upper():
            Warning('chord structure type does not match transposition type')

        if position_type.upper() == 'ST_DIFF':
            self.partials['hz'] *= 2 ** (position / 12)
        elif position_type.upper() == 'SCALE_FACTOR':
            self.partials['hz'] *= position
        elif position_type.upper() == 'HZ_SHIFT':
            self.partials['hz'] += position
        else:
            raise ValueError('invalid chord structure type')

        self.partials['fund_multiple'] = self.partials['hz'] / self.fund_hz

    # Display a stem plot of the chord
    def plot(self):
        plt.stem(self.partials['hz'], self.partials['amp'])
        plt.show()



# Sample usage: make_timbre(range(1, 13))
# def make_timbre(fund_multiple: list or range, amp: list = 1):
#     timbre = pd.DataFrame({
#         'fund_multiple': list(fund_multiple),
#         'amp': np.ones_like(fund_multiple)
#     })

#     if amp != 1:
#         timbre['amp'] = amp

#     return timbre

# default_timbre = make_timbre(range(1, 13), [1/n for n in range(1, 13)])

# Sample usage: make_chord([0, 4, 7])
# def make_chord(
#     chord_struct: list,
#     chord_struct_type: str = 'ST_DIFF',
#     *,
#     timbre: pd.DataFrame = default_timbre,
#     fund_hz: float = default_fund
# ):
#     chord = pd.DataFrame()

#     # Reference tone for generating chord
#     ref_tone = timbre.copy()
#     ref_tone['hz'] = ref_tone['fund_multiple']
#     if fund_hz > 0:
#         ref_tone['hz'] *= fund_hz

#     # Generate a new note for the chord, based on the chord_struct_type
#     def new_note_hz(note):
#         # chord_struct defines intervals by semitone difference
#         if chord_struct_type == 'ST_DIFF':
#             return 2**(note/12) * ref_tone['hz']
#         # chord_struct defines intervals by frequency scaling (ratios)
#         elif chord_struct_type == 'SCALE_FACTOR':
#             return note * ref_tone['hz']
#         # chord_struct defines intervals by absolute Hz difference
#         # NB: This is still assuming that the timbre describes each tone by
#         # multiples of that tone's fundamental.
#         elif chord_struct_type == 'HZ_SHIFT':
#             return note + ref_tone['hz']
#         else:
#             raise ValueError('invalid chord structure type')

#     # Generate chord from reference tone and chord structure
#     for (idx, note) in enumerate(chord_struct):
#         new_note = ref_tone.copy()
#         new_note['hz'] = new_note_hz(note)
#         new_note['note_id'] = idx
#         chord = chord.append(new_note, ignore_index = True)

#     return chord.reindex(['hz', 'amp', 'note_id', 'fund_multiple'], axis=1).sort_values(by = 'hz', ignore_index = True)





def plot_line(series):
    plt.plot(series)
    plt.show()
