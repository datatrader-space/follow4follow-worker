import sys
import types
from typing import List
class EventHandler:
    class Exceptions:
        """Custom error classes definition."""
        class EventNotAllowedError(Exception):
            """Will raise when tries to link a callback to nonexistent event."""
            pass  # pylint:disable=unnecessary-pass

    def __init__(self,
                 *event_names,
                 verbose=False,
                 stream_output=sys.stdout,
                 tolerate_callbacks_exceptions=False
                 ):
        """[summary]

        Args:
            verbose (bool, optional): [description]. Defaults to False.
            stream_output ([type], optional): [description]. Defaults to sys.stdout.
            tolerate_callbacks_exceptions (bool, optional): [description]. Defaults to False.
        """
        self.__events = {}
        self.verbose = verbose
        self.tolerate_exceptions = tolerate_callbacks_exceptions
        self.stream_output = stream_output

        if event_names:
            for event in event_names:
                self.register_event(str(event))  # cast as str to be safe

    @property
    def events(self) -> dict:
        """Return events as dict."""
        return self.__events

    def clear_events(self) -> bool:
        """Clear all events."""
        self.__events = {}
        return True

    @property
    def event_list(self) -> List[str]:
        """Return  list of registered events."""
        return self.__events.keys()

    @property
    def count_events(self) -> int:
        """Return number of registered events."""
        return len(self.event_list)

    def is_event_registered(self, event_name: str) -> bool:
        """Return if an event is current registered.

        Args:
            event_name (str): The event you want to consult.
        """
        return event_name in self.__events

    def register_event(self, event_name: str) -> bool:
        """Register an event name.

        Args:
            event_name (str): Event name as string.
        """
        # print('registering event', event_name, self.events)
        if self.is_event_registered(event_name):
            return False

        self.__events[event_name] = []
        return True

    def un_register_event(self, event_name: str) -> bool:
        """Un-register an event name.

        Args:
            event_name (str): Remove an event from events dict.
        """
        if event_name in self.__events:
            del self.__events[event_name]
            return True
        return False

    @staticmethod
    def is_callable(func: any) -> bool:
        """Return true if func is a callable variable.

        Args:
            func (callable): Object to validates as a callable.
        """
        return isinstance(func, (types.FunctionType,
                                 types.BuiltinFunctionType,
                                 types.MethodType,
                                 types.BuiltinMethodType
                                 )
                          )

    def is_callback_in_event(self, event_name: str, callback: callable) -> bool:
        """Return if a given callback is already registered on the events dict.

        Args:
            event_name (str): The event name to look up for the callback inside.
            callback (callable): The callback function to check.
        """
        return callback in self.__events[event_name]

    def link(self, callback: callable, event_name: str) -> bool:
        """Link a callback to be executed on fired event..

        Args:
            callback (callable): function to link.
            event_name (str): The event that will trigger the callback execution.
        """

        if not self.is_callable(callback):
            return False

        if not self.is_event_registered(event_name):
            raise EventHandler.Exceptions.EventNotAllowedError(
                f'Can not link event {event_name}, not registered. Registered events are:'
                f' {", ".join(self.__events.keys())}. Please register event {event_name} before link callbacks.')

        if callback not in self.__events[event_name]:
            self.__events[event_name].append(callback)
            return True

        return False

    def unlink(self, callback: callable, event_name: str) -> bool:
        """Unlink a callback execution from a specific event.

        Args:
            callback (callable): function to link.
            event_name (str): The event that will trigger the callback execution.
        """
        if not self.is_event_registered(event_name):
            print(f'Can not unlink event {event_name}, not registered. Registered events '
                  f'are: {", ".join(self.__events.keys())}. '
                  f'Please register event {event_name} before unlink callbacks.', file=self.stream_output)
            return False

        if callback in self.__events[event_name]:
            self.__events[event_name].remove(callback)
            return True
        return False

    def fire(self, event_name: str, *args, **kwargs) -> bool:
        """Triggers all callbacks executions linked to given event.

        Args:
            event_name (str): Event to trigger.
            *args: Arguments to be passed to callback functions execution.
            *kwargs: Keyword arguments to be passed to callback functions execution.
        """
        all_ok = True
        for callback in self.__events[event_name]:
            try:
                callable(callback(*args, **kwargs))
            except Exception as e:  # pylint:disable=broad-except
                if not self.tolerate_exceptions:
                    raise e
                
                if self.verbose:
                    pass
                all_ok = False
                continue

        return all_ok

    def __str__(self) -> str:
        """Return a string representation."""

        mem_address = str(hex(id(self)))

        event_related = \
            [f"{event}:[{', '.join([callback.__name__ for callback in self.__events[event]])}]" for event in
             self.__events]

        return f'<class {self.__class__.__name__} at ' \
            f'{mem_address}: {", ".join(event_related)}, verbose={self.verbose}, ' \
            f'tolerate_exceptions={self.tolerate_exceptions}>'

    def __repr__(self) -> str:
        """Return python object representation."""
        return self.__str__()


EVENT_BUS = EventHandler()

def subscribe(event: str):
    def _callable_event_wrapper(_func: callable):
        if not EVENT_BUS.is_event_registered(event):
            EVENT_BUS.register_event(event)
        EVENT_BUS.link(_func, event)
        return _func
    return _callable_event_wrapper

