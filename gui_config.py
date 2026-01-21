"""
GUI Configuration
Constants and settings for the GUI application
"""

# Window settings
WINDOW_TITLE = "Music Visualizer Studio"
WINDOW_SIZE = "1200x800"
CANVAS_MIN_WIDTH = 100
CANVAS_DEFAULT_WIDTH = 700
CANVAS_DEFAULT_HEIGHT = 500

# Control panel settings
CONTROLS_CANVAS_WIDTH = 280
CONTROLS_PADDING = "5"
MAIN_PADDING = "10"

# Color palettes available in dropdown
PALETTE_OPTIONS = (
    'Aurora', 'Autumn', 'Custom', 'Desert', 'Earth',
    'Fire', 'Galaxy', 'Ice', 'Jazz', 'Neon',
    'Rainbow', 'Rock', 'Spring', 'Summer', 'Sunset',
    'Synthwave', 'Water', 'Winter'
)

# Ring shape options - dynamically loaded from rings/ directory
def get_ring_shape_options():
    """Get ring shape options dynamically from the rings package"""
    try:
        import rings
        display_names = rings.get_ring_display_names()
        return tuple([name for name, _ in display_names])
    except Exception as e:
        print(f"Warning: Could not load ring shapes dynamically: {e}")
        # Fallback to defaults
        return ('Circle', 'Square', 'Triangle')

# For backward compatibility, provide a default
RING_SHAPE_OPTIONS = get_ring_shape_options()

# Rotation options for dropdowns
WAVEFORM_ROTATION_OPTIONS = (
    'none - No Rotation',
    'cw - Clockwise',
    'ccw - Counter-Clockwise'
)

RING_ROTATION_OPTIONS = (
    'none - No Rotation',
    'cw - Clockwise',
    'ccw - Counter-Clockwise'
)

STARFIELD_ROTATION_OPTIONS = (
    'none - Outward Only',
    'cw - Clockwise Spiral',
    'ccw - Counter-Clockwise'
)

# Cover timeline animation options
COVER_TIMELINE_OPTIONS = (
    'none - Always Visible',
    'fade - Fade In/Out',
    'zoom - Zoom In/Out',
    'slide_up - Slide Up/Down',
    'slide_down - Slide Down/Up'
)

# Resolution presets
RESOLUTION_OPTIONS = (
    '1280x720 - HD',
    '1920x1080 - Full HD',
    '1080x1920 - Phone Vertical',
    '1920x1080 - Phone Horizontal'
)

# FPS options
FPS_OPTIONS = ('15', '30', '60')

# File dialog filters
AUDIO_FILETYPES = [
    ("Audio files", "*.mp3 *.wav *.m4a *.flac *.ogg"),
    ("All files", "*.*")
]

IMAGE_FILETYPES = [
    ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp"),
    ("All files", "*.*")
]

VIDEO_FILETYPES = [
    ("MP4 Video", "*.mp4"),
    ("All files", "*.*")
]

# Preview settings
PREVIEW_FPS = 15
PREVIEW_RESOLUTION_DIVISOR = 2

# Ring rotation stagger options
RING_STAGGER_OPTIONS = (
    'none - Synchronized',
    'inner_catch - Inner Catches Up',
    'outer_catch - Outer Catches Up',
    'inner_lead - Inner Leads (Oscillating)',
    'outer_lead - Outer Leads (Oscillating)'
)

# Rotation speed settings
ROTATION_SPEED_MIN = 0.5
ROTATION_SPEED_MAX = 3.0
DEFAULT_ROTATION_SPEED = 1.0

# Default values
DEFAULT_PALETTE = "Rainbow"
DEFAULT_COVER_SHAPE = "square"
DEFAULT_COVER_SIZE = 1.0
DEFAULT_WAVEFORM_ROTATION = "none"
DEFAULT_RING_ROTATION = "none"
DEFAULT_RING_SHAPE = "Circle"
DEFAULT_STARFIELD_ROTATION = "none"
DEFAULT_RESOLUTION = "1280x720"
DEFAULT_FPS = 30
DEFAULT_STATIC_COVER = False
DEFAULT_RING_INNER = True
DEFAULT_RING_MIDDLE = True
DEFAULT_RING_OUTER = True
DEFAULT_RING_SCALE = 1.0
DEFAULT_WAVEFORM_ORIENTATION = 'horizontal'
DEFAULT_COVER_TIMELINE = 'none'
DEFAULT_RING_STAGGER = 'none'

# Cover size slider
COVER_SIZE_MIN = 0.5
COVER_SIZE_MAX = 2.0

# Ring scale slider
RING_SCALE_MIN = 0.5
RING_SCALE_MAX = 2.0

# Number of rings
RING_COUNT_MIN = 0
RING_COUNT_MAX = 8
DEFAULT_RING_COUNT = 3

# Text size slider
TEXT_SIZE_MIN = 0.5
TEXT_SIZE_MAX = 2.0
DEFAULT_TEXT_SIZE = 1.0

# Text alignment options
TEXT_HORIZONTAL_ALIGN_OPTIONS = ('Left', 'Center', 'Right')
TEXT_VERTICAL_ALIGN_OPTIONS = ('Top', 'Middle', 'Bottom')
DEFAULT_TEXT_H_ALIGN = 'Center'
DEFAULT_TEXT_V_ALIGN = 'Bottom'

# UI Messages
MSG_NO_FILE_SELECTED = "No file selected"
MSG_NO_COVER_SELECTED = "No cover selected"
MSG_SELECT_AUDIO_FIRST = "Select an audio file to begin"
MSG_GENERATING_PREVIEW = "Generating preview..."
MSG_PREVIEW_UPDATED = "Preview updated - Ready to render"
MSG_RENDERING = "Rendering full video... Please wait"
MSG_STARTING_RENDER = "Starting render..."
MSG_ADDING_AUDIO = "Adding audio to video..."
MSG_RENDER_COMPLETE = "Render complete!"
MSG_RENDER_CANCELLED = "Render cancelled"
MSG_RENDER_FAILED = "Render failed"
MSG_CANCELLING = "Cancelling..."