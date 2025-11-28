"""Typography design tokens for Saisonxform UI.

Font families, sizes, weights, and line heights for consistent typography.
"""


class Typography:
    """Typography scale following 8px baseline grid."""

    # Font Families
    font_sans = "'Inter', 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif"
    font_mono = "'Fira Code', 'Monaco', 'Consolas', monospace"

    # H1 - Main page title
    h1_size = "2.5rem"  # 40px
    h1_weight = "700"
    h1_line_height = "1.2"

    # H2 - Section headers
    h2_size = "2rem"  # 32px
    h2_weight = "600"
    h2_line_height = "1.3"

    # H3 - Subsection headers
    h3_size = "1.5rem"  # 24px
    h3_weight = "600"
    h3_line_height = "1.4"

    # H4 - Card headers
    h4_size = "1.25rem"  # 20px
    h4_weight = "600"
    h4_line_height = "1.5"

    # H5 - Small headers
    h5_size = "1.125rem"  # 18px
    h5_weight = "600"
    h5_line_height = "1.5"

    # H6 - Tiny headers
    h6_size = "1rem"  # 16px
    h6_weight = "600"
    h6_line_height = "1.5"

    # Body text
    body_size = "1rem"  # 16px (base)
    body_weight = "400"
    body_line_height = "1.6"

    # Body small
    body_sm_size = "0.875rem"  # 14px
    body_sm_weight = "400"
    body_sm_line_height = "1.5"

    # Caption/helper text
    caption_size = "0.75rem"  # 12px
    caption_weight = "400"
    caption_line_height = "1.4"

    # Button text
    button_size = "0.875rem"  # 14px
    button_weight = "600"
    button_line_height = "1"

    @classmethod
    def get_heading_style(cls, level: int) -> dict:
        """Get CSS style dictionary for heading level.

        Args:
            level: Heading level (1-6)

        Returns:
            Dictionary with size, weight, and line-height
        """
        styles = {
            1: {
                "size": cls.h1_size,
                "weight": cls.h1_weight,
                "line_height": cls.h1_line_height,
            },
            2: {
                "size": cls.h2_size,
                "weight": cls.h2_weight,
                "line_height": cls.h2_line_height,
            },
            3: {
                "size": cls.h3_size,
                "weight": cls.h3_weight,
                "line_height": cls.h3_line_height,
            },
            4: {
                "size": cls.h4_size,
                "weight": cls.h4_weight,
                "line_height": cls.h4_line_height,
            },
            5: {
                "size": cls.h5_size,
                "weight": cls.h5_weight,
                "line_height": cls.h5_line_height,
            },
            6: {
                "size": cls.h6_size,
                "weight": cls.h6_weight,
                "line_height": cls.h6_line_height,
            },
        }
        return styles.get(level, styles[6])
