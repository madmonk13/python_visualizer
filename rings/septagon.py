"""
Outlined Septagon
7-sided regular polygon (outline only)
"""

import math
from rings.base_ring import BaseRing


class SeptagonOutline(BaseRing):
    def get_name(self):
        return "Septagon"

    def get_internal_name(self):
        return "septagon_outline"

    def draw_glow(self, draw, cx, cy, w, h, color, width, glow_level, beat):
        alpha = int((180 + beat * 50) * (1 - glow_level / 8))
        glow_color = (*color, alpha)

        self._draw_septagon(
            draw,
            cx,
            cy,
            w,
            h,
            glow_color,
            width + glow_level
        )

    def draw_outline(self, draw, cx, cy, w, h, color, width):
        self._draw_septagon(
            draw,
            cx,
            cy,
            w,
            h,
            (*color, 255),
            width
        )

    def _draw_septagon(self, draw, cx, cy, w, h, color, width):
        sides = 7
        radius = min(w, h)

        points = []

        # Rotate so a flat edge sits near the top
        rotation = -math.pi / 2

        for i in range(sides):
            angle = rotation + (2 * math.pi * i / sides)
            x = cx + math.cos(angle) * radius
            y = cy + math.sin(angle) * radius
            points.append((x, y))

        # Close shape
        points.append(points[0])

        draw.line(
            points,
            fill=color,
            width=width,
            joint="curve"
        )
