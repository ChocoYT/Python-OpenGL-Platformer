import glfw, glm
from typing import Union

from settings import *

number = Union[int, float]

class Camera2D:
    def __init__(
            self,
            window,
            position: tuple[number, number] | None = (0, 0),
            zoom:     float                 | None = 1.0
        ) -> None:
        
        self.window = window
        self.width, self.height = glfw.get_window_size(window)
        
        self.position = glm.vec2(position)
        self.zoom     = zoom

        self._update_proj_matrix()
        self._update_view_matrix()
        
    def update(self, window, dt: float) -> None:
        move_vector = glm.vec2(
            int(glfw.get_key(window, glfw.KEY_D) == glfw.PRESS) - int(glfw.get_key(window, glfw.KEY_A) == glfw.PRESS),
            int(glfw.get_key(window, glfw.KEY_W) == glfw.PRESS) - int(glfw.get_key(window, glfw.KEY_S) == glfw.PRESS)
        )
        
        if glm.length2(move_vector) == 0:  return
        
        move_vector = glm.normalize(move_vector) * dt * CAMERA_SPEED
        self.change_position(move_vector.x, move_vector.y)
        
    def _update_proj_matrix(self) -> None:
        """Calculate Projection Matrix"""
        half_w = (self.width  * 0.5) / self.zoom
        half_h = (self.height * 0.5) / self.zoom
        
        self.proj = glm.ortho(-half_w, half_w, -half_h, half_h, -1.0, 1.0)
        
    def _update_view_matrix(self) -> None:
        """Calculate View Matrix"""
        self.view = glm.mat4(1.0)
        self.view = glm.translate(self.view, glm.vec3(-self.position.x, -self.position.y, 0.0))

    def set_position(self, x: float, y: float) -> None:
        """Set Camera Position."""
        self.position = glm.vec2(x, y)
        self._update_view_matrix()

    def change_position(self, dx: float, dy: float) -> None:
        """Change Camera Position."""
        self.position += glm.vec2(dx, dy)
        self._update_view_matrix()

    def set_zoom(self, zoom: float) -> None:
        """Set Zoom Level."""
        self.zoom = max(0.1, zoom)
        self._update_proj_matrix()
        
    def change_zoom(self, dz: float) -> None:
        """Change Zoom Level."""
        self.zoom = max(0.1, self.zoom + dz)
        self._update_proj_matrix()

    def get_proj(self) -> glm.mat4x4:  return self.proj
    def get_view(self) -> glm.mat4x4:  return self.view
