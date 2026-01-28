"""
Eighth Note Ring Shape
Musical eighth note with curved flag
"""

from rings.base_ring import BaseRing


class EighthNote(BaseRing):
    def get_name(self):
        return "Eighth Note"
    
    def get_internal_name(self):
        return "eighth_note"
    
    def draw_glow(self, draw, cx, cy, w, h, color, width, glow_level, beat):
        alpha = int((200 + beat * 55) * (1 - glow_level / 8))
        glow_color = (*color, alpha)
        
        # Note head (ellipse at bottom)
        head_w = w // 3
        head_h = h // 4
        head_x = cx - w // 4
        head_y = cy + h // 2
        draw.ellipse(
            [head_x - head_w - glow_level, head_y - head_h - glow_level,
             head_x + head_w + glow_level, head_y + head_h + glow_level],
            outline=glow_color, width=width + glow_level
        )
        
        # Stem (vertical line)
        stem_x = head_x + head_w
        stem_bottom = head_y - head_h // 2
        stem_top = cy - h // 2
        draw.line(
            [(stem_x - glow_level, stem_bottom), (stem_x - glow_level, stem_top)],
            fill=glow_color, width=width + glow_level
        )
        
        # Curved flag (bezier-like curve using arc and line)
        flag_start_x = stem_x
        flag_start_y = stem_top
        flag_end_x = stem_x + w // 2
        flag_end_y = stem_top + h // 3
        
        # Draw flag as a curved arc
        draw.arc(
            [flag_start_x - glow_level, flag_start_y - glow_level,
             flag_end_x + glow_level, flag_end_y + glow_level],
            start=270, end=360,
            fill=glow_color, width=width + glow_level
        )
    
    def draw_outline(self, draw, cx, cy, w, h, color, width):
        # Note head (filled ellipse at bottom, tilted)
        head_w = w // 3
        head_h = h // 4
        head_x = cx - w // 4
        head_y = cy + h // 2
        draw.ellipse(
            [head_x - head_w, head_y - head_h,
             head_x + head_w, head_y + head_h],
            outline=(*color, 255), width=width
        )
        
        # Stem (vertical line from top-right of note head)
        stem_x = head_x + head_w
        stem_bottom = head_y - head_h // 2
        stem_top = cy - h // 2
        draw.line(
            [(stem_x, stem_bottom), (stem_x, stem_top)],
            fill=(*color, 255), width=width
        )
        
        # Curved flag
        flag_start_x = stem_x
        flag_start_y = stem_top
        flag_end_x = stem_x + w // 2
        flag_end_y = stem_top + h // 3
        
        # Draw flag as a curved arc
        draw.arc(
            [flag_start_x, flag_start_y,
             flag_end_x, flag_end_y],
            start=270, end=360,
            fill=(*color, 255), width=width
        )