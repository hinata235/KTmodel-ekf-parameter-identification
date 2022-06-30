# -*- coding: utf-8 -*-

#モジュールのインポート
import numpy as np

def ekf(dt,simulate_time,X_hat,Y_list,Q,R,V_hat,delta,u):

    """KTモデルのekf(拡張カルマンフィルタ)
    引数:
        dt:観測幅[s],float
        simulate_time:シミュレーション時間[s],int
        X_hat:状態推定値の初期値　9行1列
            x:位置[m]
            y:位置[m]
            dx:速度[m/s]
            dy速度[m/s]
            phi:回頭角[rad]
            r:回答角速度[rad/s]
            theta1=1/T
            theta2=K/Tphi:回頭角[rad]
            r:回答角速度[rad/s]
            theta1:パラメーターθ1
            theta2:パラメーターθ2
        u:船速[m/s]

        Y:観測値[phi,r],list 2行1列
            phi:回頭角[rad]
            r:回答角速度[rad/s]
        Q:システムノイズの分散共分散行列,ndarray 8行8列
        R:観測ノイズの分散共分散行列,ndarray 2行2列
        P:共分散行列の初期値 8行8列
        delta:舵角[rad],list

    返り値
        X_hat_list:状態推定値のリスト[[phi0,r0,theta10,theta20],[phi1,r1,theta11,theta21]・・・]
            phi:回頭角[rad]
            r:回答角速度[rad/s]
            theta1
            theta2
    """

    #観測関数行列H　2行8列
    H=np.array([
        [0,0,0,0,1,0,0,0],
        [0,0,0,0,0,1,0,0]
        ])


    X_hat_list=[] #状態推定値のリスト
    X_hat_list.append(X_hat) #初期値を設定
    V_hat_list=[] #分散共分散行列のリスト
    V_hat_list.append(V_hat) #初期値を設定
    A_list=[]


    #逐次的に状態を推定
    for i in range(int(simulate_time/dt)):
        
        #状態量を更新する
        X=X_hat_list[i]
        Y=Y_list[i]

        #FのヤコビアンA 4行4列
        A=np.array([
            [1,0,dt,0,0,0,0,0],
            [0,1,0,dt,0,0,0,0],
            [0,0,0,0,-u*np.cos(X[4]),0,0,0],
            [0,0,0,0,u*np.sin(X[4]),0,0,0],
            [0,0,0,0,1,dt,0,0],
            [0,0,0,0,0,1-X[6]*dt,-X[5]*dt,delta[i]*dt],
            [0,0,0,0,0,0,1,0],
            [0,0,0,0,0,0,0,1]
            ], dtype=np.float32)

        A_list.append(A)

        #予測ステップ
        #システムノイズ

        ##事前推定値
        _X_hat=np.array([
            X[0]+X[2]*dt,
            X[1]+X[3]*dt,
            u*np.cos(X[4]),
            u*np.sin(X[4]),
            X[4]+X[5]*dt,
            (1-X[6]*dt)*X[5]+X[7]*delta[i]*dt,
            X[6],
            X[7]
        ])

        ##事前誤差共分散
        _V_hat=A@np.array([
            [V_hat_list[i][0][0],0,0,0,0,0,0,0],
            [0,V_hat_list[i][1][1],0,0,0,0,0,0],
            [0,0,V_hat_list[i][2][2],0,0,0,0,0],
            [0,0,0,V_hat_list[i][3][3],0,0,0,0],
            [0,0,0,0,V_hat_list[i][4][4],0,0,0],
            [0,0,0,0,0,V_hat_list[i][5][5],0,0],
            [0,0,0,0,0,0,V_hat_list[i][6][6],0],
            [0,0,0,0,0,0,0,V_hat_list[i][7][7]]
            ], dtype=np.float32)@A.T+Q

        #更新ステップ
        ##逆行列の計算
        inv_VR=np.linalg.pinv(H@_V_hat@H.T+R)

        ##カルマンゲイン
        G=_V_hat@H.T@inv_VR

        ##事後推定値
        X_hat=_X_hat+G@(Y-H@_X_hat)
        X_hat_list.append(X_hat)

        ##事後誤差共分散
        V_hat=_V_hat-G@H@_V_hat
        V_hat_list.append(V_hat)

    return X_hat_list,V_hat_list,A_list