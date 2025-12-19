"""Atomic UI components for Saisonxform web interface.

Reusable components implementing the design system. All components are
optimized for Streamlit and follow atomic design principles.
"""

from typing import Literal, Optional

import streamlit as st

from saisonxform.ui.tokens.colors import ColorTokens
from saisonxform.ui.tokens.effects import BorderRadius, Shadows, Transitions
from saisonxform.ui.tokens.spacing import Spacing
from saisonxform.ui.tokens.typography import Typography


class Card:
    """Card component with variants for different semantic meanings."""

    @staticmethod
    def render(
        content: str,
        variant: Literal["default", "success", "error", "warning", "info"] = "default",
        title: Optional[str] = None,
        icon: Optional[str] = None,
        elevated: bool = False,
    ) -> None:
        """Render a card component.

        Args:
            content: Card content (supports HTML)
            variant: Card style variant
            title: Optional title
            icon: Optional emoji icon
            elevated: Use elevated shadow
        """
        # Get variant colors
        if variant == "default":
            bg = ColorTokens.neutral_50
            border = ColorTokens.neutral_300
            border_left = ColorTokens.neutral_300
            icon_color = ColorTokens.primary_500
        else:
            colors = ColorTokens.get_semantic_colors(variant)
            bg = colors["light"]
            border = colors["border"]
            border_left = colors["main"]
            icon_color = colors["main"]

        shadow = Shadows.md if elevated else Shadows.sm

        card_html = f"""
        <div style="
            background-color: {bg};
            border: {'2px' if variant != 'default' else '1px'} solid {border};
            border-left: {'4px' if variant != 'default' else '1px'} solid {border_left};
            border-radius: {BorderRadius.lg};
            padding: {Spacing.card_padding};
            margin: {Spacing.md} 0;
            box-shadow: {shadow};
            {Transitions.get_transition('all', 'medium')}
        ">
            {f'''<div style="display: flex; align-items: center; gap: {Spacing.sm}; margin-bottom: {Spacing.sm};">
                {f'<span style="color: {icon_color}; font-size: {Typography.h4_size};">{icon}</span>' if icon else ''}
                <h4 style="margin: 0; color: {ColorTokens.text_primary}; font-size: {Typography.h4_size}; font-weight: {Typography.h4_weight};">{title}</h4>
            </div>''' if (icon or title) else ''}
            <div style="
                color: {ColorTokens.text_primary};
                font-size: {Typography.body_size};
                line-height: {Typography.body_line_height};
            ">
                {content}
            </div>
        </div>
        """

        st.markdown(card_html, unsafe_allow_html=True)

    @classmethod
    def default(
        cls,
        content: str,
        title: Optional[str] = None,
        icon: Optional[str] = None,
        elevated: bool = False,
    ) -> None:
        """Render default card."""
        cls.render(content, variant="default", title=title, icon=icon, elevated=elevated)

    @classmethod
    def success(cls, content: str, title: Optional[str] = None, icon: Optional[str] = "✅") -> None:
        """Render success card."""
        cls.render(content, variant="success", title=title, icon=icon)

    @classmethod
    def error(cls, content: str, title: Optional[str] = None, icon: Optional[str] = "❌") -> None:
        """Render error card."""
        cls.render(content, variant="error", title=title, icon=icon)

    @classmethod
    def warning(cls, content: str, title: Optional[str] = None, icon: Optional[str] = "⚠️") -> None:
        """Render warning card."""
        cls.render(content, variant="warning", title=title, icon=icon)

    @classmethod
    def info(cls, content: str, title: Optional[str] = None, icon: Optional[str] = "ℹ️") -> None:
        """Render info card."""
        cls.render(content, variant="info", title=title, icon=icon)


