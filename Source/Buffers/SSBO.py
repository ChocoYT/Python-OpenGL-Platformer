import ctypes
from OpenGL.GL import *

class SSBO:
    def __init__(self, binding: int) -> None:
        self.ID = glGenBuffers(1)
        
        self.binding = binding
        
        self.bind()
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, self.binding, self.ID)
        self.unbind()
                
    def bind(self)    -> None:  glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.ID)
    def unbind(self)  -> None:  glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)
    def destroy(self) -> None:  glDeleteBuffers(1, [self.ID])

    def allocate(self, size: int, usage=GL_STATIC_DRAW):
        """Allocate GPU Storage without Initializing Data."""
        self.bind()
        glBufferData(GL_SHADER_STORAGE_BUFFER, size, None, usage)
        self.unbind()

    def setData(self, data, size: int, offset: int = 0):
        """Upload Data to the Buffer at a Given Offset."""
        self.bind()
        glBufferSubData(GL_SHADER_STORAGE_BUFFER, offset, size, data)
        self.unbind()

    def map(self, access=GL_READ_WRITE):
        """Map Buffer to Client Memory."""
        self.bind()
        ptr = glMapBuffer(GL_SHADER_STORAGE_BUFFER, access)
        
        if ptr is None:
            self.unbind()
            raise RuntimeError("Failed to map SSBO")

        return ctypes.cast(ptr, ctypes.POINTER(ctypes.c_byte))

    def unmap(self):
        """Unmap Buffer to Client Memory."""
        glUnmapBuffer(GL_SHADER_STORAGE_BUFFER)
        self.unbind()
