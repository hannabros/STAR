class NoFrameTypeError(Exception):
  def __init__(self, type_name: str):
    self.message = f'No Frame Type with name {type_name}'
    super().__init__(self.message)

class NoFrameObjError(Exception):
  def __init__(self, name: str):
    self.message = f'No Frame object with name {name}'
    super().__init__(self.message)

class NextFrameNotValidError(Exception):
  def __init__(self, frame_obj_name: str, name: str):
    self.message = f'No Next Frame object in {frame_obj_name} with name {name}'
    super().__init__(self.message)