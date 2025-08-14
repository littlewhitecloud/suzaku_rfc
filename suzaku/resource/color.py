from typing import Optional

import skia


class SColor:

    colortype = str | tuple | list

    def __init__(self, color: Optional[str] = None) -> None:
        self.color = None
        self.set_color(color)

    def set_color(self, color: colortype) -> "SColor":
        """Set the color of the SColor

        :param color: the color
        :return: SColor
        """
        match color:
            case str():
                if color.startswith("#"):
                    self.set_color_hex(color)
                self.set_color_name(color)
            case tuple() | list():
                if flag := len(color) not in (3, 4):
                    raise ValueError(
                        "Color tuple/list must have 3 (RGB) or 4 (RGBA) elements"
                    )
                self.set_color_rgba(
                    color[0], color[1], color[2], color[3] if flag == 3 else 255
                )
            case _:
                ...

        return self

    def set_color_name(self, name: str) -> None:
        """Convert color name string to skia color

        :param name: the color name in skia
        :return: None
        :raise ValueError: color not exists
        """

        try:
            self.color = getattr(skia, f"Color{name.upper()}")
        except:
            raise ValueError(f"Color name not exists: {name}")

    def set_color_rgba(self, r: int, g: int, b: int, a: int = 255) -> None:
        """Convert RGB/RGBA to skia Color

        :param r: Red channel(0-255)
        :param g: Green channel(0-255)
        :param b: Blue channel(0-255)
        :param a: Alpha channel(0-255)

        :return: None
        :raise ValueError: RGB/RGBA format wrong
        """
        try:
            self.color = skia.Color(r, g, b, a)
        except:
            raise ValueError(f"RGB/RGBA for wrong: R:{r}, G:{g}, B:{b}, A:{a}")

    def set_color_hex(self, hex: str) -> None:
        """Convert HEX color string to skia Color

        :param hex: HEX color string
        :return: None
        :raise ValueError: HEX color string format wrong
        """
        hex_color = hex.lstrip("#")
        if len(hex_color) == 6:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            self.color = skia.ColorSetRGB(r, g, b)
        elif len(hex_color) == 8:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            a = int(hex_color[6:8], 16)
            self.color = skia.ColorSetARGB(a, r, g, b)
        else:
            raise ValueError("The HEX color format should be #RRGGBB or #RRGGBBAA")
