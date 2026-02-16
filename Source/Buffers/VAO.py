import ctypes
from OpenGL.GL import *

class VAO:
    def __init__(self) -> None:  self.ID = glGenVertexArrays(1)
        
    def bind(self)    -> None:  glBindVertexArray(self.ID)
    def unbind(self)  -> None:  glBindVertexArray(0)
    def destroy(self) -> None:  glDeleteVertexArrays(1, [self.ID])

    def setAttribute(self, index, size, type, stride, offset) -> None:
        glVertexAttribPointer(index, size, type, GL_FALSE, stride, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(index)
