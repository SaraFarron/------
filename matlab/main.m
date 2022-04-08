xyz = [-1.378451958678890e+03, 1.258820379702524e+03, -2.304813121561112e+03];
cords_on_earth = [5415352.9566  2917210.1635 -1685888.6292];
angle_of_place = calcUm(cords_on_earth, xyz);
blh = XYZ2BLH(xyz(1), xyz(2), xyz(3));
