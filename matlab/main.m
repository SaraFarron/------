xyz = [1942826.2687, -5804070.3514, -1796894.1312];
cords_on_earth = [5415352.9566  2917210.1635 -1685888.6292];
angle_of_place = calcUm(cords_on_earth, xyz);
blh = XYZ2BLH(xyz(1), xyz(2), xyz(3));
