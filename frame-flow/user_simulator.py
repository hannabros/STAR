# User Intent : Inform, Request, Bye, Thanks, Greet, Affirm, Negate
# Additional : Irrelevant

import random

from typing import Dict, List, Optional, Union
from environment import Environment


class UserSimulator:
  def __init__(self):
    pass

  def get_da(self, env: Environment) -> Optional[List[Dict]]:
    das = []
    da = {'intent': None, 'slot': None}
    if env.current_frame.type == 'start':
      return None
    elif env.current_frame.type == 'request':
      # 처음 시작일 경우
      if all(slot_obj.is_asked is False for slot_obj in env.current_frame.slot_objs):
        unfilled_slot_objs = [slot_obj for slot_obj in env.current_frame.slot_objs if not slot_obj.is_filled]
        rnd_n = random.randint(1, len(unfilled_slot_objs))
        rnd_slot_objs = random.sample(unfilled_slot_objs, rnd_n)
        for slot_obj in rnd_slot_objs:
          if slot_obj.dont_care:
            rnd_n = random.choice(['do_care', 'dont_care'])
            if rnd_n == 'do_care':
              da = {'intent': 'inform', 'slot': slot_obj.name}
            else:
              da = {'intent': 'inform', 'slot': slot_obj.name, 'slot_value': 'dont_care'}
          else:
            da = {'intent': 'inform', 'slot': slot_obj.name}
          if slot_obj.is_required:
            das.append(da)
          else:
            rnd_n = random.choice(['require', 'no_require'])
            if rnd_n == 'require':
              das.append(da)
          slot_obj.is_filled = True
      # is_asked slot이 있는 경우
      else:
        asked_slot_objs = [slot_obj for slot_obj in env.current_frame.slot_objs if slot_obj.is_asked]
        unfilled_slot_objs = [slot_obj for slot_obj in asked_slot_objs if not slot_obj.is_filled]
        rnd_n = random.randint(1, len(unfilled_slot_objs))
        rnd_slot_objs = random.sample(unfilled_slot_objs, rnd_n)
        for slot_obj in rnd_slot_objs:
          if slot_obj.dont_care:
            rnd_n = random.choice(['do_care', 'dont_care'])
            if rnd_n == 'do_care':
              da = {'intent': 'inform', 'slot': slot_obj.name}
            else:
              da = {'intent': 'inform', 'slot': slot_obj.name, 'slot_value': 'dont_care'}
          else:
            da = {'intent': 'inform', 'slot': slot_obj.name}
          if slot_obj.is_required:
            das.append(da)
          else:
            rnd_n = random.choice(['require', 'no_require'])
            if rnd_n == 'require':
              das.append(da)
          slot_obj.is_filled = True
      return das
    elif env.current_frame.type == 'query':
      return None
    elif env.current_frame.type == 'inform':
      return None
    elif env.current_frame.type == 'end':
      return None
