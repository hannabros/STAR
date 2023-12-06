from typing import Dict, List, Optional, Union
from frame import Frame, RequestFrame, QueryFrame, InformFrame, StartFrame, EndFrame
from util.error_handler import *

class Environment():
  def __init__(self, frames: Dict) -> None:
    self.frames = frames
    self.frame_objs = []
    self.set_frame_objs()
    self.validate_frame_objs()
    # self.set_frame_flow()
    self.current_frame = None
    self.dialogue_states = None
    self.flow_finished = False

  def set_frame_objs(self) -> None:
    for frame in self.frames:
      if frame['type'] == 'start':
        frame_obj = StartFrame(**frame)
      elif frame['type'] == 'request':
        frame_obj = RequestFrame(**frame)
      elif frame['type'] == 'query':
        frame_obj = QueryFrame(**frame)
      elif frame['type'] == 'inform':
        frame_obj = InformFrame(**frame)
      elif frame['type'] == 'end':
        frame_obj = EndFrame(**frame)
      else:
        raise NoFrameTypeError(frame['type'])
      self.frame_objs.append(frame_obj)
  
  def validate_frame_objs(self):
    for frame_obj in self.frame_objs:
      if frame_obj.type != 'end':
        next_frame = frame_obj.next_frame
        next_frame_names = [frame['frame'] for frame in next_frame]
        for name in next_frame_names:
          try:
            next_frame_obj = self._get_frame_obj_by_name(name)
          except NoFrameObjError as e:
            raise NextFrameNotValidError(frame_obj.name, name)


  def get_next_frame_obj(self, frame_obj: Frame, condition=None) -> Frame:
    next_frames = frame_obj.next_frame
    if len(next_frames) == 1:
      next_frame_name = next_frames[0]['frame']
      next_frame = self._get_frame_obj_by_name(next_frame_name)
      return next_frame
    else:
      for frame in next_frames:
        if frame['condition'] == condition:
          next_frame_name = frame['frame']
          next_frame = self._get_frame_obj_by_name(next_frame_name)
          return next_frame

  def _get_frame_obj_by_name(self, name: str) -> Frame:
    for frame_obj in self.frame_objs:
      if frame_obj.name == name:
        return frame_obj
    raise NoFrameObjError(name)
      
  def _get_frame_obj_by_type(self, type: str) -> Frame:
    for frame_obj in self.frame_objs:
      if frame_obj.type == type:
        return frame_obj
    raise NoFrameObjError(type)

  def init(self) -> None:
    init_frame_obj = self._get_frame_obj_by_type('start')
    self.current_frame = init_frame_obj

  def update(self):
    if self.current_frame.check_frame_finished():
      if isinstance(self.current_frame.check_frame_finished(), bool):
        next_frame = self.get_next_frame_obj(self.current_frame)
      else:
        if self.current_frame.type == 'query':
          condition = self.current_frame.check_frame_finished()
          next_frame = self.get_next_frame_obj(self.current_frame, condition)
      self.current_frame = next_frame

