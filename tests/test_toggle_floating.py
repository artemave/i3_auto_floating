from unittest.mock import Mock, patch
import json

from sway_auto_floating.toggle_floating import main


class TestToggleFloating:
    def setup_method(self):
        self.mock_conn = Mock()
        self.mock_focused = Mock()
        self.mock_focused.id = 123
        self.mock_focused.app_id = "firefox"
        self.mock_focused.name = "Mozilla Firefox"

        # Mock tree structure
        mock_tree = Mock()
        mock_tree.find_focused.return_value = self.mock_focused
        mock_tree.leaves.return_value = [self.mock_focused]
        self.mock_conn.get_tree.return_value = mock_tree

    @patch('sway_auto_floating.toggle_floating.i3ipc.Connection')
    def test_toggle_to_floating_saves_state(self, mock_connection, temp_state_file):
        mock_connection.return_value = self.mock_conn
        self.mock_focused.floating = "auto_off"  # Window becomes floating

        main()

        # Verify floating toggle command was called
        self.mock_focused.command.assert_called_once_with('floating toggle')

        # Verify state was updated
        final_state = json.loads(temp_state_file.read_text())
        assert final_state == {"wayland::firefox": True}

    @patch('sway_auto_floating.toggle_floating.i3ipc.Connection')
    def test_toggle_to_tiled_removes_from_state(self, mock_connection, temp_state_file):
        mock_connection.return_value = self.mock_conn
        self.mock_focused.floating = "auto_on"  # Window becomes tiled

        # Start with firefox in state
        temp_state_file.write_text(json.dumps({"wayland::firefox": True}))

        main()

        # Verify floating toggle command was called
        self.mock_focused.command.assert_called_once_with('floating toggle')

        # Verify state was updated (key removed)
        final_state = json.loads(temp_state_file.read_text())
        assert final_state == {}

    @patch('sway_auto_floating.toggle_floating.i3ipc.Connection')
    def test_toggle_preserves_other_state_entries(self, mock_connection, temp_state_file):
        mock_connection.return_value = self.mock_conn
        self.mock_focused.floating = "auto_on"  # Window becomes tiled

        # Start with multiple entries in state
        initial_state = {
            "wayland::firefox": True,
            "wayland::terminal": True
        }
        temp_state_file.write_text(json.dumps(initial_state))

        main()

        # Verify only firefox key was removed
        final_state = json.loads(temp_state_file.read_text())
        assert final_state == {"wayland::terminal": True}

    @patch('sway_auto_floating.toggle_floating.i3ipc.Connection')
    def test_toggle_with_multiple_windows_same_app(self, mock_connection, temp_state_file):
        mock_connection.return_value = self.mock_conn
        self.mock_focused.floating = "auto_off"  # Window becomes floating

        # Add another firefox window to force specific key generation
        other_firefox = Mock()
        other_firefox.id = 456
        other_firefox.app_id = "firefox"
        other_firefox.name = "Firefox - Other Tab"

        mock_tree = Mock()
        mock_tree.find_focused.return_value = self.mock_focused
        mock_tree.leaves.return_value = [self.mock_focused, other_firefox]
        self.mock_conn.get_tree.return_value = mock_tree

        main()

        # Should use specific key because multiple firefox windows exist
        final_state = json.loads(temp_state_file.read_text())
        expected_key = "wayland::firefox::Mozilla Firefox"
        assert final_state == {expected_key: True}
