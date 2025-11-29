"""Spacing design tokens for Saisonxform UI.

8px baseline spacing system for consistent layout and rhythm.
"""


class Spacing:
    """8px baseline spacing system."""

    # Base unit: 8px
    xs = "0.25rem"  # 4px  - Tight spacing
    sm = "0.5rem"  # 8px  - Small gaps
    md = "1rem"  # 16px - Default spacing
    lg = "1.5rem"  # 24px - Section spacing
    xl = "2rem"  # 32px - Large spacing
    xxl = "3rem"  # 48px - Major sections
    xxxl = "4rem"  # 64px - Page sections

    # Component-specific spacing
    button_padding_x = "1.5rem"  # 24px
    button_padding_y = "0.625rem"  # 10px

    card_padding = "1.5rem"  # 24px
    container_padding = "2rem"  # 32px

    input_padding_x = "0.75rem"  # 12px
    input_padding_y = "0.625rem"  # 10px

    @classmethod
    def get_margin(cls, size: str, direction: str = "all") -> str:
        """Get margin CSS for specified size and direction.

        Args:
            size: One of 'xs', 'sm', 'md', 'lg', 'xl', 'xxl', 'xxxl'
            direction: One of 'all', 'top', 'bottom', 'left', 'right', 'x', 'y'

        Returns:
            CSS margin string
        """
        value = getattr(cls, size, cls.md)

        if direction == "all":
            return f"margin: {value};"
        elif direction == "top":
            return f"margin-top: {value};"
        elif direction == "bottom":
            return f"margin-bottom: {value};"
        elif direction == "left":
            return f"margin-left: {value};"
        elif direction == "right":
            return f"margin-right: {value};"
        elif direction == "x":
            return f"margin-left: {value}; margin-right: {value};"
        elif direction == "y":
            return f"margin-top: {value}; margin-bottom: {value};"
        return f"margin: {value};"

    @classmethod
    def get_padding(cls, size: str, direction: str = "all") -> str:
        """Get padding CSS for specified size and direction.

        Args:
            size: One of 'xs', 'sm', 'md', 'lg', 'xl', 'xxl', 'xxxl'
            direction: One of 'all', 'top', 'bottom', 'left', 'right', 'x', 'y'

        Returns:
            CSS padding string
        """
        value = getattr(cls, size, cls.md)

        if direction == "all":
            return f"padding: {value};"
        elif direction == "top":
            return f"padding-top: {value};"
        elif direction == "bottom":
            return f"padding-bottom: {value};"
        elif direction == "left":
            return f"padding-left: {value};"
        elif direction == "right":
            return f"padding-right: {value};"
        elif direction == "x":
            return f"padding-left: {value}; padding-right: {value};"
        elif direction == "y":
            return f"padding-top: {value}; padding-bottom: {value};"
        return f"padding: {value};"
