#!/usr/bin/env python

import sys
import math

aspect_ratio = 16/9

games = {
    'source': 0.022,
    #'valorant': 0.07,
    #'ow': 0.0066,
    #'roblox': 0.36,
    #'aimpro': 360 / (1000 * 2 * math.pi),
}

def cm_to_sens(cm, dpi, fov, game):
    return 2.54 * 360 / (cm * dpi * games[game])

def zoom_ratio(fov1, fov2):
    return math.tan(math.radians(fov1) / 2) / math.tan(math.radians(fov2) / 2)

def md_ratio(fov1, fov2, r):
    theta1 = math.atan(r * math.tan(math.radians(fov1) / 2))
    theta2 = math.atan(r * math.tan(math.radians(fov2) / 2))
    return theta1 / theta2

def fov_aspect_ratio(fov, a, b):
    return 2 * math.degrees(math.atan(b * math.tan(math.radians(fov)/2) / a))

def parse_dpi(dpi):
    try:
        return int(dpi)
    except ValueError:
        print("Invalid dpi input, could not convert to number")
        exit()

def parse_sens(type, sens, dpi):
    try:
        if sys.argv[1] != 'cm':
            return float(cm_to_sens(float(sens), dpi, 0, type))
        return float(sens)
    except KeyError:
        print("Invalid game provided, try one of the following:")
        print(list(games.keys()))
        exit()
    except ValueError:
        print("Invalid sens input, could not convert to number")
        exit()

def parse_fov(fov):
    try:
        if fov[-1] == 'v':
            return fov_aspect_ratio(float(fov[:-1]), 1, aspect_ratio)
        elif fov[-1] == 's':
            return fov_aspect_ratio(float(fov[:-1]), 4/3, aspect_ratio)
        return float(fov)
    except ValueError:
        print("Invalid fov input, could not convert to number")
        exit()

def read_input():
    argc = len(sys.argv)
    if argc < 5:
        print("Usage: ./0mm <cm|game> <sens> <dpi> <fov>[v,s] [optional fovs]")
        exit()

    dpi = parse_dpi(sys.argv[3])
    base_cm = parse_sens(sys.argv[1], sys.argv[2], dpi)
    base_fov = parse_fov(sys.argv[4])

    fovs = [base_fov]
    fovs += [parse_fov(sys.argv[i]) for i in range(5, argc)]
    fovs = list(set(fovs))
    fovs.sort()

    return dpi, base_cm, base_fov, fovs

def conversions(dpi, base_cm, base_fov, fovs):
    convs = {
        'hfov': fovs,
        #'vfov': [fov_aspect_ratio(f, aspect_ratio, 1) for f in fovs],
        #'sfov': [fov_aspect_ratio(f, aspect_ratio, 4/3) for f in fovs],
        'cm': [base_cm * zoom_ratio(base_fov, fov) for fov in fovs],
        #'cm': [base_cm * md_ratio(base_fov, fov, 1) for fov in fovs],
    }

    for game in games:
        convs[game] = [cm_to_sens(convs['cm'][i], dpi, convs['hfov'][i], game) for i in range(len(convs['cm']))]
    
    return convs

def formatted_print(convs):
    # precision
    for arr in convs:
        convs[arr] = list(map(lambda x: round(x, 3), convs[arr]))
        m = max(list(map(lambda x: len(str(x)), convs[arr])))
        convs[arr] = convs[arr], max(len(arr), m)
    
    # header
    print('')
    ttls = [ttl.ljust(convs[ttl][1]) for ttl in convs]
    print(' | '.join(ttls))

    spltrs = ['-' * convs[ttl][1] for ttl in convs]
    print(' | '.join(spltrs))

    # rows
    for row in range(len(fovs)):
        vals = [str(convs[col][0][row]).ljust(convs[col][1]) for col in convs]
        print(' | '.join(vals))

dpi, base_cm, base_fov, fovs = read_input()
convs = conversions(dpi, base_cm, base_fov, fovs)
formatted_print(convs)