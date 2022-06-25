# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from KTsimulatator2 import KTsim2
from draw import draw
from ekf import ekf


if __name__=="__main__":

    #シミュレーションのパラメーターを設定
    dt=0.1
    simulate_time=150
    K=0.15
    T=60
    X0=np.array([[0],[0],[1/T],[K/T]],dtype=np.float32)

    Q_true=np.array([
    [0,0,0,0],
    [0,0.0001,0,0],
    [0,0,0,0],
    [0,0,0,0]]
    ,dtype=np.float32)

    R_true=np.array([
        [0,0],
        [0,0.01]]
        ,dtype=np.float32)

    delta=[20*np.pi/180 for i in range(int(simulate_time/dt))]


    X_list,Y_list =KTsim2(dt,simulate_time,X0,Q_true,R_true,delta)


    #拡張カルマンフィルタ用のパラメーターを設定
    dt=0.1
    simulate_time=150
    X_hat0=np.array([[0],[0],[0],[0]],dtype=np.float32)


    Q=np.array([
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0.001,0],
    [0,0,0,0.0001]]
    ,dtype=np.float32)

    R=np.array([
        [0,0],
        [0,0.001]]
        ,dtype=np.float32)

    V_hat=np.array([
        [100000000,0,0,0],
        [0,10000000,0,0],
        [0,0,10000000,0],
        [0,0,0,10000000]]
        ,dtype=np.float32)

    #カルマンフィルタを実行
    X_hat_list,V_hat_list,A_list=ekf(dt,simulate_time,X_hat0,Y_list,Q,R,V_hat,delta)

    draw([[X_hat_list,"Estimation"],[Y_list,"Observation"],[X_list,"True"]],1,dt)
    #draw([[X_hat_list,"Estimation"]],3,dt)
    plt.show()