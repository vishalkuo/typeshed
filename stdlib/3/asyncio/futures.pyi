import sys
from typing import Any, Union, Callable, TypeVar, Type, List, Iterable, Generator, Awaitable, Optional, Tuple
from .events import AbstractEventLoop
from concurrent.futures import (
    Future as _ConcurrentFuture,
    Error,
)

if sys.version_info < (3, 8):
    from concurrent.futures import CancelledError as CancelledError
    from concurrent.futures import TimeoutError as TimeoutError
    class InvalidStateError(Error): ...

if sys.version_info >= (3, 7):
    from contextvars import Context

_T = TypeVar('_T')
_S = TypeVar('_S')

if sys.version_info < (3, 7):
    class _TracebackLogger:
        exc: BaseException
        tb: List[str]
        def __init__(self, exc: Any, loop: AbstractEventLoop) -> None: ...
        def activate(self) -> None: ...
        def clear(self) -> None: ...
        def __del__(self) -> None: ...

def isfuture(obj: object) -> bool: ...

class Future(Awaitable[_T], Iterable[_T]):
    _state: str
    _exception: BaseException
    _blocking = False
    _log_traceback = False
    if sys.version_info < (3, 6):
        _tb_logger: Type[_TracebackLogger]
    def __init__(self, *, loop: Optional[AbstractEventLoop] = ...) -> None: ...
    def __repr__(self) -> str: ...
    def __del__(self) -> None: ...
    if sys.version_info >= (3, 7):
        def get_loop(self) -> AbstractEventLoop: ...
        def _callbacks(self: _S) -> List[Tuple[Callable[[_S], Any], Context]]: ...
        def add_done_callback(self: _S, __fn: Callable[[_S], Any], *, context: Optional[Context] = ...) -> None: ...
    else:
        @property
        def _callbacks(self: _S) -> List[Callable[[_S], Any]]: ...
        def add_done_callback(self: _S, __fn: Callable[[_S], Any]) -> None: ...
    def cancel(self) -> bool: ...
    def cancelled(self) -> bool: ...
    def done(self) -> bool: ...
    def result(self) -> _T: ...
    def exception(self) -> Optional[BaseException]: ...
    def remove_done_callback(self: _S, __fn: Callable[[_S], Any]) -> int: ...
    def set_result(self, __result: _T) -> None: ...
    def set_exception(self, __exception: Union[type, BaseException]) -> None: ...
    def __iter__(self) -> Generator[Any, None, _T]: ...
    def __await__(self) -> Generator[Any, None, _T]: ...
    @property
    def _loop(self) -> AbstractEventLoop: ...

def wrap_future(future: Union[_ConcurrentFuture[_T], Future[_T]], *, loop: Optional[AbstractEventLoop] = ...) -> Future[_T]: ...
