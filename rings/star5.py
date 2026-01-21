"""
5-Point Star Ring Shape
Classic five-pointed star ring
"""

import math
from rings.base_ring import BaseRing


class Star5(BaseRing):
    def get_name(self):
        return "5-Point Star"
    
    def get_internal_name(self):
        return "star"
    
    def draw_glow(self, draw, cx, cy, w, h, color, width, glow_level, beat):
        alpha = int((200 + beat * 55) * (1 - glow_level / 8))
        glow_color = (*color, alpha)
        
        points = []
        for i in range(10):
            angle = math.radians(i * 36 - 90)
            if i % 2 == 0:
                px = cx + (w + glow_level*2) * math.cos(angle)
                py = cy + (h + glow_level*2) * math.sin(angle)
            else:
                px = cx + (w + glow_level*2) * 0.4 * math.cos(angle)
                py = cy + (h + glow_level*2) * 0.4 * math.sin(angle)
            points.append((px, py))
        
        draw.polygon(points, outline=glow_color, width=width + glow_level)
    
    def draw_outline(self, draw, cx, cy, w, h, color, width):
        points = []
        for i in range(10):
            angle = math.radians(i * 36 - 90)
            if i % 2 == 0:
                px = cx + w * math.cos(angle)
                py = cy + h * math.sin(angle)
            else:
                px = cx + w * 0.4 * math.cos(angle)
                py = cy + h * 0.4 * math.sin(angle)
            points.append((px, py))
        
        draw.polygon(points, outline=(*color, 255), width=width)