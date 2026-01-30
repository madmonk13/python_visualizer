"""
Starfield effect module
Handles starfield particle system and rendering
"""

import numpy as np
import math
from PIL import Image, ImageDraw


class StarfieldEffect:
    def __init__(self, width, height, is_preview=False):
        self.width = width
        self.height = height
        self.is_preview = is_preview
        self.stars = []
        self._init_starfield()
    
    def _init_starfield(self):
        """Initialize starfield particles"""
        num_stars = 100 if self.is_preview else 200
        for _ in range(num_stars):
            self.stars.append({
                'x': np.random.rand() * self.width,
                'y': np.random.rand() * self.height,
                'z': np.random.rand() * 2,  # Depth
                'size': np.random.randint(1, 4)
            })
    
    def update(self, volume_intensity, rotation_mode='none', direction='outward'):
        """Update starfield positions based on volume, rotation, and direction"""
        speed = 0.5 + volume_intensity * 5.5
        center_x, center_y = self.width / 2, self.height / 2
        
        # Direction multiplier: 1 for outward, -1 for inward
        direction_multiplier = 1 if direction == 'outward' else -1
        
        for star in self.stars:
            # Apply rotation if enabled
            if rotation_mode == 'cw':
                angle = math.atan2(star['y'] - center_y, star['x'] - center_x)
                angle -= speed * 0.01 * star['z']
                distance = math.sqrt((star['x'] - center_x)**2 + (star['y'] - center_y)**2)
                star['x'] = center_x + distance * math.cos(angle)
                star['y'] = center_y + distance * math.sin(angle)
            elif rotation_mode == 'ccw':
                angle = math.atan2(star['y'] - center_y, star['x'] - center_x)
                angle += speed * 0.01 * star['z']
                distance = math.sqrt((star['x'] - center_x)**2 + (star['y'] - center_y)**2)
                star['x'] = center_x + distance * math.cos(angle)
                star['y'] = center_y + distance * math.sin(angle)
            
            # Move stars based on direction
            dx = star['x'] - center_x
            dy = star['y'] - center_y
            
            distance = math.sqrt(dx*dx + dy*dy)
            if distance > 0:
                # Apply direction multiplier
                star['x'] += (dx / distance) * speed * star['z'] * direction_multiplier
                star['y'] += (dy / distance) * speed * star['z'] * direction_multiplier
            
            # Wrap around edges (different logic for inward vs outward)
            if direction == 'outward':
                # For outward: respawn at center when leaving edges
                if (star['x'] < 0 or star['x'] > self.width or 
                    star['y'] < 0 or star['y'] > self.height):
                    star['x'] = center_x + np.random.randn() * 50
                    star['y'] = center_y + np.random.randn() * 50
                    star['z'] = np.random.rand() * 2
            else:
                # For inward: respawn at edges when reaching center
                if distance < 50:  # Close to center
                    # Spawn at random edge
                    edge = np.random.randint(0, 4)
                    if edge == 0:  # Top
                        star['x'] = np.random.rand() * self.width
                        star['y'] = 0
                    elif edge == 1:  # Right
                        star['x'] = self.width
                        star['y'] = np.random.rand() * self.height
                    elif edge == 2:  # Bottom
                        star['x'] = np.random.rand() * self.width
                        star['y'] = self.height
                    else:  # Left
                        star['x'] = 0
                        star['y'] = np.random.rand() * self.height
                    star['z'] = np.random.rand() * 2
    
    def draw(self, img, volume_intensity):
        """Draw the starfield with white stars"""
        star_layer = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(star_layer)
        
        for star in self.stars:
            brightness = int(150 + star['z'] * 50)
            star_color = (255, 255, 255)
            
            x, y = int(star['x']), int(star['y'])
            size = star['size']
            
            # Draw star with glow
            for glow in range(3, 0, -1):
                glow_alpha = int(brightness * 0.3 * (1 - glow / 3))
                draw.ellipse([x - size - glow, y - size - glow, 
                             x + size + glow, y + size + glow],
                            fill=(*star_color, glow_alpha))
            
            # Draw core
            draw.ellipse([x - size, y - size, x + size, y + size],
                        fill=(*star_color, brightness))
        
        img.paste(star_layer, (0, 0), star_layer)