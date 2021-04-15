import numpy as np
import chordkit.chord_utils as cu
from chordkit.graph_roughness import roughness_curve

class TestRoughnessGraph(unittest.TestCase):
    # test: Roughness graph works
    def test_roughness_graph(self):
        # tim = cu.Timbre(range(1, 13))
        # x = roughness_curve([0], 'ST_DIFF', fund_hz=220, ref_timbre=tim, test_chord_struct=[0], test_timbre=tim, slide_range=numpy.linspace(0, 12, num=1000), function_type='SETHARES')
        x = roughness_curve(cu.ChordSpectrum([0]), cu.ChordSpectrum([0]), tranpose_range=np.linspace(0, 12, num=1000), plot=True)
