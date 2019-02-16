from PIL import Image, ImageDraw, ImageFont
import fontawesome as fa


class IconHelper:
    @staticmethod
    def prepare_fontawesome_image(image_format, icon, text):
        rgb_order = image_format['order']
        width = image_format['width']
        height = image_format['height']

        img = Image.new("RGB", (width, height), "black")

        # Draw icon
        if icon:
            font = ImageFont.truetype("Assets/Font Awesome 5 Free-Solid-900.otf", 40)
            draw = ImageDraw.Draw(img)
            draw.text((15, 5), text=fa.icons[icon], font=font, fill=(255, 255, 255, 255))

        # Load a custom TrueType font and use it to overlay the key index, draw key
        # number onto the image
        font = ImageFont.truetype("Assets/Roboto Mono for Powerline.ttf", 16)
        draw = ImageDraw.Draw(img)
        draw.text((2, height - 20), text=text, font=font, fill=(255, 255, 255, 255))

        r, g, b = img.transpose(Image.FLIP_LEFT_RIGHT).split()

        # Recombine the B, G and R elements in the order the display expects them,
        # and convert the resulting image to a sequence of bytes
        rgb = {"R": r, "G": g, "B": b}
        return Image.merge("RGB", (rgb[rgb_order[0]], rgb[rgb_order[1]], rgb[rgb_order[2]])).tobytes()

    @staticmethod
    def prepare_image(image_format, icon, text):
        rgb_order = image_format['order']
        width = image_format['width']
        height = image_format['height']

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