import socket 
import sys
import threading
import os
import json
import random
import copy
import csv
from time import sleep, time

#Time at which the Master process starts
process_start_time = time()

'''
Initialising filename for Tasks log file based on the algorithm executed.
Note: Each algorithm has a different log file associated.
'''
Taskfilename = None
if sys.argv[2] == "RANDOM":
    Taskfilename = "Logs/TaskLog_Random.csv"
elif sys.argv[2] == "RR":
    Taskfilename = "Logs/TaskLog_RR.csv"
elif sys.argv[2] == "LL":
    Taskfilename = "Logs/TaskLog_LL.csv"

taskLogFile = open(Taskfilename,'w')
with open(Taskfilename, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Task_ID", "Job_ID", "MRFlag", "WorkerID_Assigned","Execution_time", "Arrival_time" ])

'''
Initialising filename for the Jobs log file based on the algorithm executed.
Note: Each algorithm has a different log file associated.
'''
Jobfilename = None
if sys.argv[2] == "RANDOM":
    Jobfilename = "Logs/JobLog_Random.csv"
elif sys.argv[2] == "RR":
    Jobfilename = "Logs/JobLog_RR.csv"
elif sys.argv[2] == "LL":
    Jobfilename = "Logs/JobLog_LL.csv"

JobLogFile = open(Jobfilename,'w')
with open(Jobfilename, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Job_ID", "Execution_time"])

'''
Initialising filename for log file to account for when a task was scheduled at the master process based on the algorithm executed.
Note: Each algorithm has a different log file associated.
'''
TaskScheduleLog = None
if sys.argv[2] == "RANDOM":
    TaskScheduleLog = "Logs/TaskScheduleLog_Random.csv"
elif sys.argv[2] == "RR":
    TaskScheduleLog = "Logs/TaskScheduleLog_RR.csv"
elif sys.argv[2] == "LL":
    TaskScheduleLog = "Logs/TaskScheduleLog_LL.csv"

taskLogFile = open(TaskScheduleLog,'w')
with open(TaskScheduleLog, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Task_id", "Worker", "Scheduled_time"])

'''
Initialising the various data structures and locks used in the Master process.

Data structures:
1. workerState - Contains state of each of the worker machines, such as worker ID, total number of slots and number of slots occupied.
2. mapTaskPool - Contains the information of all the map tasks which needs to be executed.
3. reduceTaskPool - Contains the information of all the Reduce tasks which need to be executed. 
4. jobState - Contains the information of the state of all jobs that were sent by requests.py until the given instant of time.
5. jobLog - Log information for jobs explicitly stored in a data structure as well, apart from the log file.
6. taskLog - Log information for individual tasks stored in a data structure as well, apart from the log file.

RRIndex is a counter variable used for the implementation of Round Robin algorithm.

Locks:
1. lockMapPool - Lock used when accessing the data structure mapTaskPool
2. lockReducePool - Lock used when accessing the data structure reduceTaskPool
3. lockJobState - Lock used when accessing the data structure jobState
4. lockWorkerState - Lock used when accessing the data structure workerState

'''
workersState = dict()
mapTaskPool = list()
reduceTaskPool = list()
jobState = dict()
jobLog = dict()
taskLog = dict()

RRIndex = 0

lockMapPool = threading.Lock()
lockReducePool = threading.Lock()
lockJobState = threading.Lock()
lockWorkerState = threading.Lock()

'''
Implementation of the Random Scheduling Algorithm.
Returns the port number of the worker machine to which the task is scheduled.
'''
def randomAlgorithm():
    while True:
        lockWorkerState.acquire()
        workersStateSnapshot = list()
        for worker in workersState:
            temp_list = [worker,workersState[worker][1]-workersState[worker][2]]
            workersStateSnapshot.append(temp_list)
        lockWorkerState.release()

        choice = random.randint(0,2)
        if workersStateSnapshot[choice][1]>0:
            port = workersStateSnapshot[choice][0]
            lockWorkerState.acquire()
            workersState[port][2]+=1
            lockWorkerState.release()
            return port
'''
Implementation of the Round Robin Scheduling Algorithm.
Returns the port number of the worker machine to which the task is scheduled.
'''
def RRAlgorithm():
    while True:
        lockWorkerState.acquire()
        workersStateSnapshot = list()
        for worker in workersState:
            temp_list = [worker,workersState[worker][1]-workersState[worker][2]]
            workersStateSnapshot.append(temp_list)
        lockWorkerState.release()

        global RRIndex
        if workersStateSnapshot[RRIndex][1]>0:
            port = workersStateSnapshot[RRIndex][0]
            lockWorkerState.acquire()
            workersState[port][2]+=1
            lockWorkerState.release()
            RRIndex = (RRIndex+1)%3
            return port

        RRIndex =(RRIndex+1)%3
'''
Implementation of the Least Loaded Scheduling Algorithm.
Returns the port number of the worker machine to which the task is scheduled.
'''
def leastLoadedAlgorithm():
    while True:
        lockWorkerState.acquire()
        workersStateSnapshot = list()
        for worker in workersState:
            temp_list = [worker,workersState[worker][1]-workersState[worker][2]]
            workersStateSnapshot.append(temp_list)
        lockWorkerState.release()

        max_free_slots = workersStateSnapshot[0][1]
        index = 0

        for i in range(1, 3):
            if workersStateSnapshot[i][1]>max_free_slots:
                max_free_slots = workersStateSnapshot[i][1]
                index = i

        if max_free_slots>0:
            port = workersStateSnapshot[index][0]
            lockWorkerState.acquire()
            workersState[port][2]+=1
            lockWorkerState.release()
            return port

        sleep(1)

'''
Function to listen to job requests at port 5000.
Thread 1 starts executing this function.
'''
def request_listen():
    s = socket.socket()        
    port = 5000                
    s.bind(('', port))
    s.listen(5)               
    while True:  
        c, addr = s.accept()      
        received = c.recv(2048)
        arrivalTime = time()
        jobRequest = json.loads(received)
        job_id = jobRequest['job_id']

        print("Job request {0} is added to the pool.".format(job_id))
        print("\n")

        lockMapPool.acquire()
        lockJobState.acquire()
        jobState[job_id] = list()
        map_tasks = list()
        reduce_tasks = list()

        for mapTask in jobRequest['map_tasks']:
            mapTaskPool.append((jobRequest['job_id'], mapTask['task_id'], mapTask['duration'], True))
            map_tasks.append((mapTask['task_id'], mapTask['duration']))

        for reduceTask in jobRequest['reduce_tasks']:
            reduce_tasks.append((reduceTask['task_id'], reduceTask['duration']))

        map_tasks_completed = list()
        reduce_tasks_completed = list()
        jobState[job_id].append(map_tasks)
        jobState[job_id].append(reduce_tasks)
        jobState[job_id].append(map_tasks_completed)
        jobState[job_id].append(reduce_tasks_completed)
        jobState[job_id].append(arrivalTime)

        lockJobState.release()
        lockMapPool.release()  
        c.close()  

'''
Function to listen to job and task updates from the workers at port 5001.
Thread 2 starts executing this function.
'''
def worker_update():
    s = socket.socket()        
    port = 5001                
    s.bind(('', port))
    s.listen(5)              
    while True:  
        c, addr = s.accept()      
        received=c.recv(2048)
        updateTime = time()
        updateRequest = json.loads(received)

        lockWorkerState.acquire()
        worker_port = updateRequest['port']
        worker_id = workersState[worker_port][0]
        workersState[worker_port][2] -= 1
        lockWorkerState.release()

        taskLog[(updateRequest['task_id'], updateRequest['job_id'])] = (updateRequest['execution_time'], int(worker_port))
        
        print("Task {0} of Job {1} has successfully completed execution.\nExecution time: {2} seconds".format(updateRequest['task_id'], updateRequest['job_id'], updateRequest['execution_time']))
        print("\n")

        with open(Taskfilename, 'a', newline='') as f:
            writer = csv.writer(f)
            MRFlag = None
            if updateRequest['flag'] == True:
                MRFlag = "M"
            else:
                MRFlag = "R"
            writer.writerow([updateRequest['task_id'], updateRequest['job_id'], MRFlag, worker_id, updateRequest['execution_time'], updateRequest['arrival_time']])

        if updateRequest['flag'] == True:
            lockJobState.acquire()
            job_id = updateRequest['job_id'] 
            jobState[job_id][2].append(updateRequest['task_id'])

            if len(jobState[job_id][0]) == len(jobState[job_id][2]):
                lockReducePool.acquire()
                for reduceTask in jobState[job_id][1]:
                    reduceTaskPool.append((job_id, reduceTask[0], reduceTask[1], False))

                lockReducePool.release()
            lockJobState.release()
        else:
            lockJobState.acquire()
            job_id = updateRequest['job_id'] 
            jobState[job_id][3].append(updateRequest['task_id'])

            if len(jobState[job_id][1]) == len(jobState[job_id][3]):
                job_execution_time = updateTime - jobState[job_id][4]
                jobLog[job_id] = job_execution_time
                
                print("Job {0} has successfully completed execution.\nExecution time: {1} seconds".format(job_id, job_execution_time))
                print("\n")

                with open(Jobfilename, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([job_id, job_execution_time])

            lockJobState.release()
 
        c.close() 

'''
Function to schedule tasks as and when the Map and Reduce task pools have pending tasks.
A separate thread - Thread 3 is used for scheduling the tasks, which starts executing this function. 
'''
def schedule_jobs():
    while True:
        lockReducePool.acquire()
        global reduceTaskPool
        reducePoolSnapshot = copy.deepcopy(reduceTaskPool)
        reduceTaskPool = list()
        lockReducePool.release()

        if len(reducePoolSnapshot)!=0:
            for job in reducePoolSnapshot:
                assignWorker(job)
        else:
            lockMapPool.acquire()
            global mapTaskPool
            mapTaskPoolSnapShot = copy.deepcopy(mapTaskPool)
            mapTaskPool = list()
            lockMapPool.release()

            if len(mapTaskPoolSnapShot) == 0:
                sleep(1)
            else:
                for job in mapTaskPoolSnapShot:
                    assignWorker(job)

'''
Helper function used to schedule jobs, based on the respective algorithm being executed.
'''
def assignWorker(job):
    data = dict()  
    data['job_id'] = job[0]
    data['task_id'] = job[1]
    data['duration'] = job[2]
    data['flag'] = job[3]

    worker = None
    if sys.argv[2] == "RANDOM":
        worker = randomAlgorithm()
    elif sys.argv[2] == "RR":
        worker = RRAlgorithm()
    elif sys.argv[2] == "LL":
        worker = leastLoadedAlgorithm()
    else:
        print("Invalid algorithm is entered.")

    with open(TaskScheduleLog, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([job[1], worker, time()-process_start_time])

    s = socket.socket()
    s.connect(('127.0.0.1', int(worker)))
    s.send(json.dumps(data).encode('utf-8'))
    s.close()
    return



print('\n\n--------------------------------------------------Yet Another Centralized Scheduler(YACS)------------------------------------------------------')
print("Master is ready. Listening to Job requests on port 5000.\n")
'''
Reading the configuration file and storing the state of worker machines.
'''
workers = list()
data = None
with open(sys.argv[1]) as file:
    data = json.loads(file.read())

for i in data['workers']:
    workers.append(i)

for i in workers:
    workersState[i['port']] = [i['worker_id'], i['slots'], 0]

t1 = threading.Thread(target = request_listen) 
t2 = threading.Thread(target = worker_update) 
t3 = threading.Thread(target = schedule_jobs)

t1.start() 
t2.start() 
t3.start()

t1.join() 
t2.join() 
t3.join()
