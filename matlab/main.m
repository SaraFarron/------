clear
xyz = [-21580426.31, -4233481.41, 5909056.76];
cords_on_earth = [-1248596.2520 -4819428.2840  3976506.0340];
angle_of_place = calcUm(xyz, cords_on_earth);
blh = XYZ2BLH(xyz(1), xyz(2), xyz(3));
