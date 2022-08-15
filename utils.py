from math import sqrt

from constants import consts as c

def inside_screen(obj, obj_type):
    if obj_type == "pirate":
        pos = obj.local_position
        if -c.pirate_leeway < pos[0] < c.s_width + c.pirate_leeway and -c.pirate_leeway < pos[1] < c.s_height + c.pirate_leeway:
            return True
        else:
            return False


def global_distance_between(a, b):
    return sqrt((a.global_position[0] - b.global_position[0]) ** 2 + (a.global_position[1] - b.global_position[1]) ** 2)
