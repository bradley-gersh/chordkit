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
        return Timbre(list(self.partials['fund_multiple']), list(self.partials['amp']))

def sort_partials(partials: pd.DataFrame):
    return partials.reindex(['hz', 'amp', 'note_id', 'fund_multiple', 'hz_orig'], axis=1).sort_values(by = 'hz', ignore_index = True)

class MergedSpectrum:
    # Need to overload to merge two chords
    def __init__(self, *args):
    # def __init__(self, timbre: Timbre, fund_hz: float = default_fund):
        if isinstance(args[0], Timbre):
            self.partials = args[0].partials.copy()
            self.partials['hz'] = self.partials['fund_multiple']
            if isinstance(args[1], float) or isinstance(args[1], int):
                self.fund_hz = float(args[1])
                if args[1] > 0:
                    self.partials['hz'] *= self.fund_hz
            else:
                self.fund_hz = 0

        # Constructor called with ChordSpectrum or MergedSpectrum objects: merges them
        elif isinstance(args[0].partials, pd.DataFrame):
            self.fund_hz = 0
            # Two spectra provided: merge them
            if len(args) > 1 and isinstance(args[1].partials, pd.DataFrame):
                self.partials = args[0].partials.append(args[1].partials, ignore_index = True)
                self.partials = sort_partials(self.partials)
            # Only one spectrum provided: copy it over
            else:
                self.partials = args[0].partials.copy(deep=True)

    # Display a stem plot of the spectrum
    def plot(self):
        plt.stem(self.partials['hz'], self.partials['amp'])
        plt.show()


class ChordSpectrum:
    def __init__(
        self,
        chord_struct: list,
        chord_struct_type: str = 'ST_DIFF',
        *,
        timbre: Timbre = basic_saw_timbre,
        fund_hz: float = default_fund
    ):
        self.partials = pd.DataFrame()
        self.struct = chord_struct
        self.struct_type = chord_struct_type
        self.timbre = timbre
        self.fund_hz = fund_hz
        self.fund_hz_orig = fund_hz
        self.ref_tone = MergedSpectrum(timbre, fund_hz)

        # Generate chord from reference tone and chord structure
        for (idx, note) in enumerate(chord_struct):
            new_tone = MergedSpectrum(timbre, fund_hz)
            # print('note', note)
            new_tone.partials['hz'] = self.add_note_hz(note)
            new_tone.partials['hz_orig'] = new_tone.partials['hz']
            new_tone.partials['note_id'] = idx
            self.partials = self.partials.append(new_tone.partials, ignore_index = True)

        self.partials = sort_partials(self.partials)

    # Generate a new note for the chord, based on the chord_struct_type
    def add_note_hz(self, note_hz):
        # chord_struct defines intervals by semitone difference
        if self.struct_type.upper() == 'ST_DIFF':
            return 2 ** (note_hz / 12) * self.ref_tone.partials['hz']
        # chord_struct defines intervals by frequency scaling (ratios)
        elif self.struct_type.upper() == 'SCALE_FACTOR':
            return note_hz * self.ref_tone.partials['hz']
        # chord_struct defines intervals by absolute Hz difference
        # NB: This is still assuming that the timbre describes each tone by
        # multiples of that tone's fundamental.
        elif self.struct_type.upper() == 'HZ_SHIFT':
            return note_hz + self.ref_tone.partials['hz']
        else:
            raise ValueError(f'invalid chord structure type: {self.struct_type}')

    def set_fund_hz(self, new_fund_hz: float):
        self.fund_hz = new_fund_hz
        self.partials['hz'] = self.partials['fund_multiple'] * new_fund_hz

    # Update chord's frequency table to reflect a transposition
    def transpose(self, position: float, transpose_type: str):
        if transpose_type.upper() != self.struct_type.upper():
            Warning('chord structure type does not match transposition type')

        if transpose_type.upper() == 'ST_DIFF':
            # self.partials['hz'] *= 2 ** (position / 12)
            self.set_fund_hz(2 ** (position / 12) * self.fund_hz_orig)
            self.partials['fund_multiple'] = self.partials['hz'] / self.fund_hz
        elif transpose_type.upper() == 'SCALE_FACTOR':
            # self.partials['hz'] *= position
            self.set_fund_hz(position * self.fund_hz_orig)
            self.partials['fund_multiple'] = self.partials['hz'] / self.fund_hz
        elif transpose_type.upper() == 'HZ_SHIFT':
            self.partials['hz'] = self.partials['hz_orig'] + position
        else:
            raise ValueError('invalid chord structure type')


    # Display a stem plot of the chord
    def plot(self):
        plt.stem(self.partials['hz'], self.partials['amp'])
        plt.show()


class TransposeDomain:
    def __init__(self, low_bound, high_bound, steps, transpose_type):
        self.domain = np.linspace(low_bound, high_bound, num=steps)
        self.transpose_type = transpose_type

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
