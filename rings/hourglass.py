"""
Outlined Hourglass Shape
Symmetric hourglass with narrow waist (outline only)
"""

from rings.base_ring import BaseRing


class HourglassOutline(BaseRing):
    def get_name(self):
        return "Hourglass"

    def get_internal_name(self):
        return "hourglass_outline"

    def draw_glow(self, draw, cx, cy, w, h, color, width, glow_level, beat):
        alpha = int((180 + beat * 50) * (1 - glow_level / 8))
        glow_color = (*color, alpha)

        self._draw_hourglass(
            draw,
            cx,
            cy,
            w,
            h,
            glow_color,
            width + glow_level
        )

    def draw_outline(self, draw, cx, cy, w, h, color, width):
        self._draw_hourglass(
            draw,
            cx,
            cy,
            w,
            h,
            (*color, 255),
            width
        )

    def _draw_hourglass(self, draw, cx, cy, w, h, color, width):
        size = min(w, h)

        top = size * 1.0
        bottom = size * 1.0
        waist = size * 0.15
        side = size * 0.6

        points = [
            (cx - side,  cy - top),      # top left
            (cx + side,  cy - top),      # top right
            (cx + waist, cy),            # right waist
            (cx + side,  cy + bottom),   # bottom right
            (cx - side,  cy + bottom),   # bottom left
            (cx - waist, cy),            # left waist
            (cx - side,  cy - top)       # close
        ]

        draw.line(
            points,
            fill=color,
            width=width,
            joint="curve"
        )
