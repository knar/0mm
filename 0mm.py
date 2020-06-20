#!/usr/bin/env python

import sys
import math

games = {
    'source': 0.022,
    'ow': 0.0066,
    'valorant': 0.07,
    'aimpro': 360 / (1000 * 2 * math.pi),
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

def read_input():
    argc = len(sys.argv)
    if argc < 5:
        print("Usage: ./0mm <cm|source> <sens> <dpi> <fov> [optional fovs]")
        exit()

    dpi = int(sys.argv[3])
    base_cm = float(cm_to_sens(float(sys.argv[2]), dpi, 0, sys.argv[1]) if sys.argv[1] != 'cm' else sys.argv[2])
    base_fov = float(sys.argv[4]) 
    fovs = [base_fov]
    fovs += [float(sys.argv[i]) for i in range(5, argc)]

    # default fovs to convert to
    if len(fovs) == 1:
        for f in range(70, 131, 5):
            fovs.append(f)

        fovs.append(103)
        fovs.append(fov_aspect_ratio(90, 3, 4)) # csgo
        fovs.append(fov_aspect_ratio(110, 3, 4)) # 124.blahblah for solo

    fovs = list(set(fovs))
    fovs.sort()

    return dpi, base_cm, base_fov, fovs

def conversions(dpi, base_cm, base_fov, fovs):
    convs = {
        'hfov': fovs,
        'cm': [base_cm * zoom_ratio(base_fov, fov) for fov in fovs],
    }

    for game in games:
        convs[game] = [cm_to_sens(convs['cm'][i], dpi, convs['hfov'][i], game) for i in range(len(convs['cm']))]

    # precision
    for arr in convs:
        convs[arr] = list(map(lambda x: round(x, 4), convs[arr]))
        m = max(list(map(lambda x: len(str(x)), convs[arr])))
        convs[arr] = convs[arr], max(len(arr), m)

    return convs

def formatted_print(convs):
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