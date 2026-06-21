import random
def generate_pin(): return ''.join(str(random.randint(0,9)) for _ in range(4))
