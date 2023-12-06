import os, sys
import json
from typing import Dict, List, Optional, Union

from system_simulator import SystemSimulator
from user_simulator import UserSimulator
from environment import Environment

# Function to read the configuration from a JSON file
def read_config(file_path: str) -> Dict:
  with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_path), 'r') as file:
    config = json.load(file)
  return config

if __name__ == "__main__":
  # Example usage
  config_file_path = './rsc/bank_fraud_report.json'
  config = read_config(config_file_path)
  frames = config['frames']

  sys_sim = SystemSimulator()
  usr_sim = UserSimulator()
  
  env = Environment(frames)
  env.init()
  assert env.current_frame.type == 'start'
  env.update()

  das = []
  while not env.flow_finished:
    usr_da = usr_sim.get_da(env)
    if usr_da:
      das.append(f'user: {usr_da}')
    env.update()
    sys_da = sys_sim.get_da(env)
    if sys_da:
      das.append(f'system: {sys_da}')
    if env.current_frame.type != 'end':
      env.update()

    # print(env.current_frame.name)

  print(das)