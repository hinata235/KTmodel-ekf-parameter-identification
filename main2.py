# -*- coding: utf-8 -*-
from cProfile import label
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from KTsimulator2 import KTsim2
from draw import draw
from ekf import ekf


if __name__=="__main__":
    X_hat_list_list=[]
    rmse_T_list=[]
    rmse_K_list=[]
    num_list=[]

    np.random.seed(50)


    #シミュレーションのパラメーターを設定
    dt=15
    simulate_time=1000
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
        [1/T_true],
        [K_true/T_true]],dtype=np.float32)


    Q_true=np.array([
    [0,0,0,0,0,0,0,0],#x
    [0,0,0,0,0,0,0,0],#y
    [0,0,0,0,0,0,0,0],#dx
    [0,0,0,0,0,0,0,0],#dy
    [0,0,0,0,0,0,0,0],#psi
    [0,0,0,0,0,0.001,0,0],#r
    [0,0,0,0,0,0,0,0],#theta1
    [0,0,0,0,0,0,0,0]]#theta2
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
    dt=15
    T=40
    K=0.05

    X_hat0=np.array([
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [1/T],
        [K/T]
        ],dtype=np.float32)


    Q=np.array([
    [0,0,0,0,0,0,0,0],#x
    [0,0,0,0,0,0,0,0],#y
    [0,0,0,0,0,0,0,0],#dx
    [0,0,0,0,0,0,0,0],#dy
    [0,0,0,0,0,0,0,0],#psi
    [0,0,0,0,0,0.001,0,0],#r
    [0,0,0,0,0,0,0,0],#theta1
    [0,0,0,0,0,0,0,0]]#theta2
    ,dtype=np.float32)


    R=np.array([
        [0,0],
        [0,0.01]]
        ,dtype=np.float32)


    V_hat=np.array([
    [0,0,0,0,0,0,0,0],#x
    [0,0,0,0,0,0,0,0],#y
    [0,0,0,0,0,0,0,0],#dx
    [0,0,0,0,0,0,0,0],#dy
    [0,0,0,0,0,0,0,0],#psi
    [0,0,0,0,0,0.01,0,0],#r
    [0,0,0,0,0,0,0.002,0],#theta1
    [0,0,0,0,0,0,0,0.00005]]#theta2
    ,dtype=np.float32)


    #カルマンフィルタを実行
    X_hat_list,V_hat_list,A_list=ekf(dt,simulate_time,X_hat0,Y_list,Q,R,V_hat,delta,u)
    X_hat_list_list.append(X_hat_list)


    #状態推定値を出力
    ##航路
    draw([[Y_list,"Observation"],[X_hat_list,"Estimation"],[X_list,"True"]],1,dt,simulate_time)
    #plt.savefig("r.png")
    plt.show()

    ##回頭角
    draw([[Y_list,"Observation"],[X_hat_list,"Estimation"],[X_list,"True"]],2,dt,simulate_time)
    #plt.savefig("r.png")
    plt.show()

    ##回頭角速度
    draw([[Y_list,"Observation"],[X_hat_list,"Estimation"],[X_list,"True"]],3,dt,simulate_time)
    #plt.savefig("r.png")
    plt.show()

    ##追従性指数
    draw([[X_hat_list,"Estimation"]],4,dt,simulate_time)
    #plt.savefig("T.png")
    plt.show()

    ##旋回性指数
    draw([[X_hat_list,"Estimation"]],5,dt,simulate_time)
    #plt.savefig("K.png")
    plt.show()

    ##共分散行列
    plt.plot([t*dt for t in range(int(len(V_hat_list)))],[V_hat_list[i][5][5] for i in range(len(V_hat_list))])
    plt.plot([t*dt for t in range(int(len(V_hat_list)))],[V_hat_list[i][6][6] for i in range(len(V_hat_list))],label="T")
    plt.plot([t*dt for t in range(int(len(V_hat_list)))],[V_hat_list[i][7][7] for i in range(len(V_hat_list))],label="K")
    plt.legend()
    plt.show()

    #TとKの平方平均二乗誤差を計算
    rmse_T=np.sqrt(np.mean([(1/X_hat_list[t][6]-T_true)**2 for t in range(len(X_hat_list))]))
    rmse_K=np.sqrt(np.mean([(X_hat_list[t][7]/X_hat_list[t][6]-K_true)**2 for t in range(len(X_hat_list))]))

    rmse_T_list.append(rmse_T)
    rmse_K_list.append(rmse_K)

    ##結果を出力
    plt.plot(num_list,rmse_T_list)
    plt.xlabel("")
    plt.ylabel("error [s]")
    plt.title("RMSE of T")
    plt.show()

    plt.plot(num_list,rmse_K_list)
    plt.xlabel("")
    plt.ylabel("error [1/s]")
    plt.title("RMSE of K")
    plt.show()
