import numpy as np
from OpenGL.GL import *

from Buffers.VAO import VAO
from Buffers.VBO import VBO
from Buffers.EBO import EBO

class Mesh:
    def __init__(
            self,
            vertices,
            indices
        ) -> None:
        """
        Vertices: List of Tuples ((x, y, z), (u, v, l))
        Indices:  List of Integers
        """
        self.vertices = vertices
        self.indices = indices

        # GPU buffer handles
        self.VAO0 = VAO()
        self.VBO0 = VBO()
        self.EBO0 = EBO()

        self.update()

    def update(self) -> None:
        """Upload Data to GPU and Set Attribute Pointers."""
        vertex_data = []
        for pos, uv in self.vertices:
            vertex_data.extend(pos)
            vertex_data.extend(uv)
            
        vertex_data = np.array(vertex_data,  dtype=np.float32)
        index_data  = np.array(self.indices, dtype=np.uint32)

        # Upload to GPU
        self.VAO0.bind()

        self.VBO0.bind()
        self.VBO0.sendData(vertex_data, vertex_data.nbytes)

        self.EBO0.bind()
        self.EBO0.sendData(index_data, index_data.nbytes)

        stride = 6 * 4  # 6 Floats per Vertex (4 Bytes each)

        # Set Attributes
        self.VAO0.setAttribute(0, 3, GL_FLOAT, stride, 0)      # Position (vec3)
        self.VAO0.setAttribute(1, 3, GL_FLOAT, stride, 3 * 4)  # UVs      (vec3)

        self.VBO0.unbind()

    def draw(self) -> None:
        """Render Mesh"""
        self.VAO0.bind()
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        self.VAO0.unbind()

    def clear(self) -> None:
        """Clear CPU-side Data."""
        self.vertices = []
        self.indices  = []

    def destroy(self) -> None:
        """Delete GPU Buffers, Vertices and Indices"""
        self.VAO0.destroy()
        self.VBO0.destroy()
        self.EBO0.destroy()
        
        self.clear()
