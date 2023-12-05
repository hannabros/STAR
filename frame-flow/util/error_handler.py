class NoFrameTypeError(Exception):
  def __init__(self, type_name: str):
    self.message = f'No Frame Type with name {type_name}'
    super().__init__(self.message)

class NoFrameObjError(Exception):
  def __init__(self, name: str):
    self.message = f'No Frame object with name {name}'
    super().__init__(self.message)