import pygame
import random
import math
import time
import os

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Enhanced Colors (Tech-noir palette with more depth)
BLACK = (0, 0, 0)
DARK_GRAY = (15, 15, 20)
DARKER_GRAY = (8, 8, 12)
CYAN = (0, 255, 255)
NEON_GREEN = (57, 255, 20)
NEON_BLUE = (0, 191, 255)
NEON_PINK = (255, 20, 147)
NEON_PURPLE = (138, 43, 226)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)

# Game settings
GRID_SIZE = 32
MAZE_WIDTH = SCREEN_WIDTH // GRID_SIZE
MAZE_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
ECHO_RADIUS = 150
ECHO_DURATION = 2000  # milliseconds
PLAYER_SPEED = 4

class SoundManager:
    def __init__(self):
        self.sound_enabled = False
        self.sounds = {}
        
        try:
            # Initialize pygame mixer with specific settings
            pygame.mixer.quit()  # Ensure clean state
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
            pygame.mixer.init()
            
            # Test if we can create sounds
            self.create_sound_library()
            self.sound_enabled = True
            print("Sound system initialized successfully with working sounds")
            
        except Exception as e:
            print(f"Sound system failed: {e}")
            self.sound_enabled = False
    
    def create_sound_library(self):
        """Create all sound effects using numpy for better compatibility"""
        try:
            import numpy as np
            
            # Sound parameters
            sample_rate = 22050
            
            # Create each sound effect
            self.sounds['echo'] = self.create_echo_sound(sample_rate)
            self.sounds['collect'] = self.create_collect_sound(sample_rate)
            self.sounds['chest'] = self.create_chest_sound(sample_rate)
            self.sounds['terminal'] = self.create_terminal_sound(sample_rate)
            self.sounds['code'] = self.create_code_sound(sample_rate)
            self.sounds['trap'] = self.create_trap_sound(sample_rate)
            self.sounds['death'] = self.create_death_sound(sample_rate)
            self.sounds['victory'] = self.create_victory_sound(sample_rate)
            
            print(f"Created {len(self.sounds)} sound effects")
            
        except ImportError:
            print("NumPy not available, using fallback sound creation")
            self.create_fallback_sounds()
        except Exception as e:
            print(f"Sound creation failed: {e}")
            raise
    
    def create_echo_sound(self, sample_rate):
        """Create echo ping sound"""
        import numpy as np
        
        duration = 0.3
        frequency = 800
        frames = int(sample_rate * duration)
        
        t = np.linspace(0, duration, frames, False)
        
        # Ping with exponential decay
        wave = np.sin(frequency * 2 * np.pi * t) * np.exp(-t * 8)
        wave = wave * 0.3  # Volume
        
        # Convert to stereo 16-bit
        wave_16 = (wave * 32767).astype(np.int16)
        stereo_wave = np.column_stack((wave_16, wave_16))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def create_collect_sound(self, sample_rate):
        """Create item collection sound"""
        import numpy as np
        
        duration = 0.4
        frames = int(sample_rate * duration)
        t = np.linspace(0, duration, frames, False)
        
        # Rising tone
        frequency = 400 + 600 * (t / duration)
        wave = np.sin(frequency * 2 * np.pi * t) * (1 - t / duration)
        wave = wave * 0.25
        
        wave_16 = (wave * 32767).astype(np.int16)
        stereo_wave = np.column_stack((wave_16, wave_16))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def create_chest_sound(self, sample_rate):
        """Create chest opening sound"""
        import numpy as np
        
        duration = 0.6
        frames = int(sample_rate * duration)
        t = np.linspace(0, duration, frames, False)
        
        # Mechanical sound with modulation
        base_freq = 200
        mod_freq = 100 * np.sin(t * 20)
        wave = np.sin((base_freq + mod_freq) * 2 * np.pi * t) * np.exp(-t * 2)
        
        # Add some noise for mechanical effect
        noise = np.random.uniform(-0.05, 0.05, frames)
        wave = wave * 0.3 + noise
        
        wave_16 = (wave * 32767).astype(np.int16)
        stereo_wave = np.column_stack((wave_16, wave_16))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def create_terminal_sound(self, sample_rate):
        """Create terminal solve sound"""
        import numpy as np
        
        duration = 0.8
        frames = int(sample_rate * duration)
        t = np.linspace(0, duration, frames, False)
        
        # Electronic beeping sequence
        beep_pattern = np.where((t * 8) % 2 < 1, 600, 800)
        wave = np.sin(beep_pattern * 2 * np.pi * t) * (1 - t / duration)
        wave = wave * 0.2
        
        wave_16 = (wave * 32767).astype(np.int16)
        stereo_wave = np.column_stack((wave_16, wave_16))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def create_code_sound(self, sample_rate):
        """Create code discovery sound"""
        import numpy as np
        
        duration = 0.5
        frames = int(sample_rate * duration)
        t = np.linspace(0, duration, frames, False)
        
        # Digital, mysterious sound
        frequency = 1000 + 500 * np.sin(t * 15)
        wave = np.sin(frequency * 2 * np.pi * t) * (1 - t / duration)
        wave = wave * 0.15
        
        wave_16 = (wave * 32767).astype(np.int16)
        stereo_wave = np.column_stack((wave_16, wave_16))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def create_trap_sound(self, sample_rate):
        """Create trap trigger sound"""
        import numpy as np
        
        duration = 1.0
        frames = int(sample_rate * duration)
        t = np.linspace(0, duration, frames, False)
        
        # Harsh, dangerous sound
        frequency = 150 + 50 * np.sin(t * 30)
        wave = np.sin(frequency * 2 * np.pi * t) * np.exp(-t * 1.5)
        
        # Add distortion
        wave = np.tanh(wave * 3) * 0.4
        
        wave_16 = (wave * 32767).astype(np.int16)
        stereo_wave = np.column_stack((wave_16, wave_16))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def create_death_sound(self, sample_rate):
        """Create death sound"""
        import numpy as np
        
        duration = 1.5
        frames = int(sample_rate * duration)
        t = np.linspace(0, duration, frames, False)
        
        # Descending, ominous sound
        frequency = 300 - 250 * (t / duration)
        wave = np.sin(frequency * 2 * np.pi * t) * np.exp(-t * 0.8)
        wave = wave * 0.3
        
        wave_16 = (wave * 32767).astype(np.int16)
        stereo_wave = np.column_stack((wave_16, wave_16))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def create_victory_sound(self, sample_rate):
        """Create victory sound"""
        import numpy as np
        
        duration = 2.0
        frames = int(sample_rate * duration)
        t = np.linspace(0, duration, frames, False)
        
        # Triumphant ascending melody
        base_freq = 400 + 200 * (t / duration)
        melody = 100 * np.sin(t * 8)
        frequency = base_freq + melody
        
        wave = np.sin(frequency * 2 * np.pi * t) * (1 - t / duration * 0.5)
        wave = wave * 0.3
        
        wave_16 = (wave * 32767).astype(np.int16)
        stereo_wave = np.column_stack((wave_16, wave_16))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def create_fallback_sounds(self):
        """Create simple fallback sounds without numpy"""
        import array
        
        sample_rate = 22050
        
        # Simple beep sounds
        sound_configs = {
            'echo': (800, 0.3),
            'collect': (600, 0.4),
            'chest': (400, 0.6),
            'terminal': (700, 0.8),
            'code': (1000, 0.5),
            'trap': (200, 1.0),
            'death': (150, 1.5),
            'victory': (500, 2.0)
        }
        
        for sound_name, (frequency, duration) in sound_configs.items():
            frames = int(sample_rate * duration)
            sound_array = array.array('h')
            
            for i in range(frames):
                t = i / sample_rate
                envelope = max(0, 1.0 - (t / duration))
                sample = int(0.2 * envelope * 32767 * math.sin(2 * math.pi * frequency * t))
                
                # Stereo (left, right)
                sound_array.append(sample)
                sound_array.append(sample)
            
            try:
                self.sounds[sound_name] = pygame.sndarray.make_sound(sound_array)
            except Exception as e:
                print(f"Failed to create fallback sound {sound_name}: {e}")
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if not self.sound_enabled or sound_name not in self.sounds:
            return
            
        try:
            sound = self.sounds[sound_name]
            if sound:
                sound.set_volume(0.7)  # Set volume to 70%
                channel = sound.play()
                if channel:
                    print(f"Playing sound: {sound_name}")
                else:
                    print(f"Failed to get channel for: {sound_name}")
            else:
                print(f"Sound {sound_name} is None")
                
        except Exception as e:
            print(f"Error playing sound {sound_name}: {e}")

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 16
        self.last_echo_time = 0
        
    def move(self, dx, dy, maze):
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Check collision with walls
        grid_x = int(new_x // GRID_SIZE)
        grid_y = int(new_y // GRID_SIZE)
        
        if (0 <= grid_x < MAZE_WIDTH and 0 <= grid_y < MAZE_HEIGHT and 
            maze[grid_y][grid_x] == 0):
            self.x = new_x
            self.y = new_y
    
    def emit_echo(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_echo_time > 500:  # Cooldown
            self.last_echo_time = current_time
            return True
        return False
    
    def draw(self, screen):
        # Create layered glow effect
        glow_layers = [
            (self.size + 8, 30),   # Outer glow
            (self.size + 4, 60),   # Middle glow
            (self.size + 2, 100)   # Inner glow
        ]
        
        for glow_size, alpha in glow_layers:
            glow_surface = pygame.Surface((glow_size * 2, glow_size * 2))
            glow_surface.set_alpha(alpha)
            pygame.draw.circle(glow_surface, CYAN, (glow_size, glow_size), glow_size)
            screen.blit(glow_surface, (self.x - glow_size, self.y - glow_size))
        
        # Main player circle with gradient effect
        pygame.draw.circle(screen, NEON_BLUE, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (100, 200, 255), (int(self.x), int(self.y)), self.size - 2)
        
        # Inner core with pulsing effect
        pulse = abs(math.sin(time.time() * 3)) * 0.3 + 0.7
        inner_size = int((self.size - 6) * pulse)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), inner_size)
        pygame.draw.circle(screen, NEON_BLUE, (int(self.x), int(self.y)), inner_size - 2)
        
        # Outer ring with enhanced glow
        pygame.draw.circle(screen, CYAN, (int(self.x), int(self.y)), self.size + 2, 3)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size + 1, 1)
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 16
        self.last_echo_time = 0
        
    def move(self, dx, dy, maze):
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Check collision with walls
        grid_x = int(new_x // GRID_SIZE)
        grid_y = int(new_y // GRID_SIZE)
        
        if (0 <= grid_x < MAZE_WIDTH and 0 <= grid_y < MAZE_HEIGHT and 
            maze[grid_y][grid_x] == 0):
            self.x = new_x
            self.y = new_y
    
    def emit_echo(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_echo_time > 500:  # Cooldown
            self.last_echo_time = current_time
            return True
        return False
    
    def draw(self, screen):
        # Create layered glow effect
        glow_layers = [
            (self.size + 8, 30),   # Outer glow
            (self.size + 4, 60),   # Middle glow
            (self.size + 2, 100)   # Inner glow
        ]
        
        for glow_size, alpha in glow_layers:
            glow_surface = pygame.Surface((glow_size * 2, glow_size * 2))
            glow_surface.set_alpha(alpha)
            pygame.draw.circle(glow_surface, CYAN, (glow_size, glow_size), glow_size)
            screen.blit(glow_surface, (self.x - glow_size, self.y - glow_size))
        
        # Main player circle with gradient effect
        pygame.draw.circle(screen, NEON_BLUE, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (100, 200, 255), (int(self.x), int(self.y)), self.size - 2)
        
        # Inner core with pulsing effect
        pulse = abs(math.sin(time.time() * 3)) * 0.3 + 0.7
        inner_size = int((self.size - 6) * pulse)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), inner_size)
        pygame.draw.circle(screen, NEON_BLUE, (int(self.x), int(self.y)), inner_size - 2)
        
        # Outer ring with enhanced glow
        pygame.draw.circle(screen, CYAN, (int(self.x), int(self.y)), self.size + 2, 3)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size + 1, 1)

