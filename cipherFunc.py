def calculateKey(l: list | tuple) -> int:
    key1 = sum(l[0::2])
    key2 = sum(l[1::2])
    key = ((key1 + key2)**2 // (key1**2) + (key2**2))
    return key