

def global_distance_between(a, b):
    return ((a.global_position[0] - b.global_position[0]) ** 2 + (a.global_position[1] - b.global_position[1]) ** 2) ** 0.5
