"""
Lightning Bolt Ring Shape
Zigzag lightning bolt pattern
"""

from rings.base_ring import BaseRing


class Lightning(BaseRing):
    def get_name(self):
        return "Lightning Bolt"
    
    def get_internal_name(self):
        return "lightning"
    
    def draw_glow(self, draw, cx, cy, w, h, color, width, glow_level, beat):
        alpha = int((200 + beat * 55) * (1 - glow_level / 8))
        glow_color = (*color, alpha)
        
        # Create lightning bolt zigzag pattern
        points = [
            # Top point
            (cx, cy - h - glow_level*2),
            # Right side going down
            (cx + (w + glow_level*2) * 0.3, cy - (h + glow_level*2) * 0.5),
            (cx + (w + glow_level*2) * 0.6, cy - (h + glow_level*2) * 0.5),
            (cx + (w + glow_level*2) * 0.2, cy),
            (cx + (w + glow_level*2) * 0.5, cy),
            # Bottom point
            (cx + (w + glow_level*2) * 0.1, cy + h + glow_level*2),
            # Left side going up
            (cx - (w + glow_level*2) * 0.2, cy + (h + glow_level*2) * 0.3),
            (cx - (w + glow_level*2) * 0.5, cy + (h + glow_level*2) * 0.3),
            (cx - (w + glow_level*2) * 0.1, cy - (h + glow_level*2) * 0.2),
            (cx - (w + glow_level*2) * 0.4, cy - (h + glow_level*2) * 0.2),
        ]
        
        draw.polygon(points, outline=glow_color, width=width + glow_level)
    
    def draw_outline(self, draw, cx, cy, w, h, color, width):
        # Create lightning bolt zigzag pattern
        points = [
            # Top point
            (cx, cy - h),
            # Right side going down
            (cx + w * 0.3, cy - h * 0.5),
            (cx + w * 0.6, cy - h * 0.5),
            (cx + w * 0.2, cy),
            (cx + w * 0.5, cy),
            # Bottom point
            (cx + w * 0.1, cy + h),
            # Left side going up
            (cx - w * 0.2, cy + h * 0.3),
            (cx - w * 0.5, cy + h * 0.3),
            (cx - w * 0.1, cy - h * 0.2),
            (cx - w * 0.4, cy - h * 0.2),
        ]
        
        draw.polygon(points, outline=(*color, 255), width=width)