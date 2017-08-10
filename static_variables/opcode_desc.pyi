"""Typing stub for static_variables.opcode_desc"""

from typing import Tuple, Callable, Union, Iterable, Optional, Any, Dict, Generator

from dis import Instruction

__all__ = Tuple[str, ...]

_to_bytes: Callable[[bytearray], bytes]

def _neg_arg(i: Instruction) -> int:
    ...


def _error_raiser(error: BaseException) -> Callable[[Instruction], int]:
    ...


def get_stack_change(instruction: Instruction) -> int:
    ...


_unexpected_argument: Callable[[str, int, int], str]
_expected_argument: Callable[[str, int], str]

def create_instruction(
        op_name_or_code: Union[int, str], arg: int, argval: Any=None,
        argrepr: str='', offset: Optional[int]=None, starts_line: Optional[int]=None,
        is_jump_target: Optional[bool]=False
) -> Generator[Instruction, None, None]:
    ...


def reassemble(instructions: Iterable[Instruction]) -> bytes:
    ...


def validate_bytecode(code: Iterable[bytes]) -> bool:
    ...


is_non_global_scope_getter: Callable[[str], bool]

stack_change: Dict[str, Union[int, Callable[[Instruction], int], None]]