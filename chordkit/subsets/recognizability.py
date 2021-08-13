import numpy as np
import pandas as pd
import music21 as m21
import itertools as it

def makeSubsets(pcs):
    allSubsets = []

    for r in range(1, len(pcs) + 1):
        allSubsets = allSubsets + list(it.combinations(pcs, r))

    return allSubsets

def makeM12Chord(set):
    return m21.chord.Chord(set)

def calculateTnClass(m21Chord):
    return tuple(m21Chord.normalOrder)

def calculatePCMultiset(set):
    return tuple(map(lambda x : x % 12, set))

def calculatePCSet(m21Chord):
    return tuple(m21Chord.orderedPitchClasses)


def rankSubsets(pcs):
    # Accepts array of pcs as int[]

    # Make array of all subsets of `pcs`
    allSubsets = makeSubsets(pcs)
    allM12Chords = map(calculateTnClass, allSubsets)

    # Compute other columns
    pcSets = map(calculatePCMultiset, allSubsets)
    TnClasses = map(calculateTnClass, allM12Chords) # Set class

    subsetTable = pd.DataFrame({
        'subset': allSubsets,
        'pcs': pcSets,
        'TnClass': TnClasses
    })

    return subsetTable

print(rankSubsets([0,1,2,3,4,5,6,7,8,9,10,11]))
