# User Intent : Inform, Request, Bye, Thanks, Greet, Affirm, Negate
# Additional : Irrelevant

import random

from typing import Dict, List, Optional, Union
from environment import Environment


class UserSimulator:
  def __init__(self):
    pass

  def get_da(self, env: Environment) -> Optional[List[Dict]]:
    # StartFrame
    if env.current_frame.type == 'start':
      return None
    # RequestFrame
    elif env.current_frame.type == 'request':
      # initiator가 user인지 확인
      if env.current_frame.check_initiation(speaker='user'):
        slot_objs_to_fill = env.current_frame.get_slot_objs_to_fill(speaker='user')
        das = env.current_frame.get_slot_objs_to_das(slot_objs_to_fill, speaker='user')
        return das
      else:
        return None
    # QueryFrame
    elif env.current_frame.type == 'query':
      return None
    # InformFrame
    elif env.current_frame.type == 'inform':
      return None
    # EndFrame
    elif env.current_frame.type == 'end':
      return None
