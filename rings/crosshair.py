"""
Crosshair Outline
Ring with centered axis marks (outline only)
"""

from rings.base_ring import BaseRing


class CrosshairOutline(BaseRing):
    def get_name(self):
        return "Crosshair"

    def get_internal_name(self):
        return "crosshair_outline"

    def draw_glow(self, draw, cx, cy, w, h, color, width, glow_level, beat):
        alpha = int((180 + beat * 50) * (1 - glow_level / 8))
        glow_color = (*color, alpha)

        self._draw_crosshair(
            draw,
            cx,
            cy,
            w,
            h,
            glow_color,
            width + glow_level
        )

    def draw_outline(self, draw, cx, cy, w, h, color, width):
        self._draw_crosshair(
            draw,
            cx,
            cy,
            w,
            h,
            (*color, 255),
            width
        )

    def _draw_crosshair(self, draw, cx, cy, w, h, color, width):
        radius = min(w, h)
        gap = radius * 0.25
        arm = radius * 0.9

        # Outer ring
        draw.ellipse(
            [
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius
            ],
            outline=color,
            width=width
        )

        # Vertical axis (top)
        draw.line(
            [cx, cy - arm, cx, cy - gap],
            fill=color,
            width=width
        )

        # Vertical axis (bottom)
        draw.line(
            [cx, cy + gap, cx, cy + arm],
            fill=color,
            width=width
        )

        # Horizontal axis (left)
        draw.line(
            [cx - arm, cy, cx - gap, cy],
            fill=color,
            width=width
        )

        # Horizontal axis (right)
        draw.line(
            [cx + gap, cy, cx + arm, cy],
            fill=color,
            width=width
        )
