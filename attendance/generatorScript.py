a = 656550107
c = 8849371
m = 9850349

def generatorScript(seed):
    seed = (seed % m) * (a % m)
    seed = seed % m
    seed = seed + c
    seed = seed % m
    return seed
