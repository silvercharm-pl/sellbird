"""Windows-safe, offline fail-closed checks for the Sellbird pilot."""
import pytest
from tests.test_gmail_inbox import provider, message

@pytest.mark.asyncio
async def test_gmail_first_page_failure_never_returns_empty_success():
    with pytest.raises(RuntimeError):
        await provider([None]).get_replies()

@pytest.mark.asyncio
async def test_gmail_second_page_failure_never_returns_partial_success():
    with pytest.raises(RuntimeError):
        await provider([{"messages": [{"id": "first"}], "nextPageToken": "next"}, message("first"), None]).get_replies()

@pytest.mark.asyncio
async def test_gmail_second_page_optout_is_visible_to_provider():
    p = provider([{"messages": [{"id": "old"}], "nextPageToken": "next"}, message("old"), {"messages": [{"id": "stop"}]}, message("stop", "bob@beta.com", "unsubscribe")])
    replies = await p.get_replies()
    assert [m.provider_id for m in replies] == ["old", "stop"]
    assert replies[1].body == "unsubscribe"
