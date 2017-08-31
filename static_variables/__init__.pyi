"""Typing stub for static_variables.codetools"""

from typing import Tuple, List, TypeVar, Optional, Union, Callable, Any, Mapping, Dict
from types import FunctionType, CodeType

# Submodules
codetools: Any
opcode_desc: Any

TYPE_CHECKING: bool

__all__: Tuple[str, ...]


__author__: str
__credits__: List[str]
__license__: str
__version__: str
__maintainer__: str
__author_email__: str
__email__: str
__status__: str

EMPTY_SET: set
NoValueType: type
NO_VALUE: NoValueType

_FLAG_MASK: int

_GET_ATTRIBUTE: Mapping[str, Callable[
    [FunctionType],
    Union[
        CodeType,
        Dict[str, Any],
        str,
        None,
        Tuple[Any, ...],
        int,
        bytes
    ]
]]

T = TypeVar('T')
try:
    CellType = type((lambda x=None: lambda: x)().__closure__[0])
except AttributeError:
    try:
        CellType = type((lambda x=None: lambda: x)().func_closure[0])
    except (AttributeError, IndexError):
        CellType = Any
except IndexError:
    CellType = Any

def static(expression: T) -> T:
    return expression


def _evaluate_static(f: FunctionType, code: bytes) -> Any:
    ...


def make_cell(value: Any) -> CellType:
    ...


INVALID_STATIC_VARIABLES: Tuple[str, ...]
STATIC_FLAG_MASK: int


def resolve_static(
        f: Optional[FunctionType]=None,
        empty_set_literal: bool=False,
        static_variables: Optional[Mapping[str, Any]]=None
) -> Union[FunctionType, Callable[[FunctionType], FunctionType]]:
    if f is None:
        def decorator(f):
            return resolve_static(f, empty_set_literal=empty_set_literal)
        return decorator
    return f


def check_static() -> int:
    return 0

del T, CellType
