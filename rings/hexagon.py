"""
Hexagon Ring Shape
Six-sided hexagonal ring
"""

import math
from rings.base_ring import BaseRing


class Hexagon(BaseRing):
    def get_name(self):
        return "Hexagon"
    
    def get_internal_name(self):
        return "hexagon"
    
    def draw_glow(self, draw, cx, cy, w, h, color, width, glow_level, beat):
        alpha = int((200 + beat * 55) * (1 - glow_level / 8))
        glow_color = (*color, alpha)
        
        points = []
        for i in range(6):
            angle = math.radians(i * 60)
            px = cx + (w + glow_level*2) * math.cos(angle)
            py = cy + (h + glow_level*2) * math.sin(angle)
            points.append((px, py))
        
        draw.polygon(points, outline=glow_color, width=width + glow_level)
    
    def draw_outline(self, draw, cx, cy, w, h, color, width):
        points = []
        for i in range(6):
            angle = math.radians(i * 60)
            px = cx + w * math.cos(angle)
            py = cy + h * math.sin(angle)
            points.append((px, py))
        
        draw.polygon(points, outline=(*color, 255), width=width)