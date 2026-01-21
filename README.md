# Music Visualizer Studio

A powerful Python-based tool for creating stunning, psychedelic music visualizations with audio-reactive effects. Features both a GUI application and command-line interface for maximum flexibility.

![Music Visualizer Demo](demo.png)

## Features

### Visual Effects
- **Frequency Band Waveforms**: 8 distinct frequency bands (Sub-Bass to Presence) with individual colors
- **Starfield Background**: Particle-based starfield with optional rotation
- **Reactive Rings**: Up to 3 customizable rings (inner/middle/outer) that react to music
- **Cover Art Support**: Display album artwork with square or round masking
- **Text Overlays**: Two-line text display with music-reactive fading
- **Trail/Afterimage Effects**: Motion blur for smooth, psychedelic motion
- **Beat Detection**: Automatic beat detection for enhanced visual reactions

### Customization Options

#### Color Schemes
- **9 Built-in Palettes**: Rainbow, Spring, Summer, Autumn, Winter, Ice, Fire, Water, Earth
- **Custom Colors**: Full color picker support for each of the 8 frequency bands
- Colors apply to both waveforms and rings

#### Rotation Effects
- **Waveform Rotation**: None, Clockwise, or Counter-Clockwise
- **Ring Rotation**: Independent rotation control with stagger patterns
- **Starfield Rotation**: Spiral or outward-only motion
- **Ring Stagger Modes**: 
  - Synchronized (default)
  - Inner/Outer Catches Up
  - Inner/Outer Leads (oscillating)

#### Ring Shapes
- Circle
- Square
- Triangle
- Pentagon
- Hexagon
- Octagon
- 5 Point Star
- 4 Point Star
- 6 Point Star

#### Timeline Animations
Apply entrance/exit animations to cover art and text:
- **Fade**: Smooth fade in/out
- **Zoom**: Scale and fade
- **Slide Up**: Slide from bottom
- **Slide Down**: Slide from top
- **None**: Always visible (default)

#### Waveform Options
- **Orientation**: Horizontal (rows) or Vertical (columns)
- **Glow Effects**: Multi-layer glow with gaussian blur
- **Particle Effects**: Dynamic particles on audio peaks

#### Cover Art Options
- **Shapes**: Square or Round masking
- **Size**: Adjustable from 0.5x to 2.0x
- **Static Mode**: Disable music reaction for cover
- **Timeline Animations**: Fade, zoom, or slide effects

#### Ring Options
- **Individual Control**: Toggle inner, middle, and outer rings independently
- **Scale**: Adjustable from 0.5x to 2.0x
- **Color Integration**: Rings use palette colors (Bass, Mid, Presence bands)

### Output Options
- **Resolutions**: 
  - 1280x720 (HD)
  - 1920x1080 (Full HD)
  - 1080x1920 (Phone Vertical)
  - 1920x1080 (Phone Horizontal)
  - Custom resolutions via command line
- **Frame Rates**: 15, 30, or 60 FPS
- **Quick Preview**: 30-second preview render for fast iteration
- **Full Render**: Complete video with audio

## Installation

### Requirements
- Python 3.8+
- FFmpeg (for audio processing)

### Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html)

### Install Python Dependencies

```bash
pip install numpy scipy opencv-python Pillow tqdm
```

For GUI support:
```bash
# tkinter is usually included with Python, but if needed:
# macOS: Already included
# Ubuntu/Debian: sudo apt-get install python3-tk
# Windows: Already included
```

## Usage

### GUI Application (Recommended)

Launch the graphical interface:

```bash
python visualizer_gui.py
```

#### GUI Workflow:
1. **Select Audio File**: Choose your music file (MP3, WAV, M4A, FLAC, OGG)
2. **Optional - Select Cover Image**: Add album artwork (JPG, PNG, GIF, BMP)
3. **Customize Settings**:
   - Choose color palette or create custom colors
   - Adjust rotation effects
   - Configure rings (shape, scale, positions)
   - Set cover options (shape, size, timeline)
   - Add text overlays
   - Select output resolution and frame rate
4. **Update Preview**: Click to see a preview frame with current settings
5. **Render**:
   - **Render 30s Preview Video**: Quick 30-second test (10-15x faster)
   - **Render Full Video**: Complete video render

### Command Line Interface

For automation or advanced usage:

#### Basic Usage
```bash
python main.py song.mp3
```

#### With Cover and Text
```bash
python main.py song.mp3 -c cover.jpg -t "Song Title" -t2 "Artist Name"
```

#### Custom Palette and Settings
```bash
python main.py song.mp3 -c cover.jpg -p fire --fps 60 --waveform-rotation cw
```

#### Quick 30-Second Preview
```bash
python main.py song.mp3 --preview 30 -c cover.jpg -t "Test"
```

#### Full Command Line Options

