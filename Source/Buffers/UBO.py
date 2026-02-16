from OpenGL.GL import *

class UBO:
    def __init__(self, binding: int):
        self.ID = glGenBuffers(1)
        self.bindingPoint = binding

        self.bind()
        glBindBufferBase(GL_UNIFORM_BUFFER, binding, self.ID)
        self.unbind()

    def __del__(self):
        self.destroy()

    def bind(self):
        glBindBuffer(GL_UNIFORM_BUFFER, self.ID)

    def unbind(self):
        glBindBuffer(GL_UNIFORM_BUFFER, 0)

    def destroy(self):
        glDeleteBuffers(1, [self.ID])

    def allocate(self, size: int, usage=GL_STATIC_DRAW):
        """Allocate GPU Storage without Initializing Data."""
        self.bind()
        glBufferData(GL_UNIFORM_BUFFER, size, None, usage)
        self.unbind()

    def setData(self, size: int, offset: int, data):
        """Upload Data to the Buffer at a Given Offset."""
        self.bind()
        glBufferSubData(GL_UNIFORM_BUFFER, offset, size, data)
        self.unbind()
