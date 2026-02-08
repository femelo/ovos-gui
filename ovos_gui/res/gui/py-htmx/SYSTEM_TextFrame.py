from __future__ import annotations
from typing import Any, Optional, Dict
from pyhtmx import Div, Button  # type: ignore
from pyhtmx_gui.kit import Widget, SessionItem, Control, Page


class SystemTextFrameWidget(Widget):
    _parameters = ("title", "text")

    def __init__(
        self: SystemTextFrameWidget,
        session_data: Optional[Dict[str, Any]] = None,
    ):
        session_data = session_data or {}
        super().__init__(
            name="system-text-frame-widget",
            session_data=session_data,
        )

        title_text = session_data.get("title", "")
        has_title = bool(title_text)

        self._title: Div = Div(
            inner_content=title_text,
            _id="title",
            _class="text-[2.5vw] font-bold text-[currentColor] opacity-90",
            style={"display": "block" if has_title else "none"},
        )
        self.add_interaction(
            "title",
            SessionItem(
                parameter="title",
                attribute="inner_content",
                component=self._title,
            ),
        )

        self._main_text: Div = Div(
            inner_content=session_data.get("text"),
            _id="text",
            _class="text-gray-900 text-[6vw] font-bold leading-tight text-center",
        )
        self.add_interaction(
            "text",
            SessionItem(
                parameter="text",
                attribute="inner_content",
                component=self._main_text,
            ),
        )

        self._button: Button = Button(
            "Close",
            _id="btn-close",
            _class="btn btn-outline btn-md text-white border-white hover:bg-white hover:text-blue-900 transition duration-300 mt-6",
        )
        self.add_interaction(
            "btn-close-click",
            Control(
                context="global",
                event="click",
                callback=lambda renderer, _: renderer.close(),
                source=self._button,
                target=None,
                target_level="innerHTML",
            ),
        )

        # Widget container met lichte achtergrond en afgeronde hoeken
        self._widget: Div = Div(
            [
                self._title,
                self._main_text,
                self._button,
            ],
            _id="system-text-frame-widget",
            _class=[
                "p-[2vw]",
                "flex",
                "flex-col",
                "items-center",
                "justify-center",
                "rounded-2xl",
                "shadow-xl",
                "bg-blue-100",  # lichte achtergrond, net als weather widget
            ],
            style={
                "width": "80vw",
                "height": "80vh",
            },
        )


class SystemTextFramePage(Page):

    def __init__(
        self: SystemTextFramePage,
        session_data: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(name="system-text-frame-page", session_data=session_data)

        widget = SystemTextFrameWidget(session_data=session_data)

        background_container = Div(
            [widget._widget],
            _id="system-text-frame-bg",
            _class=[
                "h-full",
                "w-full",
                "flex",
                "flex-col",
                "items-center",
                "justify-center",
            ],
            style={
                "background": "linear-gradient(to right, rgb(59, 130, 246), rgb(255, 182, 193))",
                "transition": "background 0.5s ease",
                "width": "100vw",
                "height": "100vh",
            },
        )

        self._page: Div = Div(
            [background_container],
            _id="system-text-frame-page",
            _class="flex flex-col",
            style={
                "width": "100vw",
                "height": "100vh",
            },
        )
