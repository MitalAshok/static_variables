"""Typing stub for static_variables.codetools"""

from typing import Tuple, List, TypeVar, Optional, Union, Callable, Any, Mapping, Dict
from types import FunctionType, CodeType

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

def static(expression: T) -> T:
    return expression


def _evaluate_static(f: FunctionType, code: bytes) -> Any:
    ...


def resolve_static(f: Optional[FunctionType]=None, empty_set_literal: bool=False) -> Union[FunctionType, Callable[[FunctionType], FunctionType]]:
    if f is None:
        def decorator(f):
            return resolve_static(f, empty_set_literal=empty_set_literal)
        return decorator
    return f


def check_static() -> int:
    return 0

del T
