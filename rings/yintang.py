"""
Yin-Yang Ring Shape
Classic yin-yang symbol
"""

from rings.base_ring import BaseRing


class YinYang(BaseRing):
    def get_name(self):
        return "Yin-Yang"
    
    def get_internal_name(self):
        return "yin_yang"
    
    def draw_glow(self, draw, cx, cy, w, h, color, width, glow_level, beat):
        alpha = int((200 + beat * 55) * (1 - glow_level / 8))
        glow_color = (*color, alpha)
        
        # Outer circle glow
        draw.ellipse(
            [cx - w - glow_level*2, cy - h - glow_level*2, 
             cx + w + glow_level*2, cy + h + glow_level*2],
            outline=glow_color, width=width + glow_level
        )
        
        # S-curve dividing line (using two semicircles)
        # Top semicircle (upper half)
        top_radius = h // 2
        draw.arc(
            [cx - top_radius - glow_level, cy - h - glow_level,
             cx + top_radius + glow_level, cy + glow_level],
            start=90, end=270,
            fill=glow_color, width=width + glow_level
        )
        
        # Bottom semicircle (lower half)
        draw.arc(
            [cx - top_radius - glow_level, cy - glow_level,
             cx + top_radius + glow_level, cy + h + glow_level],
            start=270, end=90,
            fill=glow_color, width=width + glow_level
        )
        
        # Small dot in upper half (yin dot)
        dot_radius = w // 8
        draw.ellipse(
            [cx - dot_radius - glow_level, cy - h//2 - dot_radius - glow_level,
             cx + dot_radius + glow_level, cy - h//2 + dot_radius + glow_level],
            outline=glow_color, width=width + glow_level
        )
        
        # Small dot in lower half (yang dot)
        draw.ellipse(
            [cx - dot_radius - glow_level, cy + h//2 - dot_radius - glow_level,
             cx + dot_radius + glow_level, cy + h//2 + dot_radius + glow_level],
            outline=glow_color, width=width + glow_level
        )
    
    def draw_outline(self, draw, cx, cy, w, h, color, width):
        # Outer circle
        draw.ellipse(
            [cx - w, cy - h, cx + w, cy + h],
            outline=(*color, 255), width=width
        )
        
        # S-curve dividing line (using two semicircles)
        # Top semicircle - curves from left to right in upper half
        top_radius = h // 2
        draw.arc(
            [cx - top_radius, cy - h,
             cx + top_radius, cy],
            start=90, end=270,
            fill=(*color, 255), width=width
        )
        
        # Bottom semicircle - curves from right to left in lower half
        draw.arc(
            [cx - top_radius, cy,
             cx + top_radius, cy + h],
            start=270, end=90,
            fill=(*color, 255), width=width
        )
        
        # Small dot in upper half (yin dot - on the light side)
        dot_radius = w // 8
        draw.ellipse(
            [cx - dot_radius, cy - h//2 - dot_radius,
             cx + dot_radius, cy - h//2 + dot_radius],
            outline=(*color, 255), width=width
        )
        
        # Small dot in lower half (yang dot - on the dark side)
        draw.ellipse(
            [cx - dot_radius, cy + h//2 - dot_radius,
             cx + dot_radius, cy + h//2 + dot_radius],
            outline=(*color, 255), width=width
        )