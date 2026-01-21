"""
Outlined Eye with Pupil
Almond-shaped eye outline with circular outlined pupil
"""

import math
from rings.base_ring import BaseRing


class EyeOutline(BaseRing):
    def get_name(self):
        return "Eye"

    def get_internal_name(self):
        return "eye_outline"

    def draw_glow(self, draw, cx, cy, w, h, color, width, glow_level, beat):
        alpha = int((180 + beat * 50) * (1 - glow_level / 8))
        glow_color = (*color, alpha)

        self._draw_eye(
            draw,
            cx,
            cy,
            w,
            h,
            glow_color,
            width + glow_level
        )

    def draw_outline(self, draw, cx, cy, w, h, color, width):
        self._draw_eye(
            draw,
            cx,
            cy,
            w,
            h,
            (*color, 255),
            width
        )

    def _draw_eye(self, draw, cx, cy, w, h, color, width):
        radius_x = min(w, h) * 1.2
        radius_y = min(w, h) * 0.6

        steps = 60
        points = []

        # Upper eyelid
        for i in range(steps + 1):
            t = i / steps
            angle = math.pi * t
            x = cx + math.cos(angle) * radius_x
            y = cy - math.sin(angle) * radius_y
            points.append((x, y))

        # Lower eyelid
        for i in range(steps + 1):
            t = i / steps
            angle = math.pi * (1 - t)
            x = cx + math.cos(angle) * radius_x
            y = cy + math.sin(angle) * radius_y
            points.append((x, y))

        # Close outline
        points.append(points[0])

        # Eye outline
        draw.line(
            points,
            fill=color,
            width=width,
            joint="curve"
        )

        # Pupil (outline only)
        pupil_r = min(w, h) * 0.25
        draw.ellipse(
            [
                cx - pupil_r,
                cy - pupil_r,
                cx + pupil_r,
                cy + pupil_r
            ],
            outline=color,
            width=width
        )
