import alembic
from alembic.autogenerate.api import AutogenContext

from .enum_lifecycle_base import EnumLifecycleOp, render_enum_lifecycle_op


class DropEnumOp(EnumLifecycleOp):
    operation_name = "drop_enum"

    def reverse(self):
        from .create_enum import CreateEnumOp

        return CreateEnumOp(
            name=self.name,
            schema=self.schema,
            enum_values=self.enum_values,
        )


@alembic.autogenerate.render.renderers.dispatch_for(DropEnumOp)
def render_drop_enum_op(autogen_context: AutogenContext, op: DropEnumOp):
    return render_enum_lifecycle_op(autogen_context, op, "drop")
