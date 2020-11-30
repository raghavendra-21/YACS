# YACS
Yet Another Centralized Scheduler (YACS) - 
A simulation consisting of a Master, a dedicated machine to manage the resources of other machines in the cluster. Worker machines execute the tasks in their respective slots. The Master machine schedules tasks to different slots in the Worker machines based on the algorithm implemented.

Execution:
1. Master process
  To run the Master process, execute the follwing command
  python3 Master.py <path_to_configuration_file> <algorithm_implementation>

  <algorithm_implementation> options:
  RANDOM - for Random Scheduling Algorithm
  RR - for Round Robin Scheduling Algorithm
  LL - for Least Loades Scheduling Algorithm
  
  Example:
  python3 Master.py config.json RR

2. Worker process
  To run the Worker process, execute the following command
  python3 Worker.py <port_number> <worker_id>
  
  Example:
  python3 Worker.py 7000 1

3. To generate random requests
  The requests.py is used to generate random requests, each as a JSON object of the following format
  {
    "job_id":<job_id>,
    "map_tasks":[
    {
      "task_id":"<task_id>",
      "duration":<in seconds>
    },
    {
      "task_id":"<task_id>",
      "duration":<in seconds>
    }
    ...
    ],
    "reduce_tasks":[
    {
      "task_id":"<task_id>",
      "duration":<in seconds>
    },
    {
      "task_id":"<task_id>",
      "duration":<in seconds>
    }
    ...
    ]
  }
  
  Command:
  python3 requests.py <number_of_requests>
  