class Alert:
    """Alert component for inline notifications."""

    @staticmethod
    def render(
        message: str,
        variant: Literal["success", "error", "warning", "info"] = "info",
        icon: Optional[str] = None,
        dismissible: bool = False,
        key: Optional[str] = None,
    ) -> None:
        """Render an alert.

        Args:
            message: Alert message
            variant: Alert style variant
            icon: Optional custom icon
            dismissible: Show dismiss button
            key: Unique key for Streamlit
        """
        colors = ColorTokens.get_semantic_colors(variant)

        # Default icons
        default_icons = {
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️",
        }
        display_icon = icon or default_icons[variant]

        alert_html = f"""
        <div style="
            background-color: {colors['light']};
            border: 2px solid {colors['border']};
            border-left: 4px solid {colors['main']};
            border-radius: {BorderRadius.md};
            padding: {Spacing.md};
            margin: {Spacing.md} 0;
            display: flex;
            align-items: center;
            gap: {Spacing.sm};
        ">
            <span style="font-size: {Typography.h5_size}; color: {colors['main']};">{display_icon}</span>
            <div style="flex: 1; color: {ColorTokens.text_primary}; font-size: {Typography.body_size};">
                {message}
            </div>
        </div>
        """

        st.markdown(alert_html, unsafe_allow_html=True)

    @classmethod
    def success(cls, message: str, icon: Optional[str] = None) -> None:
        """Render success alert."""
        cls.render(message, variant="success", icon=icon)

    @classmethod
    def error(cls, message: str, icon: Optional[str] = None) -> None:
        """Render error alert."""
        cls.render(message, variant="error", icon=icon)

    @classmethod
    def warning(cls, message: str, icon: Optional[str] = None) -> None:
        """Render warning alert."""
        cls.render(message, variant="warning", icon=icon)

    @classmethod
    def info(cls, message: str, icon: Optional[str] = None) -> None:
        """Render info alert."""
        cls.render(message, variant="info", icon=icon)


class Badge:
    """Badge component for labels and status indicators."""

    @staticmethod
    def render(
        text: str,
        variant: Literal["default", "primary", "success", "error", "warning", "info"] = "default",
        size: Literal["sm", "md", "lg"] = "md",
    ) -> None:
        """Render a badge.

        Args:
            text: Badge text
            variant: Badge color variant
            size: Badge size
        """
        # Size mapping
        sizes = {
            "sm": {"font": Typography.caption_size, "padding": f"{Spacing.xs} {Spacing.sm}"},
            "md": {"font": Typography.body_sm_size, "padding": f"{Spacing.sm} {Spacing.md}"},
            "lg": {"font": Typography.body_size, "padding": f"{Spacing.sm} {Spacing.lg}"},
        }
        size_style = sizes[size]

        # Color mapping
        if variant == "default":
            bg = ColorTokens.neutral_200
            color = ColorTokens.text_primary
        elif variant == "primary":
            bg = ColorTokens.primary_500
            color = ColorTokens.text_inverse
        else:
            colors = ColorTokens.get_semantic_colors(variant)
            bg = colors["main"]
            color = ColorTokens.text_inverse

        badge_html = f"""
        <span style="
            background-color: {bg};
            color: {color};
            font-size: {size_style['font']};
            font-weight: {Typography.button_weight};
            padding: {size_style['padding']};
            border-radius: {BorderRadius.full};
            display: inline-block;
            margin: 0 {Spacing.xs};
        ">
            {text}
        </span>
        """

        st.markdown(badge_html, unsafe_allow_html=True)

    @classmethod
    def default(cls, text: str, size: Literal["sm", "md", "lg"] = "md") -> None:
        """Render default badge."""
        cls.render(text, variant="default", size=size)

    @classmethod
    def primary(cls, text: str, size: Literal["sm", "md", "lg"] = "md") -> None:
        """Render primary badge."""
        cls.render(text, variant="primary", size=size)

    @classmethod
    def success(cls, text: str, size: Literal["sm", "md", "lg"] = "md") -> None:
        """Render success badge."""
        cls.render(text, variant="success", size=size)

    @classmethod
    def error(cls, text: str, size: Literal["sm", "md", "lg"] = "md") -> None:
        """Render error badge."""
        cls.render(text, variant="error", size=size)

    @classmethod
    def warning(cls, text: str, size: Literal["sm", "md", "lg"] = "md") -> None:
        """Render warning badge."""
        cls.render(text, variant="warning", size=size)

    @classmethod
    def info(cls, text: str, size: Literal["sm", "md", "lg"] = "md") -> None:
        """Render info badge."""
        cls.render(text, variant="info", size=size)


