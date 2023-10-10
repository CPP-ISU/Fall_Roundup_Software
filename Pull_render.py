import mysql.connector
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import numpy as np
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="darkcyde15",
  database='pulls'
)

mycursor = mydb.cursor(buffered=True)



def render_pull(id,team_name,tractor,hook):

    mycursor.execute("SELECT * FROM pull_data where pull_id='"+str(id)+"'")
    dist=[]
    speed=[]
    force=[]
    time=[]
    power=[]
    myresult = mycursor.fetchall()
    
    for i,x in enumerate(myresult):
        id_pulldata,pull_num,local_time,local_dist,local_speed,local_force=x
        time.append(local_time)
        dist.append(local_dist)
        speed.append(local_speed)
        force.append(local_force)
        power.append(local_speed*(0.44704)*local_force*(4.4482189159)*1.3596216173/1000)
    smooth_force=savgol_filter(force,window_length=10,polyorder=2)
    pow_np=np.array(power)
    speed_np=np.array(speed)
    coefficients = np.polyfit(speed_np, pow_np, 3)
    trendline = np.poly1d(coefficients)
    plt.plot(dist,speed)
    plt.xlabel("Distance (ft)")
    plt.ylabel("Speed (mph)")
    plt.title(team_name+" "+str(tractor)+" Hook "+str(hook)+" Speed Over Distance")
    plt.savefig('images/pull_data_SD'+str(id))
    plt.figure()
    plt.plot(time,speed)
    plt.xlabel("Time (s)")
    plt.ylabel("Speed (mph)")
    plt.title(team_name+" "+str(tractor)+" Hook "+str(hook)+" Speed Over Time")
    plt.savefig('images/pull_data_ST'+str(id))
    plt.figure()
    plt.plot(time,smooth_force)
    plt.xlabel("Time (s)")
    plt.ylabel("Force (lb)")
    plt.title(team_name+" "+str(tractor)+" Hook "+str(hook)+" Force Over Time")
    plt.savefig('images/pull_data_FT'+str(id))
    plt.figure()
    plt.plot(dist,smooth_force)
    plt.xlabel("Distance (ft)")
    plt.ylabel("Force (lb)")
    plt.title(team_name+" "+str(tractor)+" Hook "+str(hook)+" Force Over Distance")
    plt.savefig('images/pull_data_FD'+str(id))
    plt.figure()
    plt.plot(dist,power)
    plt.xlabel("Distance (ft)")
    plt.ylabel("Power (lb*mph)")
    plt.title(team_name+" "+str(tractor)+" Hook "+str(hook)+" Power Over Distance")
    plt.savefig('images/pull_data_PD'+str(id))
    plt.figure()
    ##plt.plot(speed,power)
    plt.scatter(speed_np,pow_np)
    plt.plot(speed_np,trendline(speed_np))
    plt.xlabel("Distance (ft)")
    plt.ylabel("Power (lb*mph)")
    plt.title(team_name+" "+str(tractor)+" Hook "+str(hook)+" Power Over speed")
    plt.savefig('images/pull_data_PS'+str(id))
    plt.figure()
    plt.plot(time,power)
    plt.xlabel("Time (s)")
    plt.ylabel("Power (lb*mph)")
    plt.title(team_name+" "+str(tractor)+" Hook "+str(hook)+" Power Over Time")
    plt.savefig('images/pull_data_PT'+str(id))

    
def get_pull(id):
    mycursor.execute("SELECT * FROM all_pull_results where pull_id='"+str(id)+"'")
    myresult = mycursor.fetchall()
    if len(myresult)==0:
        return 0

    for i,x in enumerate(myresult):
        id_out,pull_class,team_id,tractor_id,distance,speed=x
        dict={"id":id,"team":team_id,"tractor":tractor_id,"distance":distance,"speed":speed,"hook_num":1}
    mycursor.execute("SELECT * FROM all_pull_results where team_id='"+str(dict["team"])+"' and tractor_id='"+str(dict["tractor"])+"'")
    for i,x in enumerate(myresult):
        id_out,pull_class,team_id,tractor_id,distance,speed=x
        if (id_out==id):
            dict["hook_num"]=(1+i)

    return dict

def tractor_name(tractor_id):
  localdb=mysql.connector.connect(
  host="localhost",
  user="root",
  password="darkcyde15",
  database='pulls'
    )
  localcursor=localdb.cursor()
  localcursor.execute("SELECT tractor_num FROM tractors where tractor_id="+str(tractor_id))
  result=localcursor.fetchone()
  return result
        
def get_last5():
    mycursor.execute("SELECT * FROM all_pull_results")
    myresult = mycursor.fetchall()
    result=[]
    for x in myresult[-5:]:
        id_out,pull_class,team_id,tractor_id,distance,speed=x
        dict={"id":id_out,"team":team,"tractor":tractor,"distance":distance,"speed":speed,"hook_num":1}
        result.append(dict)
    return result

def team_tractors(team_id):
    mycursor.execute("SELECT tractor_id,tractor_num FROM tractors where team_id="+str(team_id))
    myresult = mycursor.fetchall()
    tractors=[]
    for result in myresult:
        tractor_id,tractor_num=result
        tractor={"tractor_id":tractor_id,"tractor_name":tractor_num}
        tractors.append(tractor)
    return tractors

def teams():
    teams=[]
    mycursor.execute("SELECT team_name , team_abv, team_id FROM teams")
    myresult = mycursor.fetchall()
    for result in myresult:
        team_name,team_abrev,team_id=result
        tractors=team_tractors(team_id)
        team={"team_name":team_name,"team_abrev":team_abrev,"tractors":tractors}
        teams.append(team)
    return teams






if(__name__=="__main__"):
    render_pull(1,"Iowa State",23,1)