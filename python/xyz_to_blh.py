from math import pi, sin, cos, sqrt, atan2, degrees, asin


def xyz_to_blh(x: float, y: float, z: float) -> tuple[float, float, float]:

    a = 6378137.0  # in meters
    b = 6356752.314245  # in meters

    f = (a - b) / a
    f_inv = 1.0 / f

    e_sq = f * (2 - f)                       
    eps = e_sq / (1.0 - e_sq)

    p = sqrt(x * x + y * y)
    q = atan2((z * a), (p * b))

    sin_q = sin(q)
    cos_q = cos(q)

    sin_q_3 = sin_q * sin_q * sin_q
    cos_q_3 = cos_q * cos_q * cos_q

    phi = atan2((z + eps * b * sin_q_3), (p - e_sq * a * cos_q_3))
    lam = atan2(y, x)

    v = a / sqrt(1.0 - e_sq * sin(phi) * sin(phi))
    h   = (p / cos(phi)) - v

    lat = degrees(phi)
    lon = degrees(lam)

    return lat, lon, h


def xyz2blh_gost(x: float, y: float, z: float) -> tuple[float, float, float]:
    a, e = 6378137.0, 0.0167  # большая полуось и эксцентриситет 

    D = (x ** 2 + y ** 2) ** 0.5

    if D == 0:
        B = pi * z / (2 * abs(z))
        L = 0
        H = z * sin(B) - a * (1 - e ** 2 * sin(B) ** 2) ** 0.5
    else:
        la = abs(asin(y / D))
        if   y < 0 and x > 0: L = 2 * pi - la
        elif y < 0 and x < 0: L = pi + la
        elif y > 0 and x < 0: L = pi - la
        elif y > 0 and x > 0: L = la
        elif y == 0 and x > 0: L = 0
        elif y == 0 and x < 0: L = pi

    if z == 0:
        B = 0
        H = D - a
    else:
        r = sqrt(x ** 2 + y ** 2 + z ** 2)
        c = asin(z / r)
        p = e ** 2 * a / (2 * r)
        s1 = 0
        counter = 0
        while counter < 100:
            b = c + s1
            s2 = asin(p * sin(2 * b) / sqrt(1 - e ** 2 * sin(b) ** 2 * b))
            d = abs(s2 - s1)
            if d < 1e-4:
                B = b
                H = D * cos(B) + z * sin(B) - a * sqrt(1 - e ** 2 * sin(B) ** 2)
                break
            else:
                s1 = s2
            counter += 1
        else:
            return None, None, None

    return degrees(B), degrees(L), H

if __name__ == '__main__':
    print('по конвертеру ' + str(xyz_to_blh(-1.378451958678890e+03, 1.258820379702524e+03, -2.304813121561112e+03)))
    print('по госту ' + str(xyz2blh_gost(-1.378451958678890e+03, 1.258820379702524e+03, -2.304813121561112e+03)))
