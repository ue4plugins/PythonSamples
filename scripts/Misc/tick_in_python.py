import unreal
from collections import deque
from collections.abc import Iterable
  
class PyTick():
 
    _delegate_handle = None
    _current = None
    schedule = None
 
    def __init__(self):
        self.schedule = deque()
        self._delegate_handle = unreal.register_slate_post_tick_callback(self._callback)
 
    def _callback(self, _):
        if self._current is None:
            if self.schedule:
                self._current = self.schedule.popleft()
 
            else:
                print ('Done jobs')
                unreal.unregister_slate_post_tick_callback(self._delegate_handle)
                return
 
        try:
            task = next(self._current)
 
            if task is not None and isinstance(task, Iterable):
                # reschedule current task, and do the new one
                self.schedule.appendleft(self._current)
                self._current = task
 
        except StopIteration:
            self._current = None
 
        except:
            self._current = None
            raise
 
def my_loop():
    for i in range(10):
        print ('Tick A %s'% i)
        yield my_inner_loop() # chain another task inside
 
def my_inner_loop():
    for i in range(2):
        print ('Tick B %s'% i)
        yield
 
py_tick = PyTick()
py_tick.schedule.append(my_loop())