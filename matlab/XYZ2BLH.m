function out=XYZ2BLH(X,Y,Z,a,ex)
if ~exist('a')
    a = 6378136.0;
end
if ~exist('ex')
    alfa = 1/298.25784;
    ex = sqrt(2*alfa - alfa*alfa);
end
L=atan2(X,Y);
D=sqrt(X^2+Y^2);
if D==0
   B=pi/2*Z/abs(Z);
   L=0;
   H=Z*sin(B)-a*sqrt(1-ex^2*sin(B)^2);    
else 
    Ls=abs(asin(Y/D));  %либо L=atan2(Y,X), тогда все if выполнять ненужно
    if Y<0 && X>0       %убрать если L=atan2(Y,X)
        L=2*pi-Ls;
    elseif Y<0 && X<0
        L=pi+Ls;
    elseif Y>0 && X<0
        L=pi-Ls;
    elseif Y>0 && X>0
        L=Ls;
    elseif Y==0 && X>0
        L=0;
    elseif Y==0 && X<0
        L=pi;
    end             %убрать 
    
    if Z==0
       B=0;
       H=D-a;
    else
       r=sqrt(X^2+Y^2+Z^2);
       c=asin(Z/r);
       p=ex^2*a/(2*r);
       s1=1;
       for i=1:20
          b=c+s1;
          s2=asin(p*sin(2*b)/sqrt(1-ex^2*sin(b)^2));
          if abs(s2-s1)<1e-9
              B=b;
              H=D*cos(B)+Z*sin(B)-a*sqrt(1-ex^2*sin(B)^2);
              break;
          end
          s1=s2;   
       end
    end
end
out(1)=B;
out(2)=L;
out(3)=H;
end