class Button:
    """Button component wrapper for consistent styling."""

    @staticmethod
    def render(
        label: str,
        variant: Literal["primary", "secondary", "danger", "ghost"] = "primary",
        icon: Optional[str] = None,
        key: Optional[str] = None,
        disabled: bool = False,
        use_container_width: bool = False,
    ) -> bool:
        """Render a styled button using Streamlit's native button.

        Args:
            label: Button text
            variant: Button style variant
            icon: Optional emoji icon
            key: Unique key for Streamlit
            disabled: Disable button
            use_container_width: Expand button to container width

        Returns:
            True if button was clicked
        """
        # Map variant to Streamlit type
        button_type = "primary" if variant == "primary" else "secondary"

        # Add icon to label if provided
        display_label = f"{icon} {label}" if icon else label

        return st.button(
            display_label,
            key=key,
            type=button_type,
            disabled=disabled,
            use_container_width=use_container_width,
        )

    @classmethod
    def primary(
        cls,
        label: str,
        icon: Optional[str] = None,
        key: Optional[str] = None,
        disabled: bool = False,
        use_container_width: bool = False,
    ) -> bool:
        """Render primary button."""
        return cls.render(
            label,
            variant="primary",
            icon=icon,
            key=key,
            disabled=disabled,
            use_container_width=use_container_width,
        )

    @classmethod
    def secondary(
        cls,
        label: str,
        icon: Optional[str] = None,
        key: Optional[str] = None,
        disabled: bool = False,
        use_container_width: bool = False,
    ) -> bool:
        """Render secondary button."""
        return cls.render(
            label,
            variant="secondary",
            icon=icon,
            key=key,
            disabled=disabled,
            use_container_width=use_container_width,
        )

    @classmethod
    def danger(
        cls,
        label: str,
        icon: Optional[str] = None,
        key: Optional[str] = None,
        disabled: bool = False,
        use_container_width: bool = False,
    ) -> bool:
        """Render danger button."""
        return cls.render(
            label,
            variant="danger",
            icon=icon,
            key=key,
            disabled=disabled,
            use_container_width=use_container_width,
        )


class Divider:
    """Divider component for section separation."""

    @staticmethod
    def render(
        spacing: Literal["sm", "md", "lg"] = "md",
        color: Optional[str] = None,
        thickness: str = "1px",
    ) -> None:
        """Render a horizontal divider.

        Args:
            spacing: Vertical spacing around divider
            color: Optional custom color (hex)
            thickness: Border thickness
        """
        spacing_map = {"sm": Spacing.sm, "md": Spacing.md, "lg": Spacing.lg}
        margin = spacing_map[spacing]
        border_color = color or ColorTokens.neutral_300

        divider_html = f"""
        <hr style="
            border: none;
            border-top: {thickness} solid {border_color};
            margin: {margin} 0;
        "/>
        """

        st.markdown(divider_html, unsafe_allow_html=True)


class SectionHeader:
    """Section header component with optional icon and subtitle."""

    @staticmethod
    def render(
        text: str,
        level: Literal[1, 2, 3, 4, 5, 6] = 2,
        icon: Optional[str] = None,
        subtitle: Optional[str] = None,
        divider: bool = False,
    ) -> None:
        """Render a section header.

        Args:
            text: Header text
            level: Heading level (1-6)
            icon: Optional emoji icon
            subtitle: Optional subtitle text
            divider: Show divider below header
        """
        heading_style = Typography.get_heading_style(level)
        spacing_top = Spacing.xl if level <= 2 else Spacing.lg
        spacing_bottom = Spacing.lg if level <= 2 else Spacing.md

        header_html = f"""
        <div style="margin-top: {spacing_top}; margin-bottom: {spacing_bottom};">
            <div style="display: flex; align-items: center; gap: {Spacing.sm};">
                {f'<span style="font-size: {heading_style["size"]};">{icon}</span>' if icon else ''}
                <h{level} style="
                    margin: 0;
                    font-size: {heading_style['size']};
                    font-weight: {heading_style['weight']};
                    line-height: {heading_style['line_height']};
                    color: {ColorTokens.text_primary};
                ">{text}</h{level}>
            </div>
            {f'<p style="margin: {Spacing.xs} 0 0 0; color: {ColorTokens.text_secondary}; font-size: {Typography.body_sm_size}; line-height: {Typography.body_sm_line_height};">{subtitle}</p>' if subtitle else ''}
        </div>
        """

        st.markdown(header_html, unsafe_allow_html=True)

        if divider:
            Divider.render(spacing="sm")

    @classmethod
    def h1(cls, text: str, icon: Optional[str] = None, subtitle: Optional[str] = None, divider: bool = False) -> None:
        """Render H1 header."""
        cls.render(text, level=1, icon=icon, subtitle=subtitle, divider=divider)

    @classmethod
    def h2(cls, text: str, icon: Optional[str] = None, subtitle: Optional[str] = None, divider: bool = False) -> None:
        """Render H2 header."""
        cls.render(text, level=2, icon=icon, subtitle=subtitle, divider=divider)

    @classmethod
    def h3(cls, text: str, icon: Optional[str] = None, subtitle: Optional[str] = None, divider: bool = False) -> None:
        """Render H3 header."""
        cls.render(text, level=3, icon=icon, subtitle=subtitle, divider=divider)


