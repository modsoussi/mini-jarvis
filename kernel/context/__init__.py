from typing import List

class Context:
  def __init__(self) -> None:
    self._memory: List[str] = []
    self._input: str = None
  
  @property
  def memory(self):
    return self._memory
  
  def add(self, mem):
    self._memory.append(mem)
  
  @property
  def input(self):
    return self._input
  
  @input.setter
  def input(self, val):
    self._input = val