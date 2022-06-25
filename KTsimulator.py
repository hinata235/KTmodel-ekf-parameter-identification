# -*- coding: utf-8 -*-

#モジュールのインポート
import numpy as np

def KTsim(dt,simulate_time,X0,parameter,Q,R,delta):

    """KTモデルのシミュレーションの値を生成する
    引数:
        dt:観測幅[s],float
        simulate_time:シミュレーション時間[s],int
        x0:状態値[phi,r],ndarray
            phi:回頭角[rad]
            r:回答角速度[rad/s]
        parameter:真値の[theta1,theta2],list
            theta1=1/T
            theta2=K/T
            K:追従性指数[1/s]
            T:時定数[s]
        Q:システムノイズの分散共分散行列,ndarray 2行1列
        R:観測ノイズの分散共分散行列,ndarray 2行1列
        delta:舵角[rad],list

    返り値
        X_list:状態値のリスト[[phi0,r0],[phi1,r1],[phi2,r2]・・・]
            phi:回頭角[rad]
            r:回答角速度[rad/s]

        Y_list:観測値のリスト[[phi0,r0],[phi1,r1],[phi2,r2]・・・]
    """

    #状態遷移関数行列F
    F=np.array(
    [[1,dt],
    [0,1-parameter[0]*dt]])

    #入力遷移関数行列B
    B=np.array(
    [[0],
    [parameter[1]*dt]])

    #観測関数行列H
    H=np.identity(2)

    #行列C
    C=np.array([])


    X_list=[]
    X_list.append(X0)
    Y_list=[]
    Y_list.append(X0)


    for i in range(int(simulate_time/dt)):
        
        #システムノイズ
        v=np.array([[0],[np.random.normal(loc=0,scale=Q)]])
        #観測ノイズ
        w=np.array([[0],[np.random.normal(loc=0,scale=R)]])

        #状態値を更新
        X=X_list[i]

        #状態値を計算
        X=F@X+B*delta[i]+v

        X_list.append(X)

        #観測値を計算
        Y=H@X+w

        Y_list.append(Y)
    

    return X_list,Y_list