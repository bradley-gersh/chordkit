import numpy as np

# Implementation of Bark formula (eq. 6) from Terhardt, Stoll, and Seewann 1982.
# Uses the Zwicker and Terhardt 1980 convention. See
# https://ccrma.stanford.edu/courses/120-fall-2003/lecture-5.html for
# other conventions, as well as Voelk 2015.
def bark_zwicker(hz):
    khz = hz / 1000
    return 13 * np.atan(0.76 * khz) + 3.5 * np.atan((khz / 7.5) ** 2)

# Critical bandwidth, using Voelk 2015
def cbw_volk(hz):
    khz = hz / 1000
    gz = 25 + 75 * (1 + 1.4 * (khz ** 2)) ** 0.69
    return gz * (1 - 1 / ((38.73 * khz) ** 2+1))

# Critical bandwidth, per Zwicker and Terhardt 1980
def cbw_zwicker(hz):
    khz = hz / 1000
    return 25 + 75 * (1 + 1.4 * khz ** 2) ** 0.69

# Critical bandwidth, per Hutchinson and Knopoff 1978, 5
def cbw_hutchinson(hz):
    return 1.72 * (hz ** 0.65)
