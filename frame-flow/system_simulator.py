
import random
from typing import Dict, List, Optional, Union
from environment import Environment


class SystemSimulator:
  def __init__(self):
    pass

  def get_da(self, env: Environment) -> Optional[List[Dict]]:
    das = []
    da = {'intent': None, 'slot': None}
    # StartFrame
    if env.current_frame.type == 'start':
      return None
    # RequestFrame
    elif env.current_frame.type == 'request':
      slot_objs_to_fill = env.current_frame.get_slot_objs_to_fill(speaker='system')
      das = env.current_frame.get_slot_objs_to_das(slot_objs_to_fill, speaker='system')
      return das
    # QueryFrame
    elif env.current_frame.type == 'query':
      da = {'intent': env.current_frame.rnd_condition}
      return da
    # InformFrame
    elif env.current_frame.type == 'inform':
      da = {'intent': 'inform', 'message': env.current_frame.message}
      return da
    # EndFrame
    elif env.current_frame.type == 'end':
      da = {'intent': env.current_frame.intent}
      env.flow_finished = True
      return da