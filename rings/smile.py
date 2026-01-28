"""
Smiley Face Ring Shape
A cheerful smiley face with eyes and mouth
"""

from rings.base_ring import BaseRing


class SmileyFace(BaseRing):
    def get_name(self):
        return "Smiley Face"
    
    def get_internal_name(self):
        return "smiley_face"
    
    def draw_glow(self, draw, cx, cy, w, h, color, width, glow_level, beat):
        alpha = int((200 + beat * 55) * (1 - glow_level / 8))
        glow_color = (*color, alpha)
        
        # Face outline glow
        draw.ellipse(
            [cx - w - glow_level*2, cy - h - glow_level*2, 
             cx + w + glow_level*2, cy + h + glow_level*2],
            outline=glow_color, width=width + glow_level
        )
        
        # Left eye glow
        eye_radius = w // 6
        left_eye_x = cx - w // 3
        eye_y = cy - h // 4
        draw.ellipse(
            [left_eye_x - eye_radius - glow_level, eye_y - eye_radius - glow_level,
             left_eye_x + eye_radius + glow_level, eye_y + eye_radius + glow_level],
            outline=glow_color, width=width + glow_level
        )
        
        # Right eye glow
        right_eye_x = cx + w // 3
        draw.ellipse(
            [right_eye_x - eye_radius - glow_level, eye_y - eye_radius - glow_level,
             right_eye_x + eye_radius + glow_level, eye_y + eye_radius + glow_level],
            outline=glow_color, width=width + glow_level
        )
        
        # Mouth arc glow
        mouth_w = w // 2
        mouth_h = h // 3
        mouth_y = cy + h // 6
        draw.arc(
            [cx - mouth_w - glow_level, mouth_y - mouth_h - glow_level,
             cx + mouth_w + glow_level, mouth_y + mouth_h + glow_level],
            start=0, end=180,
            fill=glow_color, width=width + glow_level
        )
    
    def draw_outline(self, draw, cx, cy, w, h, color, width):
        # Face outline
        draw.ellipse(
            [cx - w, cy - h, cx + w, cy + h],
            outline=(*color, 255), width=width
        )
        
        # Left eye
        eye_radius = w // 6
        left_eye_x = cx - w // 3
        eye_y = cy - h // 4
        draw.ellipse(
            [left_eye_x - eye_radius, eye_y - eye_radius,
             left_eye_x + eye_radius, eye_y + eye_radius],
            outline=(*color, 255), width=width
        )
        
        # Right eye
        right_eye_x = cx + w // 3
        draw.ellipse(
            [right_eye_x - eye_radius, eye_y - eye_radius,
             right_eye_x + eye_radius, eye_y + eye_radius],
            outline=(*color, 255), width=width
        )
        
        # Mouth (smiling arc)
        mouth_w = w // 2
        mouth_h = h // 3
        mouth_y = cy + h // 6
        draw.arc(
            [cx - mouth_w, mouth_y - mouth_h,
             cx + mouth_w, mouth_y + mouth_h],
            start=0, end=180,
            fill=(*color, 255), width=width
        )