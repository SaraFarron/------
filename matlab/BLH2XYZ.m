function out=BLH2XYZ(B,L,H,a,ex)
%B и L - широта и долгота в радианах
%H - высота в метрах
%a - большая полуось в метрах, для ПЗ90.11  a=6378136,0
%ex - эксцентриситет или сжатие эллипсойда, вычисляется как:
%ex = sqrt(2*alfa - alfa*alfa), где alpha = 1/298.25784
if ~exist('a')
    a = 6378136.0;
end
if ~exist('ex')
    alfa = 1/298.25784;
    ex = sqrt(2*alfa - alfa*alfa);
end
N=a/sqrt(1-ex^2*sin(B)^2);
out(1)=(N+H)*cos(B)*cos(L);
out(2)=(N+H)*cos(B)*sin(L);
out(3)=((1-ex^2)*N+H)*sin(B);
end