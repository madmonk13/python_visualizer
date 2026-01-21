"""
Outlined Plus Sign
A closed, outlined plus shape (not crossing lines)
"""

from rings.base_ring import BaseRing


class PlusOutline(BaseRing):
    def get_name(self):
        return "Plus Sign"

    def get_internal_name(self):
        return "plus_outline"

    def draw_glow(self, draw, cx, cy, w, h, color, width, glow_level, beat):
        alpha = int((180 + beat * 50) * (1 - glow_level / 8))
        glow_color = (*color, alpha)

        self._draw_plus(
            draw,
            cx,
            cy,
            w,
            h,
            glow_color,
            width + glow_level
        )

    def draw_outline(self, draw, cx, cy, w, h, color, width):
        self._draw_plus(
            draw,
            cx,
            cy,
            w,
            h,
            (*color, 255),
            width
        )

    def _draw_plus(self, draw, cx, cy, w, h, color, width):
        size = min(w, h)
        arm = size * 0.55
        half_thickness = size * 0.12

        # Define outline points clockwise
        points = [
            (cx - half_thickness, cy - arm),
            (cx + half_thickness, cy - arm),
            (cx + half_thickness, cy - half_thickness),
            (cx + arm,           cy - half_thickness),
            (cx + arm,           cy + half_thickness),
            (cx + half_thickness, cy + half_thickness),
            (cx + half_thickness, cy + arm),
            (cx - half_thickness, cy + arm),
            (cx - half_thickness, cy + half_thickness),
            (cx - arm,           cy + half_thickness),
            (cx - arm,           cy - half_thickness),
            (cx - half_thickness, cy - half_thickness),
            (cx - half_thickness, cy - arm),
        ]

        draw.line(
            points,
            fill=color,
            width=width,
            joint="curve"
        )
