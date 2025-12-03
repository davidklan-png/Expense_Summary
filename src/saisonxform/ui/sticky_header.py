"""Sticky Header Component with Step Indicator.

Displays workflow progress and provides reset functionality.
"""

import streamlit as st

from .translations import get_text, load_translations
from .workflow_state import (
    WorkflowStep,
    can_access_step,
    get_current_step,
    get_step_status,
    is_step_complete,
    reset_workflow,
)


def render_sticky_header():
    """Render sticky header with step indicator and status using Streamlit components."""
    # Initialize translations and language
    load_translations()
    current_step = get_current_step()

    # Use Streamlit container instead of raw HTML
    header_container = st.container()

    with header_container:
        # Language toggle and title in top row
        top_col1, top_col2 = st.columns([8, 1])

        with top_col2:
            # Language toggle button in upper-right
            current_lang = st.session_state.lang
            current_lang_display = "🇯🇵 日本語" if current_lang == "en" else "🇺🇸 English"
            if st.button(current_lang_display, key="lang-toggle", use_container_width=True):
                st.session_state.lang = "ja" if current_lang == "en" else "en"
                st.rerun()

        # Title and step indicator in columns
        col1, col2, col3 = st.columns([2, 5, 1])

        with col1:
            st.markdown(f"### 💳 {get_text('global.app_title')}")
            st.caption(get_text('global.app_subtitle'))

        with col2:
            # Step indicator using columns
            step_cols = st.columns([1, 0.3, 1, 0.3, 1])

            steps = [
                {"step": WorkflowStep.UPLOAD, "number": "①", "label": get_text("steps.step_1")},
                {"step": WorkflowStep.PROCESS_EDIT, "number": "②", "label": get_text("steps.step_2")},
                {"step": WorkflowStep.DOWNLOAD, "number": "③", "label": get_text("steps.step_3")},
            ]

            for idx, step_info in enumerate(steps):
                col_idx = idx * 2
                step = step_info["step"]
                status = get_step_status(step)
                is_current = current_step == step

                with step_cols[col_idx]:
                    # Determine emoji based on actual step state (not translated text)
                    if is_step_complete(step):
                        emoji = "✅"
                        color = "green"
                    elif is_current:
                        emoji = step_info["number"]
                        color = "blue"
                    elif can_access_step(step):
                        emoji = step_info["number"]
                        color = "gray"
                    else:
                        emoji = "🔒"
                        color = "lightgray"

                    st.markdown(f"**{emoji} {step_info['label']}**")
                    st.caption(status)

                # Connector
                if idx < len(steps) - 1:
                    with step_cols[col_idx + 1]:
                        st.markdown("**→**")

        with col3:
            if st.button(f"🔄 {get_text('global.reset')}", key="reset-workflow-btn", use_container_width=True):
                reset_workflow()
                st.rerun()

    st.divider()
