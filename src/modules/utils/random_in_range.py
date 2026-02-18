import random

def random_in_range(base_val:int, variance_ratio:float =0.25):
    if base_val <= 1:
        return 1
    min_val = round(base_val - (base_val * variance_ratio))
    max_val = round(base_val + (base_val * variance_ratio))
    return random.randint(min_val, max_val)