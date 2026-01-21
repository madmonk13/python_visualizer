"""
GUI Renderer
Handles preview generation and full video rendering in background threads
"""

import threading
import subprocess
import os
import sys
import tempfile
import tkinter as tk

# Add current directory to path if needed
if '.' not in sys.path:
    sys.path.insert(0, '.')

try:
    import cv2
    import numpy as np
    from PIL import Image
    from visualizer import MusicVisualizer
    from gui_config import *
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    raise


class RenderManager:
    def __init__(self, root, controls_panel, preview_panel):
        self.root = root
        self.controls = controls_panel
        self.preview = preview_panel
        
        self.preview_thread = None
        self.render_thread = None
        self.is_rendering = False
        self.cancel_render_flag = False
    
    def generate_preview(self):
        """Start preview generation in background thread"""
        if not self.controls.audio_path:
            return
        
        if self.preview_thread and self.preview_thread.is_alive():
            # Don't start another preview if one is already running
            print("Preview already generating, skipping...")
            return
        
        # Clear the preview FIRST and show message
        self.preview.clear()
        self.preview.set_info("Generating Preview - Please Wait...", "blue")
        self.controls.preview_btn.config(state='disabled')
        
        self.preview_thread = threading.Thread(target=self._generate_preview_background, 
                                              daemon=True)
        self.preview_thread.start()
    
    def _generate_preview_background(self):
        """Background thread to generate preview"""
        try:
            settings = self.controls.get_settings()
            width, height = settings['resolution']
            
            # Use full resolution for preview since it's manual
            preview_width = width
            preview_height = height
            preview_fps = 10  # Still use lower FPS for audio processing
            
            self.root.after(0, lambda: self.preview.set_info("Loading audio..."))
            
            # Create fresh visualizer each time for clean render
            visualizer = MusicVisualizer(
                audio_path=settings['audio_path'],
                cover_image_path=settings['cover_image_path'],
                fps=preview_fps,
                resolution=(preview_width, preview_height),
                text_overlay=settings['text_overlay'],
                text_overlay2=settings['text_overlay2'],
                text_size=settings.get('text_size', 1.0),
                text_h_align=settings.get('text_h_align', 'center'),
                text_v_align=settings.get('text_v_align', 'bottom'),
                color_palette=settings['color_palette'],
                waveform_rotation=settings['waveform_rotation'],
                waveform_rotation_speed=settings.get('waveform_rotation_speed', 1.0),
                ring_rotation=settings['ring_rotation'],
                ring_rotation_speed=settings.get('ring_rotation_speed', 1.0),
                starfield_rotation=settings['starfield_rotation'],
                preview_seconds=None,
                cover_shape=settings['cover_shape'],
                cover_size=settings['cover_size'],
                disable_rings=settings['disable_rings'],
                disable_starfield=settings['disable_starfield'],
                ring_shape=settings['ring_shape'],
                ring_count=settings.get('ring_count', 3),
                ring_scale=settings['ring_scale'],
                waveform_orientation=settings['waveform_orientation'],
                static_cover=settings['static_cover'],
                cover_timeline=settings.get('cover_timeline', 'none'),
                ring_stagger=settings.get('ring_stagger', 'none')
            )
            
            self.root.after(0, lambda: self.preview.set_info("Rendering frame..."))
            
            # Render a frame from first 1/8th of song
            frame_idx = min(len(visualizer.audio_processor.times) // 8, 
                           len(visualizer.audio_processor.times) - 1)
            total_frames = len(visualizer.audio_processor.times)
            
            preview_img = visualizer.render_frame(frame_idx, total_frames)
            
            # Display at full resolution - canvas will scale to fit
            
            # Update UI in main thread
            self.root.after(0, lambda: self._display_preview(preview_img))
            
        except Exception as error:
            error_msg = str(error)
            import traceback
            traceback.print_exc()
            self.root.after(0, lambda: self._preview_error(error_msg))
    
    def _display_preview(self, img):
        """Display the generated preview (called from main thread)"""
        self.preview.display_image(img)
        self.preview.set_info("Preview Ready", "green")
        self.controls.preview_btn.config(state='normal')
    
    def _preview_error(self, error_msg):
        """Handle preview generation error"""
        self.preview.set_info(f"Error: {error_msg}", "red")
        self.controls.preview_btn.config(state='normal')
        from tkinter import messagebox
        messagebox.showerror("Preview Error", f"Could not generate preview:\n{error_msg}")
    
    def start_render(self, output_path, preview_seconds=None):
        """Start full video render (can optionally render just preview_seconds)"""
        if self.is_rendering:
            return False
        
        self.is_rendering = True
        self.cancel_render_flag = False
        self.controls.render_btn.config(state='disabled')
        self.controls.quick_render_btn.config(state='disabled')
        self.controls.preview_btn.config(state='disabled')
        
        # Show progress UI using grid instead of pack
        self.controls.progress_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        self.controls.cancel_btn.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        self.controls.progress_bar['value'] = 0
        self.controls.progress_label.config(text=MSG_STARTING_RENDER)
        
        # Generate a preview frame to show during render
        if preview_seconds:
            self.preview.set_info(f"Rendering {preview_seconds}s preview video... 0%")
        else:
            self.preview.set_info("Rendering full video... 0%")
        
        # Start render thread - PASS preview_seconds as argument
        self.render_thread = threading.Thread(
            target=self._render_video_background,
            args=(output_path, preview_seconds),
            daemon=True
        )
        self.render_thread.start()
        return True
    
    def cancel_render(self):
        """Cancel the current render"""
        from tkinter import messagebox
        if messagebox.askyesno("Cancel Render", 
                              "Are you sure you want to cancel the current render?"):
            self.cancel_render_flag = True
            self.controls.progress_label.config(text=MSG_CANCELLING)
    
    def update_progress(self, current_frame, total_frames):
        """Update progress bar from render thread"""
        if self.cancel_render_flag:
            return False
        
        progress = int((current_frame / total_frames) * 100)
        
        self.root.after(0, lambda: self.controls.progress_bar.config(value=progress))
        self.root.after(0, lambda: self.controls.progress_label.config(
            text=f"Rendering frame {current_frame}/{total_frames} ({progress}%)"
        ))
        
        # Also update the preview info label with percentage
        self.root.after(0, lambda: self.preview.set_info(
            f"Rendering... {progress}% complete"
        ))
        
        return True
    
    def _render_video_background(self, output_path, preview_seconds=None):
        """Background thread for rendering - ACCEPTS preview_seconds parameter"""
        try:
            settings = self.controls.get_settings()
            
            # Create visualizer - PASS preview_seconds to it
            visualizer = MusicVisualizer(
                audio_path=settings['audio_path'],
                output_path=output_path,
                cover_image_path=settings['cover_image_path'],
                fps=settings['fps'],
                resolution=settings['resolution'],
                text_overlay=settings['text_overlay'],
                text_overlay2=settings['text_overlay2'],
                text_size=settings.get('text_size', 1.0),
                text_h_align=settings.get('text_h_align', 'center'),
                text_v_align=settings.get('text_v_align', 'bottom'),
                color_palette=settings['color_palette'],
                waveform_rotation=settings['waveform_rotation'],
                waveform_rotation_speed=settings.get('waveform_rotation_speed', 1.0),
                ring_rotation=settings['ring_rotation'],
                ring_rotation_speed=settings.get('ring_rotation_speed', 1.0),
                starfield_rotation=settings['starfield_rotation'],
                preview_seconds=preview_seconds,
                cover_shape=settings['cover_shape'],
                cover_size=settings['cover_size'],
                disable_rings=settings['disable_rings'],
                disable_starfield=settings['disable_starfield'],
                ring_shape=settings['ring_shape'],
                ring_count=settings.get('ring_count', 3),
                ring_scale=settings['ring_scale'],
                waveform_orientation=settings['waveform_orientation'],
                static_cover=settings['static_cover'],
                cover_timeline=settings.get('cover_timeline', 'none'),
                ring_stagger=settings.get('ring_stagger', 'none')
            )
            
            # Calculate frames
            render_duration = visualizer.duration
            if preview_seconds:
                render_duration = min(preview_seconds, visualizer.duration)
            
            total_frames = int(render_duration * visualizer.fps)
            
            # Generate and display a preview frame at start of render
            preview_frame_idx = min(len(visualizer.audio_processor.times) // 8, 
                                   len(visualizer.audio_processor.times) - 1)
            preview_img = visualizer.render_frame(preview_frame_idx, total_frames)
            self.root.after(0, lambda: self.preview.display_image(preview_img))
            
            # Create temporary video
            temp_video = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
            temp_video_path = temp_video.name
            temp_video.close()
            
            # Setup video writer
            import cv2
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(temp_video_path, fourcc, visualizer.fps,
                                 (visualizer.width, visualizer.height))
            
            # Render frames
            import numpy as np
            for frame_idx in range(total_frames):
                if not self.update_progress(frame_idx + 1, total_frames):
                    out.release()
                    os.remove(temp_video_path)
                    self.root.after(0, self._render_cancelled)
                    return
                
                img = visualizer.render_frame(frame_idx, total_frames)
                frame_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                out.write(frame_cv)
            
            out.release()
            
            # Add audio
            self.root.after(0, lambda: self.controls.progress_label.config(
                text=MSG_ADDING_AUDIO))
            self.root.after(0, lambda: self.preview.set_info("Adding audio to video..."))
            
            # Build FFmpeg command properly
            ffmpeg_cmd = [
                'ffmpeg',
                '-i', temp_video_path,
                '-i', settings['audio_path']
            ]
            
            # Add duration limit if rendering preview (BEFORE the codec options)
            if preview_seconds:
                ffmpeg_cmd.extend(['-t', str(render_duration)])
            
            # Add codec and output options
            ffmpeg_cmd.extend([
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-shortest',
                '-y',
                output_path
            ])
            
            try:
                result = subprocess.run(
                    ffmpeg_cmd,
                    check=True,
                    capture_output=True,
                    text=True
                )
            except subprocess.CalledProcessError as e:
                # FFmpeg failed - log the error
                error_details = f"""
FFmpeg Error Details:
Command: {' '.join(ffmpeg_cmd)}
Return code: {e.returncode}

STDOUT:
{e.stdout}

STDERR:
{e.stderr}
"""
                print(error_details)
                
                # Clean up temp file
                try:
                    os.remove(temp_video_path)
                except:
                    pass
                
                # Raise with more details
                raise Exception(f"FFmpeg failed with code {e.returncode}.\n\nError output:\n{e.stderr}")
            
            os.remove(temp_video_path)
            
            self.root.after(0, lambda: self._render_complete(output_path))
            
        except Exception as error:
            error_msg = str(error)
            import traceback
            traceback.print_exc()
            self.root.after(0, lambda: self._render_error(error_msg))
    
    def _render_complete(self, output_path):
        """Handle successful render"""
        self.is_rendering = False
        self.controls.render_btn.config(state='normal')
        self.controls.quick_render_btn.config(state='normal')
        self.controls.preview_btn.config(state='normal')
        self.preview.set_info(MSG_RENDER_COMPLETE, "green")
        
        # Hide progress UI using grid_forget
        self.controls.progress_frame.grid_forget()
        self.controls.cancel_btn.grid_forget()
        
        from tkinter import messagebox
        result = messagebox.askyesno("Render Complete",
                                     f"Video saved to:\n{output_path}\n\nOpen in Finder?")
        if result:
            subprocess.run(['open', '-R', output_path])
    
    def _render_cancelled(self):
        """Handle cancelled render"""
        self.is_rendering = False
        self.cancel_render_flag = False
        self.controls.render_btn.config(state='normal')
        self.controls.quick_render_btn.config(state='normal')
        self.controls.preview_btn.config(state='normal')
        self.preview.set_info(MSG_RENDER_CANCELLED, "yellow")
        
        # Hide progress UI using grid_forget
        self.controls.progress_frame.grid_forget()
        self.controls.cancel_btn.grid_forget()
        
        from tkinter import messagebox
        messagebox.showinfo("Cancelled", "Render was cancelled.")
    
    def _render_error(self, error_msg):
        """Handle render error"""
        self.is_rendering = False
        self.controls.render_btn.config(state='normal')
        self.controls.quick_render_btn.config(state='normal')
        self.controls.preview_btn.config(state='normal')
        self.preview.set_info(MSG_RENDER_FAILED, "red")
        
        # Hide progress UI using grid_forget
        self.controls.progress_frame.grid_forget()
        self.controls.cancel_btn.grid_forget()
        
        from tkinter import messagebox
        messagebox.showerror("Render Error", f"Could not render video:\n{error_msg}")