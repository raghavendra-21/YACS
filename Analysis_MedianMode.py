import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import plotly.express as px
import seaborn as sns

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