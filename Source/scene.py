import glm
from OpenGL.GL import *

from camera   import Camera2D
from mesh     import Mesh
from program  import Program

from settings import *

class Scene:
    def __init__(self):
        from loader import assets

        self.assets = assets
        self.tiles = {}
        
        vertices = [
        ((0.0, 0.0, 0.0), (0.0, 0.0)),
        ((1.0, 0.0, 0.0), (1.0, 0.0)),
        ((1.0, 1.0, 0.0), (0.0, 1.0)),
        ((0.0, 1.0, 0.0), (1.0, 1.0)),
        ]
        indices = [
            0, 1, 2,
            2, 3, 0
        ]
        
        self.mesh = Mesh(vertices, indices)
        
    def add_tile(self, x: int, y: int, z: int, name: str) -> None:
        self.tiles[(x, y, z)] = name
    
    def update(self, camera: Camera2D, dt: float) -> None:
        self._create_geometry(camera)
    
    def _create_geometry(self, camera: Camera2D) -> None:
        vertices = []
        indices = []
        idx_offset = 0
        
        textures  = self.assets["textures"]
        tile_meta = self.assets["meta"]["tiles"]
        tile_size = self.assets["meta"]["tile_size"]
        
        #for x in range(camera.position.x // )

        for world_pos, name in self.tiles.items():
            if name not in tile_meta:
                print(f"Warning: Tile {name} not in metadata")
                continue
            
            x_world, y_world, z_world = world_pos
            
            tx, ty, layer = tile_meta[name]

            sheet_width  = textures.width
            sheet_height = textures.height

            # UVs
            u0 = tx * tile_size / sheet_width
            v0 = ty * tile_size / sheet_height
            u1 = (tx + 1) * tile_size / sheet_width
            v1 = (ty + 1) * tile_size / sheet_height
            
            v0, v1 = v1, v0  # Flip Image

            # Quad Positions
            x0, y0 = x_world, y_world
            x1, y1 = x0 + 1,  y0 + 1

            quad_vertices = [
                ((x0, y0, z_world), (u0, v0, float(layer))),
                ((x1, y0, z_world), (u1, v0, float(layer))),
                ((x1, y1, z_world), (u1, v1, float(layer))),
                ((x0, y1, z_world), (u0, v1, float(layer))),
            ]

            vertices.extend(quad_vertices)
            indices.extend([
                idx_offset, idx_offset + 1, idx_offset + 2,
                idx_offset + 2, idx_offset + 3, idx_offset
            ])
            idx_offset += 4

        # Update Mesh
        self.mesh.vertices = vertices
        self.mesh.indices = indices
        self.mesh.update()

    def draw(self, camera: Camera2D, program: Program) -> None:
        program.use()
        
        glUniformMatrix4fv(glGetUniformLocation(program.ID, "projMatrix"), 1, GL_FALSE, glm.value_ptr(camera.get_proj()))
        glUniformMatrix4fv(glGetUniformLocation(program.ID, "viewMatrix"), 1, GL_FALSE, glm.value_ptr(camera.get_view()))
        
        glUniform1f(glGetUniformLocation(program.ID, "scale"), SCREEN_SCALE)
        
        self.assets["textures"].bind(slot=0)
        glUniform1i(glGetUniformLocation(program.ID, "texArray"), 0)
        
        self.mesh.draw()

    def destroy(self) -> None:
        self.mesh.destroy()
