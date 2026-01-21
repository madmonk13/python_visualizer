"""
Base Ring Shape Class
All ring shapes must inherit from this class
"""

from abc import ABC, abstractmethod


class BaseRing(ABC):
    """Abstract base class for all ring shapes"""
    
    @abstractmethod
    def get_name(self):
        """Return the display name for the UI dropdown"""
        pass
    
    @abstractmethod
    def get_internal_name(self):
        """Return the internal identifier (lowercase, no spaces)"""
        pass
    
    @abstractmethod
    def draw_glow(self, draw, cx, cy, w, h, color, width, glow_level, beat):
        """
        Draw a single glow layer for this ring shape
        
        Parameters:
        -----------
        draw : PIL.ImageDraw
            The drawing context
        cx, cy : int
            Center point coordinates
        w, h : int
            Width and height (ring size)
        color : tuple
            RGB color tuple (r, g, b)
        width : int
            Line thickness
        glow_level : int
            Glow layer number (0-8), higher = outer glow
        beat : float
            Beat intensity (0.0 to 1.0) for pulsing effects
        """
        pass
    
    @abstractmethod
    def draw_outline(self, draw, cx, cy, w, h, color, width):
        """
        Draw the main ring outline
        
        Parameters:
        -----------
        draw : PIL.ImageDraw
            The drawing context
        cx, cy : int
            Center point coordinates
        w, h : int
            Width and height (ring size)
        color : tuple
            RGB color tuple (r, g, b)
        width : int
            Line thickness
        """
        pass