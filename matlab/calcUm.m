function um = calcUm( crdSat, xyzPos )
Rang = sqrt( (crdSat(1) - xyzPos(1))*(crdSat(1) - xyzPos(1)) + (crdSat(2) - xyzPos(2))*(crdSat(2) - xyzPos(2)) + (crdSat(3) - xyzPos(3))*(crdSat(3) - xyzPos(3)) );
kx = (crdSat(1) - xyzPos(1))/Rang;
ky = (crdSat(2) - xyzPos(2))/Rang;
kz = (crdSat(3) - xyzPos(3))/Rang;
um = asin(  (kx*xyzPos(1) + ky*xyzPos(2) + kz*xyzPos(3)) / sqrt( xyzPos(1)*xyzPos(1) + xyzPos(2)*xyzPos(2) + xyzPos(3)*xyzPos(3)))*180.0/pi;
	
end
