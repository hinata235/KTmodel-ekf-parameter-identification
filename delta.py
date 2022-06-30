import numpy as np

#舵角を決定する関数
def delta_maker(time,dt):
    delta_list=[]
    Ts = 50.0
    for t in range(int(time/dt)):
        delta = 10 * np.pi / 180  * np.sin(2.0 * np.pi / Ts * t*dt)
        delta_list.append(delta)
    return delta_list
