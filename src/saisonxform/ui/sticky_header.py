"""Sticky Header Component with Step Indicator.

Displays workflow progress and provides reset functionality.
"""

import streamlit as st

from .workflow_state import WorkflowStep, get_current_step, get_step_status, reset_workflow


def render_sticky_header():
    """Render sticky header with step indicator and status using Streamlit components."""
    current_step = get_current_step()

    # Use Streamlit container instead of raw HTML
    header_container = st.container()

    with header_container:
        # Title and step indicator in columns
        col1, col2, col3 = st.columns([2, 5, 1])

        with col1:
            st.markdown("### 💳 Saison Transform")
            st.caption("Financial Transaction Processor")

        with col2:
            # Step indicator using columns
            step_cols = st.columns([1, 0.3, 1, 0.3, 1])

            steps = [
                {"step": WorkflowStep.UPLOAD, "number": "①", "label": "Upload"},
                {"step": WorkflowStep.PROCESS_EDIT, "number": "②", "label": "Review & Edit"},
                {"step": WorkflowStep.DOWNLOAD, "number": "③", "label": "Download"},
            ]

            for idx, step_info in enumerate(steps):
                col_idx = idx * 2
                step = step_info["step"]
                status = get_step_status(step)
                is_current = current_step == step

                with step_cols[col_idx]:
                    # Determine emoji based on status
                    if "Complete" in status:
                        emoji = "✅"
                        color = "green"
                    elif is_current:
                        emoji = step_info["number"]
                        color = "blue"
                    elif "Ready" in status:
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
            if st.button("🔄 Reset", key="reset-workflow-btn", use_container_width=True):
                reset_workflow()
                st.rerun()

    st.divider()
