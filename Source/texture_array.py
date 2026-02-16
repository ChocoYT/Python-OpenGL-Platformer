import numpy as np
from PIL       import Image
from OpenGL.GL import *

class TextureArray:
    def __init__(self, filepaths: list[str]):
        self.ID = glGenTextures(1)
        
        self.filepaths = filepaths
        self.layers    = len(filepaths)
        
        self.width = 0
        self.height = 0
        
        self._load()

    def _load(self) -> None:
        images: list[Image.Image] = []
        max_width, max_height = 0, 0
        for path in self.filepaths:
            img = Image.open(path).convert("RGBA")
            
            if img.width  > max_width:   max_width  = img.width
            if img.height > max_height:  max_height = img.height
            
            images.append(img)

        self.width, self.height = max_width, max_height

        self.bind(activate=False)
        glTexStorage3D(GL_TEXTURE_2D_ARRAY, 1, GL_RGBA8, self.width, self.height, self.layers)

        for i, img in enumerate(images):
            if img.size != (self.width, self.height):
                padded = Image.new("RGBA", (self.width, self.height))
                padded.paste(img, (0, 0))
                img = padded
            
            img_data = np.array(img, dtype=np.uint8)
            glTexSubImage3D(GL_TEXTURE_2D_ARRAY, 0, 0, 0, i, self.width, self.height, 1, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        # Texture Parameters
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        
        self.unbind()

    def bind(self, slot: int | None = 0, activate: bool | None = True) -> None:
        if activate:
            glActiveTexture(GL_TEXTURE0 + slot)
        
        glBindTexture(GL_TEXTURE_2D_ARRAY, self.ID)

    def unbind(self) -> None:
        glBindTexture(GL_TEXTURE_2D_ARRAY, 0)

    def destroy(self) -> None:
        glDeleteTextures(1, [self.ID])
