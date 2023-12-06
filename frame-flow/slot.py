
class Slot():
  def __init__(self, **kwargs) -> None:
    self.name = kwargs.get('name')
    self.is_required = kwargs.get('required', False)
    self.dont_care = kwargs.get('dont_care', False)
    self.order = kwargs.get('order', None)
    self.is_asked = False
    self.is_filled = False
    self.value = None