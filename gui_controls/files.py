"""
GUI Controls - Files Section
"""

import tkinter as tk
from tkinter import ttk
from gui_config import MSG_NO_FILE_SELECTED, MSG_NO_COVER_SELECTED


def create_section(parent, row, controls_panel):
    """Create the Files section"""
    section = ttk.LabelFrame(parent, text="Files", padding="10")
    section.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
    section.columnconfigure(0, weight=1)
    
    # Audio file
    ttk.Label(section, text="Audio:").grid(row=0, column=0, sticky=tk.W, pady=2)
    controls_panel.audio_label = ttk.Label(section, text=MSG_NO_FILE_SELECTED, 
                                          foreground="gray", 
                                          wraplength=240, justify=tk.LEFT)
    controls_panel.audio_label.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)
    ttk.Button(section, text="Select Audio...", 
              command=controls_panel.callback.select_audio).grid(row=2, column=0, 
                                                                 sticky=(tk.W, tk.E), pady=5)
    
    # Cover image
    ttk.Label(section, text="Cover Image (Optional):").grid(row=3, column=0, sticky=tk.W, 
                                                            pady=(10, 2))
    controls_panel.cover_label = ttk.Label(section, text=MSG_NO_COVER_SELECTED, 
                                          foreground="gray",
                                          wraplength=240, justify=tk.LEFT)
    controls_panel.cover_label.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=2)
    
    cover_btn_frame = ttk.Frame(section)
    cover_btn_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=5)
    cover_btn_frame.columnconfigure(0, weight=1)
    cover_btn_frame.columnconfigure(1, weight=0)
    ttk.Button(cover_btn_frame, text="Select Cover...", 
              command=controls_panel.callback.select_cover).grid(row=0, column=0, 
                                                                 sticky=(tk.W, tk.E), 
                                                                 padx=(0, 5))
    ttk.Button(cover_btn_frame, text="Clear", 
              command=controls_panel.callback.clear_cover).grid(row=0, column=1, sticky=tk.E)
    
    return section