```
Audio and Output:
  audio                     Path to audio file
  -o, --output             Output video path (default: visualization.mp4)
  -c, --cover              Path to cover image
  -t, --text               Text overlay line 1
  -t2, --text2             Text overlay line 2

Visual Settings:
  -p, --palette            Color palette: rainbow, spring, summer, autumn,
                          winter, ice, fire, water, earth (default: rainbow)
  --waveform-rotation      none, cw, ccw (default: none)
  --waveform-orientation   horizontal, vertical (default: horizontal)
  --ring-rotation          none, cw, ccw (default: none)
  --ring-shape             circle, square, triangle, pentagon, hexagon,
                          octagon, 5 point star, 4 point star, 6 point star
  --ring-stagger          none, inner_catch, outer_catch, inner_lead,
                          outer_lead (default: none)
  --starfield-rotation     none, cw, ccw (default: none)

Cover Options:
  --cover-shape            square, round (default: square)
  --cover-size             Size multiplier 0.5-2.0 (default: 1.0)
  --cover-timeline         none, fade, zoom, slide_up, slide_down
  --static-cover           Disable cover music reaction

Ring Options:
  --disable-rings          Disable all rings
  --no-ring-inner          Disable inner ring
  --no-ring-middle         Disable middle ring
  --no-ring-outer          Disable outer ring
  --ring-scale             Ring scale 0.5-2.0 (default: 1.0)

Effects:
  --disable-starfield      Disable starfield background

Output Options:
  --fps                    Frame rate: 15, 30, 60 (default: 30)
  --resolution            Custom WIDTHxHEIGHT (e.g., 1920x1080)
  --phone-vertical        Use 1080x1920 resolution
  --phone-horizontal      Use 1920x1080 resolution
  --preview               Render only first N seconds (for testing)
```

## Examples

### Simple Music Video
```bash
python main.py song.mp3 -c album_art.jpg -t "Song Title" -t2 "Artist"
```

### Psychedelic Fire Theme
```bash
python main.py song.mp3 -p fire --waveform-rotation cw --ring-rotation ccw \
  --starfield-rotation cw --ring-shape star
```

### Minimal Clean Look
```bash
python main.py song.mp3 -c cover.jpg --disable-starfield --disable-rings \
  --waveform-orientation vertical
```

### Phone Vertical with Animation
```bash
python main.py song.mp3 -c cover.jpg --phone-vertical \
  --cover-timeline fade --ring-stagger inner_lead
```

### High Quality 60fps
```bash
python main.py song.mp3 -c cover.jpg -p rainbow --fps 60 \
  --resolution 1920x1080 -o output_hq.mp4
```

## Performance Tips

### Preview Mode
Use the `--preview` flag or GUI's "30s Preview" button for fast iteration:
- 10-15x faster rendering
- Half resolution
- Lower FPS for audio processing
- Perfect for testing settings

### Rendering Speed
Full render times depend on:
- **Song length**: ~2-5 minutes per minute of audio
- **Resolution**: Higher = slower (1080p takes ~2x longer than 720p)
- **FPS**: 60fps takes ~2x longer than 30fps
- **Effects**: Starfield and rings add minimal overhead

### Optimization
- Test with preview mode first
- Use 30fps for most content (60fps for slow motion)
- Start with 720p, upgrade to 1080p when satisfied
- Disable effects you don't need

## Technical Details

### Audio Processing
- **STFT Analysis**: Short-Time Fourier Transform for frequency data
- **8 Frequency Bands**: 20Hz - 1000Hz range
- **Beat Detection**: Bass/low-mid energy analysis
- **Supported Formats**: MP3, WAV, M4A, FLAC, OGG

### Visual Rendering
- **PIL/Pillow**: Image generation and compositing
- **OpenCV**: Video encoding
- **NumPy/SciPy**: Audio and signal processing
- **Multi-threaded**: GUI uses background threads for responsive UI

### Color System
- **HSV Color Space**: Hue, Saturation, Value for smooth transitions
- **RGB Input**: Custom colors converted from RGB to HSV
- **Palette System**: Pre-defined color schemes with saturation/brightness
- **Vibrancy Boost**: 1.2x multiplier for enhanced colors

### Rotation Synchronization
- Calculates rotation speeds for whole rotations over song duration
- ~1 rotation per 3 minutes of audio
- Volume-reactive speed multiplier
- Independent rotation for waveforms, rings, and starfield

## Project Structure

```
.
├── visualizer_gui.py          # Main GUI application
├── main.py                    # Command-line interface
├── visualizer.py              # Core visualizer engine
├── audio_processor.py         # Audio loading and analysis
├── beat_detector.py           # Beat detection algorithm
├── config.py                  # Global configuration
├── effects.py                 # Effects coordinator
├── effects_starfield.py       # Starfield particle system
├── effects_waveforms.py       # Waveform rendering
├── effects_rings.py           # Ring and cover art rendering
├── gui_config.py              # GUI configuration
├── gui_controls.py            # GUI controls panel
├── gui_preview.py             # GUI preview display
├── gui_renderer.py            # GUI render manager
└── README.md                  # This file
```

## Troubleshooting

### FFmpeg Not Found
```
Error: FFmpeg is required to process audio files
```
**Solution**: Install FFmpeg (see Installation section)

### Import Errors
```
ImportError: No module named 'cv2'
```
**Solution**: Install required packages:
```bash
pip install opencv-python numpy scipy Pillow tqdm
```

### GUI Not Opening
**macOS**: tkinter should be included with Python
**Linux**: Install python3-tk: `sudo apt-get install python3-tk`
**Windows**: tkinter is included with Python installer

### Slow Rendering
- Use preview mode for testing (`--preview 30` or GUI's "30s Preview")
- Lower resolution or FPS
- Disable unused effects
- Close other applications

### Color Picker Not Updating
This is a known issue on some systems. The colors are being saved correctly even if the button doesn't update visually. You can verify by updating the preview.

## Credits

Created with Python, PIL/Pillow, OpenCV, NumPy, SciPy, and FFmpeg.

## License

MIT License - Feel free to use and modify for your projects!

## Contributing

Contributions welcome! Feel free to:
- Add new effects or shapes
- Create new color palettes
- Improve performance
- Fix bugs
- Enhance documentation

## Support

For issues, questions, or feature requests, please open an issue on the project repository.

---

**Enjoy creating stunning music visualizations!** 🎵✨🎨