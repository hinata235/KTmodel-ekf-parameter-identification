from cProfile import label
import matplotlib.pyplot as plt

def draw(list,mode,dt,simulate_time):
    """時間変化する値を描画する関数
    引数:
        list:リスト
            [[X_list,name],[Y_list,name],[Z_list,name]...]
            X_list:状態値のリスト
        mode:表示したい状態値
                1:位置(x,y)
                2:回頭角phi
                3:回頭角速度r
                4:時定数T
                5:追従性指数K
        dt:観測幅

    """
    #(x,y)
    if mode==1:
        for l in list:
            plt.plot([l[0][i][0] for i in range(len(l[0]))],[l[0][i][1] for i in range(len(l[0]))],label=f'{l[1]}')
        plt.xlabel("x[m]")
        plt.ylabel("y[m]")
        plt.title("trajectory")
        plt.legend()

    #phi
    elif mode==2:
        for l in list:
            if l[1]=="Observation":
                plt.plot([t*dt for t in range(len(l[0]))],[l[0][i][0] for i in range(len(l[0]))],label=f'{l[1]}')
            else:
                plt.plot([t*dt for t in range(len(l[0]))],[l[0][i][4] for i in range(len(l[0]))],label=f'{l[1]}')
        plt.xlabel("time[s]")
        plt.ylabel("angle phi[rad]")
        plt.title("time VS angle")
        plt.legend()
        
    #r
    elif mode==3:
        for l in list:
            if l[1]=="Observation":
                plt.plot([t*dt for t in range(len(l[0]))],[l[0][i][1] for i in range(len(l[0]))],label=f'{l[1]}')
            else:
                plt.plot([t*dt for t in range(len(l[0]))],[l[0][i][5] for i in range(len(l[0]))],label=f'{l[1]}')
        plt.xlabel("time[s]")
        plt.ylabel("angle rate r[rad/s]")
        plt.title("time VS angle rate")
        plt.legend()
        
    #T
    elif mode==4:
        for l in list:
            plt.plot([t*dt for t in range(len(l[0]))],[1/l[0][i][7] for i in range(len(l[0]))],label=f'{l[1]}')
        plt.plot([t*dt for t in range(len(l[0]))],[60 for t in range(len(l[0]))],label="True")
        plt.xlabel("time[s]")
        plt.ylabel("T [s]")
        plt.title("time VS T")
        plt.xlim(0,simulate_time)
        plt.ylim(-0.1,100)
        plt.legend()
        
    #K
    elif mode==5:
        for l in list:
            plt.plot([t*dt for t in range(len(l[0]))],[l[0][i][8]/l[0][i][7] for i in range(len(l[0]))],label=f'{l[1]}')
        plt.plot([t*dt for t in range(len(l[0]))],[0.15 for t in range(len(l[0]))],label="True")
        plt.xlabel("time[s]")
        plt.ylabel("K [1/s]")
        plt.title("time VS K")
        plt.xlim(0,simulate_time)
        plt.ylim(-0.1,0.3)
        plt.legend()
        
    
    else:
        print("mode must be 0,1,2,3,4,5")




