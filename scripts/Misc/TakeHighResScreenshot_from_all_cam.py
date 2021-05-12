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

def take_all_cam_screenshots():
    level_actors = unreal.EditorLevelLibrary.get_all_level_actors()
    all_cameras = unreal.EditorFilterLibrary.by_class(
        level_actors,
        unreal.CameraActor
    )

    for cam in all_cameras:
        camera_name = cam.get_actor_label()
        unreal.AutomationLibrary.take_high_res_screenshot(1280, 720, camera_name, cam)
        print ('Requested screenshot for '+ camera_name )
        yield

py_tick = PyTick()
py_tick.schedule.append(take_all_cam_screenshots())
