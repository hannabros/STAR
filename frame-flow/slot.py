
class Slot():
  def __init__(self, **kwargs) -> None:
    self.name = kwargs.get('name')
    self.is_required = kwargs.get('required')
    self.dont_care = kwargs.get('dont_care')
    self.is_asked = False
    self.is_filled = False
    self.value = None