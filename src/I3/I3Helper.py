import i3ipc
import mss
import mss.tools
from PIL import Image, ImageDraw, ImageFont


# Wrapper around i3
class I3Helper(object):
    def __init__(self, deck):
        self.i3 = i3ipc.Connection()
        self.workspaces = self.i3.get_workspaces()
        self.image_format = deck.key_image_format()
        self.default_icon = Image.open('Assets/i3_logo.png').convert("RGBA")

    def get_workspace(self, key):
        for w in self.workspaces:
            if w.num == key:
                return w

        return None

    def go_to_workspace(self, key):
        self.i3.command('workspace number ' + str(key))

        # Update workspaces (could be changed)
        self.workspaces = self.i3.get_workspaces()

    def get_key_image(self, key, state):
        if key < 10:
            return self.get_key_workspace_image(key)

    def get_key_workspace_image(self, workspace_num):
        # Check if workspace is visible
        workspace = None

        for ws in self.workspaces:
            if ws.num == workspace_num and ws.visible:
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

        return self.prepare_image(img, str(workspace_num))

    def prepare_image(self, icon, text):
        rgb_order = self.image_format['order']
        width = self.image_format['width']
        height = self.image_format['height']

        img = Image.new("RGB", (width, height), "black")

        # RGB Icon
        icon.thumbnail((width, height), Image.LANCZOS)

        img.paste(icon, (0, 0), icon)

        # Load a custom TrueType font and use it to overlay the key index, draw key
        # number onto the image
        font = ImageFont.truetype("Assets/Roboto Mono for Powerline.ttf", 16)
        draw = ImageDraw.Draw(img)
        draw.text((30, height - 20), text=text, font=font, fill=(255, 0, 128, 255))

        # Get the raw r, g and b components of the generated image (note we need to
        # flip it horizontally to match the format the StreamDeck expects)
        r, g, b = img.transpose(Image.FLIP_LEFT_RIGHT).split()

        # Recombine the B, G and R elements in the order the display expects them,
        # and convert the resulting image to a sequence of bytes
        rgb = {"R": r, "G": g, "B": b}
        return Image.merge("RGB", (rgb[rgb_order[0]], rgb[rgb_order[1]], rgb[rgb_order[2]])).tobytes()