class GameObject:
    def __init__(self, x, y, obj_type, color, size=12):
        self.x = x
        self.y = y
        self.type = obj_type
        self.color = color
        self.size = size
        self.collected = False
        self.unlocked = False
        self.pulse_time = 0
        self.triggered = False  # For traps
        
    def get_label(self, game_inventory=None, game_codes=None):
        if self.type == "small_key":
            return "Small Key - Use to open first chest"
        elif self.type == "large_key":
            return "Large Key - Needed for Terminal 3"
        elif self.type == "document":
            return "Document - Needed for Terminal 2"
        elif self.type == "tool":
            return "Tool - Use to open third chest"
        elif self.type == "chest":
            return self.get_chest_label(game_inventory)
        elif self.type == "terminal":
            return self.get_terminal_label(game_inventory, game_codes)
        elif self.type == "code_puzzle":
            return "Code Puzzle - Interact to reveal terminal code"
        elif self.type == "exit":
            return "EXIT - Escape to victory!"
        elif self.type.startswith("trap_") and self.triggered:
            trap_names = {
                "trap_spike": "Spike Trap",
                "trap_laser": "Laser Grid", 
                "trap_shock": "Electric Trap",
                "trap_pit": "Pit Trap",
                "trap_gas": "Gas Trap",
                "trap_blade": "Blade Trap",
                "trap_fire": "Fire Trap"
            }
            return trap_names.get(self.type, "Trap")
        else:
            return ""
    
    def get_chest_label(self, inventory):
        if self.unlocked:
            return "Open Chest - Already looted"
        else:
            if not inventory:
                return "Locked Chest - Need small key"
            elif "small_key" in inventory and "document" not in inventory:
                return "Locked Chest - Use small key to open"
            elif "document" in inventory and "tool" not in inventory:
                return "Locked Chest - Use document to open"
            elif "tool" in inventory and "large_key" not in inventory:
                return "Locked Chest - Use tool to open"
            else:
                return "Locked Chest - Need correct item"
    
    def get_terminal_label(self, inventory, codes):
        if not codes:
            return "Terminal - Need code from puzzle"
        elif "2048" in codes:
            return "Terminal - Use code 2048"
        elif "ECHO" in codes:
            if "document" in inventory:
                return "Terminal - Use code ECHO + document"
            else:
                return "Terminal - Need code ECHO + document"
        elif "NEURAL" in codes:
            if "large_key" in inventory:
                return "Terminal - Use code NEURAL + large key"
            else:
                return "Terminal - Need code NEURAL + large key"
        else:
            return "Terminal - Need correct code + items"
        
    def draw(self, screen, visible=True, show_label=False, font=None, game_inventory=None, game_codes=None):
        if not self.collected and visible:
            # Add pulsing effect
            self.pulse_time += 0.1
            pulse = abs(math.sin(self.pulse_time)) * 0.3 + 0.7
            
            if self.type == "small_key":
                # Enhanced small key with green glow
                glow_layers = [(self.size * 2, 40), (self.size * 1.5, 80)]
                for glow_size, alpha in glow_layers:
                    glow_surface = pygame.Surface((glow_size * 2, glow_size * 2))
                    glow_surface.set_alpha(int(alpha * pulse))
                    pygame.draw.circle(glow_surface, self.color, (glow_size, glow_size), glow_size)
                    screen.blit(glow_surface, (self.x - glow_size, self.y - glow_size))
                
                # Key head with gradient
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
                pygame.draw.circle(screen, (100, 255, 100), (int(self.x), int(self.y)), self.size - 2)
                pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size, 3)
                
                # Key shaft with 3D effect
                shaft_rect = pygame.Rect(self.x - 4, self.y - self.size, 8, self.size)
                pygame.draw.rect(screen, self.color, shaft_rect)
                pygame.draw.rect(screen, (100, 255, 100), (self.x - 3, self.y - self.size + 1, 6, self.size - 2))
                pygame.draw.rect(screen, WHITE, shaft_rect, 2)
                
                # Enhanced key teeth
                teeth_points = [
                    (self.x + 4, self.y - self.size + 4),
                    (self.x + 10, self.y - self.size + 4),
                    (self.x + 10, self.y - self.size + 8),
                    (self.x + 4, self.y - self.size + 8)
                ]
                pygame.draw.polygon(screen, self.color, teeth_points)
                pygame.draw.polygon(screen, WHITE, teeth_points, 2)
                
            elif self.type == "large_key":
                # Enhanced large key with golden glow
                glow_layers = [(self.size * 2.5, 50), (self.size * 2, 100)]
                for glow_size, alpha in glow_layers:
                    glow_surface = pygame.Surface((glow_size * 2, glow_size * 2))
                    glow_surface.set_alpha(int(alpha * pulse))
                    pygame.draw.circle(glow_surface, GOLD, (glow_size, glow_size), glow_size)
                    screen.blit(glow_surface, (self.x - glow_size, self.y - glow_size))
                
                # Key head with metallic gradient
                pygame.draw.circle(screen, GOLD, (int(self.x), int(self.y)), self.size)
                pygame.draw.circle(screen, (255, 235, 100), (int(self.x), int(self.y)), self.size - 2)
                pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size, 4)
                pygame.draw.circle(screen, GOLD, (int(self.x), int(self.y)), self.size - 4, 3)
                
                # Ornate shaft
                shaft_rect = pygame.Rect(self.x - 6, self.y - self.size, 12, self.size)
                pygame.draw.rect(screen, GOLD, shaft_rect)
                pygame.draw.rect(screen, (255, 235, 100), (self.x - 5, self.y - self.size + 1, 10, self.size - 2))
                pygame.draw.rect(screen, WHITE, shaft_rect, 3)
                
                # Elaborate teeth with details
                teeth_points = [
                    (self.x + 6, self.y - self.size + 3),
                    (self.x + 14, self.y - self.size + 3),
                    (self.x + 14, self.y - self.size + 6),
                    (self.x + 11, self.y - self.size + 6),
                    (self.x + 11, self.y - self.size + 9),
                    (self.x + 14, self.y - self.size + 9),
                    (self.x + 14, self.y - self.size + 12),
                    (self.x + 6, self.y - self.size + 12)
                ]
                pygame.draw.polygon(screen, GOLD, teeth_points)
                pygame.draw.polygon(screen, WHITE, teeth_points, 2)
                
            elif self.type == "document":
                # Enhanced document with paper texture
                glow_size = int(self.size * 1.5 * pulse)
                glow_surface = pygame.Surface((glow_size * 2, glow_size * 2))
                glow_surface.set_alpha(60)
                pygame.draw.rect(glow_surface, SILVER, (0, 0, glow_size * 2, glow_size * 2))
                screen.blit(glow_surface, (self.x - glow_size, self.y - glow_size))
                
                # Main document with shadow
                shadow_rect = pygame.Rect(self.x - self.size + 2, self.y - self.size + 2, 
                                         self.size * 2, self.size * 2)
                pygame.draw.rect(screen, (50, 50, 50), shadow_rect)
                
                doc_rect = pygame.Rect(self.x - self.size, self.y - self.size, 
                                      self.size * 2, self.size * 2)
                pygame.draw.rect(screen, self.color, doc_rect)
                pygame.draw.rect(screen, WHITE, (self.x - self.size + 2, self.y - self.size + 2, 
                                               self.size * 2 - 4, self.size * 2 - 4))
                pygame.draw.rect(screen, DARK_GRAY, doc_rect, 3)
                
                # Enhanced text lines with varying lengths
                line_data = [(0.8, 3), (0.6, 6), (0.9, 9), (0.4, 12)]
                for width_factor, y_offset in line_data:
                    line_width = int(self.size * width_factor)
                    line_y = self.y - self.size + y_offset
                    pygame.draw.line(screen, DARK_GRAY, 
                                   (self.x - line_width//2, line_y), 
                                   (self.x + line_width//2, line_y), 2)
                
            elif self.type == "tool":
                # Enhanced tool with metallic finish
                glow_size = int(self.size * 1.4 * pulse)
                glow_surface = pygame.Surface((glow_size * 2, glow_size * 2))
                glow_surface.set_alpha(70)
                pygame.draw.circle(glow_surface, (200, 100, 50), (glow_size, glow_size), glow_size)
                screen.blit(glow_surface, (self.x - glow_size, self.y - glow_size))
                
                # Tool handle with grip texture
                handle_rect = pygame.Rect(self.x - 3, self.y - self.size, 6, self.size * 2)
                pygame.draw.rect(screen, self.color, handle_rect)
                pygame.draw.rect(screen, (200, 100, 50), (self.x - 2, self.y - self.size + 2, 4, self.size * 2 - 4))
                
                # Grip lines
                for i in range(4):
                    grip_y = self.y - self.size//2 + i * 4
                    pygame.draw.line(screen, (100, 50, 25), (self.x - 2, grip_y), (self.x + 2, grip_y), 1)
                
                # Tool head with metallic shine
                head_rect = pygame.Rect(self.x - self.size, self.y - self.size//2, 
                                       self.size * 2, self.size)
                pygame.draw.rect(screen, self.color, head_rect)
                pygame.draw.rect(screen, (200, 100, 50), (self.x - self.size + 2, self.y - self.size//2 + 2, 
                                                         self.size * 2 - 4, self.size - 4))
                pygame.draw.rect(screen, WHITE, head_rect, 3)
                
                # Tool details with shine
                pygame.draw.circle(screen, SILVER, (int(self.x - self.size//2), int(self.y)), 3)
                pygame.draw.circle(screen, WHITE, (int(self.x - self.size//2), int(self.y)), 3, 1)
                pygame.draw.circle(screen, SILVER, (int(self.x + self.size//2), int(self.y)), 3)
                pygame.draw.circle(screen, WHITE, (int(self.x + self.size//2), int(self.y)), 3, 1)
                # Enhanced key shape with glow
                glow_size = int(self.size * 1.5 * pulse)
                pygame.draw.circle(screen, (*self.color, 100), (int(self.x), int(self.y)), glow_size)
                
                # Key head (circle)
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
                pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size, 2)
                
                # Key shaft
                shaft_rect = pygame.Rect(self.x - 4, self.y - self.size, 8, self.size)
                pygame.draw.rect(screen, self.color, shaft_rect)
                pygame.draw.rect(screen, WHITE, shaft_rect, 2)
                
                # Key teeth
                teeth_points = [
                    (self.x + 4, self.y - self.size + 4),
                    (self.x + 8, self.y - self.size + 4),
                    (self.x + 8, self.y - self.size + 8),
                    (self.x + 4, self.y - self.size + 8)
                ]
                pygame.draw.polygon(screen, self.color, teeth_points)
                
            elif self.type == "chest":
                # Enhanced chest with 3D effect and glow
                glow_size = int(self.size * 1.8 * pulse)
                glow_surface = pygame.Surface((glow_size * 2, glow_size * 2))
                glow_surface.set_alpha(50)
                pygame.draw.rect(glow_surface, NEON_PINK, (0, 0, glow_size * 2, glow_size * 2))
                screen.blit(glow_surface, (self.x - glow_size, self.y - glow_size))
                
                # Shadow
                shadow_rect = pygame.Rect(self.x - self.size + 3, self.y - self.size + 3, 
                                         self.size * 2, self.size * 2)
                pygame.draw.rect(screen, (30, 30, 30), shadow_rect)
                
                # Main chest body with gradient
                base_rect = pygame.Rect(self.x - self.size, self.y - self.size, 
                                       self.size * 2, self.size * 2)
                pygame.draw.rect(screen, self.color, base_rect)
                pygame.draw.rect(screen, (255, 100, 200), (self.x - self.size + 2, self.y - self.size + 2, 
                                                          self.size * 2 - 4, self.size * 2 - 4))
                pygame.draw.rect(screen, WHITE, base_rect, 4)
                
                # Chest lid with metallic bands
                lid_rect = pygame.Rect(self.x - self.size, self.y - self.size, 
                                      self.size * 2, self.size)
                pygame.draw.rect(screen, (255, 150, 220), lid_rect)
                pygame.draw.rect(screen, WHITE, lid_rect, 3)
                
                # Metallic bands
                for i in range(3):
                    band_y = self.y - self.size + 2 + i * 6
                    pygame.draw.line(screen, SILVER, (self.x - self.size + 4, band_y), 
                                   (self.x + self.size - 4, band_y), 2)
                
                # Lock or keyhole with enhanced detail
                if not self.unlocked:
                    # Lock body
                    pygame.draw.circle(screen, (150, 0, 0), (int(self.x), int(self.y)), 8)
                    pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), 8, 3)
                    pygame.draw.circle(screen, (200, 50, 50), (int(self.x), int(self.y)), 6)
                    
                    # Keyhole with depth
                    pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), 4)
                    pygame.draw.circle(screen, (50, 50, 50), (int(self.x), int(self.y)), 3)
                    pygame.draw.rect(screen, BLACK, (self.x - 2, self.y, 4, 6))
                    pygame.draw.rect(screen, (50, 50, 50), (self.x - 1, self.y + 1, 2, 4))
                else:
                    # Open chest indicator with sparkle effect
                    pygame.draw.circle(screen, NEON_GREEN, (int(self.x), int(self.y)), 6)
                    pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 6, 2)
                    
                    # Sparkle effects
                    for i in range(4):
                        angle = i * 90 + time.time() * 100
                        rad = math.radians(angle)
                        spark_x = self.x + math.cos(rad) * 10
                        spark_y = self.y + math.sin(rad) * 10
                        pygame.draw.circle(screen, WHITE, (int(spark_x), int(spark_y)), 2)
                    
            elif self.type == "terminal":
                # Enhanced terminal with holographic screen effect
                glow_size = int(self.size * 1.6 * pulse)
                glow_surface = pygame.Surface((glow_size * 2, glow_size * 2))
                glow_surface.set_alpha(60)
                pygame.draw.rect(glow_surface, self.color, (0, 0, glow_size * 2, glow_size * 2))
                screen.blit(glow_surface, (self.x - glow_size, self.y - glow_size))
                
                # Terminal base with depth
                shadow_rect = pygame.Rect(self.x - self.size + 2, self.y - self.size + 2, 
                                         self.size * 2, self.size * 2)
                pygame.draw.rect(screen, (40, 40, 40), shadow_rect)
                
                base_rect = pygame.Rect(self.x - self.size, self.y - self.size, 
                                       self.size * 2, self.size * 2)
                pygame.draw.rect(screen, GRAY, base_rect)
                pygame.draw.rect(screen, (160, 160, 160), (self.x - self.size + 2, self.y - self.size + 2, 
                                                          self.size * 2 - 4, self.size * 2 - 4))
                pygame.draw.rect(screen, WHITE, base_rect, 4)
                
                # Screen with holographic effect
                screen_rect = pygame.Rect(self.x - self.size + 6, self.y - self.size + 6, 
                                         self.size * 2 - 12, self.size * 2 - 12)
                pygame.draw.rect(screen, BLACK, screen_rect)
                pygame.draw.rect(screen, self.color, screen_rect, 3)
                
                # Screen glow layers
                for i in range(3):
                    glow_rect = pygame.Rect(self.x - self.size + 4 - i, self.y - self.size + 4 - i, 
                                           self.size * 2 - 8 + i*2, self.size * 2 - 8 + i*2)
                    glow_surface = pygame.Surface((glow_rect.width, glow_rect.height))
                    glow_surface.set_alpha(30 - i*10)
                    pygame.draw.rect(glow_surface, self.color, (0, 0, glow_rect.width, glow_rect.height))
                    screen.blit(glow_surface, (glow_rect.x, glow_rect.y))
                
                # Animated terminal text lines
                for i in range(4):
                    line_y = self.y - self.size + 10 + i * 5
                    line_alpha = int(150 + 100 * math.sin(time.time() * 2 + i))
                    line_color = (*self.color[:3], line_alpha) if len(self.color) == 4 else self.color
                    
                    # Simulate text with varying line lengths
                    line_length = self.size - 8 - (i % 2) * 4
                    pygame.draw.line(screen, self.color, 
                                   (self.x - line_length//2, line_y), 
                                   (self.x + line_length//2, line_y), 2)
                
                # Corner LEDs
                led_positions = [(-self.size + 4, -self.size + 4), (self.size - 4, -self.size + 4),
                               (-self.size + 4, self.size - 4), (self.size - 4, self.size - 4)]
                for led_x, led_y in led_positions:
                    pygame.draw.circle(screen, NEON_GREEN, (int(self.x + led_x), int(self.y + led_y)), 2)
                    pygame.draw.circle(screen, WHITE, (int(self.x + led_x), int(self.y + led_y)), 2, 1)
                
            elif self.type == "code_puzzle":
                # Enhanced code puzzle with holographic circuit pattern
                glow_layers = [(self.size * 1.8, 40), (self.size * 1.4, 80)]
                for glow_size, alpha in glow_layers:
                    glow_surface = pygame.Surface((glow_size * 2, glow_size * 2))
                    glow_surface.set_alpha(int(alpha * pulse))
                    pygame.draw.circle(glow_surface, self.color, (glow_size, glow_size), glow_size)
                    screen.blit(glow_surface, (self.x - glow_size, self.y - glow_size))
                
                # Main circle with depth
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
                pygame.draw.circle(screen, (100, 255, 255), (int(self.x), int(self.y)), self.size - 2)
                pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.size - 6)
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size, 3)
                
                # Animated circuit pattern
                center_x, center_y = int(self.x), int(self.y)
                time_offset = time.time() * 50
                
                for angle in range(0, 360, 30):
                    rad = math.radians(angle + time_offset)
                    # Inner ring
                    start_x = center_x + math.cos(rad) * 6
                    start_y = center_y + math.sin(rad) * 6
                    mid_x = center_x + math.cos(rad) * (self.size - 8)
                    mid_y = center_y + math.sin(rad) * (self.size - 8)
                    end_x = center_x + math.cos(rad) * (self.size - 4)
                    end_y = center_y + math.sin(rad) * (self.size - 4)
                    
                    # Animated circuit lines
                    line_alpha = int(150 + 100 * math.sin(time.time() * 3 + angle/30))
                    pygame.draw.line(screen, self.color, (start_x, start_y), (mid_x, mid_y), 2)
                    pygame.draw.line(screen, WHITE, (mid_x, mid_y), (end_x, end_y), 1)
                    
                    # Circuit nodes
                    pygame.draw.circle(screen, WHITE, (int(mid_x), int(mid_y)), 2)
                
                # Pulsing center core
                core_size = int(4 + 2 * math.sin(time.time() * 4))
                pygame.draw.circle(screen, WHITE, (center_x, center_y), core_size)
                pygame.draw.circle(screen, self.color, (center_x, center_y), core_size - 1)
                
            elif self.type == "exit":
                # Enhanced exit with dramatic glow and animation
                glow_layers = [(self.size * 2.5, 30), (self.size * 2, 60), (self.size * 1.5, 120)]
                for glow_size, alpha in glow_layers:
                    glow_surface = pygame.Surface((glow_size * 2, glow_size * 2))
                    glow_surface.set_alpha(int(alpha * pulse))
                    pygame.draw.rect(glow_surface, self.color, (0, 0, glow_size * 2, glow_size * 2))
                    screen.blit(glow_surface, (self.x - glow_size, self.y - glow_size))
                
                # Main exit portal with depth
                base_rect = pygame.Rect(self.x - self.size, self.y - self.size, 
                                       self.size * 2, self.size * 2)
                pygame.draw.rect(screen, self.color, base_rect)
                pygame.draw.rect(screen, (100, 255, 100), (self.x - self.size + 3, self.y - self.size + 3, 
                                                          self.size * 2 - 6, self.size * 2 - 6))
                pygame.draw.rect(screen, WHITE, base_rect, 5)
                
                # Inner portal effect
                inner_rect = pygame.Rect(self.x - self.size + 6, self.y - self.size + 6, 
                                        self.size * 2 - 12, self.size * 2 - 12)
                pygame.draw.rect(screen, BLACK, inner_rect)
                pygame.draw.rect(screen, self.color, inner_rect, 3)
                
                # Swirling energy effect
                for i in range(8):
                    angle = i * 45 + time.time() * 100
                    rad = math.radians(angle)
                    energy_x = self.x + math.cos(rad) * (self.size - 10)
                    energy_y = self.y + math.sin(rad) * (self.size - 10)
                    energy_size = int(3 + 2 * math.sin(time.time() * 2 + i))
                    pygame.draw.circle(screen, NEON_GREEN, (int(energy_x), int(energy_y)), energy_size)
                
                # Enhanced exit arrow with glow
                arrow_points = [
                    (self.x - 8, self.y),
                    (self.x + 4, self.y - 8),
                    (self.x + 4, self.y - 3),
                    (self.x + 10, self.y - 3),
                    (self.x + 10, self.y + 3),
                    (self.x + 4, self.y + 3),
                    (self.x + 4, self.y + 8)
                ]
                pygame.draw.polygon(screen, WHITE, arrow_points)
                pygame.draw.polygon(screen, NEON_GREEN, arrow_points, 2)
                
            # All trap types are now completely invisible when not triggered
            elif self.type.startswith("trap_") and not self.triggered:
                # Traps are completely invisible - no visual hints at all
                pass
                
            elif self.type == "trap_spike":
                if self.triggered:
                    # Visible spike trap (triggered)
                    base_rect = pygame.Rect(self.x - self.size, self.y - self.size, 
                                           self.size * 2, self.size * 2)
                    pygame.draw.rect(screen, (100, 50, 50), base_rect)
                    pygame.draw.rect(screen, RED, base_rect, 2)
                    
                    # Spikes
                    for i in range(3):
                        for j in range(3):
                            spike_x = self.x - self.size + 4 + i * 8
                            spike_y = self.y - self.size + 4 + j * 8
                            spike_points = [
                                (spike_x, spike_y + 6),
                                (spike_x + 3, spike_y),
                                (spike_x + 6, spike_y + 6)
                            ]
                            pygame.draw.polygon(screen, RED, spike_points)
                else:
                    # Hidden trap - only show subtle floor difference during echo
                    if visible:
                        floor_rect = pygame.Rect(self.x - self.size, self.y - self.size, 
                                               self.size * 2, self.size * 2)
                        pygame.draw.rect(screen, (40, 40, 45), floor_rect)
                        pygame.draw.rect(screen, (60, 60, 65), floor_rect, 1)
                        
            elif self.type == "trap_laser":
                if self.triggered:
                    # Visible laser grid
                    for i in range(3):
                        laser_y = self.y - self.size + i * self.size // 1.5
                        pygame.draw.line(screen, RED, 
                                       (self.x - self.size, laser_y), 
                                       (self.x + self.size, laser_y), 2)
                        # Laser glow
                        pygame.draw.line(screen, (255, 100, 100), 
                                       (self.x - self.size, laser_y), 
                                       (self.x + self.size, laser_y), 4)
                else:
                    # Hidden - show as normal floor with slight shimmer
                    if visible:
                        floor_rect = pygame.Rect(self.x - self.size, self.y - self.size, 
                                               self.size * 2, self.size * 2)
                        shimmer_color = (30 + int(10 * pulse), 30 + int(10 * pulse), 35 + int(10 * pulse))
                        pygame.draw.rect(screen, shimmer_color, floor_rect)
                        
            elif self.type == "trap_shock":
                if self.triggered:
                    # Electric trap with lightning effect
                    base_rect = pygame.Rect(self.x - self.size, self.y - self.size, 
                                           self.size * 2, self.size * 2)
                    pygame.draw.rect(screen, (50, 50, 100), base_rect)
                    pygame.draw.rect(screen, NEON_BLUE, base_rect, 2)
                    
                    # Lightning bolts
                    for i in range(4):
                        angle = i * 90 + self.pulse_time * 50
                        rad = math.radians(angle)
                        end_x = self.x + math.cos(rad) * self.size
                        end_y = self.y + math.sin(rad) * self.size
                        pygame.draw.line(screen, CYAN, (self.x, self.y), (end_x, end_y), 2)
                        pygame.draw.line(screen, WHITE, (self.x, self.y), (end_x, end_y), 1)
                else:
                    # Hidden - metallic floor panel
                    if visible:
                        floor_rect = pygame.Rect(self.x - self.size, self.y - self.size, 
                                               self.size * 2, self.size * 2)
                        pygame.draw.rect(screen, (60, 60, 70), floor_rect)
                        pygame.draw.rect(screen, (80, 80, 90), floor_rect, 1)
                        
            elif self.type == "trap_pit":
                if self.triggered:
                    # Open pit trap
                    pit_rect = pygame.Rect(self.x - self.size, self.y - self.size, 
                                          self.size * 2, self.size * 2)
                    pygame.draw.rect(screen, BLACK, pit_rect)
                    pygame.draw.rect(screen, (100, 50, 50), pit_rect, 3)
                    
                    # Jagged edges
                    for i in range(8):
                        angle = i * 45
                        rad = math.radians(angle)
                        edge_x = self.x + math.cos(rad) * (self.size - 4)
                        edge_y = self.y + math.sin(rad) * (self.size - 4)
                        pygame.draw.circle(screen, (80, 40, 40), (int(edge_x), int(edge_y)), 3)
                else:
                    # Hidden pit - slightly different floor
                    if visible:
                        floor_rect = pygame.Rect(self.x - self.size, self.y - self.size, 
                                               self.size * 2, self.size * 2)
                        pygame.draw.rect(screen, (35, 35, 40), floor_rect)
                        pygame.draw.rect(screen, (50, 50, 55), floor_rect, 1)
                        
            elif self.type == "trap_gas":
                if self.triggered:
                    # Visible gas cloud
                    for i in range(5):
                        cloud_x = self.x + random.randint(-self.size, self.size)
                        cloud_y = self.y + random.randint(-self.size, self.size)
                        cloud_size = random.randint(8, 16)
                        cloud_alpha = random.randint(100, 180)
                        
                        cloud_surface = pygame.Surface((cloud_size * 2, cloud_size * 2))
                        cloud_surface.set_alpha(cloud_alpha)
                        pygame.draw.circle(cloud_surface, (100, 150, 100), 
                                         (cloud_size, cloud_size), cloud_size)
                        screen.blit(cloud_surface, (cloud_x - cloud_size, cloud_y - cloud_size))
                else:
                    # Hidden gas vent
                    if visible:
                        floor_rect = pygame.Rect(self.x - self.size, self.y - self.size, 
                                               self.size * 2, self.size * 2)
                        pygame.draw.rect(screen, (50, 60, 50), floor_rect)
                        pygame.draw.rect(screen, (70, 80, 70), floor_rect, 1)
                        
            elif self.type == "trap_blade":
                if self.triggered:
                    # Spinning blades
                    blade_angle = self.pulse_time * 200
                    for i in range(4):
                        angle = blade_angle + i * 90
                        rad = math.radians(angle)
                        blade_start_x = self.x + math.cos(rad) * 4
                        blade_start_y = self.y + math.sin(rad) * 4
                        blade_end_x = self.x + math.cos(rad) * (self.size - 2)
                        blade_end_y = self.y + math.sin(rad) * (self.size - 2)
                        
                        pygame.draw.line(screen, (200, 200, 220), 
                                       (blade_start_x, blade_start_y), 
                                       (blade_end_x, blade_end_y), 3)
                        pygame.draw.line(screen, WHITE, 
                                       (blade_start_x, blade_start_y), 
                                       (blade_end_x, blade_end_y), 1)
                else:
                    # Hidden blade mechanism
                    if visible:
                        floor_rect = pygame.Rect(self.x - self.size, self.y - self.size, 
                                               self.size * 2, self.size * 2)
                        pygame.draw.rect(screen, (70, 70, 80), floor_rect)
                        pygame.draw.rect(screen, (90, 90, 100), floor_rect, 1)
                        
            elif self.type == "trap_fire":
                if self.triggered:
                    # Fire effect
                    for i in range(6):
                        flame_x = self.x + random.randint(-8, 8)
                        flame_y = self.y + random.randint(-self.size, self.size//2)
                        flame_size = random.randint(4, 12)
                        
                        # Fire colors
                        fire_colors = [(255, 100, 0), (255, 150, 0), (255, 200, 50), (255, 255, 100)]
                        fire_color = random.choice(fire_colors)
                        
                        pygame.draw.circle(screen, fire_color, (int(flame_x), int(flame_y)), flame_size)
                        if flame_size > 6:
                            pygame.draw.circle(screen, (255, 255, 150), 
                                             (int(flame_x), int(flame_y)), flame_size - 4)
                else:
                    # Hidden fire trap
                    if visible:
                        floor_rect = pygame.Rect(self.x - self.size, self.y - self.size, 
                                               self.size * 2, self.size * 2)
                        pygame.draw.rect(screen, (60, 50, 50), floor_rect)
                        pygame.draw.rect(screen, (80, 70, 70), floor_rect, 1)
                        
            # Draw label if requested
            if show_label and font:
                label_text = self.get_label(game_inventory, game_codes)
                if label_text:  # Only draw if there's text to show
                    text_surface = font.render(label_text, True, WHITE)
                    text_rect = text_surface.get_rect()
                    
                    # Position label above object
                    label_x = self.x - text_rect.width // 2
                    label_y = self.y - self.size - 25
                    
                    # Background for label
                    bg_rect = pygame.Rect(label_x - 4, label_y - 2, 
                                         text_rect.width + 8, text_rect.height + 4)
                    
                    # Create semi-transparent surface for background
                    bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
                    bg_surface.set_alpha(180)
                    bg_surface.fill((20, 20, 30))
                    screen.blit(bg_surface, (bg_rect.x, bg_rect.y))
                    pygame.draw.rect(screen, CYAN, bg_rect, 1)
                    
                    screen.blit(text_surface, (label_x, label_y))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Echo Escape")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize sound manager
        self.sound_manager = SoundManager()
        
        # Game state
        self.game_state = "start_screen"  # start_screen, playing, game_over, victory
        self.inventory = []
        self.codes_found = []
        self.terminals_solved = 0
        self.game_won = False
        self.game_over = False
        self.death_message = ""
        self.flash_message = ""
        self.flash_message_time = 0
        
        # Echo system
        self.echo_active = False
        self.echo_start_time = 0
        self.echo_center = (0, 0)
        
        # Initialize empty game objects (will be created when game starts)
        self.player = None
        self.objects = []
        self.maze = []
        
        # Font for UI
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def generate_maze(self):
        # Simple maze generation - create walls and open spaces
        self.maze = [[0 for _ in range(MAZE_WIDTH)] for _ in range(MAZE_HEIGHT)]
        
        # Add border walls
        for x in range(MAZE_WIDTH):
            self.maze[0][x] = 1
            self.maze[MAZE_HEIGHT-1][x] = 1
        for y in range(MAZE_HEIGHT):
            self.maze[y][0] = 1
            self.maze[y][MAZE_WIDTH-1] = 1
            
        # Add some internal walls randomly (avoid starting area)
        start_grid_x = 2
        start_grid_y = SCREEN_HEIGHT // 2 // GRID_SIZE
        
        for _ in range(50):
            x = random.randint(2, MAZE_WIDTH-3)
            y = random.randint(2, MAZE_HEIGHT-3)
            
            # Don't place walls too close to starting position
            if abs(x - start_grid_x) > 2 or abs(y - start_grid_y) > 2:
                self.maze[y][x] = 1
            
        # Add some wall clusters for more interesting layout (avoid start area)
        for _ in range(10):
            x = random.randint(3, MAZE_WIDTH-4)
            y = random.randint(3, MAZE_HEIGHT-4)
            
            # Don't place wall clusters too close to starting position
            if abs(x - start_grid_x) > 3 or abs(y - start_grid_y) > 3:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if 0 <= x+dx < MAZE_WIDTH and 0 <= y+dy < MAZE_HEIGHT:
                            self.maze[y+dy][x+dx] = 1
    
    def place_objects(self):
        self.objects = []
        
        # Find valid positions (not walls, not too close to start)
        start_grid_x = 2  # Player starts at x = GRID_SIZE * 2
        start_grid_y = SCREEN_HEIGHT // 2 // GRID_SIZE  # Player starts at middle height
        
        valid_positions = []
        for y in range(2, MAZE_HEIGHT-2):
            for x in range(2, MAZE_WIDTH-2):
                if (self.maze[y][x] == 0 and 
                    abs(x - start_grid_x) > 4 and abs(y - start_grid_y) > 3):  # Avoid start area
                    valid_positions.append((x * GRID_SIZE + GRID_SIZE//2, 
                                          y * GRID_SIZE + GRID_SIZE//2))
        
        random.shuffle(valid_positions)
        
        # Place objects for three-chest progression
        if len(valid_positions) >= 12:
            pos_index = 0
            
            # Only place small key as standalone object (others come from chests)
            self.objects.append(GameObject(valid_positions[pos_index][0], valid_positions[pos_index][1], 
                                         "small_key", NEON_GREEN, 8))
            pos_index += 1
            
            # Three chests for progression (document, tool, large_key come from these)
            for i in range(3):
                self.objects.append(GameObject(valid_positions[pos_index][0], valid_positions[pos_index][1], 
                                             "chest", NEON_PINK, 16))
                pos_index += 1
            
            # Code puzzles (3 needed for terminals)
            for i in range(3):
                self.objects.append(GameObject(valid_positions[pos_index][0], valid_positions[pos_index][1], 
                                             "code_puzzle", CYAN, 12))
                pos_index += 1
            
            # Terminals (3 needed to complete game)
            for i in range(3):
                self.objects.append(GameObject(valid_positions[pos_index][0], valid_positions[pos_index][1], 
                                             "terminal", WHITE, 20))
                pos_index += 1
            
            # 7 deadly traps, well spaced
            trap_types = ["trap_spike", "trap_laser", "trap_shock", "trap_pit", "trap_gas", "trap_blade", "trap_fire"]
            trap_positions = []
            
            for i in range(7):
                attempts = 0
                while attempts < 50 and pos_index < len(valid_positions):
                    pos = valid_positions[pos_index]
                    
                    # Ensure traps are well separated (at least 100 units apart)
                    too_close = False
                    for trap_pos in trap_positions:
                        if math.sqrt((pos[0] - trap_pos[0])**2 + (pos[1] - trap_pos[1])**2) < 100:
                            too_close = True
                            break
                    
                    if not too_close:
                        trap_type = trap_types[i]
                        self.objects.append(GameObject(pos[0], pos[1], trap_type, RED, 20))
                        trap_positions.append(pos)
                        break
                    
                    pos_index += 1
                    attempts += 1
                
                pos_index += 1
    
    def handle_interaction(self):
        player_rect = pygame.Rect(self.player.x - 16, self.player.y - 16, 32, 32)
        
        for obj in self.objects:
            if obj.collected:
                continue
                
            obj_rect = pygame.Rect(obj.x - obj.size, obj.y - obj.size, 
                                 obj.size * 2, obj.size * 2)
            
            if player_rect.colliderect(obj_rect):
                if obj.type == "small_key":
                    obj.collected = True
                    self.inventory.append("small_key")
                    self.sound_manager.play_sound('collect')
                    return f"Found small key!"
                    
                elif obj.type == "chest" and not obj.unlocked:
                    # First chest: needs small key, gives document
                    if "small_key" in self.inventory and "document" not in self.inventory:
                        obj.unlocked = True
                        self.inventory.append("document")
                        self.sound_manager.play_sound('chest')
                        return f"Opened chest with small key! Found document."
                    # Second chest: needs document, gives tool
                    elif "document" in self.inventory and "tool" not in self.inventory:
                        obj.unlocked = True
                        self.inventory.append("tool")
                        self.sound_manager.play_sound('chest')
                        return f"Opened chest with document! Found tool."
                    # Third chest: needs tool, gives large key
                    elif "tool" in self.inventory and "large_key" not in self.inventory:
                        obj.unlocked = True
                        self.inventory.append("large_key")
                        self.sound_manager.play_sound('chest')
                        return f"Opened chest with tool! Found large key."
                    else:
                        return f"Chest is locked. Need the right item to open it."
                        
                elif obj.type == "code_puzzle":
                    codes = ["2048", "ECHO", "NEURAL"]
                    code = random.choice([c for c in codes if c not in self.codes_found])
                    if code:
                        self.codes_found.append(code)
                        obj.collected = True
                        self.sound_manager.play_sound('code')
                        return f"Found code: {code}"
                    
                elif obj.type == "terminal":
                    # Terminal 1: Requires code "2048" only
                    if "2048" in self.codes_found:
                        obj.collected = True
                        self.terminals_solved += 1
                        self.codes_found.remove("2048")
                        self.sound_manager.play_sound('terminal')
                        
                        if self.check_all_requirements_met():
                            return self.spawn_exit_with_message()
                        
                        return f"Terminal solved with code 2048!"
                        
                    # Terminal 2: Requires code "ECHO" and document
                    elif "ECHO" in self.codes_found and "document" in self.inventory:
                        obj.collected = True
                        self.terminals_solved += 1
                        self.codes_found.remove("ECHO")
                        self.sound_manager.play_sound('terminal')
                        
                        if self.check_all_requirements_met():
                            return self.spawn_exit_with_message()
                        
                        return f"Terminal solved with code ECHO and document!"
                        
                    # Terminal 3: Requires code "NEURAL" and large key
                    elif "NEURAL" in self.codes_found and "large_key" in self.inventory:
                        obj.collected = True
                        self.terminals_solved += 1
                        self.codes_found.remove("NEURAL")
                        self.sound_manager.play_sound('terminal')
                        
                        if self.check_all_requirements_met():
                            return self.spawn_exit_with_message()
                        
                        return f"Terminal solved with code NEURAL and large key!"
                        
                    else:
                        return f"Terminal needs a specific code and required items."
                        
                elif obj.type == "exit":
                    self.game_won = True
                    self.sound_manager.play_sound('victory')
                    return f"Escaped! You win!"
        
        return None
    
    def check_all_requirements_met(self):
        """Check if all requirements are met before allowing exit to spawn"""
        # Must have solved all 3 terminals
        if self.terminals_solved < 3:
            return False
        
        # Must have collected all essential items
        required_items = ["small_key", "document", "tool", "large_key"]
        for item in required_items:
            if item not in self.inventory:
                return False
        
        # Must have opened all chests
        chests_opened = 0
        for obj in self.objects:
            if obj.type == "chest" and obj.unlocked:
                chests_opened += 1
        
        if chests_opened < 3:
            return False
        
        # Must have found and used all codes
        all_codes_used = len(self.codes_found) == 0  # All codes should be used up
        
        return all_codes_used
    
    def spawn_exit_with_message(self):
        # Spawn exit
        valid_pos = self.find_valid_position()
        if valid_pos:
            self.objects.append(GameObject(valid_pos[0], valid_pos[1], 
                                         "exit", NEON_GREEN, 24))
        
        # Set flash message
        self.flash_message = "ALL TERMINALS SOLVED! FIND THE EXIT!"
        self.flash_message_time = pygame.time.get_ticks()
        
        return f"All terminals solved! The exit has appeared - find it to escape!"
    
    def check_traps(self):
        player_rect = pygame.Rect(self.player.x - 12, self.player.y - 12, 24, 24)
        
        for obj in self.objects:
            if obj.type.startswith("trap_") and not obj.triggered:
                obj_rect = pygame.Rect(obj.x - obj.size//2, obj.y - obj.size//2, 
                                     obj.size, obj.size)
                
                if player_rect.colliderect(obj_rect):
                    obj.triggered = True
                    self.game_over = True
                    self.sound_manager.play_sound('trap')
                    self.sound_manager.play_sound('death')
                    
                    trap_messages = {
                        "trap_spike": "GAME OVER: Impaled by hidden spikes!",
                        "trap_laser": "GAME OVER: Disintegrated by laser grid!",
                        "trap_shock": "GAME OVER: Electrocuted by shock trap!",
                        "trap_pit": "GAME OVER: Fell into a deadly pit!",
                        "trap_gas": "GAME OVER: Poisoned by toxic gas!",
                        "trap_blade": "GAME OVER: Sliced by spinning blades!",
                        "trap_fire": "GAME OVER: Incinerated by flames!"
                    }
                    
                    self.death_message = trap_messages.get(obj.type, "GAME OVER: Killed by trap!")
                    return True
        
        return False
    
    def find_valid_position(self):
        for _ in range(100):
            x = random.randint(2, MAZE_WIDTH-3) * GRID_SIZE + GRID_SIZE//2
            y = random.randint(2, MAZE_HEIGHT-3) * GRID_SIZE + GRID_SIZE//2
            
            # Check if position is free
            grid_x, grid_y = x // GRID_SIZE, y // GRID_SIZE
            if self.maze[grid_y][grid_x] == 0:
                # Check distance from other objects
                too_close = False
                for obj in self.objects:
                    if math.sqrt((x - obj.x)**2 + (y - obj.y)**2) < 64:
                        too_close = True
                        break
                if not too_close:
                    return (x, y)
        return None
    
    def draw_maze(self):
        current_time = pygame.time.get_ticks()
        echo_visible = (self.echo_active and 
                       current_time - self.echo_start_time < ECHO_DURATION)
        
        if echo_visible:
            # Draw enhanced walls within echo radius
            echo_x, echo_y = self.echo_center
            for y in range(MAZE_HEIGHT):
                for x in range(MAZE_WIDTH):
                    if self.maze[y][x] == 1:
                        wall_x = x * GRID_SIZE + GRID_SIZE // 2
                        wall_y = y * GRID_SIZE + GRID_SIZE // 2
                        distance = math.sqrt((wall_x - echo_x)**2 + (wall_y - echo_y)**2)
                        
                        if distance <= ECHO_RADIUS:
                            # Enhanced fade effect with multiple layers
                            time_factor = 1 - (current_time - self.echo_start_time) / ECHO_DURATION
                            distance_factor = 1 - (distance / ECHO_RADIUS)
                            alpha = int(255 * time_factor * distance_factor)
                            
                            # Main wall with depth
                            wall_rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                            
                            # Wall shadow/depth
                            shadow_surface = pygame.Surface((GRID_SIZE, GRID_SIZE))
                            shadow_surface.set_alpha(alpha // 2)
                            shadow_surface.fill((0, 100, 100))
                            self.screen.blit(shadow_surface, (x * GRID_SIZE + 2, y * GRID_SIZE + 2))
                            
                            # Main wall surface
                            wall_surface = pygame.Surface((GRID_SIZE, GRID_SIZE))
                            wall_surface.set_alpha(alpha)
                            wall_surface.fill(CYAN)
                            self.screen.blit(wall_surface, (x * GRID_SIZE, y * GRID_SIZE))
                            
                            # Wall highlight
                            highlight_surface = pygame.Surface((GRID_SIZE - 4, GRID_SIZE - 4))
                            highlight_surface.set_alpha(alpha // 3)
                            highlight_surface.fill(WHITE)
                            self.screen.blit(highlight_surface, (x * GRID_SIZE + 2, y * GRID_SIZE + 2))
                            
                            # Wall border
                            if alpha > 100:
                                pygame.draw.rect(self.screen, WHITE, wall_rect, 1)
            
            # Draw subtle trap hints during echo (now removed - traps are invisible)
            self.draw_trap_hints(echo_x, echo_y, current_time)
            
            # Draw safety indicator
            self.draw_safety_indicator(echo_x, echo_y, current_time)
        else:
            self.echo_active = False
    
    def draw_start_screen(self):
        """Draw the start game screen"""
        # Dark gradient background
        for y in range(SCREEN_HEIGHT):
            color_factor = y / SCREEN_HEIGHT
            r = int(DARKER_GRAY[0] + (DARK_GRAY[0] - DARKER_GRAY[0]) * color_factor)
            g = int(DARKER_GRAY[1] + (DARK_GRAY[1] - DARKER_GRAY[1]) * color_factor)
            b = int(DARKER_GRAY[2] + (DARK_GRAY[2] - DARKER_GRAY[2]) * color_factor)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Add subtle grid pattern
        grid_alpha = 20
        grid_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        grid_surface.set_alpha(grid_alpha)
        
        for x in range(0, SCREEN_WIDTH, GRID_SIZE * 2):
            pygame.draw.line(grid_surface, CYAN, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE * 2):
            pygame.draw.line(grid_surface, CYAN, (0, y), (SCREEN_WIDTH, y))
            
        self.screen.blit(grid_surface, (0, 0))
        
        # Animated particles
        current_time = pygame.time.get_ticks()
        for i in range(15):
            particle_x = (i * 137 + current_time * 0.02) % SCREEN_WIDTH
            particle_y = (i * 211 + current_time * 0.01) % SCREEN_HEIGHT
            particle_alpha = int(40 + 30 * math.sin(current_time * 0.002 + i))
            
            particle_surface = pygame.Surface((3, 3))
            particle_surface.set_alpha(particle_alpha)
            particle_surface.fill(CYAN)
            self.screen.blit(particle_surface, (particle_x, particle_y))
        
        # Calculate vertical centering - start from center and work up/down
        center_y = SCREEN_HEIGHT // 2
        
        # Main title with glow effect
        title_y = center_y - 120
        
        # Title glow layers
        glow_colors = [(CYAN[0]//4, CYAN[1]//4, CYAN[2]//4), 
                       (CYAN[0]//2, CYAN[1]//2, CYAN[2]//2)]
        
        for i, glow_color in enumerate(glow_colors):
            glow_offset = (len(glow_colors) - i) * 2
            for dx in range(-glow_offset, glow_offset + 1):
                for dy in range(-glow_offset, glow_offset + 1):
                    if dx*dx + dy*dy <= glow_offset*glow_offset:
                        title_surface = self.font.render("ECHO ESCAPE", True, glow_color)
                        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2 + dx, title_y + dy))
                        self.screen.blit(title_surface, title_rect)
        
        # Main title
        pulse = abs(math.sin(current_time * 0.003)) * 0.3 + 0.7
        title_color = (int(CYAN[0] * pulse), int(CYAN[1] * pulse), int(CYAN[2] * pulse))
        title_surface = self.font.render("ECHO ESCAPE", True, title_color)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, title_y))
        self.screen.blit(title_surface, title_rect)
        
        # Game description (centered vertically)
        description_y = center_y - 40
        descriptions = [
            "Navigate through darkness using sound waves",
            "Avoid deadly invisible traps",
            "Collect items and solve puzzles to escape",
            "Use SPACE to emit echo pings and see your surroundings"
        ]
        
        for i, desc in enumerate(descriptions):
            desc_surface = self.small_font.render(desc, True, WHITE)
            desc_rect = desc_surface.get_rect(center=(SCREEN_WIDTH//2, description_y + i * 25))
            self.screen.blit(desc_surface, desc_rect)
        
        # Controls section
        controls_y = center_y + 60
        controls_title = self.small_font.render("CONTROLS:", True, NEON_PINK)
        controls_title_rect = controls_title.get_rect(center=(SCREEN_WIDTH//2, controls_y))
        self.screen.blit(controls_title, controls_title_rect)
        
        controls = [
            "SPACE: Echo Ping",
            "Arrow Keys: Move",
            "E: Interact",
            "ESC: Quit Game"
        ]
        
        for i, control in enumerate(controls):
            control_surface = self.small_font.render(control, True, SILVER)
            control_rect = control_surface.get_rect(center=(SCREEN_WIDTH//2, controls_y + 30 + i * 20))
            self.screen.blit(control_surface, control_rect)
        
        # Start instruction with pulsing effect
        start_y = center_y + 180
        start_pulse = abs(math.sin(current_time * 0.005)) * 0.5 + 0.5
        start_color = (int(NEON_GREEN[0] * start_pulse), int(NEON_GREEN[1] * start_pulse), int(NEON_GREEN[2] * start_pulse))
        
        start_text = "Press ENTER to Start Game"
        start_surface = self.font.render(start_text, True, start_color)
        start_rect = start_surface.get_rect(center=(SCREEN_WIDTH//2, start_y))
        self.screen.blit(start_surface, start_rect)
        
        # Warning message
        credits_text = "Navigate carefully - death is permanent!"
        credits_surface = self.small_font.render(credits_text, True, RED)
        credits_rect = credits_surface.get_rect(center=(SCREEN_WIDTH//2, start_y + 40))
        self.screen.blit(credits_surface, credits_rect)
    
    def draw_background(self):
        """Draw enhanced background with gradient and subtle effects"""
        # Create gradient background
        for y in range(SCREEN_HEIGHT):
            color_factor = y / SCREEN_HEIGHT
            r = int(DARKER_GRAY[0] + (DARK_GRAY[0] - DARKER_GRAY[0]) * color_factor)
            g = int(DARKER_GRAY[1] + (DARK_GRAY[1] - DARKER_GRAY[1]) * color_factor)
            b = int(DARKER_GRAY[2] + (DARK_GRAY[2] - DARKER_GRAY[2]) * color_factor)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Add subtle grid pattern
        grid_alpha = 15
        grid_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        grid_surface.set_alpha(grid_alpha)
        
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(grid_surface, CYAN, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(grid_surface, CYAN, (0, y), (SCREEN_WIDTH, y))
            
        self.screen.blit(grid_surface, (0, 0))
        
        # Add ambient particles
        current_time = pygame.time.get_ticks()
        for i in range(20):
            particle_x = (i * 137 + current_time * 0.01) % SCREEN_WIDTH
            particle_y = (i * 211 + current_time * 0.005) % SCREEN_HEIGHT
            particle_alpha = int(30 + 20 * math.sin(current_time * 0.001 + i))
            
            particle_surface = pygame.Surface((2, 2))
            particle_surface.set_alpha(particle_alpha)
            particle_surface.fill(CYAN)
            self.screen.blit(particle_surface, (particle_x, particle_y))
        """Draw enhanced background with gradient and subtle effects"""
        # Create gradient background
        for y in range(SCREEN_HEIGHT):
            color_factor = y / SCREEN_HEIGHT
            r = int(DARKER_GRAY[0] + (DARK_GRAY[0] - DARKER_GRAY[0]) * color_factor)
            g = int(DARKER_GRAY[1] + (DARK_GRAY[1] - DARKER_GRAY[1]) * color_factor)
            b = int(DARKER_GRAY[2] + (DARK_GRAY[2] - DARKER_GRAY[2]) * color_factor)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Add subtle grid pattern
        grid_alpha = 15
        grid_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        grid_surface.set_alpha(grid_alpha)
        
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(grid_surface, CYAN, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(grid_surface, CYAN, (0, y), (SCREEN_WIDTH, y))
            
        self.screen.blit(grid_surface, (0, 0))
        
        # Add ambient particles
        current_time = pygame.time.get_ticks()
        for i in range(20):
            particle_x = (i * 137 + current_time * 0.01) % SCREEN_WIDTH
            particle_y = (i * 211 + current_time * 0.005) % SCREEN_HEIGHT
            particle_alpha = int(30 + 20 * math.sin(current_time * 0.001 + i))
            
            particle_surface = pygame.Surface((2, 2))
            particle_surface.set_alpha(particle_alpha)
            particle_surface.fill(CYAN)
            self.screen.blit(particle_surface, (particle_x, particle_y))
    
    def draw_safety_indicator(self, echo_x, echo_y, current_time):
        """Draw safety indicator during echo ping"""
        time_factor = 1 - (current_time - self.echo_start_time) / ECHO_DURATION
        
        # Check for nearby traps
        nearby_traps = []
        immediate_danger = False
        
        for obj in self.objects:
            if obj.type.startswith("trap_") and not obj.triggered:
                distance = math.sqrt((obj.x - self.player.x)**2 + (obj.y - self.player.y)**2)
                
                if distance <= 60:  # Immediate danger zone
                    immediate_danger = True
                elif distance <= 120:  # Nearby danger zone
                    nearby_traps.append(obj)
        
        # Determine safety status
        if immediate_danger:
            status_text = "DANGER"
            status_color = RED
            ring_color = RED
        elif nearby_traps:
            status_text = "CAUTION"
            status_color = (255, 165, 0)  # Orange
            ring_color = (255, 165, 0)
        else:
            status_text = "SAFE"
            status_color = NEON_GREEN
            ring_color = NEON_GREEN
        
        # Draw safety ring around player
        alpha = int(150 * time_factor)
        ring_surface = pygame.Surface((120, 120))
        ring_surface.set_alpha(alpha)
        pygame.draw.circle(ring_surface, ring_color, (60, 60), 60, 4)
        self.screen.blit(ring_surface, (self.player.x - 60, self.player.y - 60))
        
        # Draw inner safety circle
        inner_alpha = int(50 * time_factor)
        inner_surface = pygame.Surface((80, 80))
        inner_surface.set_alpha(inner_alpha)
        pygame.draw.circle(inner_surface, ring_color, (40, 40), 40)
        self.screen.blit(inner_surface, (self.player.x - 40, self.player.y - 40))
        
        # Draw status text above player
        font_alpha = int(255 * time_factor)
        text_surface = self.small_font.render(status_text, True, status_color)
        
        # Add text background for better visibility
        text_rect = text_surface.get_rect()
        bg_surface = pygame.Surface((text_rect.width + 8, text_rect.height + 4))
        bg_surface.set_alpha(int(180 * time_factor))
        bg_surface.fill((0, 0, 0))
        
        text_x = self.player.x - text_rect.width // 2
        text_y = self.player.y - 50
        
        self.screen.blit(bg_surface, (text_x - 4, text_y - 2))
        self.screen.blit(text_surface, (text_x, text_y))
        
        # Draw directional indicators for nearby traps (CAUTION mode)
        if nearby_traps and not immediate_danger:
            for obj in nearby_traps:
                # Calculate direction to trap
                dx = obj.x - self.player.x
                dy = obj.y - self.player.y
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance > 0:
                    # Normalize direction
                    dx /= distance
                    dy /= distance
                    
                    # Draw directional arrow
                    arrow_distance = 35
                    arrow_x = self.player.x + dx * arrow_distance
                    arrow_y = self.player.y + dy * arrow_distance
                    
                    # Arrow points
                    arrow_size = 8
                    arrow_points = [
                        (arrow_x + dx * arrow_size, arrow_y + dy * arrow_size),
                        (arrow_x - dx * arrow_size + dy * arrow_size/2, arrow_y - dy * arrow_size - dx * arrow_size/2),
                        (arrow_x - dx * arrow_size - dy * arrow_size/2, arrow_y - dy * arrow_size + dx * arrow_size/2)
                    ]
                    
                    arrow_surface = pygame.Surface((50, 50))
                    arrow_surface.set_alpha(int(120 * time_factor))
                    arrow_surface.fill((0, 0, 0))
                    arrow_surface.set_colorkey((0, 0, 0))
                    
                    # Adjust points for surface coordinates
                    adjusted_points = [(p[0] - arrow_x + 25, p[1] - arrow_y + 25) for p in arrow_points]
                    pygame.draw.polygon(arrow_surface, (255, 165, 0), adjusted_points)
                    
                    self.screen.blit(arrow_surface, (arrow_x - 25, arrow_y - 25))
    
    def draw_trap_hints(self, echo_x, echo_y, current_time):
        """Traps are now completely invisible - no hints provided"""
        pass
    
    def draw_objects(self):
        current_time = pygame.time.get_ticks()
        echo_visible = (self.echo_active and 
                       current_time - self.echo_start_time < ECHO_DURATION)
        
        if echo_visible:
            echo_x, echo_y = self.echo_center
            for obj in self.objects:
                distance = math.sqrt((obj.x - echo_x)**2 + (obj.y - echo_y)**2)
                if distance <= ECHO_RADIUS:
                    # Check if player is close enough for label
                    player_distance = math.sqrt((obj.x - self.player.x)**2 + (obj.y - self.player.y)**2)
                    show_label = player_distance <= 60
                    obj.draw(self.screen, True, show_label, self.small_font, self.inventory, self.codes_found)
        
        # Always draw objects very close to player
        for obj in self.objects:
            distance = math.sqrt((obj.x - self.player.x)**2 + (obj.y - self.player.y)**2)
            if distance <= 40:  # Very close proximity
                show_label = distance <= 60
                obj.draw(self.screen, True, show_label, self.small_font, self.inventory, self.codes_found)
    
    def draw_ui(self):
        # Enhanced UI with better styling
        ui_alpha = 200
        
        # Create semi-transparent panels for UI elements
        def draw_ui_panel(x, y, width, height, color=(0, 0, 0)):
            panel_surface = pygame.Surface((width, height))
            panel_surface.set_alpha(ui_alpha)
            panel_surface.fill(color)
            self.screen.blit(panel_surface, (x, y))
            pygame.draw.rect(self.screen, CYAN, (x, y, width, height), 2)
        
        # Left panel for game info - make it larger to accommodate inventory
        panel_width = 400
        panel_height = 140
        draw_ui_panel(10, 10, panel_width, panel_height)
        
        # Inventory with enhanced styling and word wrapping
        y_offset = 20
        inventory_items = ', '.join(self.inventory) if self.inventory else 'EMPTY'
        
        # Handle long inventory text by wrapping it
        max_chars_per_line = 45  # Adjust based on panel width
        if len(inventory_items) > max_chars_per_line:
            # Split long inventory into multiple lines
            words = inventory_items.split(', ')
            lines = []
            current_line = "INVENTORY: "
            
            for word in words:
                if len(current_line + word + ', ') <= max_chars_per_line:
                    if current_line == "INVENTORY: ":
                        current_line += word
                    else:
                        current_line += ', ' + word
                else:
                    lines.append(current_line)
                    current_line = '           ' + word  # Indent continuation
            
            if current_line.strip():
                lines.append(current_line)
            
            # Draw each line
            for i, line in enumerate(lines):
                text_surface = self.small_font.render(line, True, NEON_GREEN)
                self.screen.blit(text_surface, (20, y_offset + i * 20))
            
            y_offset += len(lines) * 20
        else:
            inventory_text = f"INVENTORY: {inventory_items}"
            text_surface = self.small_font.render(inventory_text, True, NEON_GREEN)
            self.screen.blit(text_surface, (20, y_offset))
            y_offset += 25
        
        # Codes found
        codes_text = f"CODES: {', '.join(self.codes_found) if self.codes_found else 'NONE'}"
        text_surface = self.small_font.render(codes_text, True, CYAN)
        self.screen.blit(text_surface, (20, y_offset))
        y_offset += 25
        
        # Terminals solved with progress bar
        terminals_text = f"TERMINALS: {self.terminals_solved}/3"
        text_surface = self.small_font.render(terminals_text, True, NEON_PINK)
        self.screen.blit(text_surface, (20, y_offset))
        y_offset += 25
        
        # Progress bar for terminals
        progress_width = 250
        progress_height = 8
        progress_x = 20
        progress_y = y_offset
        
        # Progress background
        pygame.draw.rect(self.screen, DARK_GRAY, (progress_x, progress_y, progress_width, progress_height))
        pygame.draw.rect(self.screen, WHITE, (progress_x, progress_y, progress_width, progress_height), 1)
        
        # Progress fill
        if self.terminals_solved > 0:
            fill_width = int((self.terminals_solved / 3) * progress_width)
            pygame.draw.rect(self.screen, NEON_PINK, (progress_x, progress_y, fill_width, progress_height))
        
        # Right panel for instructions
        instruction_panel_width = 220
        instruction_panel_height = 160
        draw_ui_panel(SCREEN_WIDTH - instruction_panel_width - 10, 10, 
                     instruction_panel_width, instruction_panel_height)
        
        # Enhanced instructions
        instructions = [
            ("CONTROLS:", WHITE),
            ("SPACE: Echo Ping", CYAN),
            ("E: Interact", NEON_GREEN),
            ("Arrow Keys: Move", NEON_BLUE),
            ("ESC: Quit", RED),
            ("", WHITE),
            ("BEWARE:", NEON_PINK),
            ("Hidden Traps!", RED)
        ]
        
        for i, (instruction, color) in enumerate(instructions):
            if instruction:  # Skip empty lines
                text_surface = self.small_font.render(instruction, True, color)
                self.screen.blit(text_surface, (SCREEN_WIDTH - instruction_panel_width + 10, 20 + i * 18))
        
        # Game over screen with enhanced styling
        if self.game_over:
            # Dark overlay with gradient
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            for y in range(SCREEN_HEIGHT):
                alpha = int(180 * (y / SCREEN_HEIGHT))
                overlay.set_alpha(alpha)
                pygame.draw.line(overlay, (20, 0, 0), (0, y), (SCREEN_WIDTH, y))
            self.screen.blit(overlay, (0, 0))
            
            # Death message with glow effect
            death_surface = self.font.render(self.death_message, True, RED)
            glow_surface = self.font.render(self.death_message, True, (100, 0, 0))
            
            text_rect = death_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20))
            glow_rect = glow_surface.get_rect(center=(SCREEN_WIDTH//2 + 2, SCREEN_HEIGHT//2 - 18))
            
            self.screen.blit(glow_surface, glow_rect)
            self.screen.blit(death_surface, text_rect)
            
            restart_text = self.small_font.render("Press R to restart or ESC to quit", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
            self.screen.blit(restart_text, restart_rect)
        
        # Win screen with celebration effects
        elif self.game_won:
            # Victory overlay with green tint
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0, 40, 0))
            self.screen.blit(overlay, (0, 0))
            
            # Animated victory text
            pulse = abs(math.sin(time.time() * 3)) * 0.3 + 0.7
            win_color = (int(NEON_GREEN[0] * pulse), int(NEON_GREEN[1] * pulse), int(NEON_GREEN[2] * pulse))
            
            win_text = self.font.render("YOU ESCAPED!", True, win_color)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40))
            self.screen.blit(win_text, text_rect)
            
            success_text = self.small_font.render("You navigated the deadly maze successfully!", True, WHITE)
            success_rect = success_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 10))
            self.screen.blit(success_text, success_rect)
            
            # Play again option
            play_again_text = self.small_font.render("Press R to play again or ESC to quit", True, CYAN)
            play_again_rect = play_again_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
            self.screen.blit(play_again_text, play_again_rect)
            
            # Victory sparkles
            for i in range(10):
                sparkle_x = SCREEN_WIDTH//2 + random.randint(-100, 100)
                sparkle_y = SCREEN_HEIGHT//2 + random.randint(-50, 50)
                sparkle_size = random.randint(2, 6)
                sparkle_alpha = int(255 * random.random())
                
                sparkle_surface = pygame.Surface((sparkle_size, sparkle_size))
                sparkle_surface.set_alpha(sparkle_alpha)
                sparkle_surface.fill(NEON_GREEN)
                self.screen.blit(sparkle_surface, (sparkle_x, sparkle_y))
    
    def start_new_game(self):
        """Initialize a new game"""
        self.game_state = "playing"
        self.inventory = []
        self.codes_found = []
        self.terminals_solved = 0
        self.game_won = False
        self.game_over = False
        self.death_message = ""
        self.flash_message = ""
        self.flash_message_time = 0
        
        # Reset echo system
        self.echo_active = False
        self.echo_start_time = 0
        self.echo_center = (0, 0)
        
        # Generate maze and objects
        self.generate_maze()
        self.place_objects()
        
        # Create player at middle left position
        start_x = GRID_SIZE * 2  # Left side of screen
        start_y = SCREEN_HEIGHT // 2  # Middle height
        self.player = Player(start_x, start_y)
    
    def restart_game(self):
        """Reset game state for restart"""
        self.game_state = "playing"
        self.inventory = []
        self.codes_found = []
        self.terminals_solved = 0
        self.game_won = False
        self.game_over = False
        self.death_message = ""
        self.flash_message = ""
        self.flash_message_time = 0
        
        # Reset echo system
        self.echo_active = False
        self.echo_start_time = 0
        self.echo_center = (0, 0)
        
        # Regenerate maze and objects
        self.generate_maze()
        self.place_objects()
        
        # Reset player position to middle left
        start_x = GRID_SIZE * 2  # Left side of screen
        start_y = SCREEN_HEIGHT // 2  # Middle height
        self.player = Player(start_x, start_y)
    
    def run(self):
        message = ""
        message_time = 0
        
        while self.running:
            current_time = pygame.time.get_ticks()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.game_state == "start_screen":
                            self.running = False
                        else:
                            self.game_state = "start_screen"
                    
                    # Start screen controls
                    elif self.game_state == "start_screen":
                        if event.key == pygame.K_RETURN:
                            self.start_new_game()
                            message = "Navigate carefully! Find the small key to begin..."
                            message_time = current_time
                    
                    # Playing game controls
                    elif self.game_state == "playing":
                        if event.key == pygame.K_r and (self.game_over or self.game_won):
                            self.restart_game()
                            message = "New game started! Find the small key to begin..."
                            message_time = current_time
                        elif event.key == pygame.K_SPACE and not self.game_over and not self.game_won:
                            if self.player and self.player.emit_echo():
                                self.echo_active = True
                                self.echo_start_time = current_time
                                self.echo_center = (self.player.x, self.player.y)
                                self.sound_manager.play_sound('echo')
                        elif event.key == pygame.K_e and not self.game_over and not self.game_won:
                            if self.player:
                                interaction_result = self.handle_interaction()
                                if interaction_result:
                                    message = interaction_result
                                    message_time = current_time
            
            # Handle continuous key presses (only during gameplay)
            if self.game_state == "playing" and self.player and not self.game_over and not self.game_won:
                keys = pygame.key.get_pressed()
                dx = dy = 0
                if keys[pygame.K_LEFT]:
                    dx = -PLAYER_SPEED
                if keys[pygame.K_RIGHT]:
                    dx = PLAYER_SPEED
                if keys[pygame.K_UP]:
                    dy = -PLAYER_SPEED
                if keys[pygame.K_DOWN]:
                    dy = PLAYER_SPEED
                
                self.player.move(dx, dy, self.maze)
                
                # Check for traps
                if self.check_traps():
                    message = self.death_message
                    message_time = current_time
            
            # Render based on game state
            if self.game_state == "start_screen":
                self.draw_start_screen()
            
            elif self.game_state == "playing":
                # Draw game
                self.draw_background()
                self.draw_maze()
                self.draw_objects()
                
                # Draw player (always visible if alive)
                if not self.game_over and self.player:
                    self.player.draw(self.screen)
                
                # Draw UI
                self.draw_ui()
                
                # Draw message
                if message and current_time - message_time < 4000:
                    text_surface = self.font.render(message, True, NEON_GREEN)
                    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
                    self.screen.blit(text_surface, text_rect)
                
                # Draw flash message (priority over regular message)
                if self.flash_message and current_time - self.flash_message_time < 5000:
                    # Flashing effect
                    flash_alpha = int(255 * (0.5 + 0.5 * math.sin(current_time * 0.01)))
                    flash_color = (255, flash_alpha, 0)  # Orange flashing
                    
                    flash_surface = self.font.render(self.flash_message, True, flash_color)
                    flash_rect = flash_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
                    
                    # Background for flash message
                    bg_surface = pygame.Surface((flash_rect.width + 20, flash_rect.height + 10))
                    bg_surface.set_alpha(150)
                    bg_surface.fill((50, 25, 0))
                    self.screen.blit(bg_surface, (flash_rect.x - 10, flash_rect.y - 5))
                    
                    self.screen.blit(flash_surface, flash_rect)
                elif self.flash_message and current_time - self.flash_message_time >= 5000:
                    self.flash_message = ""  # Clear flash message after 5 seconds
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
