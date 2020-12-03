import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import plotly.express as px
import seaborn as sns

# PART 1 - Median and Mode of job and task execution times

df_jobll = pd.read_csv("./Logs/JobLog_LL.csv")
df_jobrr = pd.read_csv("./Logs/JobLog_RR.csv")
df_jobran = pd.read_csv("./Logs/JobLog_Random.csv")
df_taskll = pd.read_csv("./Logs/TaskLog_LL.csv")
df_taskrr = pd.read_csv("./Logs/TaskLog_RR.csv")
df_taskran = pd.read_csv("./Logs/TaskLog_Random.csv")

mean_taskll = df_taskll.mean(axis = 0)['Execution_time']
mean_taskrr = df_taskrr.mean(axis = 0)['Execution_time']
mean_taskran = df_taskran.mean(axis = 0)['Execution_time']
print("Mean task execution time in least loaded algorithm:", mean_taskll)
print("Mean task execution time in round robin algorithm:", mean_taskrr)
print("Mean task execution time in random algorithm:", mean_taskran)
print("\n")

mean_jobll = df_jobll.mean(axis = 0)['Execution_time']
mean_jobrr = df_jobrr.mean(axis = 0)['Execution_time']
mean_jobran = df_jobran.mean(axis = 0)['Execution_time']
print("Mean job execution time in least loaded algorithm:", mean_jobll)
print("Mean job execution time in round robin algorithm:", mean_jobrr)
print("Mean job execution time in random algorithm:", mean_jobran)
print("\n")

median_taskll = df_taskll.median(axis = 0)['Execution_time']
median_taskrr = df_taskrr.median(axis = 0)['Execution_time']
median_taskran = df_taskran.median(axis = 0)['Execution_time']
print("Median task execution time in least loaded algorithm:", median_taskll)
print("Median task execution time in round robin algorithm:", median_taskrr)
print("Median task execution time in random algorithm:", median_taskran)
print("\n")

median_jobll = df_jobll.median(axis = 0)['Execution_time']
median_jobrr = df_jobrr.median(axis = 0)['Execution_time']
median_jobran = df_jobran.median(axis = 0)['Execution_time']
print("Median job execution time in least loaded algorithm:", median_jobll)
print("Median job execution time in round robin algorithm:", median_jobrr)
print("Median job execution time in random algorithm:", median_jobran)
print("\n")



# PART 2 - Plots the number of tasks scheduled on each machine, against time, for each scheduling algorithm

# Round Robin Algorithm
df = pd.read_csv("./Logs/TaskScheduleLog_RR.csv")

w1_et = []
w2_et = []
w3_et = []

for i in range(0,len(df)):
    if(df.loc[i,'Worker'] == 7000):
        w1_et.append(df.loc[i,'Scheduled_time'])
    elif(df.loc[i,'Worker'] == 7001):
        w2_et.append(df.loc[i,'Scheduled_time'])     
    elif(df.loc[i,'Worker'] == 7002):
        w3_et.append(df.loc[i,'Scheduled_time'])

w1_et.sort()
w2_et.sort()
w3_et.sort()

final_time = max(w1_et[-1],w2_et[-1],w3_et[-1])

w1_et.append(final_time)
w2_et.append(final_time)
w3_et.append(final_time)

num_tasks = [i for i in range(0,len(w1_et))]
plt.plot(w1_et,num_tasks,linestyle='dashed',color='r',label="Worker-1")
plt.legend(loc="upper left")

num_tasks = [i for i in range(0,len(w2_et))]
plt.plot(w2_et,num_tasks,linestyle='dashdot',color='b',label="Worker-2")
plt.legend(loc="upper left")

num_tasks = [i for i in range(0,len(w3_et))]
plt.plot(w3_et,num_tasks,linestyle='solid',color='k',label="Worker-3")
plt.legend(loc="upper left")

plt.title('Round Robin Algorithm tasks Vs time ')
plt.xlabel('Time')
plt.ylabel('Number of tasks')
plt.savefig('./Logs/Plots/RR_Algorithm.jpeg', bbox_inches='tight')
plt.show()


# Least Loaded Algorithm
df = pd.read_csv("./Logs/TaskScheduleLog_LL.csv")

w1_et = []
w2_et = []
w3_et = []

for i in range(0,len(df)):
    if(df.loc[i,'Worker']==7000):
        w1_et.append(df.loc[i,'Scheduled_time'])
    elif(df.loc[i,'Worker']==7001):
        w2_et.append(df.loc[i,'Scheduled_time'])
    elif(df.loc[i,'Worker']==7002):
        w3_et.append(df.loc[i,'Scheduled_time'])

w1_et.sort()
w2_et.sort()
w3_et.sort()

final_time = max(w1_et[-1],w2_et[-1],w3_et[-1])
w1_et.append(final_time)
w2_et.append(final_time)
w3_et.append(final_time)

num_tasks = [i for i in range(0,len(w1_et))]
plt.plot(w1_et,num_tasks,linestyle='dashed',color='r',label="Worker-1")
plt.legend(loc="upper left")

num_tasks=[i for i in range(0,len(w2_et))]
plt.plot(w2_et,num_tasks,linestyle='dashdot',color='b',label="Worker-2")
plt.legend(loc="upper left")

num_tasks=[i for i in range(0,len(w3_et))]
plt.plot(w3_et,num_tasks,linestyle='solid',color='k',label="Worker-3")
plt.legend(loc="upper left")

plt.title('Least Loaded Algorithm tasks vs time')
plt.xlabel('Time')
plt.ylabel('Number of tasks')
plt.savefig('./Logs/Plots/LL_Algorithm.jpeg', bbox_inches='tight')
plt.show()

# Random algorithm
df = pd.read_csv("./Logs/TaskScheduleLog_Random.csv")

w1_et = []
w2_et = []
w3_et = []

for i in range(0,len(df)):
    if(df.loc[i,'Worker']==7000):
        w1_et.append(df.loc[i,'Scheduled_time'])
    elif(df.loc[i,'Worker']==7001):
        w2_et.append(df.loc[i,'Scheduled_time'])
    elif(df.loc[i,'Worker']==7002):
        w3_et.append(df.loc[i,'Scheduled_time'])

w1_et.sort()
w2_et.sort()
w3_et.sort()

final_time = max(w1_et[-1],w2_et[-1],w3_et[-1])
w1_et.append(final_time)
w2_et.append(final_time)
w3_et.append(final_time)

num_tasks=[i for i in range(0,len(w1_et))]
plt.plot(w1_et,num_tasks,linestyle='dashed',color='r',label="Worker-1")
plt.legend(loc="upper left")

num_tasks=[i for i in range(0,len(w2_et))]
plt.plot(w2_et,num_tasks,linestyle='dashdot',color='b',label="Worker-2")
plt.legend(loc="upper left")

num_tasks=[i for i in range(0,len(w3_et))]
plt.plot(w3_et,num_tasks,linestyle='solid',color='k',label="Worker-3")
plt.legend(loc="upper left")

plt.title('Random Algorithm tasks Vs time')
plt.xlabel('Time')
plt.ylabel('Number of tasks')
plt.savefig('./Logs/Plots/Random_Algorithm.jpeg', bbox_inches='tight')
plt.show()