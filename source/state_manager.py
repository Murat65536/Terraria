from typing import Any, List
import pygame

class State:
    def update(self, dt: float) -> None:
        pass
    def draw(self, surface: pygame.Surface) -> None:
        pass
    def handle_events(self, events: List[pygame.event.Event]) -> None:
        pass

class StateManager:
    def __init__(self):
        self.states = {}
        self.current_state_name = None
        self.current_state = None

    def add_state(self, name: str, state: State) -> None:
        self.states[name] = state

    def update(self, dt: float) -> None:
        if self.current_state:
            self.current_state.update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        if self.current_state:
            self.current_state.draw(surface)

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        if self.current_state:
            self.current_state.handle_events(events)
