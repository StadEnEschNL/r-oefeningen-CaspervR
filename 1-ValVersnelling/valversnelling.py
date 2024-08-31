import matplotlib.pyplot as plt

doorgaan = True

y=20
t=0
v=0
g=9.81
m=20
dt=5

y_waarden = [y]
t_waarden = [t]
while doorgaan:
  Fz=m*g
  Fres=Fz
  a=Fres/m
  dv=a*dt
  v=v+dv
  dy=v*dt
  y=y-dy
  if y <= 0:
    doorgaan = False
  t=t+dt
  y_waarden.append(y)
  t_waarden.append(t)
  

plt.plot(t_waarden, y_waarden, 'r.')
plt.ylabel('data ofzo idk')
plt.show()
