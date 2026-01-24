"""
GUI Renderer (Hardware Accelerated)
Handles preview generation and full video rendering with GPU encoding
"""

import threading
import subprocess
import os
import sys
import tempfile
import tkinter as tk
import time

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
        
        # Time tracking for ETA
        self.render_start_time = None
        self.last_frame_time = None
    
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
        self.preview.set_info("Preview Ready - Hardware Acceleration Enabled 🚀", "green")
        self.controls.preview_btn.config(state='normal')
    
    def _preview_error(self, error_msg):
        """Handle preview generation error"""
        self.preview.set_info(f"Error: {error_msg}", "red")
        self.controls.preview_btn.config(state='normal')
        from tkinter import messagebox
        messagebox.showerror("Preview Error", f"Could not generate preview:\n{error_msg}")
    
    def start_render(self, output_path, preview_seconds=None):
        """Start full video render with hardware acceleration"""
        if self.is_rendering:
            return False
        
        self.is_rendering = True
        self.cancel_render_flag = False
        self.render_start_time = time.time()
        self.last_frame_time = time.time()
        
        self.controls.render_btn.config(state='disabled')
        self.controls.quick_render_btn.config(state='disabled')
        self.controls.preview_btn.config(state='disabled')
        
        # Show progress UI using grid instead of pack
        self.controls.progress_frame.grid(row=100, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        self.controls.cancel_btn.grid(row=101, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        self.controls.progress_bar['value'] = 0
        self.controls.progress_label.config(text=MSG_STARTING_RENDER)
        
        # Generate a preview frame to show during render
        if preview_seconds:
            self.preview.set_info(f"Rendering {preview_seconds}s preview (GPU accelerated)... 0%")
        else:
            self.preview.set_info("Rendering full video (GPU accelerated)... 0%")
        
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
    
    def update_progress(self, current_frame, total_frames, visualizer=None):
        """Update progress bar from render thread with ETA"""
        if self.cancel_render_flag:
            return False
        
        progress = int((current_frame / total_frames) * 100)
        
        # Calculate ETA
        current_time = time.time()
        elapsed = current_time - self.render_start_time
        
        if current_frame > 0:
            avg_time_per_frame = elapsed / current_frame
            frames_remaining = total_frames - current_frame
            eta_seconds = avg_time_per_frame * frames_remaining
            
            # Format ETA as hh:mm:ss
            hours = int(eta_seconds // 3600)
            minutes = int((eta_seconds % 3600) // 60)
            seconds = int(eta_seconds % 60)
            
            if hours > 0:
                eta_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                eta_str = f"{minutes:02d}:{seconds:02d}"
            
            # Split into two lines: progress on line 1, time on line 2
            status_text = f"Frame {current_frame}/{total_frames} ({progress}%)\n{eta_str} remaining"
        else:
            status_text = f"Frame {current_frame}/{total_frames} ({progress}%)"
        
        self.root.after(0, lambda: self.controls.progress_bar.config(value=progress))
        self.root.after(0, lambda: self.controls.progress_label.config(text=status_text))
        
        # Also update the preview info label with percentage
        self.root.after(0, lambda: self.preview.set_info(
            f"Rendering with GPU... {progress}% complete"
        ))
        
        # Update live preview if enabled and visualizer provided
        if self.controls.live_preview_var.get() and visualizer is not None:
            # Update every N frames based on FPS
            fps = self.controls.fps_var.get()
            if current_frame % fps == 0:
                try:
                    # Render current frame for preview
                    preview_img = visualizer.render_frame(current_frame - 1, total_frames)
                    self.root.after(0, lambda img=preview_img: self.preview.display_image(img))
                except Exception as e:
                    print(f"Error updating live preview: {e}")
        
        self.last_frame_time = current_time
        return True
    
    def _render_video_background(self, output_path, preview_seconds=None):
        """Background thread for hardware-accelerated rendering"""
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
            
            # Setup FFmpeg with hardware encoding (VideoToolbox for macOS)
            ffmpeg_cmd = [
                'ffmpeg',
                '-y',  # Overwrite output
                '-f', 'rawvideo',
                '-vcodec', 'rawvideo',
                '-s', f'{visualizer.width}x{visualizer.height}',
                '-pix_fmt', 'rgb24',
                '-r', str(visualizer.fps),
                '-i', '-',  # Read from stdin
                '-i', settings['audio_path'],  # Audio input
                '-c:v', 'h264_videotoolbox',  # Hardware encoder for macOS
                '-b:v', '8M',  # Bitrate
                '-c:a', 'aac',
                '-b:a', '192k',
                '-shortest',
                '-t', str(render_duration),  # Duration limit
                output_path
            ]
            
            # Start FFmpeg process
            try:
                process = subprocess.Popen(
                    ffmpeg_cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            except FileNotFoundError:
                raise Exception("FFmpeg not found. Please install: brew install ffmpeg")
            
            # Render frames and pipe to FFmpeg
            try:
                for frame_idx in range(total_frames):
                    if not self.update_progress(frame_idx + 1, total_frames, visualizer):
                        # Render was cancelled
                        try:
                            process.stdin.close()
                        except:
                            pass
                        process.terminate()
                        try:
                            process.wait(timeout=2)
                        except subprocess.TimeoutExpired:
                            process.kill()
                            process.wait()
                        self.root.after(0, self._render_cancelled)
                        return
                    
                    img = visualizer.render_frame(frame_idx, total_frames)
                    
                    # Convert PIL Image to raw RGB bytes
                    frame_bytes = img.tobytes()
                    
                    # Write to FFmpeg stdin
                    try:
                        process.stdin.write(frame_bytes)
                    except (BrokenPipeError, OSError):
                        # FFmpeg died, treat as cancelled
                        self.root.after(0, self._render_cancelled)
                        return
                
                # Close stdin to signal end of input
                try:
                    process.stdin.close()
                except:
                    pass
                
                # Wait for FFmpeg to finish with timeout
                self.root.after(0, lambda: self.controls.progress_label.config(
                    text="Finalizing video (encoding audio)..."))
                
                try:
                    stdout, stderr = process.communicate(timeout=30)
                    
                    if process.returncode == 0:
                        self.root.after(0, lambda: self._render_complete(output_path))
                    else:
                        stderr_output = stderr.decode('utf-8') if stderr else "No error output"
                        error_msg = f"FFmpeg error (code {process.returncode}):\n{stderr_output[-500:]}"
                        self.root.after(0, lambda: self._render_error(error_msg))
                except subprocess.TimeoutExpired:
                    # FFmpeg taking longer - wait without timeout
                    stdout, stderr = process.communicate()
                    if process.returncode == 0:
                        self.root.after(0, lambda: self._render_complete(output_path))
                    else:
                        error_msg = "FFmpeg timeout/error"
                        self.root.after(0, lambda: self._render_error(error_msg))
                        
            except BrokenPipeError:
                # FFmpeg closed early - might be cancelled or error
                try:
                    process.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
                
                # Check if it was a cancellation
                if self.cancel_render_flag:
                    self.root.after(0, self._render_cancelled)
                    return
                
                # Otherwise check if file exists and has content
                import os
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    self.root.after(0, lambda: self._render_complete(output_path))
                else:
                    error_msg = "FFmpeg closed unexpectedly"
                    self.root.after(0, lambda: self._render_error(error_msg))
                    
            except Exception as e:
                try:
                    process.stdin.close()
                except:
                    pass
                process.terminate()
                try:
                    process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
                
                # Check if it was a cancellation
                if self.cancel_render_flag:
                    self.root.after(0, self._render_cancelled)
                    return
                
                raise e
            
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
        self.preview.set_info("✅ Render Complete (Hardware Accelerated)", "green")
        
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