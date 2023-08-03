
def index_sequence(key, mask=0b111, PERTURB_SHIFT = 5):
    perturb = hash(key)
    i = perturb & mask
    yield i
    while True:
        perturb >>= PERTURB_SHIFT
        i = (i * 5 + perturb + 1) & mask
        yield i


print(ord("A"))