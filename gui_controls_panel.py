"""
GUI Controls Panel - Main Coordinator
Creates and manages the left control panel with all settings
"""

import tkinter as tk
from tkinter import ttk
from gui_config import *

# Import section builders from gui_controls package
from gui_controls import (
    files, cover, colors, waveforms, rings, 
    starfield, text, output, actions
)


class ControlsPanel:
    def __init__(self, parent, callback_handler):
        self.parent = parent
        self.callback = callback_handler
        
        # Create variables for all controls
        self._create_variables()
        
        # Build the controls panel
        self.frame = self._create_scrollable_frame()
        self._build_controls()
    
    def _get_text_color(self):
        """Get appropriate text color based on system appearance"""
        try:
            # Try to detect dark mode on macOS
            import subprocess
            result = subprocess.run(
                ['defaults', 'read', '-g', 'AppleInterfaceStyle'],
                capture_output=True,
                text=True,
                timeout=1
            )
            if result.returncode == 0 and 'Dark' in result.stdout:
                return 'white'
        except:
            pass
        
        # Default to black for light mode (or if detection fails)
        return 'black'
    
    def _create_variables(self):
        """Initialize all tkinter variables"""
        # File paths (not tk variables)
        self.audio_path = None
        self.cover_path = None
        
        # Visual settings
        self.palette_var = tk.StringVar(value=DEFAULT_PALETTE)
        self.cover_shape_var = tk.StringVar(value=DEFAULT_COVER_SHAPE)
        self.cover_size_var = tk.DoubleVar(value=DEFAULT_COVER_SIZE)
        
        # Rotation settings
        self.waveform_rot_var = tk.StringVar(value=DEFAULT_WAVEFORM_ROTATION)
        self.waveform_rot_speed_var = tk.DoubleVar(value=DEFAULT_ROTATION_SPEED)
        self.ring_rot_var = tk.StringVar(value=DEFAULT_RING_ROTATION)
        self.ring_rot_speed_var = tk.DoubleVar(value=DEFAULT_ROTATION_SPEED)
        self.ring_shape_var = tk.StringVar(value=DEFAULT_RING_SHAPE)
        self.starfield_rot_var = tk.StringVar(value=DEFAULT_STARFIELD_ROTATION)
        
        # Waveform orientation
        self.waveform_orientation_var = tk.StringVar(value=DEFAULT_WAVEFORM_ORIENTATION)
        
        # Effects toggles
        self.rings_enabled_var = tk.BooleanVar(value=True)
        self.starfield_enabled_var = tk.BooleanVar(value=True)
        
        # Number of rings
        self.ring_count_var = tk.IntVar(value=DEFAULT_RING_COUNT)
        
        # Ring scale
        self.ring_scale_var = tk.DoubleVar(value=DEFAULT_RING_SCALE)
        
        # Ring stagger
        self.ring_stagger_var = tk.StringVar(value=DEFAULT_RING_STAGGER)
        
        # Cover settings
        self.static_cover_var = tk.BooleanVar(value=DEFAULT_STATIC_COVER)
        self.cover_timeline_var = tk.StringVar(value=DEFAULT_COVER_TIMELINE)
        
        # Text and output
        self.text_var = tk.StringVar()
        self.text_var2 = tk.StringVar()
        self.text_size_var = tk.DoubleVar(value=DEFAULT_TEXT_SIZE)
        self.text_h_align_var = tk.StringVar(value=DEFAULT_TEXT_H_ALIGN)
        self.text_v_align_var = tk.StringVar(value=DEFAULT_TEXT_V_ALIGN)
        self.resolution_var = tk.StringVar(value=DEFAULT_RESOLUTION)
        self.fps_var = tk.IntVar(value=DEFAULT_FPS)
    
    def _create_scrollable_frame(self):
        """Create scrollable container for controls"""
        scroll_container = ttk.Frame(self.parent)
        scroll_container.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                            padx=(0, 10))
        scroll_container.columnconfigure(0, weight=1)
        scroll_container.rowconfigure(0, weight=1)
        
        # Canvas and scrollbar
        canvas = tk.Canvas(scroll_container, width=CONTROLS_CANVAS_WIDTH, highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
        
        # Controls frame
        controls_frame = ttk.Frame(canvas, padding=CONTROLS_PADDING)
        
        # Configure canvas
        canvas_window = canvas.create_window((0, 0), window=controls_frame, anchor="nw")
        
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())
        
        def configure_canvas(event=None):
            canvas.itemconfig(canvas_window, width=event.width)
        
        controls_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_canvas)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mousewheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta)), "units")
        
        def bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        def unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind("<Enter>", bind_mousewheel)
        canvas.bind("<Leave>", unbind_mousewheel)
        
        # Grid canvas and scrollbar
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        return controls_frame
    
    def _build_controls(self):
        """Build all control sections using modular section builders"""
        row = 0
        
        # 1. Files
        files.create_section(self.frame, row, self)
        row += 1
        
        # 2. Cover Options
        cover.create_section(self.frame, row, self)
        row += 1
        
        # 3. Colors
        colors.create_section(self.frame, row, self)
        row += 1
        
        # 4. Waveforms
        waveforms.create_section(self.frame, row, self)
        row += 1
        
        # 5. Rings
        rings.create_section(self.frame, row, self)
        row += 1
        
        # 6. Starfield
        starfield.create_section(self.frame, row, self)
        row += 1
        
        # 7. Text
        text.create_section(self.frame, row, self)
        row += 1
        
        # 8. Output
        output.create_section(self.frame, row, self)
        row += 1
        
        # 9-11. Action Buttons
        actions.create_section(self.frame, row, self)
    
    def get_rotation_value(self, combo_value):
        """Extract rotation axis from combo box value"""
        return combo_value.split(' - ')[0]
    
    def get_timeline_value(self, combo_value):
        """Extract timeline animation from combo box value"""
        return combo_value.split(' - ')[0]
    
    def get_stagger_value(self, combo_value):
        """Extract stagger mode from combo box value"""
        return combo_value.split(' - ')[0]
    
    def get_palette_value(self, display_name):
        """Convert display name to internal palette name"""
        return display_name.lower()
    
    def get_ring_shape_value(self, display_name):
        """Convert display name to internal ring shape value"""
        # Try to get the mapping from the rings module if available
        try:
            import rings
            shape_code = rings.get_shape_code_from_display_name(display_name)
            print(f"DEBUG Ring Shape (from rings module): '{display_name}' -> '{shape_code}'")
            return shape_code
        except:
            pass
        
        # Fallback mapping - handle both hyphenated and space-separated versions
        shape_map = {
            'Circle': 'circle',
            'Triangle': 'triangle',
            'Square': 'square',
            'Pentagon': 'pentagon',
            'Hexagon': 'hexagon',
            'Octagon': 'octagon',
            '4 Point Star': 'star4',
            '4-Point Star': 'star4',
            '6 Point Star': 'star6',
            '6-Point Star': 'star6',
            '5 Point Star': 'star',
            '5-Point Star': 'star',
            'Gear': 'gear'
        }
        
        result = shape_map.get(display_name, 'circle')
        print(f"DEBUG Ring Shape (fallback): '{display_name}' -> '{result}'")
        return result
    
    def get_settings(self):
        """Return all current settings as a dictionary"""
        # Parse resolution
        res_str = self.resolution_var.get().split(' - ')[0]
        width, height = map(int, res_str.split('x'))
        
        # Get ring count value
        ring_count = self.ring_count_var.get()
        print(f"DEBUG Ring Count: {ring_count}")
        
        settings = {
            'audio_path': self.audio_path,
            'cover_image_path': self.cover_path,
            'resolution': (width, height),
            'fps': self.fps_var.get(),
            'text_overlay': self.text_var.get() or None,
            'text_overlay2': self.text_var2.get() or None,
            'text_size': self.text_size_var.get(),
            'text_h_align': self.text_h_align_var.get().lower(),
            'text_v_align': self.text_v_align_var.get().lower(),
            'color_palette': self.get_palette_value(self.palette_var.get()),
            'waveform_rotation': self.get_rotation_value(self.waveform_rot_var.get()),
            'waveform_rotation_speed': self.waveform_rot_speed_var.get(),
            'ring_rotation': self.get_rotation_value(self.ring_rot_var.get()),
            'ring_rotation_speed': self.ring_rot_speed_var.get(),
            'starfield_rotation': self.get_rotation_value(self.starfield_rot_var.get()),
            'cover_shape': self.cover_shape_var.get(),
            'cover_size': self.cover_size_var.get(),
            'disable_rings': not self.rings_enabled_var.get(),
            'disable_starfield': not self.starfield_enabled_var.get(),
            'ring_shape': self.get_ring_shape_value(self.ring_shape_var.get()),
            'ring_count': ring_count,
            'ring_scale': self.ring_scale_var.get(),
            'waveform_orientation': self.waveform_orientation_var.get(),
            'static_cover': self.static_cover_var.get(),
            'cover_timeline': self.get_timeline_value(self.cover_timeline_var.get()),
            'ring_stagger': self.get_stagger_value(self.ring_stagger_var.get())
        }
        
        print(f"DEBUG Settings: ring_count={settings['ring_count']}, ring_shape={settings['ring_shape']}")
        return settings