import alembic
from alembic.autogenerate.api import AutogenContext

from .enum_lifecycle_base import EnumLifecycleOp, render_enum_lifecycle_op


class CreateEnumOp(EnumLifecycleOp):
    operation_name = "create_enum"

    def reverse(self):
        from .drop_enum import DropEnumOp

        return DropEnumOp(
            name=self.name,
            schema=self.schema,
            enum_values=self.enum_values,
        )


@alembic.autogenerate.render.renderers.dispatch_for(CreateEnumOp)
def render_create_enum_op(autogen_context: AutogenContext, op: CreateEnumOp):
    return render_enum_lifecycle_op(autogen_context, op, "create")
