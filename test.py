
import faststat

import os
import numpy as np
import array
import random
import functools
import json
import math

_ITER = 100000       # size of population  should be 10 m
_PERC = [0.25, 0.5, 0.99, 0.9, 0.95]  #  percentiles to check
_RES_SIZES = [8192, 16384, 32768]    # sizes of reservoir to check


def average(s):
    return sum(s) * 1.0 / len(s)

def variance(s):
    avg = average(s)
    return average(map(lambda x: (x - avg)**2, s))

def stddev(s):
    return math.sqrt(variance(s))



things = [('expo, 1', functools.partial(random.expovariate, 1)), 
          ('expo, 10', functools.partial(random.expovariate, 10)), 
          ('expo, 100', functools.partial(random.expovariate, 100)),
          ('expo, 100', functools.partial(random.expovariate, 100)),
          ('pareto, 1', functools.partial(random.paretovariate, 1)),
          ('pareto, 10', functools.partial(random.paretovariate, 10)),
          ('pareto, 100', functools.partial(random.paretovariate, 100)),
          ('inv norm, 0, 1', lambda:  1/(random.gauss(0, 1))),
          ('inv norm, 0, 10', lambda:  1/(random.gauss(0, 10))),
          ('inv norm, 0, 100', lambda:  1/(random.gauss(0, 100))),
          ('gausss 1 1', functools.partial(random.gauss, 1, 1)),
          ('gauss 10 1', functools.partial(random.gauss, 10, 1)),
          ('gauss 100 1', functools.partial(random.gauss, 100, 1)),
          ('gauss 1 10', functools.partial(random.gauss, 1, 10)),
          ('gauss 10 10', functools.partial(random.gauss, 10, 10)),
          ('gauss 100 10', functools.partial(random.gauss, 100, 10)),
          ('gauss 1 100', functools.partial(random.gauss, 1, 100)),
          ('gauss 10 100', functools.partial(random.gauss, 10, 100)),
          ('gauss 100 100', functools.partial(random.gauss, 100, 100))]

results = {}

for name, distribution in things:
    results[name] = {}
    print "__________" + name + "__________"
    for x in _PERC:
        results[name][str(x * 100)] = {}
        results[name][str(x * 100)]['true'] = []
        results[name][str(x * 100)]['p2'] = []
        for ss in _RES_SIZES:
            results[name][str(x * 100)]['reservoir' +  str(ss)] = []
    for trials in xrange(0, 100):
        nums = np.zeros(_ITER, dtype=np.dtype('d'))
        samples = []
        for x in _RES_SIZES: 
            samples.append(faststat.Sample(sample_size=x))
        stats = faststat.Stats()
        for i in xrange(0, _ITER):
            try:
                num = distribution()
            except Exception as e:
                continue
            for s in samples:
                s.add(num)
            nums[i] = num
            stats.add(num)
        for x in _PERC:
            results[name][str(x * 100)]['true'].append(np.percentile(nums, x * 100))
            results[name][str(x * 100)]['p2'].append(stats.percentiles[x])
            for samp in samples:
                short_array = np.array(samp.sample)
                results[name][str(x * 100 )]['reservoir' +  str(samp.sample_size)].append(np.percentile(short_array, x * 100))
    with open("results-" + name, 'w') as f:
        print >> f, json.dumps(results[name])
    for x in _PERC:
        for a in results[name][str(x * 100)].keys():
            print a, average(results[name][str(x * 100)][a]), stddev(results[name][str(x * 100)][a])
    
