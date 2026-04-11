import pytest

from app.models.session import SessionState
from app.tools.registry import (
    AuthorityLevel,
    ToolCategory,
    ToolDefinition,
    ToolRegistry,
    lending_tool,
)


@pytest.fixture(autouse=True)
def clear_registry():
    saved = dict(ToolRegistry._tools)
    ToolRegistry.clear()
    yield
    ToolRegistry.clear()
    ToolRegistry._tools = saved


async def mock_handler(**kwargs):
    return {"status": "ok"}


def test_register_and_get():
    tool_def = ToolDefinition(
        name="test_tool",
        description="A test tool",
        category=ToolCategory.IDENTITY,
        handler=mock_handler,
    )
    ToolRegistry.register(tool_def)
    retrieved = ToolRegistry.get("test_tool")
    assert retrieved is not None
    assert retrieved.name == "test_tool"
    assert retrieved.category == ToolCategory.IDENTITY


def test_get_nonexistent():
    assert ToolRegistry.get("nonexistent") is None


def test_get_by_category():
    ToolRegistry.register(
        ToolDefinition(
            name="id_1", description="ID 1", category=ToolCategory.IDENTITY, handler=mock_handler
        )
    )
    ToolRegistry.register(
        ToolDefinition(
            name="id_2", description="ID 2", category=ToolCategory.IDENTITY, handler=mock_handler
        )
    )
    ToolRegistry.register(
        ToolDefinition(
            name="data_1", description="Data 1", category=ToolCategory.DATA, handler=mock_handler
        )
    )

    id_tools = ToolRegistry.get_by_category(ToolCategory.IDENTITY)
    assert len(id_tools) == 2

    data_tools = ToolRegistry.get_by_category(ToolCategory.DATA)
    assert len(data_tools) == 1


def test_get_available_for_state():
    ToolRegistry.register(
        ToolDefinition(
            name="id_tool",
            description="Identity",
            category=ToolCategory.IDENTITY,
            handler=mock_handler,
        )
    )
    ToolRegistry.register(
        ToolDefinition(
            name="data_tool",
            description="Data",
            category=ToolCategory.DATA,
            handler=mock_handler,
        )
    )
    ToolRegistry.register(
        ToolDefinition(
            name="exec_tool",
            description="Exec",
            category=ToolCategory.EXECUTION,
            handler=mock_handler,
        )
    )

    unverified_tools = ToolRegistry.get_available_for_state(SessionState.UNVERIFIED)
    assert len(unverified_tools) == 1
    assert unverified_tools[0].name == "id_tool"

    verified_tools = ToolRegistry.get_available_for_state(SessionState.VERIFIED)
    assert len(verified_tools) == 2
    tool_names = {t.name for t in verified_tools}
    assert "id_tool" in tool_names
    assert "data_tool" in tool_names

    confirmed_tools = ToolRegistry.get_available_for_state(SessionState.CONFIRMED)
    assert len(confirmed_tools) == 3


def test_default_min_state():
    tool_def = ToolDefinition(
        name="identity_tool",
        description="Identity tool",
        category=ToolCategory.IDENTITY,
        handler=mock_handler,
    )
    assert tool_def.min_session_state == SessionState.UNVERIFIED

    tool_def2 = ToolDefinition(
        name="data_tool",
        description="Data tool",
        category=ToolCategory.DATA,
        handler=mock_handler,
    )
    assert tool_def2.min_session_state == SessionState.VERIFIED

    tool_def3 = ToolDefinition(
        name="exec_tool",
        description="Exec tool",
        category=ToolCategory.EXECUTION,
        handler=mock_handler,
    )
    assert tool_def3.min_session_state == SessionState.CONFIRMED


def test_lending_tool_decorator():
    @lending_tool(
        name="decorated_tool",
        description="A decorated tool",
        category=ToolCategory.IDENTITY,
        requires_confirmation=True,
        authority_level=AuthorityLevel.WRITE,
    )
    async def my_tool(**kwargs):
        return {"result": "decorated"}

    tool_def = ToolRegistry.get("decorated_tool")
    assert tool_def is not None
    assert tool_def.name == "decorated_tool"
    assert tool_def.requires_confirmation is True
    assert tool_def.authority_level == AuthorityLevel.WRITE
