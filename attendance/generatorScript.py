RANDOM_MAX = 2147483647

def generatorScript(seed):
    if seed == 0:
        seed = 123459876
    hi = seed // 127773
    lo = seed % 127773
    seed = 16807 * lo - 2836 * hi
    if seed < 0:
        seed += RANDOM_MAX
    return seed % (RANDOM_MAX + 1)
