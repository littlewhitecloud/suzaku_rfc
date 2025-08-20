import typing

"""
SWindow -> glfw -> generate_event 
产生对应事件
Widget -> generate_event -> register
注册对应组件的trigger
generate_event -> triggered -> call back registed function


SWindow的bind和glfw挂钩
所以只需要执行generate_event

"""


class SEventHandler:

    eventlist: dict[str, dict[str, typing.Callable]] = {}

    #              dict{eventname: {widgetid: callable}}
    def __init__(self) -> None: ...

    def generate_event(self, eventname: str, *args, **kwargs) -> None:
        """
        Generate event from SWindow which connects to glfw
        And also check the list of the event to call the registed functions


        :param eventname: name of the event
        :param _id: id of the widget
        """
        try:
            for event in self.eventlist[eventname].values():
                event(*args, **kwargs)
        except KeyError:
            self.register_event(eventname)

        del args, kwargs

    def register_event(self, eventname: str):
        """Register event from SWindow"""
        self.eventlist[eventname] = {}

    def bind_event(
        self, widgetid: int, eventname: str, function: typing.Callable
    ) -> "SEventHandler":
        """Bind event

        :param eventname: the name of the event
        :param function: the registed callable function
        """

        if eventname not in self.eventlist:
            self.register_event(eventname)

        self.eventlist[eventname][widgetid] = function
        return self

    def unbind_event(
        self, widgetid: int, eventname: str
    ) -> typing.Optional[typing.Callable]:
        """Unbind event

        :param eventname: the name of the event
        :return: might be registed callable function or if it failed, return None
        """

        if widgetid and eventname:
            return self.eventlist[eventname].pop(widgetid, None)


class SEvent:
    def __init__(
        self,
        **kwargs,
    ):
        __slots__ = []
        for k, v in kwargs.items():
            setattr(self, k, v)
            __slots__.append(k)

        # event_type: typing.Optional[str] = None,
        # x: typing.Optional[int] = None,
        # y: typing.Optional[int] = None,
        # rootx: typing.Optional[int] = None,
        # rooty: typing.Optional[int] = None,
        # key: typing.Optional[int] = None,
        # keyname: typing.Optional[str] = None,
        # mods: typing.Optional[str] = None,
        # char: typing.Optional[int] = None,
        # width: typing.Optional[int] = None,
        # height: typing.Optional[int] = None,
        # id: typing.Optional[str] = None,
