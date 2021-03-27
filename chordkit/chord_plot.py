import pandas as pd
import matplotlib.pyplot as plt
import chord_utils as cu

def chord_plot(chord: pd.DataFrame):
    plt.stem(chord['hz'], chord['amp'])
    plt.show()
