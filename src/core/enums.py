from enum import Enum

class Role(str, Enum):
    SUPER = "super"
    GESTOR = "gestor"
    FUNCIONARIO = "funcionario"
