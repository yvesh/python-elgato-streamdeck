import i3ipc
import mss
import mss.tools
from PIL import Image, ImageDraw, ImageFont
from Icon.IconHelper import IconHelper


# Wrapper around i3
class I3Helper(object):
    def __init__(self, deck, config):
        self.deck = deck
        self.config = config
        self.i3 = i3ipc.Connection()
        self.workspaces = self.i3.get_workspaces()
        self.image_format = deck.key_image_format()
        self.default_icon = Image.open('Assets/i3_logo.png').convert("RGBA")

    def get_key_config(self, key):
        # Make sure we have a Key config
        for k in self.config:
            if k['key'] == key:
                return k

        return None

    def get_key_image(self, key, state):
        key_config = self.get_key_config(key)

        if key_config["type"] == "workspace":
            return self.get_key_workspace_image(key_config)
        elif key_config["type"] in ["exit", "reload", "layout", "dummy"]:
            return IconHelper.prepare_fontawesome_image(self.image_format, key_config['icon'], key_config['text'])

    def get_workspace(self, key):
        for w in self.workspaces:
            if w.num == key:
                return w

        return None

    def get_key_workspace_image(self, key_config):
        # Check if workspace is visible
        workspace = None

        for ws in self.workspaces:
            if ws.num == key_config['workspace'] and ws.visible:
                workspace = ws

        if workspace:
            rect = workspace.rect

            with mss.mss() as sct:
                monitor = {"top": rect.y, "left": rect.x, "width": rect.width, "height": rect.height}
                raw_img = sct.grab(monitor)
                img = Image.frombytes("RGB", raw_img.size, raw_img.rgb).convert('RGBA')
        else:
            # Default i3 Icon
            img = self.default_icon

        return IconHelper.prepare_image(self.image_format, img, key_config['text'])

    def go_to_workspace(self, workspace):
        self.i3.command("workspace number " + str(workspace))

        # Update workspaces (could be changed)
        self.workspaces = self.i3.get_workspaces()

    def switch_layout(self, key_config):
        self.i3.command("layout " + key_config["layout"])

        # Update workspaces (could be changed)
        self.workspaces = self.i3.get_workspaces()

    def reload(self):
        self.i3.command("reload")

    def exit(self):
        self.i3.command("exit")
