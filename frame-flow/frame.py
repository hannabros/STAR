import random
from typing import Dict, List, Optional, Union

from slot import Slot

class Frame:
  def __init__(self, name: str, type: str, next_frame: Dict):
    self.name = name
    self.type = type
    self.next_frame = next_frame
    self.is_finished = False

  def check_frame_finished(self) -> bool:
    raise NotImplementedError("This method should be overridden in subclasses")

class StartFrame(Frame):
  def __init__(self, **kwargs) -> None:
    name = kwargs.get('name')
    type = kwargs.get('type')
    next_frame = kwargs.get('next_frame')
    super().__init__(name, type, next_frame)
    self.intent = 'hi'

  def check_frame_finished(self) -> bool:
    return True

class RequestFrame(Frame):
  def __init__(self, **kwargs) -> None:
    name = kwargs.get('name')
    type = kwargs.get('type')
    next_frame = kwargs.get('next_frame')
    super().__init__(name, type, next_frame)
    self.slots = kwargs.get('slots')
    self.initiator = kwargs.get('initiator')
    assert self.initiator in ['both', 'system', 'user']
    self.slot_objs = []
    for slot in self.slots:
    #   name = slot['name']
    #   required = slot['required']
    #   dont_care = slot['dont_care']
    #   order = slot['order']
      # slot_obj = Slot(name=name, required=required, dont_care=dont_care, order=order)
      slot_obj = Slot(**slot)
      self.slot_objs.append(slot_obj)
    self.slot_has_order = all([slot_obj.order for slot_obj in self.slot_objs])
      
  def check_initiation(self, speaker: str) -> bool:
    if speaker in ['both', 'system']:
      return True
    else:
      if all([slot_obj.is_asked is False for slot_obj in self.slot_objs]):
        return False
      else:
        return True
      
  def get_slot_objs_to_fill(self, speaker: str) -> List[Slot]:
    assert speaker in ['user', 'system']
    slot_objs_to_fill = []
    if speaker == 'user':
      asked_slot_objs = [slot_obj for slot_obj in self.slot_objs if slot_obj.is_asked]
      if len(asked_slot_objs) > 0:
        slot_objs_to_fill = [slot_obj for slot_obj in asked_slot_objs if not slot_obj.is_filled]
      else:
        slot_objs_to_fill = [slot_obj for slot_obj in self.slot_objs if not slot_obj.is_filled]
    else:
      slot_objs_to_fill = [slot_obj for slot_obj in self.slot_objs if not slot_obj.is_filled]
    return slot_objs_to_fill
  
  def get_slot_objs_to_das(self, slot_objs_to_fill: List[Slot], speaker: str) -> List[Dict]:
    assert speaker in ['user', 'system']
    das = []
    da = {'intent': None, 'slot': None}
    if speaker == 'user':
      if self.slot_has_order:
        orders = [slot_obj.order for slot_obj in slot_objs_to_fill]
        rnd_order = random.choice(orders)
        rnd_slot_objs = [slot_obj for slot_obj in slot_objs_to_fill if slot_obj.order <= rnd_order]
      else:
        rnd_n = random.randint(1, len(slot_objs_to_fill))
        rnd_slot_objs = random.sample(slot_objs_to_fill, rnd_n)
      for slot_obj in rnd_slot_objs:
        if slot_obj.dont_care:
          rnd_select = random.choice(['do_care', 'dont_care'])
          if rnd_select == 'do_care':
            da = {'intent': 'inform', 'slot': slot_obj.name}
          else:
            da = {'intent': 'inform', 'slot': slot_obj.name, 'slot_value': 'dont_care'}
        else:
          da = {'intent': 'inform', 'slot': slot_obj.name}
        if slot_obj.is_required:
          das.append(da)
        else:
          rnd_select = random.choice(['require', 'no_require'])
          if rnd_select == 'require':
            das.append(da)
        slot_obj.is_filled = True
      return das
    else:
      if self.slot_has_order:
        orders = [slot_obj.order for slot_obj in slot_objs_to_fill]
        rnd_order = random.choice(orders)
        rnd_slot_objs = [slot_obj for slot_obj in slot_objs_to_fill if slot_obj.order <= rnd_order]
      else:
        rnd_n = random.randint(1, len(slot_objs_to_fill))
        rnd_slot_objs = random.sample(slot_objs_to_fill, rnd_n)
      for slot_obj in rnd_slot_objs:
        da = {'intent': 'request', 'slot': slot_obj.name}
        slot_obj.is_asked = True
        das.append(da)
      return das

  def check_frame_finished(self) -> bool:
    if all([slot_obj.is_filled for slot_obj in self.slot_objs]):
      return True
    else:
      return False

class QueryFrame(Frame):
  def __init__(self, **kwargs) -> None:
    name = kwargs.get('name')
    type = kwargs.get('type')
    next_frame = kwargs.get('next_frame')
    super().__init__(name, type, next_frame)
    self.conditions = self.get_conditions()
    assert len(self.conditions) > 0
    self.rnd_condition = random.sample(self.conditions, 1)[0]

  def get_conditions(self) -> List:
    conditions = []
    for frame in self.next_frame:
      conditions.append(frame['condition'])
    return conditions

  def check_frame_finished(self) -> str:
    return self.rnd_condition
  
class InformFrame(Frame):
  def __init__(self, **kwargs) -> None:
    name = kwargs.get('name')
    type = kwargs.get('type')
    next_frame = kwargs.get('next_frame')
    super().__init__(name, type, next_frame)
    self.message = kwargs.get('message')

  def check_frame_finished(self) -> bool:
    return True

class EndFrame(Frame):
  def __init__(self, **kwargs) -> None:
    name = kwargs.get('name')
    type = kwargs.get('type')
    next_frame = kwargs.get('next_frame')
    super().__init__(name, type, next_frame)
    self.intent = 'bye'

  def check_frame_finished(self) -> bool:
    return True