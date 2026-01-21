"""
Gear Ring Shape
Gear-shaped ring with teeth
"""

import math
from rings.base_ring import BaseRing


class Gear(BaseRing):
    def get_name(self):
        return "Gear"
    
    def get_internal_name(self):
        return "gear"
    
    def draw_glow(self, draw, cx, cy, w, h, color, width, glow_level, beat):
        alpha = int((200 + beat * 55) * (1 - glow_level / 8))
        glow_color = (*color, alpha)
        
        points = []
        num_teeth = 16
        for i in range(num_teeth * 2):
            angle = math.radians(i * (360 / (num_teeth * 2)))
            if i % 2 == 0:
                # Outer tooth
                px = cx + (w + glow_level*2) * math.cos(angle)
                py = cy + (h + glow_level*2) * math.sin(angle)
            else:
                # Inner valley
                px = cx + (w + glow_level*2) * 0.85 * math.cos(angle)
                py = cy + (h + glow_level*2) * 0.85 * math.sin(angle)
            points.append((px, py))
        
        draw.polygon(points, outline=glow_color, width=width + glow_level)
    
    def draw_outline(self, draw, cx, cy, w, h, color, width):
        points = []
        num_teeth = 16
        for i in range(num_teeth * 2):
            angle = math.radians(i * (360 / (num_teeth * 2)))
            if i % 2 == 0:
                # Outer tooth
                px = cx + w * math.cos(angle)
                py = cy + h * math.sin(angle)
            else:
                # Inner valley
                px = cx + w * 0.85 * math.cos(angle)
                py = cy + h * 0.85 * math.sin(angle)
            points.append((px, py))
        
        draw.polygon(points, outline=(*color, 255), width=width)