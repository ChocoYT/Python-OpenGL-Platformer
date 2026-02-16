import sys
from OpenGL.GL import *

from shader import Shader

class Program:
    def __init__(self) -> None:  self.ID = glCreateProgram()

    def use(self)     -> None:  glUseProgram(self.ID)
    def destroy(self) -> None:  glDeleteProgram(self.ID)

    def compileProgram(self, shaders: list[Shader]) -> None:
        # Attach Shaders
        for shader in shaders:
            shader.attach(self.ID)

        glLinkProgram(self.ID)

        # Check for Linking Errors
        success = glGetProgramiv(self.ID, GL_LINK_STATUS)
        if not success:
            info_log = glGetProgramInfoLog(self.ID)
            print(f"ERROR::SHADER::PROGRAM::LINKING_FAILED\n{info_log.decode()}", file=sys.stderr)

        # Delete Shaders
        for shader in shaders:
            shader.destroy()

    @staticmethod
    def create_vertex_fragment(vert_path, frag_path) -> "Program":
        vert = Shader(vert_path, GL_VERTEX_SHADER)
        frag = Shader(frag_path, GL_FRAGMENT_SHADER)
        shaders = [vert, frag]
        
        program = Program()
        program.compileProgram(shaders)
        
        return program

    @staticmethod
    def create_compute(comp_path) -> "Program":
        comp = Shader(comp_path, GL_COMPUTE_SHADER)
        shaders = [comp]
        
        program = Program()
        program.compileProgram(shaders)
        
        return program

    @staticmethod
    def create_geometry(geom_path) -> "Program":
        geom = Shader(geom_path, GL_GEOMETRY_SHADER)
        shaders = [geom]
        
        program = Program()
        program.compileProgram(shaders)
        
        return program
