"""
Common interface for all event listeners.
"""

__author__ = "Dong Le Quoc Bao"
__version__ = "1.0.0"

from abc import ABC, abstractmethod

class EventListener(ABC):
    """Abstract base class for an event listener."""
    
    @abstractmethod
    def update (self, sender) -> None:
        """
        Respond to an event raised by the sender.
        
        Args:
            sender: The object that raised the event.
        """
        
        raise NotImplementedError