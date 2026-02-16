from OpenGL.GL import *

class EBO:
    def __init__(self) -> None:  self.ID = glGenBuffers(1)
        
    def bind(self)    -> None:  glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ID)
    def unbind(self)  -> None:  glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
    def destroy(self) -> None:  glDeleteBuffers(1, [self.ID])

    def sendData(self, indices, size) -> None:
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, size, indices, GL_STATIC_DRAW)
