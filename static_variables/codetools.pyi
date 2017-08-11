"""Typing stub for static_variables.codetools"""

from typing import Tuple, Dict, Union, Any, Callable, TypeVar, overload
from types import FunctionType, CodeType

__all__: Tuple[str, ...]

_constructor_args = Union[
    CodeType,  # f.__code__
    Dict[str, Any],  # f.__globals__
    str,  # f.__name__
    None,  # f.__defaults__, f.__closure__
    Tuple[Any, ...],  # f.__defaults__, f.__code__.co_consts
    # Tuple[CellType, ...],  # f.__closure__  # Subset of above
    int,  # f.__code__.co_arg_count, ..., f.__code__.co_flags, f.__code__.co_firstlineno
    bytes,  # f.__code__.co_code, f.__code__.co_lnotab
    Tuple[str, ...],  # f.__code__.co_name, f.__code__.co_freevars, f.__code__.co_cellvars
]

T = TypeVar('T')

CODE_ATTR: str
GLOBALS_ATTR: str
NAME_ATTR: str
DEFAULTS_ATTR: str
CLOSURE_ATTR: str

DICT_ATTR: str

FUNCTION_ARGS: Tuple[str, str, str, str, str]

METHOD_FUNC_ATTR: str
METHOD_SELF_ATTR: str

METHOD_HAS_CLASS: bool

METHOD_ARGS = Union[Tuple[str, str, str], Tuple[str, str]]

HAS_KWARGS: bool

CODE_ARGS: Tuple[str, ...]

def copy(x: T) -> T:
    ...


def deepcopy(x: T) -> T:
    ...


_ATTRIBUTE_ALIASES: Callable[[str], Union[str, None]]

_NORMALISE_CACHE: Dict[str, Tuple[bool, str]]


def _normalise_func_attr(attribute: str) -> Tuple[bool, str]:
    ...


def __normalise_func_attr(attribute: str) -> Tuple[bool, str]:
    ...


@overload
def set_attr(f: FunctionType, attribute: str, new_value: _constructor_args) -> FunctionType:
    ...


@overload
def set_attr(f: FunctionType, **kwargs: _constructor_args) -> FunctionType:
    ...


def set_attr(f: FunctionType, *args: Union[str, _constructor_args], **kwargs: _constructor_args) -> FunctionType:
    ...


def _set_attr(f: FunctionType, attribute: str, new_value: _constructor_args) -> FunctionType:
    ...


def _set_attrs(f: FunctionType, **new_attributes: _constructor_args) -> FunctionType:
    ...


def get_attr(f: FunctionType, attribute: str) -> _constructor_args:
    ...


def attr_getter(attribute: str) -> Callable[[FunctionType], _constructor_args]:
    ...

del _constructor_args, T
