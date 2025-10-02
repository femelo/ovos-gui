from __future__ import annotations
from typing import Any, Optional, Dict
from pyhtmx import Div, Button, Img  # type: ignore
from pyhtmx_gui.kit import Widget, SessionItem, Control, Page


SKILLS_DATA_PATH = "/skills"


class SystemImageFrameWidget(Widget):
    _parameters = ("title", "caption", "image_path", "fill", "background_color")

    def __init__(
        self: SystemImageFrameWidget,
        session_data: Optional[Dict[str, Any]] = None,
    ):
        session_data = session_data or {}
        super().__init__(
            name="system-text-frame-widget",
            session_data=session_data,
        )

        title_text = session_data.get("title", "")
        caption_text = session_data.get("caption", "")
        has_title = bool(title_text)
        has_caption = bool(caption_text)

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

        self._caption: Div = Div(
            inner_content=caption_text,
            _id="caption",
            _class="text-gray-900 text-[6vw] font-bold leading-tight text-center",
            style={"display": "block" if has_caption else "none"},
        )
        self.add_interaction(
            "caption",
            SessionItem(
                parameter="caption",
                attribute="inner_content",
                component=self._caption,
            ),
        )

        # Weather icon
        self._image: Img = Img(
            _id="image",
            src=f"{SKILLS_DATA_PATH}/{session_data.get('image_path', '')}",
            width="auto",
            height="auto",
            style={"filter": "drop-shadow(0.5vw 0.5vh 1vw #272727)"},
        )
        self.add_interaction(
            "image",
            SessionItem(
                parameter="image_path",
                attribute="src",
                component=self._image,
                format_value=lambda pth: f"{SKILLS_DATA_PATH}/{pth}",
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
                Div(
                    [self._image, self._caption],
                    _class="flex-1 flex items-center justify-center",
                ),
                self._button,
            ],
            _id="system-image-frame-widget",
            _class=[
                "p-[2vw]",
                "flex",
                "flex-col",
                "items-center",
                "justify-center",
                "rounded-2xl",
                "shadow-xl",
            ],
            style={
                "width": "80vw",
                "height": "80vh",
                "background-color": session_data.get("background_color", "rgba(255, 255, 255, 0.8)"),
            },
        )


class SystemImageFramePage(Page):

    def __init__(
        self: SystemImageFramePage,
        session_data: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(name="system-image-frame-page", session_data=session_data)

        widget = SystemImageFrameWidget(session_data=session_data)

        background_container = Div(
            [widget._widget],
            _id="system-image-frame-bg",
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
            _id="system-image-frame-page",
            _class="flex flex-col",
            style={
                "width": "100vw",
                "height": "100vh",
            },
        )
