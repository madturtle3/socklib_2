from typing import Coroutine
from textual.app import App, ComposeResult
import textual.binding
import textual.color as color
import textual.containers
import textual.events
import textual.keys
import textual.layouts
import textual.layouts.horizontal
import textual.message
from textual.screen import Screen
import textual.widgets as widgets
import textual

class ButtonList(textual.containers.Horizontal):
    BINDINGS=[("right","next_item"),("left","previous_item")]
    index = 0
    @textual.on(textual.events.Focus)
    def on_focus(self):
        self.index = 0

    
    def action_next_item(self):
        self.index += 1
        if self.index >= len(self.children):
            self.index = 0
        self.children[self.index].focus()
        
    def action_previous_item(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.children)-1
        self.children[self.index].focus()
        
        

class MsgBox(widgets.Input):
    BINDINGS = [
        textual.binding.Binding("ctrl+r", "app.focus_previous", "View Messagebox")
    ]


class MsgLog(widgets.RichLog):
    BINDINGS = [textual.binding.Binding("escape", "app.focus_next", "Go back")]


class ChatApp(App):
    """A Textual app to manage stopwatches."""

    AUTO_FOCUS = "#msgbox"
    CSS_PATH = "richtest.tcss"
    BINDINGS = [("ctrl+q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield MsgLog(classes="mains", id="log")
        yield ButtonList(widgets.Button("Hello!"),widgets.Button("World!"))
        yield MsgBox(placeholder="message...", id="msgbox", classes="mains")
        yield widgets.Footer()

    @textual.on(widgets.Input.Submitted)
    def handle_input(self):
        msgbox = self.get_child_by_id("msgbox", expect_type=widgets.Input)
        richlog = self.get_child_by_id("log", expect_type=widgets.RichLog)
        if msgbox.value:
            richlog.write(msgbox.value)
            msgbox.clear()


if __name__ == "__main__":
    app = ChatApp(ansi_color=True)
    app.run(mouse=False)
