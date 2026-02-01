"""
GUI Renderer (Hardware Accelerated)
Handles preview generation and full video rendering with GPU encoding
"""

import threading
import subprocess
import os
import sys
import tkinter as tk
import time

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

        self.render_start_time = None
        self.last_frame_time = None

    # ------------------------------------------------------------------
    # Preview
    # ------------------------------------------------------------------

    def generate_preview(self):
        if not self.controls.audio_path:
            return
        if self.preview_thread and self.preview_thread.is_alive():
            print("Preview already generating, skipping...")
            return

        self.preview.clear()
        self.preview.set_info("Generating Preview - Please Wait...", "blue")
        self.controls.preview_btn.config(state='disabled')

        self.preview_thread = threading.Thread(
            target=self._generate_preview_background, daemon=True
        )
        self.preview_thread.start()

    def _generate_preview_background(self):
        try:
            settings = self.controls.get_settings()
            w, h = settings['resolution']

            self.root.after(0, lambda: self.preview.set_info("Loading audio..."))

            vis = MusicVisualizer(
                audio_path=settings['audio_path'],
                cover_image_path=settings['cover_image_path'],
                fps=10,
                resolution=(w, h),
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
                starfield_direction=settings.get('starfield_direction', 'outward'),
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
                ring_stagger=settings.get('ring_stagger', 'none'),
            )

            self.root.after(0, lambda: self.preview.set_info("Rendering frame..."))

            frame_idx = min(
                len(vis.audio_processor.times) // 8,
                len(vis.audio_processor.times) - 1,
            )
            total_frames = len(vis.audio_processor.times)
            preview_img = vis.render_frame(frame_idx, total_frames)

            self.root.after(0, lambda: self._display_preview(preview_img))

        except Exception as err:
            import traceback
            traceback.print_exc()
            self.root.after(0, lambda: self._preview_error(str(err)))

    def _display_preview(self, img):
        self.preview.display_image(img)
        self.preview.set_info("Preview Ready - Hardware Acceleration Enabled", "green")
        self.controls.preview_btn.config(state='normal')

    def _preview_error(self, error_msg):
        self.preview.set_info(f"Error: {error_msg}", "red")
        self.controls.preview_btn.config(state='normal')
        from tkinter import messagebox
        messagebox.showerror("Preview Error", f"Could not generate preview:\n{error_msg}")

    # ------------------------------------------------------------------
    # Render lifecycle
    # ------------------------------------------------------------------

    def start_render(self, output_path, preview_seconds=None):
        if self.is_rendering:
            return False

        self.is_rendering = True
        self.cancel_render_flag = False
        self.render_start_time = time.time()
        self.last_frame_time = time.time()

        self.controls.render_btn.config(state='disabled')
        self.controls.quick_render_btn.config(state='disabled')
        self.controls.preview_btn.config(state='disabled')

        self.controls.progress_frame.grid(row=100, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        self.controls.cancel_btn.grid(row=101, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        self.controls.progress_bar['value'] = 0
        self.controls.progress_label.config(text=MSG_STARTING_RENDER)

        if preview_seconds:
            self.preview.set_info(f"Rendering {preview_seconds}s preview (GPU accelerated)... 0%")
        else:
            self.preview.set_info("Rendering full video (GPU accelerated)... 0%")

        self.render_thread = threading.Thread(
            target=self._render_video_background,
            args=(output_path, preview_seconds),
            daemon=True,
        )
        self.render_thread.start()
        return True

    def cancel_render(self):
        from tkinter import messagebox
        if messagebox.askyesno(
            "Cancel Render", "Are you sure you want to cancel the current render?"
        ):
            self.cancel_render_flag = True
            self.controls.progress_label.config(text=MSG_CANCELLING)

    # ------------------------------------------------------------------
    # Progress updates
    # ------------------------------------------------------------------

    def update_progress(self, current_frame, total_frames, visualizer=None):
        if self.cancel_render_flag:
            return False

        progress = int((current_frame / total_frames) * 100)

        current_time = time.time()
        elapsed = current_time - self.render_start_time

        if current_frame > 0:
            eta_seconds = (elapsed / current_frame) * (total_frames - current_frame)
            hours = int(eta_seconds // 3600)
            minutes = int((eta_seconds % 3600) // 60)
            seconds = int(eta_seconds % 60)
            eta_str = (
                f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                if hours > 0
                else f"{minutes:02d}:{seconds:02d}"
            )
            status_text = f"Frame {current_frame}/{total_frames} ({progress}%)\n{eta_str} remaining"
        else:
            status_text = f"Frame {current_frame}/{total_frames} ({progress}%)"

        self.root.after(0, lambda: self.controls.progress_bar.config(value=progress))
        self.root.after(0, lambda: self.controls.progress_label.config(text=status_text))
        self.root.after(
            0,
            lambda: self.preview.set_info(f"Rendering with GPU... {progress}% complete"),
        )

        # Live preview update every N frames (N = fps -> once per second)
        if self.controls.live_preview_var.get() and visualizer is not None:
            fps = self.controls.fps_var.get()
            if current_frame % fps == 0:
                try:
                    preview_img = visualizer.render_frame(current_frame - 1, total_frames)
                    self.root.after(0, lambda img=preview_img: self.preview.display_image(img))
                except Exception as e:
                    print(f"Error updating live preview: {e}")

        self.last_frame_time = current_time
        return True

    # ------------------------------------------------------------------
    # Main render thread
    # ------------------------------------------------------------------

    def _render_video_background(self, output_path, preview_seconds=None):
        process = None
        stderr_thread = None
        stderr_output = ['']  # list so the inner function can mutate it

        def _drain_stderr():
            """Read all of stderr so the pipe buffer never fills and blocks FFmpeg."""
            try:
                stderr_output[0] = process.stderr.read().decode('utf-8')
            except Exception:
                pass

        def _cleanup(terminate=False):
            """Best-effort cleanup of process and stderr thread."""
            if process is None:
                return
            if process.stdin and not process.stdin.closed:
                try:
                    process.stdin.close()
                except Exception:
                    pass
            if terminate and process.poll() is None:
                process.terminate()
            process.wait()
            if stderr_thread is not None:
                stderr_thread.join()

        try:
            settings = self.controls.get_settings()

            vis = MusicVisualizer(
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
                starfield_direction=settings.get('starfield_direction', 'outward'),
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
                ring_stagger=settings.get('ring_stagger', 'none'),
            )

            render_duration = vis.duration
            if preview_seconds:
                render_duration = min(preview_seconds, vis.duration)
            total_frames = int(render_duration * vis.fps)

            # Show a preview frame immediately
            prev_idx = min(
                len(vis.audio_processor.times) // 8,
                len(vis.audio_processor.times) - 1,
            )
            prev_img = vis.render_frame(prev_idx, total_frames)
            self.root.after(0, lambda: self.preview.display_image(prev_img))

            # Start FFmpeg
            ffmpeg_cmd = [
                'ffmpeg', '-y',
                '-f', 'rawvideo',
                '-vcodec', 'rawvideo',
                '-s', f'{vis.width}x{vis.height}',
                '-pix_fmt', 'rgb24',
                '-r', str(vis.fps),
                '-i', '-',
                '-i', settings['audio_path'],
                '-c:v', 'h264_videotoolbox',
                '-b:v', '8M',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-shortest',
                '-t', str(render_duration),
                output_path,
            ]

            try:
                process = subprocess.Popen(
                    ffmpeg_cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            except FileNotFoundError:
                raise Exception("FFmpeg not found. Please install: brew install ffmpeg")

            # Start draining stderr immediately so the pipe never blocks
            stderr_thread = threading.Thread(target=_drain_stderr, daemon=True)
            stderr_thread.start()

            # --- Frame loop ---
            for frame_idx in range(total_frames):
                # Check for cancellation
                if not self.update_progress(frame_idx + 1, total_frames, vis):
                    _cleanup(terminate=True)
                    self.root.after(0, self._render_cancelled)
                    return

                img = vis.render_frame(frame_idx, total_frames)

                try:
                    process.stdin.write(img.tobytes())
                except (BrokenPipeError, OSError):
                    # FFmpeg died while we were writing
                    _cleanup(terminate=False)
                    if self.cancel_render_flag:
                        self.root.after(0, self._render_cancelled)
                    else:
                        self.root.after(0, lambda: self._render_error(
                            "FFmpeg process terminated unexpectedly during frame write"
                        ))
                    return

            # --- All frames written ---
            process.stdin.close()

            self.root.after(0, lambda: self.controls.progress_label.config(
                text="Finalizing video...\n(encoding audio)"
            ))

            # Wait for FFmpeg to finish muxing. stderr_thread keeps the pipe drained
            # so this will not deadlock regardless of how much output FFmpeg produces.
            process.wait()
            stderr_thread.join()

            if process.returncode == 0:
                self.root.after(0, lambda: self._render_complete(output_path))
            else:
                err = f"FFmpeg error (code {process.returncode}):\n{stderr_output[0][-500:]}"
                self.root.after(0, lambda: self._render_error(err))

        except Exception as error:
            # If we got here with a live process, clean it up
            if process is not None and process.poll() is None:
                _cleanup(terminate=True)

            import traceback
            traceback.print_exc()
            self.root.after(0, lambda: self._render_error(str(error)))

    # ------------------------------------------------------------------
    # Render result callbacks (always called on the main thread via after())
    # ------------------------------------------------------------------

    def _render_complete(self, output_path):
        self.is_rendering = False
        self.controls.render_btn.config(state='normal')
        self.controls.quick_render_btn.config(state='normal')
        self.controls.preview_btn.config(state='normal')
        self.preview.set_info("Render Complete", "green")

        self.controls.progress_frame.grid_forget()
        self.controls.cancel_btn.grid_forget()

        from tkinter import messagebox
        if messagebox.askyesno(
            "Render Complete", f"Video saved to:\n{output_path}\n\nOpen in Finder?"
        ):
            subprocess.run(['open', '-R', output_path])

    def _render_cancelled(self):
        self.is_rendering = False
        self.cancel_render_flag = False
        self.controls.render_btn.config(state='normal')
        self.controls.quick_render_btn.config(state='normal')
        self.controls.preview_btn.config(state='normal')
        self.preview.set_info(MSG_RENDER_CANCELLED, "yellow")

        self.controls.progress_frame.grid_forget()
        self.controls.cancel_btn.grid_forget()

        from tkinter import messagebox
        messagebox.showinfo("Cancelled", "Render was cancelled.")

    def _render_error(self, error_msg):
        self.is_rendering = False
        self.controls.render_btn.config(state='normal')
        self.controls.quick_render_btn.config(state='normal')
        self.controls.preview_btn.config(state='normal')
        self.preview.set_info(MSG_RENDER_FAILED, "red")

        self.controls.progress_frame.grid_forget()
        self.controls.cancel_btn.grid_forget()

        from tkinter import messagebox
        messagebox.showerror("Render Error", f"Could not render video:\n{error_msg}")