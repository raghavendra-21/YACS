import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import plotly.express as px
import seaborn as sns

# PART 1 - Median and Mean of job and task execution times

df_jobll = pd.read_csv("./Logs/JobLog_LL.csv")
df_jobrr = pd.read_csv("./Logs/JobLog_RR.csv")
df_jobran = pd.read_csv("./Logs/JobLog_Random.csv")
df_taskll = pd.read_csv("./Logs/TaskLog_LL.csv")
df_taskrr = pd.read_csv("./Logs/TaskLog_RR.csv")
df_taskran = pd.read_csv("./Logs/TaskLog_Random.csv")

mean_taskll = df_taskll.mean(axis = 0)['Execution_time']
mean_taskrr = df_taskrr.mean(axis = 0)['Execution_time']
mean_taskran = df_taskran.mean(axis = 0)['Execution_time']
median_taskll = df_taskll.median(axis = 0)['Execution_time']
median_taskrr = df_taskrr.median(axis = 0)['Execution_time']
median_taskran = df_taskran.median(axis = 0)['Execution_time']

# Mean and median bar graph for task execution times
barWidth = 0.25

pos = list(range(3))
labels = ['Random', 'Least-Loaded', 'Round-Robin']
task_means = [mean_taskran, mean_taskll, mean_taskrr]
task_medians = [median_taskran, median_taskll, median_taskrr]

r1 = np.arange(len(task_means))
r2 = [x + barWidth for x in r1]

fig, ax = plt.subplots(figsize=(12,9))
plt.bar(r1, task_means, color='#EE631D', width=barWidth, edgecolor='white', label='Mean')
plt.bar(r2, task_medians, color='#1874A0', width=barWidth, edgecolor='white', label='Median')

ax.set_title('Mean and median task execution time comparison of three algorithms', fontsize=18)
ax.set_xticks([p + 0.5 * barWidth for p in pos])
ax.set_xticklabels(labels)

plt.ylabel('Execution time (sec)', fontsize=16)
plt.xticks([r - 0.125 + barWidth for r in range(len(task_means))], labels, fontsize=13)
plt.legend()
plt.savefig('./Logs/Plots/TaskMeanMedian.jpeg', bbox_inches='tight')
plt.show()

mean_jobll = df_jobll.mean(axis = 0)['Execution_time']
mean_jobrr = df_jobrr.mean(axis = 0)['Execution_time']
mean_jobran = df_jobran.mean(axis = 0)['Execution_time']
median_jobll = df_jobll.median(axis = 0)['Execution_time']
median_jobrr = df_jobrr.median(axis = 0)['Execution_time']
median_jobran = df_jobran.median(axis = 0)['Execution_time']

# Mean and median bar graph for job execution times
barWidth = 0.25

pos = list(range(3))
labels = ['Random', 'Least-Loaded', 'Round-Robin']
job_means = [mean_jobran, mean_jobll, mean_jobrr]
job_medians = [median_jobran, median_jobll, median_jobrr]

r1 = np.arange(len(job_means))
r2 = [x + barWidth for x in r1]

fig, ax = plt.subplots(figsize=(12,9))
plt.bar(r1, job_means, color='#EE631D', width=barWidth, edgecolor='white', label='Mean')
plt.bar(r2, job_medians, color='#1874A0', width=barWidth, edgecolor='white', label='Median')

ax.set_title('Mean and median job execution time comparison of three algorithms', fontsize=18)
ax.set_xticks([p + 0.5 * barWidth for p in pos])
ax.set_xticklabels(labels)

plt.ylabel('Execution time (sec)', fontsize=16)
plt.xticks([r - 0.125 + barWidth for r in range(len(task_means))], labels, fontsize=13)
plt.legend()
plt.savefig('./Logs/Plots/JobMeanMedian.jpeg', bbox_inches='tight')
plt.show()


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