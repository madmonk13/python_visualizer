#!/usr/bin/env python3
"""
Music Visualizer GUI - Main Application
Provides live preview and interactive controls for the music visualizer
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import subprocess

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import GUI modules
try:
    from gui_config import (
        WINDOW_TITLE, WINDOW_SIZE, AUDIO_FILETYPES, 
        IMAGE_FILETYPES, VIDEO_FILETYPES, MSG_NO_COVER_SELECTED
    )
    from gui_controls import ControlsPanel
    from gui_preview import PreviewPanel
    from gui_renderer import RenderManager
except ImportError as e:
    print("=" * 60)
    print("ERROR: Could not import required modules")
    print("=" * 60)
    print(f"Error: {e}")
    print(f"\nCurrent directory: {os.getcwd()}")
    print(f"Script directory: {current_dir}")
    print(f"\nFiles in script directory:")
    for f in sorted(os.listdir(current_dir)):
        if f.endswith('.py'):
            print(f"  - {f}")
    print("\nMake sure these files exist in the same directory:")
    print("  - gui_config.py")
    print("  - gui_controls.py")
    print("  - gui_preview.py")
    print("  - gui_renderer.py")
    print("  - visualizer.py")
    print("  - config.py")
    print("  - audio_processor.py")
    print("  - effects.py")
    print("  - beat_detector.py")
    print("=" * 60)
    sys.exit(1)


class VisualizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        
        # Create main UI
        self._create_ui()
        
        # Initialize render manager (after panels are created)
        self.render_manager = RenderManager(self.root, self.controls, self.preview)
    
    def _get_text_color(self):
        """Get appropriate text color based on system appearance"""
        try:
            # Try to detect dark mode on macOS
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
    
    def _create_ui(self):
        """Create the main UI layout"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Create panels
        self.controls = ControlsPanel(main_frame, self)
        self.preview = PreviewPanel(main_frame)
    
    # Callback methods for controls panel
    def select_audio(self):
        """Open file dialog to select audio"""
        filename = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=AUDIO_FILETYPES
        )
        if filename:
            self.controls.audio_path = filename
            display_name = os.path.basename(filename)
            # Truncate long filenames
            if len(display_name) > 35:
                display_name = display_name[:32] + "..."
            self.controls.audio_label.config(text=display_name, 
                                            foreground=self._get_text_color())
            # Don't auto-update preview - user clicks button when ready
    
    def select_cover(self):
        """Open file dialog to select cover image"""
        filename = filedialog.askopenfilename(
            title="Select Cover Image",
            filetypes=IMAGE_FILETYPES
        )
        if filename:
            self.controls.cover_path = filename
            display_name = os.path.basename(filename)
            # Truncate long filenames
            if len(display_name) > 35:
                display_name = display_name[:32] + "..."
            self.controls.cover_label.config(text=display_name, 
                                            foreground=self._get_text_color())
            # Don't auto-update preview
    
    def clear_cover(self):
        """Clear the cover image"""
        self.controls.cover_path = None
        self.controls.cover_label.config(text=MSG_NO_COVER_SELECTED, 
                                        foreground="gray")
        # Don't auto-update preview
    
    def preview_dirty(self):
        """Mark preview as needing update (but don't regenerate)"""
        # This method is kept for compatibility but does nothing now
        # Preview only updates when user clicks "Update Preview" button
        pass
    
    def update_preview(self):
        """Generate and display preview frame"""
        if not self.controls.audio_path:
            return
        
        self.render_manager.generate_preview()
    
    def render_video(self):
        """Render the full video"""
        if not self.controls.audio_path:
            messagebox.showwarning("No Audio", "Please select an audio file first.")
            return
        
        if self.render_manager.is_rendering:
            messagebox.showinfo("Rendering", "A video is already being rendered.")
            return
        
        # Ask for output location
        output_path = filedialog.asksaveasfilename(
            title="Save Video As",
            defaultextension=".mp4",
            filetypes=VIDEO_FILETYPES
        )
        
        if not output_path:
            return
        
        # Confirm before rendering
        duration_estimate = "several minutes"
        if messagebox.askyesno("Confirm Render",
                              f"This will render the full video, which may take {duration_estimate}.\n\nContinue?"):
            self.render_manager.start_render(output_path)
    
    def render_quick_preview(self):
        """Render a 30-second preview video"""
        if not self.controls.audio_path:
            messagebox.showwarning("No Audio", "Please select an audio file first.")
            return
        
        if self.render_manager.is_rendering:
            messagebox.showinfo("Rendering", "A video is already being rendered.")
            return
        
        # Ask for output location
        output_path = filedialog.asksaveasfilename(
            title="Save 30s Preview Video As",
            defaultextension=".mp4",
            filetypes=VIDEO_FILETYPES,
            initialfile="preview_30s.mp4"
        )
        
        if not output_path:
            return
        
        # Start quick preview render
        self.render_manager.start_render(output_path, preview_seconds=30)
    
    def cancel_render(self):
        """Cancel the current render"""
        self.render_manager.cancel_render()
    
    def open_color_picker(self):
        """Open custom color picker dialog"""
        from tkinter import colorchooser
        import json
        
        # Create a simple dialog for choosing 8 colors
        color_window = tk.Toplevel(self.root)
        color_window.title("Custom Color Palette")
        color_window.geometry("400x500")
        
        ttk.Label(color_window, text="Choose 8 colors for your custom palette:", 
                 font=('TkDefaultFont', 12, 'bold')).pack(pady=10)
        
        colors = []
        color_labels = []
        
        def pick_color(index):
            color = colorchooser.askcolor(title=f"Choose Color {index + 1}")
            if color[0]:  # color[0] is RGB tuple
                r, g, b = color[0]
                # Convert RGB to HSV for hue
                r, g, b = r/255, g/255, b/255
                mx = max(r, g, b)
                mn = min(r, g, b)
                df = mx - mn
                
                if mx == mn:
                    h = 0
                elif mx == r:
                    h = (60 * ((g - b) / df) + 360) % 360
                elif mx == g:
                    h = (60 * ((b - r) / df) + 120) % 360
                else:
                    h = (60 * ((r - g) / df) + 240) % 360
                
                colors[index] = int(h)
                color_labels[index].config(text=f"Color {index + 1}: Hue {int(h)}°", 
                                          background=color[1])
        
        # Create 8 color pickers
        for i in range(8):
            frame = ttk.Frame(color_window)
            frame.pack(fill=tk.X, padx=20, pady=5)
            
            colors.append(i * 45)  # Default rainbow
            
            label = tk.Label(frame, text=f"Color {i + 1}: Hue {i * 45}°", 
                           width=30, relief=tk.RAISED, padx=10, pady=5)
            label.pack(side=tk.LEFT, padx=(0, 10))
            color_labels.append(label)
            
            ttk.Button(frame, text="Pick Color", 
                      command=lambda idx=i: pick_color(idx)).pack(side=tk.LEFT)
        
        def apply_custom_palette():
            # Create custom palette and save it
            custom_palette = {
                'name': 'Custom',
                'colors': colors,
                'saturation': 1.0,
                'brightness': 1.0
            }
            
            # Save to a temp file that the visualizer can read
            import tempfile
            import os
            custom_file = os.path.join(tempfile.gettempdir(), 'visualizer_custom_palette.json')
            with open(custom_file, 'w') as f:
                json.dump(custom_palette, f)
            
            # Set palette to 'custom'
            self.controls.palette_var.set('custom')
            color_window.destroy()
            
            messagebox.showinfo("Custom Palette", 
                              "Custom palette applied! Update preview to see changes.")
        
        ttk.Button(color_window, text="Apply Custom Palette", 
                  command=apply_custom_palette).pack(pady=20)


def main():
    """Main entry point"""
    root = tk.Tk()
    
    # Set macOS style
    style = ttk.Style()
    try:
        style.theme_use('aqua')  # macOS native theme
    except:
        pass  # Fall back to default theme on other platforms
    
    # Create and run app
    try:
        app = VisualizerGUI(root)
        root.mainloop()
    except Exception as e:
        print("=" * 60)
        print("ERROR: Failed to start GUI")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        print("=" * 60)
        sys.exit(1)


if __name__ == '__main__':
    main()