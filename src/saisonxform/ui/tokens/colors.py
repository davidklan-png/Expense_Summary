"""Color design tokens for Saisonxform UI.

Complete color palette including primary, secondary, accent, neutral,
and semantic colors. All colors are WCAG AA compliant.
"""


class ColorTokens:
    """Design system color palette."""

    # Primary - Main brand color (blue)
    primary_50 = "#E3F2FD"
    primary_100 = "#BBDEFB"
    primary_200 = "#90CAF9"
    primary_300 = "#64B5F6"
    primary_400 = "#42A5F5"
    primary_500 = "#1f77b4"  # Main brand color
    primary_600 = "#1565C0"
    primary_700 = "#0D47A1"
    primary_800 = "#0A3D91"
    primary_900 = "#063060"

    # Secondary - Accent color (teal/green for success)
    secondary_50 = "#E0F2F1"
    secondary_100 = "#B2DFDB"
    secondary_200 = "#80CBC4"
    secondary_300 = "#4DB6AC"
    secondary_400 = "#26A69A"
    secondary_500 = "#009688"
    secondary_600 = "#00897B"
    secondary_700 = "#00695C"
    secondary_800 = "#00564A"
    secondary_900 = "#003D33"

    # Accent - Call-to-action (orange/amber)
    accent_50 = "#FFF8E1"
    accent_100 = "#FFECB3"
    accent_200 = "#FFE082"
    accent_300 = "#FFD54F"
    accent_400 = "#FFCA28"
    accent_500 = "#FFC107"
    accent_600 = "#FFB300"
    accent_700 = "#F57C00"
    accent_800 = "#EF6C00"
    accent_900 = "#E65100"

    # Neutral - Grays for text, borders, backgrounds
    neutral_50 = "#FAFAFA"
    neutral_100 = "#F5F5F5"
    neutral_200 = "#EEEEEE"
    neutral_300 = "#E0E0E0"
    neutral_400 = "#BDBDBD"
    neutral_500 = "#9E9E9E"
    neutral_600 = "#757575"
    neutral_700 = "#616161"
    neutral_800 = "#424242"
    neutral_900 = "#212121"

    # Semantic Colors - Success
    success_light = "#d4edda"
    success = "#28a745"
    success_dark = "#1e7e34"
    success_border = "#c3e6cb"

    # Semantic Colors - Error
    error_light = "#f8d7da"
    error = "#dc3545"
    error_dark = "#bd2130"
    error_border = "#f5c6cb"

    # Semantic Colors - Warning
    warning_light = "#fff3cd"
    warning = "#ffc107"
    warning_dark = "#e0a800"
    warning_border = "#ffc107"

    # Semantic Colors - Info
    info_light = "#d1ecf1"
    info = "#17a2b8"
    info_dark = "#117a8b"
    info_border = "#bee5eb"

    # Text Colors
    text_primary = "#212121"
    text_secondary = "#616161"
    text_disabled = "#9E9E9E"
    text_inverse = "#FFFFFF"

    @classmethod
    def get_semantic_colors(cls, variant: str) -> dict:
        """Get semantic color set for a variant.

        Args:
            variant: One of 'success', 'error', 'warning', 'info'

        Returns:
            Dictionary with light, main, dark, and border colors
        """
        variants = {
            "success": {
                "light": cls.success_light,
                "main": cls.success,
                "dark": cls.success_dark,
                "border": cls.success_border,
            },
            "error": {
                "light": cls.error_light,
                "main": cls.error,
                "dark": cls.error_dark,
                "border": cls.error_border,
            },
            "warning": {
                "light": cls.warning_light,
                "main": cls.warning,
                "dark": cls.warning_dark,
                "border": cls.warning_border,
            },
            "info": {
                "light": cls.info_light,
                "main": cls.info,
                "dark": cls.info_dark,
                "border": cls.info_border,
            },
        }
        return variants.get(variant, variants["info"])
