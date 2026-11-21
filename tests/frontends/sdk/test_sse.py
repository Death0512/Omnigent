"""Focused tests for the Python SDK SSE byte-stream boundary handling."""

from __future__ import annotations

from collections.abc import AsyncIterator

import pytest
from omnigent_client._events import TextDelta
from omnigent_client._sse import parse_sse_stream


async def _chunks(*chunks: bytes) -> AsyncIterator[bytes]:
    for chunk in chunks:
        yield chunk


@pytest.mark.asyncio
async def test_sse_preserves_utf8_code_points_split_across_transport_chunks() -> None:
    """Transport chunk boundaries must not replace a split UTF-8 code point."""
    events = [
        event
        async for event in parse_sse_stream(
            _chunks(
                b'event: response.output_text.delta\ndata: {"delta":"\xc3',
                b'\xa9"}\n',
                b"data: [DONE]\n",
            )
        )
    ]

    assert events == [TextDelta(delta="é")]
