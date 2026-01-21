"""
GUI Controls Panel
Creates and manages the left control panel with all settings
Uses dynamic ring shape loading from rings/ directory
"""

import tkinter as tk
from tkinter import ttk
from gui_config import *


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
        scroll_container.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
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
        """Build all control sections"""
        row = 0
        
        # File selection
        self._create_file_section(self.frame, row)
        row += 1
        
        # Visual settings
        self._create_visual_section(self.frame, row)
        row += 1
        
        # Rotation effects
        self._create_rotation_section(self.frame, row)
        row += 1
        
        # Ring settings
        self._create_ring_section(self.frame, row)
        row += 1
        
        # Effects toggles
        self._create_effects_section(self.frame, row)
        row += 1
        
        # Text overlay
        self._create_text_section(self.frame, row)
        row += 1
        
        # Output settings
        self._create_output_section(self.frame, row)
        row += 1
        
        # Action buttons and progress
        self._create_action_section(self.frame, row)
    
    def _create_file_section(self, parent, row):
        """Create file selection section"""
        section = ttk.LabelFrame(parent, text="Files", padding="10")
        section.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        section.columnconfigure(0, weight=1)
        
        # Audio file
        ttk.Label(section, text="Audio:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.audio_label = ttk.Label(section, text=MSG_NO_FILE_SELECTED, foreground="gray", 
                                     wraplength=240, justify=tk.LEFT)
        self.audio_label.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(section, text="Select Audio...", 
                  command=self.callback.select_audio).grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Cover image
        ttk.Label(section, text="Cover Image (Optional):").grid(row=3, column=0, sticky=tk.W, pady=(10, 2))
        self.cover_label = ttk.Label(section, text=MSG_NO_COVER_SELECTED, foreground="gray",
                                     wraplength=240, justify=tk.LEFT)
        self.cover_label.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=2)
        
        cover_btn_frame = ttk.Frame(section)
        cover_btn_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=5)
        cover_btn_frame.columnconfigure(0, weight=1)
        cover_btn_frame.columnconfigure(1, weight=0)
        ttk.Button(cover_btn_frame, text="Select Cover...", 
                  command=self.callback.select_cover).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(cover_btn_frame, text="Clear", 
                  command=self.callback.clear_cover).grid(row=0, column=1, sticky=tk.E)
    
    def _create_visual_section(self, parent, row):
        """Create visual settings section"""
        section = ttk.LabelFrame(parent, text="Visual Settings", padding="10")
        section.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        section.columnconfigure(0, weight=1)
        
        # Color palette
        ttk.Label(section, text="Color Palette:").grid(row=0, column=0, sticky=tk.W, pady=2)
        palette_combo = ttk.Combobox(section, textvariable=self.palette_var, 
                                     state="readonly", width=18)
        palette_combo['values'] = PALETTE_OPTIONS
        palette_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2, padx=(0, 0))
        
        # Custom color picker button
        ttk.Button(section, text="Custom...", 
                  command=self.callback.open_color_picker).grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(5, 2))
        
        # Cover shape
        ttk.Label(section, text="Cover Shape:").grid(row=3, column=0, sticky=tk.W, pady=(10, 2))
        shape_frame = ttk.Frame(section)
        shape_frame.grid(row=4, column=0, sticky=tk.W, pady=2)
        ttk.Radiobutton(shape_frame, text="Square", variable=self.cover_shape_var, 
                       value="square").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(shape_frame, text="Round", variable=self.cover_shape_var, 
                       value="round").pack(side=tk.LEFT)
        
        # Cover size
        ttk.Label(section, text="Cover Size:").grid(row=5, column=0, sticky=tk.W, pady=(10, 2))
        cover_size_frame = ttk.Frame(section)
        cover_size_frame.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=2)
        cover_size_slider = ttk.Scale(cover_size_frame, from_=COVER_SIZE_MIN, to=COVER_SIZE_MAX, 
                                      variable=self.cover_size_var, orient=tk.HORIZONTAL)
        cover_size_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.cover_size_label = ttk.Label(cover_size_frame, text="1.0x", width=5)
        self.cover_size_label.pack(side=tk.LEFT)
        self.cover_size_var.trace_add('write', 
                                      lambda *args: self.cover_size_label.config(
                                          text=f"{self.cover_size_var.get():.1f}x"))
        
        # Static cover (no music reaction)
        ttk.Checkbutton(section, text="Static Cover (no music reaction)", 
                       variable=self.static_cover_var).grid(row=7, column=0, sticky=tk.W, pady=(10, 2))
        
        # Cover timeline animation
        ttk.Label(section, text="Cover Timeline Animation:").grid(row=8, column=0, sticky=tk.W, pady=(10, 2))
        timeline_combo = ttk.Combobox(section, textvariable=self.cover_timeline_var, 
                                      state="readonly", width=18)
        timeline_combo['values'] = COVER_TIMELINE_OPTIONS
        timeline_combo.current(0)
        timeline_combo.grid(row=9, column=0, sticky=(tk.W, tk.E), pady=2)
    
    def _create_rotation_section(self, parent, row):
        """Create rotation effects section"""
        section = ttk.LabelFrame(parent, text="Rotation Effects", padding="10")
        section.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        section.columnconfigure(0, weight=1)
        
        # Waveform Rotation
        ttk.Label(section, text="Waveform Rotation:").grid(row=0, column=0, sticky=tk.W, pady=2)
        wf_rot_combo = ttk.Combobox(section, textvariable=self.waveform_rot_var, 
                                    state="readonly", width=18)
        wf_rot_combo['values'] = WAVEFORM_ROTATION_OPTIONS
        wf_rot_combo.current(0)
        wf_rot_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Waveform Rotation Speed
        ttk.Label(section, text="Waveform Rotation Speed:").grid(row=2, column=0, sticky=tk.W, pady=(10, 2))
        wf_speed_frame = ttk.Frame(section)
        wf_speed_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=2)
        wf_speed_slider = ttk.Scale(wf_speed_frame, from_=ROTATION_SPEED_MIN, to=ROTATION_SPEED_MAX, 
                                    variable=self.waveform_rot_speed_var, orient=tk.HORIZONTAL)
        wf_speed_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.waveform_speed_label = ttk.Label(wf_speed_frame, text="100%", width=5)
        self.waveform_speed_label.pack(side=tk.LEFT)
        self.waveform_rot_speed_var.trace_add('write', 
                                              lambda *args: self.waveform_speed_label.config(
                                                  text=f"{int(self.waveform_rot_speed_var.get() * 100)}%"))
        
        # Waveform Orientation
        ttk.Label(section, text="Waveform Orientation:").grid(row=4, column=0, sticky=tk.W, pady=(10, 2))
        wf_orient_frame = ttk.Frame(section)
        wf_orient_frame.grid(row=5, column=0, sticky=tk.W, pady=2)
        ttk.Radiobutton(wf_orient_frame, text="Horizontal", variable=self.waveform_orientation_var, 
                       value="horizontal").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(wf_orient_frame, text="Vertical", variable=self.waveform_orientation_var, 
                       value="vertical").pack(side=tk.LEFT)
        
        # Starfield rotation
        ttk.Label(section, text="Starfield Rotation:").grid(row=6, column=0, sticky=tk.W, pady=(10, 2))
        star_rot_combo = ttk.Combobox(section, textvariable=self.starfield_rot_var, 
                                      state="readonly", width=18)
        star_rot_combo['values'] = STARFIELD_ROTATION_OPTIONS
        star_rot_combo.current(0)
        star_rot_combo.grid(row=7, column=0, sticky=(tk.W, tk.E), pady=2)
    
    def _create_ring_section(self, parent, row):
        """Create ring settings section"""
        section = ttk.LabelFrame(parent, text="Ring Settings", padding="10")
        section.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        section.columnconfigure(0, weight=1)
        
        ttk.Checkbutton(section, text="Show Rings", variable=self.rings_enabled_var).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        # Ring rotation
        ttk.Label(section, text="Ring Rotation:").grid(row=1, column=0, sticky=tk.W, pady=(10, 2))
        ring_rot_combo = ttk.Combobox(section, textvariable=self.ring_rot_var, 
                                      state="readonly", width=18)
        ring_rot_combo['values'] = RING_ROTATION_OPTIONS
        ring_rot_combo.current(0)
        ring_rot_combo.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Ring Rotation Speed
        ttk.Label(section, text="Ring Rotation Speed:").grid(row=3, column=0, sticky=tk.W, pady=(10, 2))
        ring_speed_frame = ttk.Frame(section)
        ring_speed_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=2)
        ring_speed_slider = ttk.Scale(ring_speed_frame, from_=ROTATION_SPEED_MIN, to=ROTATION_SPEED_MAX, 
                                      variable=self.ring_rot_speed_var, orient=tk.HORIZONTAL)
        ring_speed_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.ring_speed_label = ttk.Label(ring_speed_frame, text="100%", width=5)
        self.ring_speed_label.pack(side=tk.LEFT)
        self.ring_rot_speed_var.trace_add('write', 
                                          lambda *args: self.ring_speed_label.config(
                                              text=f"{int(self.ring_rot_speed_var.get() * 100)}%"))
        
        # Ring shape - now dynamically loaded
        ttk.Label(section, text="Ring Shape:").grid(row=5, column=0, sticky=tk.W, pady=(10, 2))
        ring_shape_combo = ttk.Combobox(section, textvariable=self.ring_shape_var, 
                                       state="readonly", width=18)
        ring_shape_combo['values'] = RING_SHAPE_OPTIONS
        ring_shape_combo.current(0)
        ring_shape_combo.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Number of rings
        ttk.Label(section, text="Number of Rings:").grid(row=7, column=0, sticky=tk.W, pady=(10, 2))
        ring_count_frame = ttk.Frame(section)
        ring_count_frame.grid(row=8, column=0, sticky=(tk.W, tk.E), pady=2)
        ring_count_slider = ttk.Scale(ring_count_frame, from_=RING_COUNT_MIN, to=RING_COUNT_MAX, 
                                      variable=self.ring_count_var, orient=tk.HORIZONTAL,
                                      command=lambda v: self.ring_count_var.set(int(float(v))))
        ring_count_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.ring_count_label = ttk.Label(ring_count_frame, text="3", width=5)
        self.ring_count_label.pack(side=tk.LEFT)
        self.ring_count_var.trace_add('write', 
                                      lambda *args: self.ring_count_label.config(
                                          text=f"{self.ring_count_var.get()}"))
        
        # Ring scale
        ttk.Label(section, text="Ring Scale:").grid(row=9, column=0, sticky=tk.W, pady=(10, 2))
        ring_scale_frame = ttk.Frame(section)
        ring_scale_frame.grid(row=10, column=0, sticky=(tk.W, tk.E), pady=2)
        ring_scale_slider = ttk.Scale(ring_scale_frame, from_=RING_SCALE_MIN, to=RING_SCALE_MAX, 
                                      variable=self.ring_scale_var, orient=tk.HORIZONTAL)
        ring_scale_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.ring_scale_label = ttk.Label(ring_scale_frame, text="1.0x", width=5)
        self.ring_scale_label.pack(side=tk.LEFT)
        self.ring_scale_var.trace_add('write', 
                                      lambda *args: self.ring_scale_label.config(
                                          text=f"{self.ring_scale_var.get():.1f}x"))
        
        # Ring rotation stagger
        ttk.Label(section, text="Ring Rotation Stagger:").grid(row=11, column=0, sticky=tk.W, pady=(10, 2))
        ring_stagger_combo = ttk.Combobox(section, textvariable=self.ring_stagger_var, 
                                         state="readonly", width=18)
        ring_stagger_combo['values'] = RING_STAGGER_OPTIONS
        ring_stagger_combo.current(0)
        ring_stagger_combo.grid(row=12, column=0, sticky=(tk.W, tk.E), pady=2)
    
    def _create_effects_section(self, parent, row):
        """Create effects toggles section"""
        section = ttk.LabelFrame(parent, text="Effects", padding="10")
        section.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Checkbutton(section, text="Show Starfield", variable=self.starfield_enabled_var).grid(row=0, column=0, sticky=tk.W, pady=2)
    
    def _create_text_section(self, parent, row):
        """Create text overlay section"""
        section = ttk.LabelFrame(parent, text="Text Overlay", padding="10")
        section.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        section.columnconfigure(0, weight=1)
        
        ttk.Label(section, text="Text Line 1 (Optional):").grid(row=0, column=0, sticky=tk.W, pady=2)
        text_entry = ttk.Entry(section, textvariable=self.text_var, width=25)
        text_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(section, text="Text Line 2 (Optional):").grid(row=2, column=0, sticky=tk.W, pady=(10, 2))
        text_entry2 = ttk.Entry(section, textvariable=self.text_var2, width=25)
        text_entry2.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Text size slider
        ttk.Label(section, text="Text Size:").grid(row=4, column=0, sticky=tk.W, pady=(10, 2))
        text_size_frame = ttk.Frame(section)
        text_size_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=2)
        text_size_slider = ttk.Scale(text_size_frame, from_=TEXT_SIZE_MIN, to=TEXT_SIZE_MAX, 
                                     variable=self.text_size_var, orient=tk.HORIZONTAL)
        text_size_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.text_size_label = ttk.Label(text_size_frame, text="1.0x", width=5)
        self.text_size_label.pack(side=tk.LEFT)
        self.text_size_var.trace_add('write', 
                                     lambda *args: self.text_size_label.config(
                                         text=f"{self.text_size_var.get():.1f}x"))
        
        # Horizontal alignment
        ttk.Label(section, text="Horizontal Alignment:").grid(row=6, column=0, sticky=tk.W, pady=(10, 2))
        h_align_combo = ttk.Combobox(section, textvariable=self.text_h_align_var, 
                                     state="readonly", width=18)
        h_align_combo['values'] = TEXT_HORIZONTAL_ALIGN_OPTIONS
        h_align_combo.current(1)  # Center
        h_align_combo.grid(row=7, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Vertical alignment
        ttk.Label(section, text="Vertical Alignment:").grid(row=8, column=0, sticky=tk.W, pady=(10, 2))
        v_align_combo = ttk.Combobox(section, textvariable=self.text_v_align_var, 
                                     state="readonly", width=18)
        v_align_combo['values'] = TEXT_VERTICAL_ALIGN_OPTIONS
        v_align_combo.current(2)  # Bottom
        v_align_combo.grid(row=9, column=0, sticky=(tk.W, tk.E), pady=2)
    
    def _create_output_section(self, parent, row):
        """Create output settings section"""
        section = ttk.LabelFrame(parent, text="Output Settings", padding="10")
        section.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        section.columnconfigure(0, weight=1)
        
        # Resolution
        ttk.Label(section, text="Resolution:").grid(row=0, column=0, sticky=tk.W, pady=2)
        res_combo = ttk.Combobox(section, textvariable=self.resolution_var, 
                                state="readonly", width=18)
        res_combo['values'] = RESOLUTION_OPTIONS
        res_combo.current(0)
        res_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # FPS
        ttk.Label(section, text="Frame Rate:").grid(row=2, column=0, sticky=tk.W, pady=(10, 2))
        fps_combo = ttk.Combobox(section, textvariable=self.fps_var, 
                                state="readonly", width=18)
        fps_combo['values'] = FPS_OPTIONS
        fps_combo.current(1)
        fps_combo.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=2)
    
    def _create_action_section(self, parent, row):
        """Create action buttons and progress section"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        button_frame.columnconfigure(0, weight=1)
        
        self.preview_btn = ttk.Button(button_frame, text="Update Preview", 
                                      command=self.callback.update_preview)
        self.preview_btn.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.quick_render_btn = ttk.Button(button_frame, text="Render 30s Preview Video", 
                                           command=self.callback.render_quick_preview)
        self.quick_render_btn.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.render_btn = ttk.Button(button_frame, text="Render Full Video", 
                                     command=self.callback.render_video)
        self.render_btn.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Progress section (hidden by default) - use grid consistently
        self.progress_frame = ttk.Frame(button_frame)
        self.progress_frame.columnconfigure(0, weight=1)
        self.progress_label = ttk.Label(self.progress_frame, text="", 
                                       font=('TkDefaultFont', 9))
        self.progress_label.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 2))
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='determinate', 
                                           maximum=100)
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.cancel_btn = ttk.Button(button_frame, text="Cancel Render", 
                                     command=self.callback.cancel_render)
    
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
        """Convert display name to internal ring shape value - uses dynamic lookup"""
        try:
            import rings
            display_names = rings.get_ring_display_names()
            # Find the internal name that matches this display name
            for disp_name, internal_name in display_names:
                if disp_name == display_name:
                    return internal_name
        except Exception as e:
            print(f"Warning: Could not look up ring shape: {e}")
        
        # Fallback to lowercase conversion
        return display_name.lower().replace(' ', '').replace('-', '')
    
    def get_settings(self):
        """Return all current settings as a dictionary"""
        # Parse resolution
        res_str = self.resolution_var.get().split(' - ')[0]
        width, height = map(int, res_str.split('x'))
        
        return {
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
            'ring_count': self.ring_count_var.get(),
            'ring_scale': self.ring_scale_var.get(),
            'waveform_orientation': self.waveform_orientation_var.get(),
            'static_cover': self.static_cover_var.get(),
            'cover_timeline': self.get_timeline_value(self.cover_timeline_var.get()),
            'ring_stagger': self.get_stagger_value(self.ring_stagger_var.get())
        }