from abc import ABC, abstractmethod
from typing import Iterable, Tuple, Any

import alembic
from alembic.autogenerate.api import AutogenContext

from alembic_postgresql_enum.enum_variables import enum_variables


class EnumLifecycleOp(alembic.operations.ops.MigrateOperation, ABC):
    def __init__(
        self,
        schema: str,
        name: str,
        enum_values: Iterable[str],
    ):
        self.schema = schema
        self.name = name
        self.enum_values = enum_values

    @property
    @abstractmethod
    def operation_name(self) -> str:
        pass

    def to_diff_tuple(self) -> Tuple[Any, ...]:
        return self.operation_name, self.name, self.schema, self.enum_values


def render_enum_lifecycle_op(autogen_context: AutogenContext, op: EnumLifecycleOp, method_name: str) -> str:
    """Render enum creation or deletion, method_name is either create or drop"""
    assert autogen_context.dialect is not None
    sqlalchemy_module_prefix = autogen_context.opts.get("sqlalchemy_module_prefix", "sa.")
    alembic_module_prefix = autogen_context.opts.get("alembic_module_prefix", "op.")
    bind = f"{alembic_module_prefix}get_bind()"

    variable_name = enum_variables.get(op.schema, op.name)
    if variable_name is not None:
        enum_variables.add_definitions_to_imports(autogen_context)
        return f"{variable_name}.{method_name}({bind})"

    arguments = [repr(value) for value in op.enum_values]
    arguments.append(f"name={op.name!r}")
    if op.schema != autogen_context.dialect.default_schema_name:
        arguments.append(f"schema={op.schema!r}")

    return f"{sqlalchemy_module_prefix}Enum({', '.join(arguments)}).{method_name}({bind})"
