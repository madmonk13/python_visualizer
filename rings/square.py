"""
Square Ring Shape
Four-sided rectangular ring
"""

from rings.base_ring import BaseRing


class Square(BaseRing):
    def get_name(self):
        return "Square"
    
    def get_internal_name(self):
        return "square"
    
    def draw_glow(self, draw, cx, cy, w, h, color, width, glow_level, beat):
        alpha = int((200 + beat * 55) * (1 - glow_level / 8))
        glow_color = (*color, alpha)
        
        draw.rectangle(
            [cx - w - glow_level*2, cy - h - glow_level*2, 
             cx + w + glow_level*2, cy + h + glow_level*2],
            outline=glow_color, width=width + glow_level
        )
    
    def draw_outline(self, draw, cx, cy, w, h, color, width):
        draw.rectangle(
            [cx - w, cy - h, cx + w, cy + h],
            outline=(*color, 255), width=width
        )