import sys
from OpenGL.GL import *

class Shader:
    def __init__(self, path, shader_type):
        self.ID = glCreateShader(shader_type)

        with open(path, 'r') as f:
            source = f.read()
        
        glShaderSource(self.ID, source)
        glCompileShader(self.ID)

        # Check for compilation errors
        success = glGetShaderiv(self.ID, GL_COMPILE_STATUS)
        if not success:
            info_log = glGetShaderInfoLog(self.ID)
            print(f"ERROR::SHADER::COMPILATION_FAILED\n{info_log.decode()}", file=sys.stderr)

    def attach(self, program_id):
        """Attach this shader to a given program."""
        glAttachShader(program_id, self.ID)

    def destroy(self):
        """Delete this shader from OpenGL."""
        glDeleteShader(self.ID)
