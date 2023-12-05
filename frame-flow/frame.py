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
    self.slot_objs = []
    # self.required_slots = []
    # self.optional_slots = []
    for slot in self.slots:
      name = slot['name']
      required = slot['required']
      dont_care = slot['dont_care']
      slot_obj = Slot(name=name, required=required, dont_care=dont_care)
      self.slot_objs.append(slot_obj)
      # if slot_obj.is_required == True:
      #   self.required_slots.append(slot_obj)
      # else:
      #   self.optional_slots.append(slot_obj)

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