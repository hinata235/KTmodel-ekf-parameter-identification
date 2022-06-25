# -*- coding: utf-8 -*-

#モジュールのインポート
import numpy as np

def KTsim2(dt,simulate_time,X0,Q,R,delta):

    """KTモデルのシミュレーションの値を生成する
    引数:
        dt:観測幅[s],float
        simulate_time:シミュレーション時間[s],int
        x0:状態値[phi,r],ndarray
            phi:回頭角[rad]
            r:回答角速度[rad/s]
            theta1=1/T
            theta2=K/T
            K:追従性指数[1/s]
            T:時定数[s]
        Q:システムノイズの分散共分散行列,ndarray 4行4列
        R:観測ノイズの分散共分散行列,ndarray 2行2列
        delta:舵角[rad],list

    返り値
        X_list:状態値のリスト[[phi0,r0],[phi1,r1],[phi2,r2]・・・]
            phi:回頭角[rad]
            r:回答角速度[rad/s]

        Y_list:観測値のリスト[[phi0,r0],[phi1,r1],[phi2,r2]・・・]
    """


    X_list=[]
    X_list.append(X0)
    Y_list=[]
    Y0=np.array([X0[0],X0[1]])
    Y_list.append(Y0)

    #観測行列Hを生成
    H=np.array([
        [1,0,0,0],
        [0,1,0,0]
        ])

    for i in range(int(simulate_time/dt)):
        
        #システムノイズ
        v=np.array(np.diag(np.random.normal(loc=0,scale=Q))).reshape(-1,1)
        #観測ノイズ
        w=np.array(np.diag(np.random.normal(loc=0,scale=R))).reshape(-1,1)

        #状態値を更新
        X=X_list[i]

        #状態値を計算
        X=np.array([
            X[0]+X[1]*dt,
            (1-X[2]*dt)*X[1]+X[3]*dt*delta[i],
            X[2],
            X[3]
        ])+v

        X_list.append(X)

        #観測値を計算
        Y=H@X+w

        Y_list.append(Y)
    

    return X_list,Y_list