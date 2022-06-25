from cProfile import label
import matplotlib.pyplot as plt

def draw(list,mode,dt):
    """時間変化する値を描画する関数
    引数:
        list:リスト
            [[X_list,name],[Y_list,name],[Z_list,name]...]
            X_list:状態値のリスト
        mode:表示したい状態値
                0:回頭角phi
                1:回頭角速度r
                2:時定数T
                3:追従性指数K
        dt:観測幅

    """
    if mode==0:
        for l in list:
            plt.plot([t*dt for t in range(len(l[0]))],[l[0][i][0] for i in range(len(l[0]))],label=f'{l[1]}')
        plt.xlabel("time[s]")
        plt.ylabel("angle phi[rad]")
        plt.title("time VS angle")
        plt.legend()

    elif mode==1:
        for l in list:
            plt.plot([t*dt for t in range(len(l[0]))],[l[0][i][1] for i in range(len(l[0]))],label=f'{l[1]}')
        plt.xlabel("time[s]")
        plt.ylabel("angle rate r[rad/s]")
        plt.title("time VS angle rate")
        plt.legend()
    
    elif mode==2:
        for l in list:
            plt.plot([t*dt for t in range(len(l[0]))],[1/l[0][i][2] for i in range(len(l[0]))],label=f'{l[1]}')
        plt.xlabel("time[s]")
        plt.ylabel("T [s]")
        plt.title("time VS T")
        plt.xlim(10,len(l[0])*dt)
        plt.legend()
    
    elif mode==3:
        for l in list:
            plt.plot([t*dt for t in range(len(l[0]))],[l[0][i][3]/l[0][i][2] for i in range(len(l[0]))],label=f'{l[1]}')
        plt.xlabel("time[s]")
        plt.ylabel("K [1/s]")
        plt.title("time VS K")
        plt.xlim(10,len(l[0])*dt)
        plt.legend()
    
    else:
        print("mode must be 0,1,2,3")




