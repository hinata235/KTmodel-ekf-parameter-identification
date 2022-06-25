# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from KTsimulator2 import KTsim2
from draw import draw
from ekf import ekf


if __name__=="__main__":
    np.random.seed(5)
    #シミュレーションのパラメーターを設定
    dt=0.1
    simulate_time=400
    u=15/1.944
    T_true=60
    K_true=0.15
    X0=np.array([
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [1/T_true],
        [K_true/T_true]],dtype=np.float32)

    Q_true=np.array([
    [0,0,0,0,0,0,0,0,0],#x
    [0,0,0,0,0,0,0,0,0],#y
    [0,0,0,0,0,0,0,0,0],#dx
    [0,0,0,0,0,0,0,0,0],#dy
    [0,0,0,0,0,0,0,0,0],#psi
    [0,0,0,0,0,0.000001,0,0,0],#r
    [0,0,0,0,0,0,0,0,0],#dr
    [0,0,0,0,0,0,0,0,0],#theta1
    [0,0,0,0,0,0,0,0,0]]#theta2
    ,dtype=np.float32)

    R_true=np.array([
        [0,0],
        [0,0.01]]
        ,dtype=np.float32)

    delta=[20*np.pi/180 for i in range(int(simulate_time/dt))]

    X_list=0
    Y_list=0
    X_hat_list=0
    V_hat_list=0
    A_list=0

    X_list,Y_list =KTsim2(dt,simulate_time,X0,Q_true,R_true,delta,u)

    #拡張カルマンフィルタ用のパラメーターを設定
    dt=0.1
    T=50
    K=0.1
    X_hat0=np.array([
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [1/T],
        [K/T]],dtype=np.float32)

    Q=np.array([
    [0,0,0,0,0,0,0,0,0],#x
    [0,0,0,0,0,0,0,0,0],#y
    [0,0,0,0,0,0,0,0,0],#dx
    [0,0,0,0,0,0,0,0,0],#dy
    [0,0,0,0,0,0,0,0,0],#psi
    [0,0,0,0,0,0,0,0,0],#r
    [0,0,0,0,0,0,0,0,0],#dr
    [0,0,0,0,0,0,0,0.001,0],#theta1
    [0,0,0,0,0,0,0,0,0.0001]]#theta2
    ,dtype=np.float32)

    R=np.array([
        [0,0],
        [0,0.1]]
        ,dtype=np.float32)

    V_hat=np.array([
    [1000,0,0,0,0,0,0,0,0],#x
    [0,1000,0,0,0,0,0,0,0],#y
    [0,0,1000,0,0,0,0,0,0],#dx
    [0,0,0,1000,0,0,0,0,0],#dy
    [0,0,0,0,1000,0,0,0,0],#psi
    [0,0,0,0,0,1000,0,0,0],#r
    [0,0,0,0,0,0,1000,0,0],#dr
    [0,0,0,0,0,0,0,1000,0],#theta1
    [0,0,0,0,0,0,0,0,1000]]#theta2
    ,dtype=np.float32)

    #カルマンフィルタを実行
    X_hat_list,V_hat_list,A_list=ekf(dt,simulate_time,X_hat0,Y_list,Q,R,V_hat,delta,u)


    draw([[X_list,"True"]],1,dt,simulate_time)
    #plt.savefig("r.png")
    plt.show()
    draw([[Y_list,"Observation"],[X_hat_list,"Estimation"],[X_list,"True"]],2,dt,simulate_time)
    #plt.savefig("r.png")
    plt.show()
    draw([[Y_list,"Observation"],[X_hat_list,"Estimation"],[X_list,"True"]],3,dt,simulate_time)
    #plt.savefig("r.png")
    plt.show()

    draw([[X_hat_list,"Estimation"]],4,dt,simulate_time)
    #plt.savefig("T.png")
    plt.show()

    draw([[X_hat_list,"Estimation"]],5,dt,simulate_time)
    #plt.savefig("K.png")
    plt.show()
