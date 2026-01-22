"""
Circle Segment Shapes
Quarter, Half, and Three-Quarter Circle outlines
"""

from rings.base_ring import BaseRing


class QuarterCircle(BaseRing):
    def get_name(self):
        return "Quarter Circle"

    def get_internal_name(self):
        return "quarter_circle"

    def draw_glow(self, draw, cx, cy, w, h, color, width, glow_level, beat):
        alpha = int((180 + beat * 50) * (1 - glow_level / 8))
        draw.arc(
            [cx - min(w, h), cy - min(w, h), cx + min(w, h), cy + min(w, h)],
            start=270,
            end=360,
            fill=(*color, alpha),
            width=width + glow_level
        )

    def draw_outline(self, draw, cx, cy, w, h, color, width):
        r = min(w, h)
        draw.arc(
            [cx - r, cy - r, cx + r, cy + r],
            start=270,
            end=360,
            fill=(*color, 255),
            width=width
        )


class HalfCircle(BaseRing):
    def get_name(self):
        return "Half Circle"

    def get_internal_name(self):
        return "half_circle"

    def draw_glow(self, draw, cx, cy, w, h, color, width, glow_level, beat):
        alpha = int((180 + beat * 50) * (1 - glow_level / 8))
        draw.arc(
            [cx - min(w, h), cy - min(w, h), cx + min(w, h), cy + min(w, h)],
            start=180,
            end=360,
            fill=(*color, alpha),
            width=width + glow_level
        )

    def draw_outline(self, draw, cx, cy, w, h, color, width):
        r = min(w, h)
        draw.arc(
            [cx - r, cy - r, cx + r, cy + r],
            start=180,
            end=360,
            fill=(*color, 255),
            width=width
        )


class ThreeQuarterCircle(BaseRing):
    def get_name(self):
        return "Three Quarter Circle"

    def get_internal_name(self):
        return "three_quarter_circle"

    def draw_glow(self, draw, cx, cy, w, h, color, width, glow_level, beat):
        alpha = int((180 + beat * 50) * (1 - glow_level / 8))
        draw.arc(
            [cx - min(w, h), cy - min(w, h), cx + min(w, h), cy + min(w, h)],
            start=90,
            end=360,
            fill=(*color, alpha),
            width=width + glow_level
        )

    def draw_outline(self, draw, cx, cy, w, h, color, width):
        r = min(w, h)
        draw.arc(
            [cx - r, cy - r, cx + r, cy + r],
            start=90,
            end=360,
            fill=(*color, 255),
            width=width
        )
