"""
Triangle Ring Shape
Three-pointed triangular ring
"""

from rings.base_ring import BaseRing


class Triangle(BaseRing):
    def get_name(self):
        return "Triangle"
    
    def get_internal_name(self):
        return "triangle"
    
    def draw_glow(self, draw, cx, cy, w, h, color, width, glow_level, beat):
        alpha = int((200 + beat * 55) * (1 - glow_level / 8))
        glow_color = (*color, alpha)
        
        points = [
            (cx, cy - h - glow_level*2),
            (cx - w - glow_level*2, cy + h + glow_level*2),
            (cx + w + glow_level*2, cy + h + glow_level*2)
        ]
        draw.polygon(points, outline=glow_color, width=width + glow_level)
    
    def draw_outline(self, draw, cx, cy, w, h, color, width):
        points = [
            (cx, cy - h),
            (cx - w, cy + h),
            (cx + w, cy + h)
        ]
        draw.polygon(points, outline=(*color, 255), width=width)