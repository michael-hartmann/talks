from DoublePendulum import DoublePendulum

pendulum = DoublePendulum()

dtheta2 = pendulum.dtheta2(15, 1,1)
l = pendulum.poincare(15,1,1,50)
for li in l:
    print(l)
