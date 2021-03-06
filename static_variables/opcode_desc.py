"""Description of how opcodes affect the stack"""

import opcode
import dis
try:
    from itertools import izip_longest as zip_longest
except ImportError:
    from itertools import zip_longest


__all__ = (
    'get_stack_change', 'create_instruction', 'reassemble', 'validate_bytecode',
    'is_non_global_scope_getter', 'is_variable_manipulator'
)


def _neg_arg(i):
    return -i.argval


def _neg_arg_p(i):
    return _neg_arg(i) + 1


def _error_raiser(error):
    def ret(i):
        raise error
    return ret


def get_stack_change(instruction):
    """
    Returns the number that the amount of objects on the stack changes by after executing an instruction.
    Will raise an error if it is not in the `stack_change` variable.
    """
    x = stack_change.get(instruction.opname)
    if x is None:
        raise SyntaxError('Unrecognised command: ' + instruction.opname)
    if type(x) is int:
        return x

    return x(instruction)

_unexpected_argument = 'Opcode {!r} ({!r}) should not have an arg, but has arg {!r}'.format
_expected_argument = 'Opcode {!r} ({!r}) should have an arg, but doesn\'t'.format


def create_instruction(op_name_or_code, arg=None, argval=None, argrepr='', offset=None, starts_line=None, is_jump_target=False):
    if type(op_name_or_code) is int:
        opcode_ = op_name_or_code
        try:
            if opcode_ < 0:
                opname = [][-1]  # Raise a sensible error context
            else:
                opname = opcode.opname[opcode_]
        except IndexError:
            raise ValueError('Unknown opcode: ' + repr(opcode_))
    elif type(op_name_or_code) is str:
        opname = op_name_or_code
        try:
            opcode_ = opcode.opmap[opname]
        except KeyError:
            raise ValueError('Unknown opname: ' + repr(opname))
    else:
        raise TypeError('op_name_or_code must be a str or int')
    if (opcode_ >= opcode.HAVE_ARGUMENT) == (arg is None):
        if arg is None:
            raise ValueError(_expected_argument(opname, opcode_))
        raise ValueError(_unexpected_argument(opname, opcode_, arg))
    if arg is not None and arg > 256:
        for i in range(~((-arg.bit_length()) // 8), 0, -1):
            extended_arg = arg >> (8 * i)
            arg &= (1 << 8 * i) - 1
            yield dis.Instruction('EXTENDED_ARG', dis.EXTENDED_ARG, extended_arg, extended_arg, repr(extended_arg), offset, starts_line, False)
    yield dis.Instruction(opname, opcode_, arg, argval, argrepr, offset, starts_line, is_jump_target)


def create_instructions(*arguments):
    for args in arguments:
        for i in create_instruction(*args):
            yield i


def reassemble(instructions):
    code = bytearray()
    for i in instructions:
        opcode_ = i.opcode
        code.append(opcode_)
        if opcode_ >= opcode.HAVE_ARGUMENT:
            if i.arg is None:
                raise ValueError(_expected_argument(i.opname, opcode_))
            code.append(i.arg)
        else:
            if i.arg is not None:
                raise ValueError(_unexpected_argument(i.opname, opcode_, i.arg))
            code.append(0)
    return bytes(code)


def validate_bytecode(code):
    i = iter(code)
    for instruction, arg in zip_longest(i, i):
        if (arg is None) or (instruction < opcode.HAVE_ARGUMENT and arg):
            return False
    return True


is_non_global_scope_getter = frozenset({'LOAD_DEREF', 'LOAD_FAST', 'LOAD_CONST'}).__contains__
is_variable_manipulator = frozenset({
    'STORE_FAST', 'STORE_GLOBAL', 'STORE_DEREF',
    'LOAD_FAST', 'LOAD_GLOBAL', 'LOAD_DEREF',
    'DELETE_FAST', 'DELETE_GLOBAL', 'LOAD_GLOBAL'
}).__contains__

# A mapping of opcode name to how many items from the stack are removed when executed.
stack_change = dict.fromkeys(opcode.opmap)
stack_change.update({
    'POP_TOP': -1,
    'ROT_TWO': 0,
    'ROT_THREE': 0,
    'DUP_TOP': +1,
    'DUP_TOP_TWO': +2,
    'NOP': 0,
    'UNARY_POSITIVE': 0,
    'UNARY_NEGATIVE': 0,
    'UNARY_NOT': 0,
    'UNARY_INVERT': 0,
    'BINARY_MATRIX_MULTIPLY': -1,
    'INPLACE_MATRIX_MULTIPLY': -1,
    'BINARY_POWER': -1,
    'BINARY_MULTIPLY': -1,
    'BINARY_MODULO': -1,
    'BINARY_ADD': -1,
    'BINARY_SUBTRACT': -1,
    'BINARY_SUBSCR': -1,
    'BINARY_FLOOR_DIVIDE': -1,
    'BINARY_TRUE_DIVIDE': -1,
    'INPLACE_FLOOR_DIVIDE': -1,
    'INPLACE_TRUE_DIVIDE': -1,
    'GET_AITER': 0,
    'GET_ANEXT': None,
    'BEFORE_ASYNC_WITH': None,
    'INPLACE_ADD': -1,
    'INPLACE_SUBTRACT': -1,
    'INPLACE_MULTIPLY': -1,
    'INPLACE_MODULO': -1,
    'STORE_SUBSCR': -3,
    'DELETE_SUBSCR': -2,
    'BINARY_LSHIFT': -1,
    'BINARY_RSHIFT': -1,
    'BINARY_AND': -1,
    'BINARY_XOR': -1,
    'BINARY_OR': -1,
    'INPLACE_POWER': -1,
    'GET_ITER': 0,
    'GET_YIELD_FROM_ITER': 0,
    'PRINT_EXPR': -1,
    'LOAD_BUILD_CLASS': None,
    'YIELD_FROM': None,
    'GET_AWAITABLE': 0,
    'INPLACE_LSHIFT': -1,
    'INPLACE_RSHIFT': -1,
    'INPLACE_AND': -1,
    'INPLACE_XOR': -1,
    'INPLACE_OR': -1,
    'BREAK_LOOP': None,
    'WITH_CLEANUP_START': None,
    'WITH_CLEANUP_FINISH': None,
    'RETURN_VALUE': -1,
    'IMPORT_STAR': None,
    'SETUP_ANNOTATIONS': None,
    'YIELD_VALUE': _error_raiser(SyntaxError('Cannot yield from `static`')),
    'POP_BLOCK': None,
    'END_FINALLY': None,
    'POP_EXCEPT': None,
    'STORE_NAME': None,
    'DELETE_NAME': None,
    'UNPACK_SEQUENCE': (lambda i: -_neg_arg_p(i)),
    'FOR_ITER': None,
    'UNPACK_EX': None,
    'STORE_ATTR': None,
    'DELETE_ATTR': None,
    'STORE_GLOBAL': -1,
    'DELETE_GLOBAL': 0,
    'LOAD_CONST': +1,
    'LOAD_NAME': None,
    'BUILD_TUPLE': _neg_arg_p,
    'BUILD_LIST': _neg_arg_p,
    'BUILD_SET': _neg_arg_p,
    'BUILD_MAP': (lambda i: _neg_arg(i) * 2 + 1),
    'LOAD_ATTR': 0,
    'COMPARE_OP': -1,
    'IMPORT_NAME': None,
    'IMPORT_FROM': None,
    'JUMP_FORWARD': None,
    'JUMP_IF_FALSE_OR_POP': None,
    'JUMP_IF_TRUE_OR_POP': None,
    'JUMP_ABSOLUTE': None,
    'POP_JUMP_IF_FALSE': None,
    'POP_JUMP_IF_TRUE': None,
    'LOAD_GLOBAL': +1,
    'CONTINUE_LOOP': None,
    'SETUP_LOOP': None,
    'SETUP_EXCEPT': None,
    'SETUP_FINALLY': None,
    'LOAD_FAST': +1,
    'STORE_FAST': -1,
    'DELETE_FAST': 0,
    'STORE_ANNOTATION': None,
    'RAISE_VARARGS': _neg_arg,
    'CALL_FUNCTION': _neg_arg,
    'MAKE_FUNCTION': _error_raiser(SyntaxError('Do not make functions (or list comprehensions) in `static`')),
    'BUILD_SLICE': _neg_arg,
    'LOAD_CLOSURE': None,
    'LOAD_DEREF': +1,
    'STORE_DEREF': -1,
    'DELETE_DEREF': 0,
    'CALL_FUNCTION_KW': (lambda i: _neg_arg(i) - 2),
    'CALL_FUNCTION_EX': None,
    'SETUP_WITH': None,
    'EXTENDED_ARG': 0,
    'LIST_APPEND': None,
    'SET_ADD': None,
    'MAP_ADD': None,
    'LOAD_CLASSDEREF': None,
    'BUILD_LIST_UNPACK': _neg_arg_p,
    'BUILD_MAP_UNPACK': None,
    'BUILD_MAP_UNPACK_WITH_CALL': None,
    'BUILD_TUPLE_UNPACK': _neg_arg_p,
    'BUILD_SET_UNPACK': _neg_arg_p,
    'SETUP_ASYNC_WITH': None,
    'FORMAT_VALUE': (lambda i: -1 - (i.argval & 0x04 == 0x04)),
    'BUILD_CONST_KEY_MAP': _neg_arg,
    'BUILD_STRING': _neg_arg,
    'BUILD_TUPLE_UNPACK_WITH_CALL': _neg_arg,
})
