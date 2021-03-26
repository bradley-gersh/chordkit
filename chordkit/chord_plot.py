import pandas as pd
import chord_utils as cu

def chord_plot(timbre: DataFrame, fund_hz: float, chord_struct: DataFrame, chord_type: str = 'ST_DIFF'):
    chord = []
