import mysql.connector
import csv
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="darkcyde15",
  database='fallrounudp'
)

mycursor = mydb.cursor(buffered=True)

def plot_pull_data(pull_id, team_name, tractor_num, pulls, smoothing_window=1):
    # Create a new figure for each pull
    plt.figure()

    # Query the database for pull data
    mycursor.execute(f"SELECT distance, speed, draft_force FROM pull_data WHERE pull_id={pull_id}")
    pull_result = mycursor.fetchall()

    distances = []
    speeds = []
    forces = []

    for data in pull_result:
        dist, draft, speed = data
        distances.append(dist)
        speeds.append(speed)
        forces.append(draft)

    # Apply smoothing filter to speed and force data
    smoothed_speed = speeds#savgol_filter(speeds, smoothing_window, 3)
    smoothed_force = forces#savgol_filter(forces, smoothing_window, 3)

    # Create subplots for speed and force
    plt.subplot(2, 1, 1)
    plt.plot(distances, smoothed_speed, label="Speed")
    plt.title(f"Smoothed Speed over Distance - {team_name} (Tractor {tractor_num}) - Pull {pulls}")
    plt.xlabel("Distance (ft)")
    plt.ylabel("Speed (mph)")
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(distances, smoothed_force, label="Force")
    plt.title(f"Smoothed Force over Distance - {team_name} (Tractor {tractor_num}) - Pull {pulls}")
    plt.xlabel("Distance (ft)")
    plt.ylabel("Force (lbf)")
    plt.legend()

    # Save the plot to a file
    plt.tight_layout()
    plt.savefig(f"{team_name}_{tractor_num}_{pulls}_plot.png")
    plt.close()

mycursor.execute("SELECT team_id, team_name FROM teams")
myresult = mycursor.fetchall()
teams={}
for x in myresult:
    team_id,team_name=x
    teams[team_id]=team_name

mycursor.execute("SELECT tractor_id, tractor_num FROM tractors")
myresult = mycursor.fetchall()
tractors={}
for x in myresult:
    tractor_id, tractor_num=x
    tractor={"num":tractor_num,"pulls":0}
    tractors[tractor_id]=tractor



mycursor.execute("SELECT pull_id, team_id, tractor_id, final_dist FROM all_pull_results")
myresult = mycursor.fetchall()
order_file=open("pull_order",mode="w",newline='')
order_writer=csv.writer(order_file)
for x in myresult:
    pull_id,team_id,tractor_id,dist=x
    
    if dist>0:
        tractors[tractor_id]["pulls"]+=1
        row=pull_id,teams[team_id],tractors[tractor_id]["num"],dist,tractors[tractor_id]["pulls"]
        order_writer.writerow(row)
        file=open(f"{teams[team_id]}_{tractors[tractor_id]['num']}_{tractors[tractor_id]['pulls']}",mode='w',newline='')
        writer=csv.writer(file)
        print(f"team: {team_id}, tractor: {tractor_id}")
        mycursor.execute(f"SELECT distance, speed, draft_force FROM pull_data WHERE pull_id={pull_id}")
        pull_result=mycursor.fetchall()
        plot_pull_data(pull_id, teams[team_id], tractors[tractor_id]["num"], tractors[tractor_id]["pulls"])
        for z in pull_result:
            dist,draft,speed=z
            row=z
            writer.writerow(row)
        file.flush()
        file.close()
order_file.flush()
order_file.close()
    

