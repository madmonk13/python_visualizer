"""
Peace Sign Ring Shape
Classic peace symbol
"""

from rings.base_ring import BaseRing
import math


class PeaceSign(BaseRing):
    def get_name(self):
        return "Peace Sign"
    
    def get_internal_name(self):
        return "peace_sign"
    
    def draw_glow(self, draw, cx, cy, w, h, color, width, glow_level, beat):
        alpha = int((200 + beat * 55) * (1 - glow_level / 8))
        glow_color = (*color, alpha)
        
        # Outer circle glow
        draw.ellipse(
            [cx - w - glow_level*2, cy - h - glow_level*2, 
             cx + w + glow_level*2, cy + h + glow_level*2],
            outline=glow_color, width=width + glow_level
        )
        
        # Center vertical line (from center to bottom)
        draw.line(
            [(cx, cy), (cx, cy + h + glow_level)],
            fill=glow_color, width=width + glow_level
        )
        
        # Left diagonal line (from center to bottom-left)
        # 45 degrees down and to the left
        angle_left = math.radians(225)  # 225 degrees (down-left)
        end_x_left = cx + w * math.cos(angle_left)
        end_y_left = cy + h * math.sin(angle_left)
        draw.line(
            [(cx, cy), (end_x_left - glow_level, end_y_left + glow_level)],
            fill=glow_color, width=width + glow_level
        )
        
        # Right diagonal line (from center to bottom-right)
        # 45 degrees down and to the right
        angle_right = math.radians(315)  # 315 degrees (down-right)
        end_x_right = cx + w * math.cos(angle_right)
        end_y_right = cy + h * math.sin(angle_right)
        draw.line(
            [(cx, cy), (end_x_right + glow_level, end_y_right + glow_level)],
            fill=glow_color, width=width + glow_level
        )
    
    def draw_outline(self, draw, cx, cy, w, h, color, width):
        # Outer circle
        draw.ellipse(
            [cx - w, cy - h, cx + w, cy + h],
            outline=(*color, 255), width=width
        )
        
        # Center vertical line (from center to bottom of circle)
        draw.line(
            [(cx, cy), (cx, cy + h)],
            fill=(*color, 255), width=width
        )
        
        # Left diagonal line (from center to bottom-left edge of circle)
        angle_left = math.radians(225)  # 225 degrees
        end_x_left = cx + w * math.cos(angle_left)
        end_y_left = cy + h * math.sin(angle_left)
        draw.line(
            [(cx, cy), (end_x_left, end_y_left)],
            fill=(*color, 255), width=width
        )
        
        # Right diagonal line (from center to bottom-right edge of circle)
        angle_right = math.radians(315)  # 315 degrees
        end_x_right = cx + w * math.cos(angle_right)
        end_y_right = cy + h * math.sin(angle_right)
        draw.line(
            [(cx, cy), (end_x_right, end_y_right)],
            fill=(*color, 255), width=width
        )