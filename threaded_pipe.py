from threading import Thread
from abc import abstractmethod
import typing
if typing.TYPE_CHECKING:
    from multiprocessing.connection import Connection


class ThreadedPipe(Thread):
    """"""
    def __init__(self, connect: Connection):
        Thread.__init__(self)
        self.connection = connect

    def check_pipe(self):
        if self.connection.poll():
            msg = self.connection.recv()  # type: list
            return msg
            #self.process_message(msg)
        else:
            return None

    @abstractmethod
    def process_message(self, msg):
        """Override"""
        pass

    @staticmethod
    def log_error(dysfunc):
        """decorator which wraps a function in a try statement
        and saves the traceback if an exception occurs"""
        def wrapper():
            try:
                dysfunc()
            except Exception as e:
                self.log_error(e)
                self.respond_to_error()
        return wrapper

    @abstractmethod
    def respond_to_error(self):
        """Override"""
        pass

from multiprocessing import Process


class ProcessPipe(Process):
    """"""
    def __init__(self, connection):
        Process.__init__(self)
        self.connection = connection

    def check_pipe(self):
        if self.connection.poll():
            msg = self.connection.recv()
            return msg
            #self.process_message(msg)
        else:
            return None

    def process_message(self, msg):
        """Override"""
        pass

    def log_error():
        pass

    @staticmethod
    def anticipate_error(self, dysfunc):
        """decorator which wraps a function in a try statement
        and saves the traceback if an exception occurs"""
        def wrapper():
            try:
                dysfunc()
            except Exception as e:
                self.log_error(e)
                self.respond_to_error()
        return wrapper

    def respond_to_error(self):
        """Override"""
