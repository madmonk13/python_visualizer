"""
Configuration module for music visualizer
Contains color palettes, frequency bands, and default settings
"""

# Frequency bands configuration (Hz)
FREQUENCY_BANDS = [
    {'name': 'Sub-Bass', 'min': 20, 'max': 40, 'hue_offset': 0},
    {'name': 'Bass', 'min': 40, 'max': 80, 'hue_offset': 45},
    {'name': 'Low-Bass', 'min': 80, 'max': 100, 'hue_offset': 90},
    {'name': 'Low-Mid', 'min': 100, 'max': 200, 'hue_offset': 135},
    {'name': 'Mid', 'min': 200, 'max': 400, 'hue_offset': 180},
    {'name': 'Upper-Mid', 'min': 400, 'max': 600, 'hue_offset': 225},
    {'name': 'High-Mid', 'min': 600, 'max': 800, 'hue_offset': 270},
    {'name': 'Presence', 'min': 800, 'max': 1000, 'hue_offset': 315}
]

# Color palettes
COLOR_PALETTES = {
    'rainbow': {
        'name': 'Rainbow',
        'colors': [0, 45, 90, 135, 180, 225, 270, 315],
        'saturation': 1.0,
        'brightness': 1.0
    },
    'spring': {
        'name': 'Spring',
        'colors': [80, 100, 120, 140, 280, 300, 320, 340],
        'saturation': 0.8,
        'brightness': 0.95
    },
    'summer': {
        'name': 'Summer',
        'colors': [30, 45, 60, 180, 200, 220, 240, 260],
        'saturation': 1.0,
        'brightness': 1.0
    },
    'autumn': {
        'name': 'Autumn',
        'colors': [0, 15, 30, 35, 40, 25, 20, 10],
        'saturation': 0.9,
        'brightness': 0.85
    },
    'winter': {
        'name': 'Winter',
        'colors': [180, 200, 220, 240, 260, 200, 190, 210],
        'saturation': 0.7,
        'brightness': 0.9
    },
    'ice': {
        'name': 'Ice',
        'colors': [180, 190, 200, 210, 220, 200, 195, 205],
        'saturation': 0.5,
        'brightness': 1.0
    },
    'fire': {
        'name': 'Fire',
        'colors': [0, 10, 20, 30, 40, 25, 15, 35],
        'saturation': 1.0,
        'brightness': 0.95
    },
    'water': {
        'name': 'Water',
        'colors': [160, 170, 180, 190, 150, 165, 175, 185],
        'saturation': 0.8,
        'brightness': 0.9
    },
    'earth': {
        'name': 'Earth',
        'colors': [25, 30, 35, 40, 45, 50, 55, 60],
        'saturation': 0.6,
        'brightness': 0.7
    },
    'neon': {
        'name': 'Neon',
        'colors': [330, 195, 120, 60, 300, 210, 150, 75],  # Hot pink, cyan, lime, yellow
        'saturation': 1.0,
        'brightness': 1.0
    },
    'sunset': {
        'name': 'Sunset',
        'colors': [0, 10, 20, 30, 290, 310, 330, 350],  # Reds, oranges, pinks, purples
        'saturation': 0.95,
        'brightness': 0.9
    },
    'synthwave': {
        'name': 'Synthwave',
        'colors': [280, 290, 300, 310, 320, 330, 195, 210],  # Purples, magentas, cyans
        'saturation': 1.0,
        'brightness': 0.95
    },
    'galaxy': {
        'name': 'Galaxy',
        'colors': [260, 270, 280, 290, 300, 310, 200, 220],  # Deep purples, blues, magentas
        'saturation': 0.85,
        'brightness': 0.85
    },
    'rock': {
        'name': 'Rock',
        'colors': [0, 5, 10, 15, 280, 290, 20, 25],  # Reds, oranges, deep purples
        'saturation': 0.95,
        'brightness': 0.85
    },
    'jazz': {
        'name': 'Jazz',
        'colors': [260, 270, 45, 50, 230, 240, 35, 40],  # Deep purples, golds, navy
        'saturation': 0.7,
        'brightness': 0.75
    },
    'aurora': {
        'name': 'Aurora',
        'colors': [120, 140, 160, 180, 280, 300, 200, 220],  # Greens, blues, purples, pinks
        'saturation': 0.8,
        'brightness': 0.9
    },
    'desert': {
        'name': 'Desert',
        'colors': [40, 45, 50, 30, 35, 25, 20, 55],  # Sandy yellows, burnt oranges, terracotta
        'saturation': 0.75,
        'brightness': 0.85
    }
}

# Default settings
DEFAULT_FPS = 30
DEFAULT_RESOLUTION = (1280, 720)
PHONE_VERTICAL_RESOLUTION = (1080, 1920)
PHONE_HORIZONTAL_RESOLUTION = (1920, 1080)

# Preview mode optimizations
PREVIEW_FPS_REDUCTION = 15
PREVIEW_RESOLUTION_DIVISOR = 2
PREVIEW_NPERSEG = 1024
FULL_NPERSEG = 2048

# Animation parameters
BASE_ROTATION_SPEED = 0.001
VOLUME_ROTATION_MULTIPLIER = 0.015
HUE_SHIFT_BASE = 0.5
TRAIL_FADE_FACTOR = 0.85
FADE_DURATION_SECONDS = 2.0

# Starfield parameters
STARFIELD_STARS_FULL = 200
STARFIELD_STARS_PREVIEW = 100
STARFIELD_BASE_SPEED = 0.5
STARFIELD_VOLUME_MULTIPLIER = 5.5

# Beat detection parameters
BEAT_BASS_MIN = 20
BEAT_BASS_MAX = 250
BEAT_LOW_MID_MIN = 250
BEAT_LOW_MID_MAX = 1000
BEAT_THRESHOLD_MULTIPLIER = 0.3
BEAT_DECAY_FACTOR = 0.7