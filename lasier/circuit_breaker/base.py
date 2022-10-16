import inspect
import logging
from typing import Any, Iterable, Optional, Type

from lasier.types import Timeout

from .rules.base import BaseRule

logger = logging.getLogger(__name__)
_ONE_MINUTE = 60
_ONE_HOUR = 3600


class CircuitBreakerBase:
    def __init__(
        self,
        rule: BaseRule,
        # cache: Any,
        failure_exception: Type[Exception],
        failure_timeout: Timeout = _ONE_HOUR,
        circuit_timeout: Timeout = _ONE_HOUR,
        catch_exceptions: Optional[Iterable[Type[Exception]]] = None,
        catch_status: Optional[Iterable[Type[int]]] = None,
        success_threshold=3,
    ) -> None:
        self.rule = rule
        # self.cache = cache
        self.failure_timeout = failure_timeout
        self.circuit_timeout = circuit_timeout
        self.circuit_cache_key = 'circuit_{}'.format(rule.failure_cache_key)
        self.failure_exception = failure_exception
        self.catch_exceptions = catch_exceptions or (Exception,)
        self.catch_status = catch_status
        self.state_key = f'state_{rule.request_cache_key}'
        self.state = "closed"
        self.success_threshold = success_threshold  # no. of success requests when state=half-open to close the circuit
        self.success_counter_key = f'success_{rule.request_cache_key}'

    def _is_catchable_exception(self, exception: Type[Exception]) -> bool:
        return inspect.isclass(exception) and any(
            issubclass(exception, exception_class)
            for exception_class in self.catch_exceptions
        )

    def _is_catchable_status(self, status_code: int) -> bool:
        if self.catch_status and status_code in self.catch_status:
            return True
        return False

    def _notify_open_circuit(self) -> None:
        logger.critical(
            f'Open circuit for {self.rule.failure_cache_key} '
            f'{self.circuit_cache_key}'
        )

    def _notify_half_open_circuit(self) -> None:
        logger.critical(
            f'Half-Open circuit for {self.rule.request_cache_key} '
        )

    def _notify_closed_circuit(self) -> None:
        logger.critical(f'Closed circuit for {self.rule.request_cache_key} ')

    def _notify_max_failures_exceeded(self) -> None:
        logger.info(f'Max failures exceeded by: {self.rule.failure_cache_key}')
