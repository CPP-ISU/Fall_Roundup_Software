import mysql.connector
import matplotlib
matplotlib.use('Agg')
##import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import random



class pull:
    def __init__(self,id,team,tractor,distance,speed):
        self.id=id
        self.team=team
        self.tractor=tractor
        self.distance=distance
        self.speed=speed
        self.hook_num=0
        self.team_trac=team+" "+str(tractor)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="darkcyde15",
  database='pulls'
)

mycursor = mydb.cursor()



mycursor.execute("SELECT * FROM teams")

myresult = mycursor.fetchall()
team_ab={"iowa":"isu"}
for x,i in zip(myresult,range(1000)):
  name,abbreveation,R,G,B=x
  team_ab[name]=abbreveation

def get_dist(pull):
   return pull.distance







def gen_rank_pull_img(ranked_pulls,Class_Name):
    print("Running Ranking")
    dists=[i.distance for i in ranked_pulls]
    teams=[i.team for i in ranked_pulls]
    speed=[i.speed for i in ranked_pulls]
    tractors=[i.tractor for i in ranked_pulls]
    hook_nums=[i.hook_num for i in ranked_pulls]
    team_trac=[team_ab[i]+" "+str(j)+" "+str(k) for i,j,k in zip(teams,tractors,hook_nums)]
    ##bar_colors = [plt.cm.viridis(random.random()) for _ in dists]
    fig=Figure()
    ax=fig.subplots()
    ax.barh(team_trac,dists)
    ax.xlabel=("Distance")
    ax.ylabel=("Pull")
    ax.title(Class_Name+" Leaderboard")
    ax.xlim(0,max(dists))
    ax.gca().invert_yaxis()
    for i, v in enumerate(dists):
        plt.text(v + 1, i, str(v), va='center', fontsize=12)
    ##for i, v in enumerate(team_trac):
    ##    plt.text(0, i-.5, v, va='center', fontsize=12)
    ##plt.show()
    ax.savefig(('C:\Git\Web_Dev\images\Leader_Board.png'))
    width_in_pixels= 3840/3
    height_in_pixels=600
    dpi=200
    fig = Figure(figsize=(width_in_pixels / dpi, height_in_pixels / dpi), dpi=dpi)
    ax=fig.subplots()
    ax.barh(team_trac,dists)
    ax.xlabel=("Distance")
    ax.ylabel=("Pull")
    ax.title(Class_Name+" Leaderboard")
    ax.xlim(0,max(dists))
    ax.gca().invert_yaxis()
    for i, v in enumerate(dists):
        plt.text(v + 1, i, str(v), va='center', fontsize=12)
    fig.savefig(('C:\Git\Web_Dev\images\Leader_Board_Overlay.png'),dpi=dpi)


def stock_rank():
    mycursor.execute("SELECT * FROM stock_results")

    myresult = mycursor.fetchall()
    pulls=[]
    for x,i in zip(myresult,range(1000)):
        id,team,tractor,distance,speed=x
        pulls.append(pull(id,team,tractor,distance,speed))
    for i,v in enumerate(pulls):
        num=1
        for j, h in zip(range(i),pulls):
            if v.team_trac in h.team_trac:
                num+=1
        pulls[i].hook_num=num
        
    ranked_pulls=sorted(pulls,key=get_dist,reverse=True)
    gen_rank_pull_img(ranked_pulls, "Stock")

if __name__ =="__main__":
    stock_rank()