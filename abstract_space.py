from .event_listener import XEventListener
from multiprocessing import Pipe
from .view import ViewContext
from .command import CommandHandler
from .data_structures import BranchingNode, CommandNode


class ThreadManager:
    """
    ThreadManager encapsulates the means of communication and control between
    the main AbstractSpace class (below), and the listener and UI processes.

    EventListener continuously queries the Xlib display server for keypress
    events, and thus must run on a separate thread. Similarly, ViewContext
    maintains the GUI toolkit's event loop, which also blocks other activities.
    Since AbstractSpace updates the view in response to incoming key events,
    it needs to exchange data and commands with each. So ThreadManager creates
    two-way pipes, one end of which are used to initialize XEventListener and
    ViewContext, which inherit from ThreadedPipe and ProcessPipe*, respectively.

    * due to peculiarities of Qt, it is required to run as a separate Process
    instead of as a Thread
    """
    def __init__(self):
        self.view_connect = None
        self.view_thread = None
        self.listener_connect = None
        self.listener_thread = None
        self.spawn_threads()

    def spawn_threads(self):
        #
        self.listener_connect, listener_side = Pipe()
        self.listener_thread = XEventListener(listener_side)
        self.view_connect, view_side = Pipe()
        self.view_thread = ViewContext(view_side)
        self.listener_thread.start()  # begin listening early
        print('listener started')

    def check_pipe(self):
        events = []
        while self.listener_connect.poll():
            events.append(self.listener_connect.recv())
        return events

    def disconnect_listener(self):
        self.listener_connect.send('TERMINATE')
        print('stop command sent, waiting')
        while True:
            if self.listener_connect.poll:
                msg = self.listener_connect.recv()
                if msg == 'TERMINATED':
                    break
        print('listener terminated')
        del self.listener_thread

    def dismiss_view(self):
        self.view_connect.send('TERMINATE')


class AbstractSpace:
    """
    The AbstractSpace class realizes the user's descent along the CommandTree,
    coordinating input events with the view, in accordance with the tree's structure.

    """
    def __init__(self, root_node: BranchingNode):
        # establish connection to threads
        self.threads = ThreadManager()
        # setup representation
        self.root = root_node
        self.tree_path = []
        self.current_node = self.root
        self.command = None
        self.resolved = False
        # start presentation/selection processes
        self.threads.view_thread.start()
        self.supply_view_information()
        self.processing_loop()
        if self.command is not None:
            print('executing command')
            CommandHandler(self.command)

    def processing_loop(self):
        """This function loops continuously during command selection,
        processing and recording events detected by the Listener thread.

        The descendants of the current node are checked against each incoming signal.
        If input matches a BranchingNode, the path and view are updated accordingly
        and the process continues.
        If a CommandNode, the processes closed, and the Command executed.
        If character is ESC or doesn't match, the process is terminated.
        """
        while self.resolved is False:
            events = self.threads.check_pipe()
            if len(events)>0:
                print('detected events')
                for key in events:
                    print(key)
                    # reassign self.current_node to selected descendant
                    if key in self.current_node.descendants:
                        self.current_node = \
                            self.current_node.descendants[key][1]
                    else:
                        self.terminate_processes()
                        break

                    # proceed according to node type:
                    if isinstance(self.current_node, BranchingNode):
                        # rebuild view and continue
                        self.tree_path.append(key)
                        self.supply_view_information()
                        continue
                    elif isinstance(self.current_node, CommandNode):
                        # shutdown processes and execute command
                        print(self.current_node.command)
                        self.command = self.current_node.command
                        self.terminate_processes()
                        self.execute_command()
                        break
                    else:
                        self.terminate_processes()
                        break

    def supply_view_information(self):
        labels = [(symbol, node[0]) for symbol, node in
                  self.current_node.descendants.items()]
        # sort items alphabetically by symbol character
        lsorted = sorted(labels, key=lambda x: x[0])
        def form(a, b): return '{} ⟹ {}'.format(a, b)
        items = [form(symbol, meaning) for symbol, meaning in lsorted]

        self.threads.view_connect.send(items)

    def reverse(self):
        self.current_node = self.current_node.parent
        self.supply_view_information()

    def terminate_processes(self):
        self.resolved = True
        self.threads.disconnect_listener()
        self.threads.dismiss_view()

    def execute_command(self):
        print(self.command)
        #c = CommandHandler(self.command)
