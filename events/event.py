"""
Represents an object's event that can be observed by listeners.
"""

__author__ = "Dong Le Quoc Bao"
__version__ = "1.0.0"

from events.event_listener import EventListener

class Event:
    """An observable event that notifies its listeners when raised."""
    
    def __init__(self) -> None:
        """Initialize an Event with an empty list of listeners."""
        self._listeners: list[EventListener] = []
        
    def add_listener(self, listener: EventListener) -> None:
        """Add the specified listner to the list of listeners"""
        if listener in self._listeners:
            self._listeners.remove(listener)
            
    def notify(self, sender) -> None:
        """
        Notify all registered listeners of the event.
        
        Args:
            sender: The object that raised the event.
        """
        for listener in self._listeners:
            listener.update(sender)
        