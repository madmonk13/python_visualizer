"""
Offset Circle Ring Shape
Single circle offset from center - creates intersecting patterns when rotating
"""

from rings.base_ring import BaseRing


class OffsetCircle(BaseRing):
    def get_name(self):
        return "Offset Circle"
    
    def get_internal_name(self):
        return "offset_circle"
    
    def draw_glow(self, draw, cx, cy, w, h, color, width, glow_level, beat):
        alpha = int((200 + beat * 55) * (1 - glow_level / 8))
        glow_color = (*color, alpha)
        
        # Offset the circle from center
        # Each ring will be offset, creating intersecting patterns when rotating
        offset_x = w * 0.4  # Offset 40% of ring size to the right
        offset_y = 0        # No vertical offset (or you could add one)
        
        cx_offset = cx + offset_x
        cy_offset = cy + offset_y
        
        draw.ellipse(
            [cx_offset - w - glow_level*2, cy_offset - h - glow_level*2, 
             cx_offset + w + glow_level*2, cy_offset + h + glow_level*2],
            outline=glow_color, width=width + glow_level
        )
    
    def draw_outline(self, draw, cx, cy, w, h, color, width):
        # Offset the circle from center
        offset_x = w * 0.4  # Offset 40% of ring size to the right
        offset_y = 0        # No vertical offset
        
        cx_offset = cx + offset_x
        cy_offset = cy + offset_y
        
        draw.ellipse(
            [cx_offset - w, cy_offset - h, 
             cx_offset + w, cy_offset + h],
            outline=(*color, 255), width=width
        )