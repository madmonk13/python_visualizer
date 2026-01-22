"""
Outlined Kite Shape
Symmetric kite (quadrilateral with unequal diagonals)
"""

from rings.base_ring import BaseRing


class KiteOutline(BaseRing):
    def get_name(self):
        return "Kite"

    def get_internal_name(self):
        return "kite_outline"

    def draw_glow(self, draw, cx, cy, w, h, color, width, glow_level, beat):
        alpha = int((180 + beat * 50) * (1 - glow_level / 8))
        glow_color = (*color, alpha)

        self._draw_kite(
            draw,
            cx,
            cy,
            w,
            h,
            glow_color,
            width + glow_level
        )

    def draw_outline(self, draw, cx, cy, w, h, color, width):
        self._draw_kite(
            draw,
            cx,
            cy,
            w,
            h,
            (*color, 255),
            width
        )

    def _draw_kite(self, draw, cx, cy, w, h, color, width):
        size = min(w, h)

        top = size * 1.0
        bottom = size * 0.7
        side = size * 0.55

        points = [
            (cx,           cy - top),     # top
            (cx + side,    cy),           # right
            (cx,           cy + bottom),  # bottom
            (cx - side,    cy),           # left
            (cx,           cy - top)      # close
        ]

        draw.line(
            points,
            fill=color,
            width=width,
            joint="curve"
        )
