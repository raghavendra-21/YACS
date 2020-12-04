import sys
import time
import json
import socket
import threading
from threading import Lock

locktask_pool = threading.Lock()
process_start_time = time.time()

'''
Function to listen to task assignments from the Master process.
Executed by Thread 1.
'''
def master_listen(port_number, worker_id):
  s = socket.socket()       
  port = port_number               
  s.bind(('', int(port)))        
  s.listen(5)               
  while True:  
      c, addr = s.accept()       
      recv_json = c.recv(2048)
      taskArrivalTime = time.time()
      task_desc = json.loads(recv_json)
      t2 = threading.Thread(target=updateto_master, args=(task_desc, taskArrivalTime)) 
      t2.start() 
      c.close() 

'''
Function to send task completion updates to the Master process.
Executed by Thread 2.
'''
def updateto_master(task_desc, taskArrivalTime):
  time.sleep(task_desc['duration'])
  taskEndTime = time.time()
  to_send = dict()
  to_send['task_id'] =task_desc['task_id']
  to_send['job_id'] = task_desc['job_id']
  to_send['flag'] = task_desc['flag']
  to_send['port'] = int(sys.argv[1])
  to_send['scheduled_time'] = task_desc['scheduled_time']
  to_send['execution_time'] = taskEndTime - taskArrivalTime
  to_send['arrival_time'] = taskArrivalTime - process_start_time
  s = socket.socket()       
  port = 5001                
  s.connect(('127.0.0.1', port))  
  s.send(json.dumps(to_send).encode('utf-8')) 
  s.close() 

port_number = sys.argv[1]
worker_id = sys.argv[2]
print('Worker machine {0} running at port number {1}.'.format(worker_id, port_number))
print('Listening to job requests...')
t1 = threading.Thread(target=master_listen, args=(port_number,worker_id))
t1.start() 
t1.join() 