class Metric:
    """Metric display component."""

    @staticmethod
    def render(
        label: str,
        value: str,
        delta: Optional[str] = None,
        delta_color: Literal["normal", "inverse", "off"] = "normal",
        help_text: Optional[str] = None,
    ) -> None:
        """Render a metric card.

        Args:
            label: Metric label
            value: Metric value
            delta: Optional change indicator
            delta_color: Delta color scheme
            help_text: Optional help text
        """
        metric_html = f"""
        <div style="
            background-color: {ColorTokens.neutral_50};
            border: 1px solid {ColorTokens.neutral_300};
            border-radius: {BorderRadius.md};
            padding: {Spacing.md};
            box-shadow: {Shadows.sm};
        ">
            <div style="
                font-size: {Typography.body_sm_size};
                color: {ColorTokens.text_secondary};
                margin-bottom: {Spacing.xs};
            ">{label}</div>
            <div style="
                font-size: {Typography.h3_size};
                font-weight: {Typography.h3_weight};
                color: {ColorTokens.text_primary};
                line-height: {Typography.h3_line_height};
            ">{value}</div>
            {f'<div style="font-size: {Typography.body_sm_size}; color: {ColorTokens.success}; margin-top: {Spacing.xs};">{delta}</div>' if delta else ''}
            {f'<div style="font-size: {Typography.caption_size}; color: {ColorTokens.text_secondary}; margin-top: {Spacing.xs};">{help_text}</div>' if help_text else ''}
        </div>
        """

        st.markdown(metric_html, unsafe_allow_html=True)


class FileUploadZone:
    """File upload zone component with drag-and-drop styling."""

    @staticmethod
    def render(
        label: str = "Drag and drop files here",
        accept_multiple: bool = True,
        accepted_types: Optional[list] = None,
        help_text: Optional[str] = None,
        key: Optional[str] = None,
    ):
        """Render a styled file upload zone.

        Args:
            label: Upload zone label
            accept_multiple: Allow multiple files
            accepted_types: List of accepted file extensions
            help_text: Optional help text
            key: Unique key for Streamlit

        Returns:
            Uploaded file(s) or None
        """
        # Render styled container
        zone_html = f"""
        <div style="
            background-color: {ColorTokens.primary_50};
            border: 2px dashed {ColorTokens.primary_500};
            border-radius: {BorderRadius.xl};
            padding: {Spacing.container_padding};
            margin: {Spacing.md} 0;
            text-align: center;
            {Transitions.get_transition('all', 'medium')}
        ">
            <div style="
                font-size: {Typography.h4_size};
                color: {ColorTokens.primary_500};
                margin-bottom: {Spacing.sm};
            ">📁</div>
            <div style="
                font-size: {Typography.body_size};
                color: {ColorTokens.text_primary};
                font-weight: {Typography.h5_weight};
            ">{label}</div>
            {f'<div style="font-size: {Typography.body_sm_size}; color: {ColorTokens.text_secondary}; margin-top: {Spacing.xs};">{help_text}</div>' if help_text else ''}
        </div>
        """

        st.markdown(zone_html, unsafe_allow_html=True)

        # Render actual file uploader
        return st.file_uploader(
            "Upload files",
            accept_multiple_files=accept_multiple,
            type=accepted_types,
            key=key,
            label_visibility="collapsed",
        )
