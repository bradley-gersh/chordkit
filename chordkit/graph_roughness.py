import pandas as pd
import numpy as np

from chordkit.chord_utils import default_timbre, default_fund

def diss_curve(chord_struct: list, chord_struct_type: str = 'ST_DIFF', timbre: pd.DataFrame = default_timbre, fund_hz: float = default_fund, output: str = 'ALL', normalize: bool = True, function_type: str = 'SETHARES'):

    ref_tone = timbre.copy()
    ref_tone['hz'] = ref_tone['fund_multiple']
    # If fund_hz = 0, assume that the incoming timbre is already specified to set
    # exact partial frequencies and doesn't need to be multiplied.
    if fund_hz > 0:
        ref_tone['hz'] *= fund_hz

