from dataclasses import dataclass
from typing import Callable, Optional


def default_enum_variable_name(schema: Optional[str], name: str) -> str:
    """Default name of module level variable for enum, schema is None for enums of default schema"""
    if schema is None:
        return name
    return f"{schema}_{name}"


@dataclass
class Config:
    add_type_ignore: bool = False
    type_ignore_comment: str = "  # type: ignore[attr-defined]"
    include_name: Callable[[str], bool] = lambda _: True
    drop_unused_enums: bool = True
    detect_enum_values_changes: bool = True
    force_dialect_support: bool = False
    ignore_enum_values_order: bool = False
    module_level_enums: bool = False
    enum_variable_name: Callable[[Optional[str], str], str] = default_enum_variable_name


_config = Config()


def set_configuration(config: Config):
    global _config
    _config = config


def get_configuration() -> Config:
    return _config
