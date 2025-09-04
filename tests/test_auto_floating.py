from unittest.mock import Mock, patch
import json

from sway_auto_floating.auto_floating import main


class TestAutoFloating:
    def setup_method(self):
        self.mock_conn = Mock()

        # Mock containers
        self.firefox = Mock()
        self.firefox.app_id = "firefox"
        self.firefox.name = "Firefox"
        self.firefox.id = 123

        self.terminal = Mock()
        self.terminal.app_id = "terminal"
        self.terminal.name = "Terminal"
        self.terminal.id = 456

        # Mock tree
        mock_tree = Mock()
        mock_tree.leaves.return_value = [self.firefox, self.terminal]
        self.mock_conn.get_tree.return_value = mock_tree

    @patch('sway_auto_floating.auto_floating.i3ipc.Connection')
    def test_applies_floating_to_existing_windows_at_startup(self, mock_connection, temp_state_file):
        mock_connection.return_value = self.mock_conn

        # Set state with firefox floating
        temp_state_file.write_text(json.dumps({"wayland::firefox": True}))

        main()

        # Firefox should get floating command, terminal should not
        self.firefox.command.assert_called_once_with('floating enable')
        self.terminal.command.assert_not_called()

    @patch('sway_auto_floating.auto_floating.i3ipc.Connection')
    def test_applies_floating_to_new_windows_via_events(self, mock_connection, temp_state_file):
        mock_connection.return_value = self.mock_conn

        # Set state with firefox floating
        temp_state_file.write_text(json.dumps({"wayland::firefox": True}))

        main()

        # Get the registered event handler
        event_handler = self.mock_conn.on.call_args[0][1]

        # Reset command calls from startup
        self.firefox.command.reset_mock()

        # Simulate new window event
        mock_event = Mock()
        mock_event.container = self.firefox

        event_handler(self.mock_conn, mock_event)

        # Should apply floating to the new window
        self.firefox.command.assert_called_once_with('floating enable')

    @patch('sway_auto_floating.auto_floating.i3ipc.Connection')
    def test_handles_multiple_windows_same_app_with_specific_keys(self, mock_connection, temp_state_file):
        mock_connection.return_value = self.mock_conn

        # Create two firefox windows with different names
        firefox1 = Mock()
        firefox1.app_id = "firefox"
        firefox1.name = "Mozilla Firefox - Page 1"
        firefox1.id = 123

        firefox2 = Mock()
        firefox2.app_id = "firefox"
        firefox2.name = "Mozilla Firefox - Page 2"
        firefox2.id = 456

        mock_tree = Mock()
        mock_tree.leaves.return_value = [firefox1, firefox2]
        self.mock_conn.get_tree.return_value = mock_tree

        # State uses specific key for one of the windows
        temp_state_file.write_text(json.dumps({
            "wayland::firefox::Mozilla Firefox - Page 1": True
        }))

        main()

        # Only the specifically keyed window should float
        firefox1.command.assert_called_once_with('floating enable')
        firefox2.command.assert_not_called()

    @patch('sway_auto_floating.auto_floating.i3ipc.Connection')
    def test_reads_fresh_state_on_each_event(self, mock_connection, temp_state_file):
        mock_connection.return_value = self.mock_conn

        # Start with empty state
        main()

        # Get event handler
        event_handler = self.mock_conn.on.call_args[0][1]

        # Update state file after startup
        temp_state_file.write_text(json.dumps({"wayland::firefox": True}))

        # Simulate window event
        mock_event = Mock()
        mock_event.container = self.firefox

        event_handler(self.mock_conn, mock_event)

        # Should apply floating based on the updated state
        self.firefox.command.assert_called_with('floating enable')
