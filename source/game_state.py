"""
Game state management to replace scattered global variables.
"""
import pygame


class GameState:
    """Manages global game state variables previously scattered as globals."""
    # Background and visual effects
    parallax_position: tuple[float, float] = (0, 0)
    fade_background_id: int = -1
    fade_back: bool = False
    fade_float: float = 0.0

    # UI and text rendering
    hand_text: pygame.Surface = pygame.Surface((0, 0))
    stats_text: pygame.Surface = pygame.Surface((0, 0))
    last_hovered_item = None

    # Lighting system
    light_surface: pygame.Surface = pygame.Surface((0, 0))
    newest_light_surface: pygame.Surface = pygame.Surface((0, 0))
    newest_light_surface_position: tuple[float, float] = (0, 0)
    light_min_x: int = 0
    light_max_x: int = 0
    light_min_y: int = 0
    light_max_y: int = 0
    thread_active: bool = False
    last_thread_time: float = 0.2
    last_thread_start: float = pygame.time.get_ticks()
    map_light: list[list[int]] = []

    # Menu system
    save_select_surface: pygame.Surface = pygame.Surface((315, 360), pygame.SRCALPHA)
    save_select_y_offset: int = 0
    save_select_y_velocity: int = 0

    # Item interaction
    can_drop_holding: bool = False
    can_pickup_item: bool = False
    item_drop_tick: int = 0
    item_drop_rate: int = 0

    # UI state
    exit_button_hover: bool = False

    # Timing and performance
    auto_save_tick: int = 0
    fps_tick: int = 0
    old_time_milliseconds: int = pygame.time.get_ticks()

    # Background effects
    background_id: int = 5
    background_tick: int = 0
    background_scroll_velocity: int = 0

    # Constants for lighting
    LIGHT_RENDER_DISTANCE_X = 0  # Will be set based on window size
    LIGHT_RENDER_DISTANCE_Y = 0  # Will be set based on window size

    # Colors for UI
    good_color = pygame.Color(10, 230, 10)
    bad_color = pygame.Color(230, 10, 10)