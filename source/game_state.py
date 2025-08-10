"""
Game state management to replace scattered global variables.
"""
import pygame


class GameState:
    """Manages global game state variables that were previously scattered as globals."""
    
    def __init__(self):
        # Background and visual effects
        self.parallax_position = (0, 0)
        self.fade_background_id = -1
        self.fade_back = False
        self.fade_float = 0.0
        
        # UI and text rendering
        self.hand_text = pygame.Surface((0, 0))
        self.stats_text = pygame.Surface((0, 0))
        self.last_hovered_item = None
        
        # Lighting system
        self.light_surface = pygame.Surface((0, 0))
        self.newest_light_surface = pygame.Surface((0, 0))
        self.newest_light_surface_position = (0, 0)
        self.light_min_x = 0
        self.light_max_x = 0
        self.light_min_y = 0
        self.light_max_y = 0
        self.thread_active = False
        self.last_thread_time = 0.2
        self.last_thread_start = pygame.time.get_ticks()
        self.map_light = []
        
        # Menu system
        self.save_select_surface = pygame.Surface((315, 360), pygame.SRCALPHA)
        self.save_select_y_offset = 0
        self.save_select_y_velocity = 0
        
        # Item interaction
        self.can_drop_holding = False
        self.can_pickup_item = False
        self.item_drop_tick = 0
        self.item_drop_rate = 0
        
        # UI state
        self.exit_button_hover = False
        
        # Timing and performance
        self.auto_save_tick = 0
        self.fps_tick = 0
        self.old_time_milliseconds = pygame.time.get_ticks()
        
        # Background effects
        self.background_id = 5
        self.background_tick = 0
        self.background_scroll_velocity = 0
        
        # Constants for lighting
        self.LIGHT_RENDER_DISTANCE_X = 0  # Will be set based on window size
        self.LIGHT_RENDER_DISTANCE_Y = 0  # Will be set based on window size
        
        # Colors for UI
        self.good_color = pygame.Color(10, 230, 10)
        self.bad_color = pygame.Color(230, 10, 10)


# Global instance to replace scattered globals
game_state = GameState()