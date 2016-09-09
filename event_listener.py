from Xlib.display import Display
from Xlib.X import KeyPress, KeyPressMask, KeyReleaseMask, GrabModeAsync, CurrentTime
import Xlib.XK
from .threaded_pipe import ThreadedPipe
from abc import abstractmethod

NONCHAR = {
    9: 'escape',
    36: 'enter',
    22: 'delete',
    23: 'tab',
    65: 'space',
    113: 'left',
    114: 'right',
    116: 'down',
    111: 'up'
    }


# class OSInterface:
#
#     @abstractmethod
#     def grab_keyboard(self):
#         pass
#
#     @abstractmethod
#     def event_is_keypress(self):
#         pass
#
#     @abstractmethod
#     def events_pending(self):
#         pass
#
#     @abstractmethod
#     def get_next_event(self):
#         pass
#
#     @abstractmethod
#     def stop_listening(self):
#         pass



class XlibInterface:
    def __init__(self):
        pass
        self.display = Display()
        self.root = self.display.screen().root

    def grab_keyboard(self):
        self.root.change_attributes(event_mask = KeyPressMask | KeyReleaseMask)
        self.root.grab_keyboard(False, GrabModeAsync, GrabModeAsync, CurrentTime)

    @staticmethod
    def event_is_keypress(event) -> bool:
        if event.type is KeyPress:
            return True
        else:
            return False

    def events_pending(self) -> bool:
        return self.display.pending_events()

    def get_next_event(self):
        return self.display.next_event()

    def stop_listening(self):
        self.display.ungrab_keyboard(CurrentTime)
        self.display.flush()


class XEventListener(ThreadedPipe, XlibInterface):
    """docstring for KeySequence"""
    def __init__(self, connection):
        ThreadedPipe.__init__(self, connection)
        XlibInterface.__init__(self)
        self.connection = connection
        self.terminate = False

    def run(self):
        """Mandatory override for Thread::run"""
        self.listening()

    def listening(self):
        """Main loop for key listener process."""
        self.grab_keyboard()  # using XInterface
        # loops until terminate signal is received
        while True:
            # await key event then process
            event_list = self.events_pending()
            if event_list != 0:
                event = self.get_next_event()
                self.handle_event(event)
            # check for new instructions
            x = self.check_pipe()
            if x is not None:
                self.process_message(x)
            if self.terminate is True:
                break
        self.stop_listening()
        self.connection.send('TERMINATED')

    def handle_event(self, event):
        #if self.event_is_keypress(event):
        if event.type is KeyPress:
            # lookup keysym for reported event
            keysym = self.display.keycode_to_keysym(event.detail, 0)
            keychar = self.display.lookup_string(keysym)
            # send character string
            if keychar is not None: # or len(keychar)>0:
                self.connection.send(str(keychar))
            else:
                try:
                    key = self.lookup_nonchar(event.detail)
                    self.connection.send(key)
                except KeyError:
                    pass

    @staticmethod
    def lookup_nonchar(code: int) -> str:
        """This function returns non-character keysyms for corresponding keycodes
        
        Xlib's Display::keycode_to_keysym"""
        return NONCHAR[code]

    def process_message(self, msg: str):
        if msg == 'TERMINATE':
            self.terminate = True
        elif msg == 'PAUSE':
            pass
        elif msg == 'RESUME':
            pass
        else:
            self.terminate = True





    def lookup_keysym(self, keycode):
        pass

    def report_event(self, keysym):
        pass
