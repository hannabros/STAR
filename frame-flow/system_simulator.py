
import random
from typing import Dict, List, Optional, Union
from environment import Environment


class SystemSimulator:
  def __init__(self):
    pass

  def get_da(self, env: Environment) -> Optional[List[Dict]]:
    das = []
    da = {'intent': None, 'slot': None}
    if env.current_frame.type == 'start':
      return None
    elif env.current_frame.type == 'request':
      unfilled_slot_objs = []
      for slot_obj in env.current_frame.slot_objs:
        if not slot_obj.is_filled:
          unfilled_slot_objs.append(slot_obj)
      rnd_n = random.randint(1, len(unfilled_slot_objs))
      rnd_slot_objs = random.sample(unfilled_slot_objs, rnd_n)
      for slot_obj in rnd_slot_objs:
        da = {'intent': 'request', 'slot': slot_obj.name}
        slot_obj.is_asked = True
        das.append(da)
      return das
    elif env.current_frame.type == 'query':
      da = {'intent': env.current_frame.rnd_condition}
      return da
    elif env.current_frame.type == 'inform':
      da = {'intent': 'inform', 'message': env.current_frame.message}
      return da
    elif env.current_frame.type == 'end':
      da = {'intent': env.current_frame.intent}
      env.flow_finished = True
      return da