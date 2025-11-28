"""Global styles for Saisonxform web interface.

Generates CSS using design tokens for consistent styling across the application.
"""

import streamlit as st

from saisonxform.ui.tokens.colors import ColorTokens as c
from saisonxform.ui.tokens.effects import BorderRadius as r
from saisonxform.ui.tokens.effects import Shadows as sh
from saisonxform.ui.tokens.effects import Transitions as t
from saisonxform.ui.tokens.spacing import Spacing as s
from saisonxform.ui.tokens.typography import Typography as ty


def get_global_styles() -> str:
    """Generate global CSS using design tokens.

    Returns:
        CSS string with complete design system styles
    """
    return f"""
    <style>
    /* === BASE STYLES === */
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}

    body {{
        font-family: {ty.font_sans};
        color: {c.text_primary};
        line-height: {ty.body_line_height};
        background-color: {c.neutral_50};
    }}

    /* === TYPOGRAPHY === */
    .main-header {{
        font-size: {ty.h1_size};
        font-weight: {ty.h1_weight};
        line-height: {ty.h1_line_height};
        color: {c.primary_500};
        padding: {s.lg} 0;
        margin-bottom: {s.md};
    }}

    h1 {{
        font-size: {ty.h1_size};
        font-weight: {ty.h1_weight};
        line-height: {ty.h1_line_height};
        color: {c.text_primary};
        margin: {s.xl} 0 {s.lg} 0;
    }}

    h2 {{
        font-size: {ty.h2_size};
        font-weight: {ty.h2_weight};
        line-height: {ty.h2_line_height};
        color: {c.text_primary};
        margin: {s.lg} 0 {s.md} 0;
    }}

    h3 {{
        font-size: {ty.h3_size};
        font-weight: {ty.h3_weight};
        line-height: {ty.h3_line_height};
        color: {c.text_primary};
        margin: {s.md} 0 {s.sm} 0;
    }}

    h4 {{
        font-size: {ty.h4_size};
        font-weight: {ty.h4_weight};
        line-height: {ty.h4_line_height};
        color: {c.text_primary};
        margin: {s.sm} 0;
    }}

    p {{
        font-size: {ty.body_size};
        line-height: {ty.body_line_height};
        color: {c.text_primary};
        margin: {s.sm} 0;
    }}

    code {{
        font-family: {ty.font_mono};
        background-color: {c.neutral_100};
        padding: 0.125rem 0.25rem;
        border-radius: {r.sm};
        font-size: 0.9em;
    }}

    /* === CARDS === */
    .card {{
        background-color: {c.neutral_50};
        border: 1px solid {c.neutral_300};
        border-radius: {r.lg};
        padding: {s.card_padding};
        box-shadow: {sh.sm};
        margin: {s.md} 0;
        {t.get_transition('all', 'medium')}
    }}

    .card:hover {{
        box-shadow: {sh.md};
    }}

    .card-elevated {{
        box-shadow: {sh.md};
    }}

    .card-elevated:hover {{
        box-shadow: {sh.lg};
    }}

    /* === FILE UPLOAD ZONE === */
    .file-upload-section {{
        background-color: {c.primary_50};
        padding: {s.container_padding};
        border-radius: {r.xl};
        border: 2px dashed {c.primary_500};
        margin: {s.lg} 0;
        {t.get_transition('all', 'medium')}
    }}

    .file-upload-section:hover {{
        border-color: {c.primary_700};
        background-color: {c.primary_100};
        box-shadow: {sh.md};
        transform: translateY(-2px);
    }}

    /* === SEMANTIC BOXES === */
    .success-box {{
        background-color: {c.success_light};
        border: 2px solid {c.success_border};
        border-left: 4px solid {c.success};
        padding: {s.md};
        border-radius: {r.md};
        margin: {s.md} 0;
    }}

    .error-box {{
        background-color: {c.error_light};
        border: 2px solid {c.error_border};
        border-left: 4px solid {c.error};
        padding: {s.md};
        border-radius: {r.md};
        margin: {s.md} 0;
    }}

    .warning-box {{
        background-color: {c.warning_light};
        border: 2px solid {c.warning_border};
        border-left: 4px solid {c.warning};
        padding: {s.md};
        border-radius: {r.md};
        margin: {s.md} 0;
    }}

    .info-box {{
        background-color: {c.info_light};
        border: 2px solid {c.info_border};
        border-left: 4px solid {c.info};
        padding: {s.md};
        border-radius: {r.md};
        margin: {s.md} 0;
    }}

    .preview-box {{
        background-color: {c.warning_light};
        border: 2px solid {c.warning};
        padding: {s.lg};
        border-radius: {r.lg};
        margin: {s.md} 0;
        box-shadow: {sh.md};
    }}

    /* === BUTTONS === */
    .stButton > button {{
        border-radius: {r.md};
        padding: {s.button_padding_y} {s.button_padding_x};
        font-weight: {ty.button_weight};
        font-size: {ty.button_size};
        {t.get_transition('all', 'medium')}
        border: none;
    }}

    .stButton > button:hover {{
        box-shadow: {sh.md};
        transform: translateY(-1px);
    }}

    .stButton > button:active {{
        transform: translateY(0);
    }}

    .stButton > button[kind="primary"] {{
        background-color: {c.primary_500};
        color: {c.text_inverse};
    }}

    .stButton > button[kind="primary"]:hover {{
        background-color: {c.primary_600};
    }}

    .stButton > button[kind="secondary"] {{
        background-color: {c.neutral_100};
        color: {c.text_primary};
        border: 1px solid {c.neutral_300};
    }}

    .stButton > button[kind="secondary"]:hover {{
        background-color: {c.neutral_200};
    }}

    /* === DATA TABLES === */
    .dataframe {{
        border-radius: {r.md};
        overflow: hidden;
        box-shadow: {sh.sm};
        border: 1px solid {c.neutral_300};
    }}

    .dataframe thead tr {{
        background-color: {c.primary_50};
        color: {c.text_primary};
        font-weight: {ty.h6_weight};
    }}

    .dataframe tbody tr:hover {{
        background-color: {c.neutral_100};
    }}

    /* === METRICS === */
    div[data-testid="stMetric"] {{
        background-color: {c.neutral_50};
        border: 1px solid {c.neutral_300};
        border-radius: {r.md};
        padding: {s.md};
        box-shadow: {sh.sm};
    }}

    div[data-testid="stMetric"]:hover {{
        box-shadow: {sh.md};
    }}

    div[data-testid="stMetric"] label {{
        font-size: {ty.body_sm_size};
        color: {c.text_secondary};
    }}

    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
        font-size: {ty.h3_size};
        font-weight: {ty.h3_weight};
        color: {c.text_primary};
    }}

    /* === INPUTS === */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stMultiselect > div > div > div {{
        border-radius: {r.md};
        border: 1px solid {c.neutral_300};
        {t.get_transition('all', 'fast')}
    }}

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus,
    .stMultiselect > div > div > div:focus {{
        border-color: {c.primary_500};
        box-shadow: 0 0 0 1px {c.primary_500};
    }}

    /* === TABS === */
    .stTabs [data-baseweb="tab-list"] {{
        gap: {s.md};
        border-bottom: 2px solid {c.neutral_300};
    }}

    .stTabs [data-baseweb="tab"] {{
        border-radius: {r.md} {r.md} 0 0;
        padding: {s.sm} {s.lg};
        font-weight: {ty.h6_weight};
        color: {c.text_secondary};
        {t.get_transition('all', 'fast')}
    }}

    .stTabs [data-baseweb="tab"]:hover {{
        background-color: {c.neutral_100};
        color: {c.text_primary};
    }}

    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        background-color: {c.primary_50};
        color: {c.primary_700};
        border-bottom: 2px solid {c.primary_500};
    }}

    /* === SIDEBAR === */
    .css-1d391kg {{
        background-color: {c.neutral_50};
        border-right: 1px solid {c.neutral_300};
    }}

    /* === SCROLLBAR === */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}

    ::-webkit-scrollbar-track {{
        background: {c.neutral_100};
        border-radius: {r.sm};
    }}

    ::-webkit-scrollbar-thumb {{
        background: {c.neutral_400};
        border-radius: {r.sm};
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: {c.neutral_500};
    }}

    /* === UTILITY CLASSES === */
    .mt-xs {{ margin-top: {s.xs}; }}
    .mt-sm {{ margin-top: {s.sm}; }}
    .mt-md {{ margin-top: {s.md}; }}
    .mt-lg {{ margin-top: {s.lg}; }}
    .mt-xl {{ margin-top: {s.xl}; }}

    .mb-xs {{ margin-bottom: {s.xs}; }}
    .mb-sm {{ margin-bottom: {s.sm}; }}
    .mb-md {{ margin-bottom: {s.md}; }}
    .mb-lg {{ margin-bottom: {s.lg}; }}
    .mb-xl {{ margin-bottom: {s.xl}; }}

    .p-sm {{ padding: {s.sm}; }}
    .p-md {{ padding: {s.md}; }}
    .p-lg {{ padding: {s.lg}; }}

    .text-primary {{ color: {c.text_primary}; }}
    .text-secondary {{ color: {c.text_secondary}; }}
    .text-disabled {{ color: {c.text_disabled}; }}

    .bg-primary {{ background-color: {c.primary_500}; }}
    .bg-secondary {{ background-color: {c.secondary_500}; }}
    .bg-neutral {{ background-color: {c.neutral_100}; }}

    /* === ANIMATIONS === */
    @keyframes fade-in {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}

    @keyframes slide-up {{
        from {{
            transform: translateY(10px);
            opacity: 0;
        }}
        to {{
            transform: translateY(0);
            opacity: 1;
        }}
    }}

    @keyframes scale-in {{
        from {{
            transform: scale(0.95);
            opacity: 0;
        }}
        to {{
            transform: scale(1);
            opacity: 1;
        }}
    }}

    .animate-fade-in {{
        animation: fade-in 0.2s ease-out;
    }}

    .animate-slide-up {{
        animation: slide-up 0.3s ease-out;
    }}

    .animate-scale-in {{
        animation: scale-in 0.2s ease-out;
    }}
    </style>
    """


def apply_global_styles() -> None:
    """Apply global styles to the Streamlit app.

    Call this at the top of your main app file to apply design system styles.

    Example:
        from saisonxform.ui import apply_global_styles

        apply_global_styles()
        st.title("My App")
    """
    st.markdown(get_global_styles(), unsafe_allow_html=True)
