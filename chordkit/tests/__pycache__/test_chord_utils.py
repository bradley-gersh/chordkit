import unittest
import chord_utils as cu
import pandas as pd
from pandas.testing import assert_frame_equal

class TestMakeTimbre(unittest.TestCase):
    # test: make_timbre works with no amplitudes supplied
    def test_make_timbre_no_amps(self):
        test_timbre = pd.DataFrame({
          'fund_multiple': [1, 3, 5],
          'amps': [1, 1, 1]
        })
        assert_frame_equal(test_timbre, cu.make_timbre([1, 3, 5]))

    # test: make_timbre works for many amplitudes
    def test_make_timbre_many_amps(self):
        test_timbre = pd.DataFrame({
          'fund_multiple': [1, 2, 3, 4, 5],
          'amps': [1/1, 1/2, 1/3, 1/4, 1/5]
        })
        assert_frame_equal(test_timbre, cu.make_timbre(range(1,6), [1/n for n in range(1,6)]))

class TestMakeChord(unittest.TestCase):
    timbre = cu.make_timbre(range(1,2), [1/n for n in range(1,2)])
    fund_hz = 220

    # test: make_chord makes a chord using semitone-based intervals
    def test_make_chord_st_diff(self):
        chord_struct = [0, 4, 7]
        test_chord = pd.DataFrame({

        })
        assert_frame_equal(test_chord, cu.make_chord(timbre, fund_hz, chord_struct, 'ST_DIFF'))

    # test: make_chord makes a chord using frequency ratios for intervals
    def test_make_chord_scale_factor(self):
        chord_struct = [1, 3/2, 2]
        test_chord = pd.DataFrame({

        })
        assert_frame_equal(test_chord, cu.make_chord(timbre, fund_hz, chord_struct, 'SCALE_FACTOR'))

if __name__ == '__main__':
    unittest.main()
