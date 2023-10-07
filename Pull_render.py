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

    mycursor.execute("SELECT * FROM pull_data where pull_num='"+str(id)+"'")
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
    mycursor.execute("SELECT * FROM stock_results where id='"+str(id)+"'")
    myresult = mycursor.fetchall()
    if len(myresult)==0:
        return 0

    for i,x in enumerate(myresult):
        id_out,team,tractor,distance,speed=x
        dict={"id":id,"team":team,"tractor":tractor,"distance":distance,"speed":speed,"hook_num":1}
    mycursor.execute("SELECT * FROM stock_results where team='"+str(dict["team"])+"' and tractor='"+str(dict["tractor"])+"'")
    for i,x in enumerate(myresult):
        id_out,team,tractor,distance,speed=x
        if (id_out==id):
            dict["hook_num"]=(1+i)

    return dict
        
def get_last5():
    mycursor.execute("SELECT * FROM stock_results")
    myresult = mycursor.fetchall()
    result=[]
    for x in myresult[-5:]:
        id_out,team,tractor,distance,speed=x
        dict={"id":id_out,"team":team,"tractor":tractor,"distance":distance,"speed":speed,"hook_num":1}
        result.append(dict)
    return result





if(__name__=="__main__"):
    render_pull(1,"Iowa State",23,1)