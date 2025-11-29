"""Effects design tokens for Saisonxform UI.

Border radius and shadow definitions for elevation and depth.
"""


class BorderRadius:
    """Rounded corners scale."""

    none = "0"
    sm = "0.25rem"  # 4px  - Subtle
    md = "0.5rem"  # 8px  - Default
    lg = "0.75rem"  # 12px - Cards
    xl = "1rem"  # 16px - Modals
    xxl = "1.5rem"  # 24px - Hero sections
    full = "9999px"  # Pills/tags


class Shadows:
    """Box shadow scale for elevation."""

    none = "none"

    # Subtle elevation (1-2dp)
    sm = "0 1px 2px 0 rgba(0, 0, 0, 0.05)"

    # Default card shadow (4-6dp)
    md = "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)"

    # Elevated cards (8-12dp)
    lg = "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)"

    # Modal/popover (16-24dp)
    xl = "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)"

    # Maximum elevation (24dp+)
    xxl = "0 25px 50px -12px rgba(0, 0, 0, 0.25)"

    # Inset (form inputs)
    inner = "inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)"


class Transitions:
    """Transition timing and easing."""

    # Duration
    fast = "0.1s"  # Micro-interactions
    medium = "0.2s"  # Component state changes
    slow = "0.3s"  # Complex animations

    # Easing
    ease_out = "cubic-bezier(0.215, 0.61, 0.355, 1)"
    ease_in = "cubic-bezier(0.55, 0.055, 0.675, 0.19)"
    ease_in_out = "cubic-bezier(0.645, 0.045, 0.355, 1)"

    @classmethod
    def get_transition(cls, property: str = "all", duration: str = "medium") -> str:
        """Get CSS transition string.

        Args:
            property: CSS property to transition (default: 'all')
            duration: One of 'fast', 'medium', 'slow'

        Returns:
            CSS transition string
        """
        duration_value = getattr(cls, duration, cls.medium)
        return f"transition: {property} {duration_value} {cls.ease_out};"
