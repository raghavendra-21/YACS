# YACS
Yet Another Centralized Scheduler (YACS) - 
A simulation consisting of a Master, a dedicated machine to manage the resources of other machines in the cluster. Worker machines execute the tasks in their respective slots. The Master machine schedules tasks to different slots in the Worker machines based on the algorithm implemented.
<br>
<br>
### **Scheduling algorithms implemented:** <br>
1. Random <br>
2. Round Robin <br>
3. Least Loaded <br>

### **File Description:** <br> 
1. config.json <br>
     This is a configuration file of the format <br>
     { <br>
          "Workers": [<br>
          {<br>
               "worker_id": <worker_id>,<br>
               "slots": <number of slots>,<br>
               "port": <port number><br>
          },<br>
          {<br>
               "Worker_id": <Worker_id>,<br>
               "slots": <number of slots>,<br>
               "port": <port number><br>
           },<br>
          …<br>
          ]<br>
     }<br>
<br>
2. requests.py  <br>
     Generates job requests taking the number of requests as command line argument. <br>
     Each request has the following JSON format.<br>
     {<br>
          "job_id":<job_id>,<br>
           "map_tasks":[<br>
          {<br>
               "task_id":"<task_id>",<br>
               "duration":<in seconds><br>
          }<br>
          ...<br>
          ],<br>
           "reduce_tasks":[<br>
          { <br>
                "task_id":"<task_id>",<br>
               "duration":<in seconds><br>
           }<br>
          ...<br>
          ]<br>
      }<br>
  <br>
3. Master.py <br>
     The master machine which listens to incoming requests and schedules the tasks on workers.<br>
<br>
4. Worker.py <br>
     The worker machine which simulates the tasks given by the master.<br>
<br>


### Execution: <br>
**1. Master process** <br>
     To run the Master process, execute the follwing command<br>
     python3 Master.py <path_to_configuration_file> <algorithm_implementation> <br>

  <algorithm_implementation> options: <br>
  **RANDOM** - for Random Scheduling Algorithm <br>
  **RR** - for Round Robin Scheduling Algorithm <br>
  **LL** - for Least Loades Scheduling Algorithm <br>
  <br>
  Example: <br>
  python3 Master.py config.json RR <br>
  <br>
**2. Worker process** <br>
  To run the Worker process, execute the following command <br>
  python3 Worker.py <port_number> <worker_id> <br>
  <br>
  Example: <br>
  python3 Worker.py 7000 1 <br>
  <br>
**3. To generate random requests <br>**
  The requests.py is used to generate random requests, each as a JSON object of the following format <br>
  
  Command:<br>
  python3 requests.py <number_of_requests><br>
  


