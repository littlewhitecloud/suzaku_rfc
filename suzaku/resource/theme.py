import json
import pathlib
import typing

from .color import SColor


class SThemeError(Exception):
    def __init__(self, msg: typing.Any) -> None:
        self.msg = msg

    def __str__(self) -> typing.Any:
        return self.msg


class STheme:

    INTERNAL_THEMES = {}
    INTERNAL_THEMES_PATH = pathlib.Path(__file__).parent / "theme"

    def __init__(self, name: typing.Optional[str] = None):
        self.name = name

    def read_theme_from_json(self, file_path: str) -> "STheme":
        """Read theme file from json

        :param file_path: the theme file path
        """

        # open json file
        with open(file_path, "r") as f:
            raw_theme = json.load(f)

        # register theme name as key and theme style as values
        self.INTERNAL_THEMES[raw_theme.pop("name")] = raw_theme

        return self

    def parse_dict(self, _dict: dict):
        for key, value in _dict.items():
            # keep searching if get dict type
            if isinstance(value, dict):
                self.parse_dict(value)

            # convert rgba to skia Color
            if isinstance(value, list):
                _dict[key] = SColor(value).color

    def parse_style(self) -> "STheme":
        for _ in self.INTERNAL_THEMES[self.name].values():
            # if get dict then parse it
            if isinstance(_, dict):
                self.parse_dict(_)

        return self

    def get_style_attr(
        self, selector: str, prefix: typing.Optional[str] = None
    ) -> dict:
        """Get style attr

        :param selector: select the attr of the widget in the style
        :param prefix: to simplify the usage

        :return: dict
        """
        if prefix:
            selector = prefix + ":" + selector
        selectors = selector.split(":")

        result = self.INTERNAL_THEMES[self.name]
        try:
            # e.g. ['SButton', 'appearance', 'radius']
            # result = result["SButton"]["appearance"]["radius"]
            for _ in selectors:
                result = result[_]
        except KeyError:
            raise SThemeError(f"Check your selector spelling: '{_}'")

        return result

    def get_internal_theme(self, name: str) -> typing.Optional["STheme"]:
        try:
            self.name = name
            return self.read_theme_from_json(
                STheme.INTERNAL_THEMES_PATH / "dark.json"
            ).parse_style()
        except KeyError:
            raise SThemeError(
                f"Theme: '{theme_name}' not found, \
                check your spelling or load it from file"
            )


dark_theme = (
    STheme("dark")
    .read_theme_from_json(STheme.INTERNAL_THEMES_PATH / "dark.json")
    .parse_style()
)
light_theme = (
    STheme("light")
    .read_theme_from_json(STheme.INTERNAL_THEMES_PATH / "light.json")
    .parse_style()
)
