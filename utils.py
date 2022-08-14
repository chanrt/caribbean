from math import sqrt


def global_distance_between(a, b):
    return sqrt((a.global_position[0] - b.global_position[0]) ** 2 + (a.global_position[1] - b.global_position[1]) ** 2)
