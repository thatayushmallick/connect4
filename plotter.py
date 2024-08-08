import matplotlib.pyplot as plt
import time
import numpy as np

time_game_dict = {}
loops = 1000

for i in range(loops):
  start_time = time.time()
  from subprocess import call
  call(["python", "crazy.py"])
  end_time = time.time()
  ex_time = end_time - start_time
  ex_time = round(ex_time,2)
  if ex_time not in time_game_dict:
    time_game_dict[ex_time] = 1
  else:
    time_game_dict[ex_time] += 1

time_list = list(time_game_dict.keys())
occurence = list(time_game_dict.values())
plt.scatter(time_list,occurence,color='blue',label='time')
plt.xlabel('TIME TAKEN TO END GAME')
plt.ylabel("OCCURENCE OF SUCH EVENT")
plt.show()
print(time_list)
  
