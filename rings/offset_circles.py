"""
Offset Circles Ring Shape
Multiple circles offset from center creating intersecting patterns
"""

from rings.base_ring import BaseRing


class OffsetCircles(BaseRing):
    def get_name(self):
        return "Offset Circles"
    
    def get_internal_name(self):
        return "offset_circles"
    
    def draw_glow(self, draw, cx, cy, w, h, color, width, glow_level, beat):
        alpha = int((200 + beat * 55) * (1 - glow_level / 8))
        glow_color = (*color, alpha)
        
        # Draw 3 overlapping circles, each offset from center
        offset_amount = w * 0.3  # How far from center
        
        # Circle 1 - offset right
        cx1 = cx + offset_amount
        cy1 = cy
        draw.ellipse(
            [cx1 - w - glow_level*2, cy1 - h - glow_level*2, 
             cx1 + w + glow_level*2, cy1 + h + glow_level*2],
            outline=glow_color, width=width + glow_level
        )
        
        # Circle 2 - offset bottom-left
        cx2 = cx - offset_amount * 0.5
        cy2 = cy + offset_amount * 0.866  # sqrt(3)/2 for 60° angle
        draw.ellipse(
            [cx2 - w - glow_level*2, cy2 - h - glow_level*2, 
             cx2 + w + glow_level*2, cy2 + h + glow_level*2],
            outline=glow_color, width=width + glow_level
        )
        
        # Circle 3 - offset top-left
        cx3 = cx - offset_amount * 0.5
        cy3 = cy - offset_amount * 0.866
        draw.ellipse(
            [cx3 - w - glow_level*2, cy3 - h - glow_level*2, 
             cx3 + w + glow_level*2, cy3 + h + glow_level*2],
            outline=glow_color, width=width + glow_level
        )
    
    def draw_outline(self, draw, cx, cy, w, h, color, width):
        # Draw 3 overlapping circles, each offset from center
        offset_amount = w * 0.3  # How far from center
        
        # Circle 1 - offset right
        cx1 = cx + offset_amount
        cy1 = cy
        draw.ellipse(
            [cx1 - w, cy1 - h, cx1 + w, cy1 + h],
            outline=(*color, 255), width=width
        )
        
        # Circle 2 - offset bottom-left
        cx2 = cx - offset_amount * 0.5
        cy2 = cy + offset_amount * 0.866  # sqrt(3)/2 for 60° angle
        draw.ellipse(
            [cx2 - w, cy2 - h, cx2 + w, cy2 + h],
            outline=(*color, 255), width=width
        )
        
        # Circle 3 - offset top-left
        cx3 = cx - offset_amount * 0.5
        cy3 = cy - offset_amount * 0.866
        draw.ellipse(
            [cx3 - w, cy3 - h, cx3 + w, cy3 + h],
            outline=(*color, 255), width=width
        )