import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
import chordkit.chord_utils as cu

class TestTimbre(unittest.TestCase):
    # test: make_timbre works with no amplitudes supplied
    def test_make_timbre_no_amps(self):
        test_timbre = pd.DataFrame({
          'fund_multiple': [1, 3, 5],
          'amp': [1, 1, 1]
        })
        assert_frame_equal(test_timbre, cu.Timbre([1, 3, 5]).partials)

    # test: make_timbre works for many amplitudes
    def test_make_timbre_many_amps(self):
        test_timbre = pd.DataFrame({
          'fund_multiple': [1, 2, 3, 4, 5],
          'amp': [1/1, 1/2, 1/3, 1/4, 1/5]
        })
        assert_frame_equal(test_timbre, cu.Timbre(range(1,6), [1/n for n in range(1,6)]).partials)

class TestMakeChord(unittest.TestCase):

    # test: make_chord makes a chord using semitone-based intervals
    def test_make_chord_st_diff(self):
        timbre = cu.Timbre(range(1,3), [1/n for n in range(1,3)])
        chord_struct = [0, 12]
        fund = 220
        test_chord = pd.DataFrame({
            'hz': [220.0, 440.0, 440.0, 880.0],
            'amp': [1.0, 0.5, 1.0, 0.5],
            'note_id': [0, 0, 1, 1],
            'fund_multiple': [1, 2, 1, 2],
            'hz_orig': [220.0, 440.0, 440.0, 880.0],
        })
        assert_frame_equal(test_chord, cu.ChordSpectrum(chord_struct, 'ST_DIFF', timbre=timbre, fund_hz=fund).partials)

    # test: make_chord makes a chord using frequency ratios for intervals
    def test_make_chord_scale_factor(self):
        timbre = cu.Timbre(range(1,3), [1/n for n in range(1,3)])
        chord_struct = [1, 2]
        fund = 220
        test_chord = pd.DataFrame({
            'hz': [220., 440., 440., 880.],
            'amp': [1.0, 0.5, 1.0, 0.5],
            'note_id': [0, 0, 1, 1],
            'fund_multiple': [1, 2, 1, 2],
            'hz_orig': [220., 440., 440., 880.]
        })
        assert_frame_equal(test_chord, cu.ChordSpectrum(chord_struct, 'SCALE_FACTOR', timbre=timbre, fund_hz=fund).partials)

if __name__ == '__main__':
    unittest.main()
