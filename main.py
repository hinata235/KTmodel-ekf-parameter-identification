# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from KTsimulator import KTsim
from draw import draw
from ekf import ekf


if __name__=="__main__":

    #シミュレーションのパラメーターを設定
    dt=0.1
    simulate_time=150
    X0=np.array([[0],[0]],dtype=np.float32)
    K=0.15
    T=60
    parameter=[1/T,K/T]
    Q_true= 0.0001
    R_true=0.01
    delta=[20*np.pi/180 for i in range(int(simulate_time/dt))]


    X_list,Y_list = KTsim(dt,simulate_time,X0,parameter,Q_true,R_true,delta)


    #拡張カルマンフィルタ用のパラメーターを設定
    dt=0.1
    simulate_time=150
    X_hat0=np.array([[0],[0],[0],[0]],dtype=np.float32)

    Q=np.array([
        [0,0,0,0],
        [0,Q_true,0,0],
        [0,0,0.1,0],
        [0,0,0,0.1]]
        ,dtype=np.float32)

    R=np.array([
        [0,0],
        [0,R_true]]
        ,dtype=np.float32)

    V_hat=np.array([
        [1000000,0,0,0],
        [0,100000,0,0],
        [0,0,100000,0],
        [0,0,0,100000]]
        ,dtype=np.float32)

    #カルマンフィルタを実行
    X_hat_list,V_hat_list,A_list=ekf(dt,simulate_time,X_hat0,Y_list,Q,R,V_hat,delta)

    draw([[Y_list,"Observation"],[X_hat_list,"Estimation"],[X_list,"True"]],1,dt)
    #draw([[X_hat_list,"Estimation"]],3,dt)
    plt.show()