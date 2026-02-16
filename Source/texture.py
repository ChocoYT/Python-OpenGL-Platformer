import numpy as np
from PIL       import Image
from OpenGL.GL import *

class Texture:
    def __init__(self, path: str):
        self.ID = glGenTextures(1)
        
        self.path = path
        
        self.width  = 0
        self.height = 0

        self._load()

    def _load(self) -> None:
        img = Image.open(self.path).convert("RGBA")
        self.width, self.height = img.size
        img_data = np.array(img, dtype=np.uint8)

        self.bind()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        # Texture Parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        self.unbind()

    def bind(self, slot: int = 0) -> None:
        glActiveTexture(GL_TEXTURE0 + slot)
        glBindTexture(GL_TEXTURE_2D, self.ID)

    def unbind(self) -> None:  glBindTexture(GL_TEXTURE_2D, 0)
    
    def delete(self) -> None:
        glDeleteTextures([self.ID])
        self.ID = 0
