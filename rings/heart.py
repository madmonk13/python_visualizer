"""
Heart Ring Shape
Classic heart shape
"""

from rings.base_ring import BaseRing
import math


class Heart(BaseRing):
    def get_name(self):
        return "Heart"
    
    def get_internal_name(self):
        return "heart"
    
    def _get_heart_points(self, cx, cy, w, h, num_points=100):
        """Generate points for a heart shape"""
        points = []
        for i in range(num_points + 1):
            t = (i / num_points) * 2 * math.pi
            # Parametric heart equation
            x = 16 * math.sin(t) ** 3
            y = -(13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
            
            # Scale and translate to position
            scaled_x = cx + (x * w / 16)
            scaled_y = cy + (y * h / 17)
            points.append((scaled_x, scaled_y))
        
        return points
    
    def draw_glow(self, draw, cx, cy, w, h, color, width, glow_level, beat):
        alpha = int((200 + beat * 55) * (1 - glow_level / 8))
        glow_color = (*color, alpha)
        
        # Get heart points with expanded size for glow
        glow_w = w + glow_level * 2
        glow_h = h + glow_level * 2
        points = self._get_heart_points(cx, cy, glow_w, glow_h)
        
        draw.line(points, fill=glow_color, width=width + glow_level, joint="curve")
    
    def draw_outline(self, draw, cx, cy, w, h, color, width):
        # Get heart points
        points = self._get_heart_points(cx, cy, w, h)
        
        draw.line(points, fill=(*color, 255), width=width, joint="curve")