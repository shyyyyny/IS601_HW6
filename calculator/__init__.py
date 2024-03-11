from decimal import Decimal
from typing import Callable
import importlib


class Calculator:

    @staticmethod
    def _perform_operation(
        a: Decimal, b: Decimal, operation: Callable[[Decimal, Decimal], Decimal]
    ) -> Decimal:
        """Internal method to perform an operation."""
        from calculator.calculation import Calculation

        calculation = Calculation.create(a, b, operation)
        return calculation.perform()

    @staticmethod
    def load_operation(operation_name: str) -> Callable[[Decimal, Decimal], Decimal]:
        """Load an arithmetic operation function dynamically from a plugin."""
        try:
            plugin_module = importlib.import_module(f"plugin.{operation_name}")
            operation_func = getattr(plugin_module, operation_name)
            return operation_func
        except (ImportError, AttributeError):
            raise ValueError(f"Operation '{operation_name}' not found or invalid")

    @staticmethod
    def add(a: Decimal, b: Decimal) -> Decimal:
        return Calculator._perform_operation(a, b, Calculator.load_operation("add"))

    @staticmethod
    def subtract(a: Decimal, b: Decimal) -> Decimal:
        return Calculator._perform_operation(
            a, b, Calculator.load_operation("subtract")
        )

    @staticmethod
    def multiply(a: Decimal, b: Decimal) -> Decimal:
        return Calculator._perform_operation(
            a, b, Calculator.load_operation("multiply")
        )

    @staticmethod
    def divide(a: Decimal, b: Decimal) -> Decimal:
        return Calculator._perform_operation(a, b, Calculator.load_operation("divide"))
