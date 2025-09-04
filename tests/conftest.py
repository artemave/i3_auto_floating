import pytest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch


@pytest.fixture
def temp_state_file():
    """Provide a temporary state file for testing."""
    with TemporaryDirectory() as tmpdir:
        state_file = Path(tmpdir) / "test-state.json"
        state_file.write_text('{}')  # Start with empty state

        with patch('sway_auto_floating.shared.STATE_PATH', state_file):
            yield state_file