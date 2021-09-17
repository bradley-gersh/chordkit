# chordkit

Utility for graphing computations of roughness and overlap based on Sethares's 1993 paper and updates.

## Dependencies

This package runs on Python 3 and requires NumPy, Pandas, and Matplotlib to be installed.

## Usage

In a directory with access to the `chordkit` package, run Python and import the package:

```python
import chordkit as ck
```

The primary classes of the package are the following:

- `Timbre(fund_multiple, amp)`: specify a timbre for the pitches of a chord.
  - `freq` (list): a list of numbers specifying which multiples of the fundamental are contained in this timbre. For example, if `freq = range(1, 5)`, the timbre will contain the first four partials of the harmonic spectrum.
  - `amp` (list or int): a list of numbers specifying the amplitude (in arbitrary units) of each partial. `amp` and `freq` must be the same length. Alternatively, setting this argument to the integer `1` will create a flat spectrum.
- `Chord(chord_structure, chord_structure_type, timbre, fund_hz)`: generate a chord of a specified structure using the specified timbre.
  - `chord_structure` (list): a list of floats representing the pitches of each chord. By default, these represent semitones above `fund_hz`; for example, `[0, 4, 7]` represents a major triad in closed position, where `0` has the frequency of `fund_hz`. Fractional and negative numbers are permitted.
  - `chord_structure_type` (str): specifies the meaning of numbers in the chord structure.
    - `ST_DIFF` (default): `chord_structure` uses semitonal displacement from `fund_hz` (example: `[0, 4, 7]`)
    - `SCALE_FACTOR`: `chord_structure` uses frequency ratios above `fund_hz` (example: `[1.0, 5.0/4.0, 2.0]`)
    - `HZ_SHIFT`: `chord_structure` uses linear frequency shifts above `fund_hz` (example: `[0.0, 55.0, 220.0]`)
  - `timbre`: specifies the timbre used by each tone in the chord. If unspecified, the default timbre has 12 harmonic overtones, where overtone _p_ has amplitude 0.88^_p_.
  - `fund_hz`: specifies the frequency (Hz) of the reference for `chord_structure`. If unspecified, the default is `fund_hz = 220.0`.

Verification tests are run with `make test`.

## Sample usage

Several examples of use will be found in `ch2_figures.py`, which generates various graphs seen in the dissertation.

### Print the Sethares graph of roughness of a single pitch

```python
import chordkit as ck

# Generate a reference chord to hold fixed in place
ref_chord = ck.Chord([0])

# Generate a test chord to sweep over the reference chord
test_chord = ck.Chord([0])

# Plot the roughness of each interval produced by sweeping the test_chord
# across the ref_chord. (Uses default settings: the ref_chord is fixed at
# 220.0 Hz, and the test_chord sweeps from 0.5 semitones below the ref_chord to
# 12.5 semitones above the ref_chord.)
rough = ck.roughness_curve(ref_chord, test_chord, plot=True)
```

## References

- Sethares, William. 1993. "Local Consonance and the Relationship Between Timbre and Scale." Journal of the Acoustical Society of America 94, no. 1: 1218–1222.
- Terhardt, Ernst, Gerhard Stoll, and Manfred Seewann. 1982. "Algorithm for Extraction of Pitch and Pitch Salience from Complex Tonal Signals." Journal of the Acoustical Society of America 71, no. 3: 679–688.
- Völk, Florian. 2015. "Updated Analytical Expressions for Critical Bandwidth and Critical-Band Rate." DAGA 2015, Nürnberg.
- Zwicker, Eberhard, and Ernst Terhardt. 1980. "Analytical Expressions for Critical-Band Rate and Critical Bandwidth as a Function of Frequency." Journal of the Acoustical Society of America 68, no. 5: 1523-1525.
