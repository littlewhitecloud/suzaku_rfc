import os
from typing import Optional

import skia

os.environ["SKIA_FONT_CACHE_LIMIT_MB"] = "2"


class SFont:
    def __init__(self): ...

    def get_default_font(self):
        """Get default font with only english support"""
        return skia.Font(
            skia.FontMgr.RefDefault().legacyMakeTypeface("", skia.FontStyle()), size=14
        )

    def get_default_font_cs(self):
        """Get default font with chinese support"""
        # TODO: I don't really like to get the name of the font from tkinter
        import platform
        import tkinter as tk
        import tkinter.font as tkfont

        f = None

        root = tk.Tk()
        f = tkfont.nametofont("TkDefaultFont").actual().get("family")
        root.destroy()

        if f == ".AppleSystemUIFont":
            if int(platform.mac_ver()[0].split(".")[0]) >= 11:
                f = "SF Pro"
            elif platform.mac_ver()[0] == "10.15":
                f = "Helvetica Neue"
            else:
                f = "Lucida Grande"

        del root, tk, tkfont, platform

        return self.font(name=f)

    @staticmethod
    def get_font(
        name: Optional[str] = None, font_path: Optional[str] = None, size: int = 14
    ) -> Optional[skia.Font]:
        """
        Get font from path or local

        :param font_path: Path to a font file.
        :param name: Name of the local font.

        :param path: Path to a font file.

        :param size: SkFont size.
        :return: skia.Font object
        """
        if name:
            return skia.Font(skia.Typeface(name), size)
        if font_path:
            if not os.path.exists(font_path):
                raise FileNotFoundError
            return skia.Font(skia.Typeface.MakeFromFile(path=font_path), size)

        raise ValueError("Unexcepted name or font_path in default_font()")


default_font = SFont().get_default_font()
