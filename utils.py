

def global_distance_between(a, b):
    return sum((a.global_position - b.global_position) ** 2) ** 0.5
