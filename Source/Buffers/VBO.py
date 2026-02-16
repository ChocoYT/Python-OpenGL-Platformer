from OpenGL.GL import *

class VBO:
    def __init__(self) -> None:  self.ID = glGenBuffers(1)
        
    def bind(self)    -> None:  glBindBuffer(GL_ARRAY_BUFFER, self.ID)
    def unbind(self)  -> None:  glBindBuffer(GL_ARRAY_BUFFER, 0)
    def destroy(self) -> None:  glDeleteBuffers(1, [self.ID])

    def sendData(self, vertices, size) -> None:
        glBufferData(GL_ARRAY_BUFFER, size, vertices, GL_STATIC_DRAW)
