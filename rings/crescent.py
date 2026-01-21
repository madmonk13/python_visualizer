"""
Crescent Moon Ring Shape
Curved crescent moon pattern
"""

import math
from rings.base_ring import BaseRing


class Crescent(BaseRing):
    def get_name(self):
        return "Crescent Moon"
    
    def get_internal_name(self):
        return "crescent"
    
    def draw_glow(self, draw, cx, cy, w, h, color, width, glow_level, beat):
        alpha = int((200 + beat * 55) * (1 - glow_level / 8))
        glow_color = (*color, alpha)
        
        # Create crescent by drawing outer arc and inner arc
        points = []
        
        # Outer arc (right side) - semicircle from top to bottom
        num_points = 20
        for i in range(num_points + 1):
            angle = math.radians(-90 + i * (180 / num_points))
            px = cx + (w + glow_level*2) * math.cos(angle)
            py = cy + (h + glow_level*2) * math.sin(angle)
            points.append((px, py))
        
        # Inner arc (left side, offset inward) - from bottom to top
        for i in range(num_points + 1):
            angle = math.radians(90 - i * (180 / num_points))
            # Offset the center leftward and make it smaller for crescent effect
            offset_x = -(w + glow_level*2) * 0.35
            scale = 0.75
            px = cx + offset_x + (w + glow_level*2) * scale * math.cos(angle)
            py = cy + (h + glow_level*2) * scale * math.sin(angle)
            points.append((px, py))
        
        draw.polygon(points, outline=glow_color, width=width + glow_level)
    
    def draw_outline(self, draw, cx, cy, w, h, color, width):
        # Create crescent by drawing outer arc and inner arc
        points = []
        
        # Outer arc (right side) - semicircle from top to bottom
        num_points = 20
        for i in range(num_points + 1):
            angle = math.radians(-90 + i * (180 / num_points))
            px = cx + w * math.cos(angle)
            py = cy + h * math.sin(angle)
            points.append((px, py))
        
        # Inner arc (left side, offset inward) - from bottom to top
        for i in range(num_points + 1):
            angle = math.radians(90 - i * (180 / num_points))
            # Offset the center leftward and make it smaller for crescent effect
            offset_x = -w * 0.35
            scale = 0.75
            px = cx + offset_x + w * scale * math.cos(angle)
            py = cy + h * scale * math.sin(angle)
            points.append((px, py))
        
        draw.polygon(points, outline=(*color, 255), width=width)