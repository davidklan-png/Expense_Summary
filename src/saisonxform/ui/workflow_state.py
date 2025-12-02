"""Workflow State Management for Streamlit App.

Manages the three-step workflow state using Streamlit session state.
"""

from enum import Enum
from typing import Optional

import streamlit as st


class WorkflowStep(Enum):
    """Workflow steps enumeration."""

    UPLOAD = 1
    PROCESS_EDIT = 2
    DOWNLOAD = 3


def initialize_workflow_state():
    """Initialize workflow state in session state."""
    if "workflow_step" not in st.session_state:
        st.session_state.workflow_step = WorkflowStep.UPLOAD

    if "step_completed" not in st.session_state:
        st.session_state.step_completed = {
            WorkflowStep.UPLOAD: False,
            WorkflowStep.PROCESS_EDIT: False,
            WorkflowStep.DOWNLOAD: False,
        }

    if "scroll_to_step" not in st.session_state:
        st.session_state.scroll_to_step = None


def get_current_step() -> WorkflowStep:
    """Get current workflow step."""
    return st.session_state.workflow_step


def set_current_step(step: WorkflowStep):
    """Set current workflow step."""
    st.session_state.workflow_step = step


def mark_step_complete(step: WorkflowStep):
    """Mark a step as completed."""
    st.session_state.step_completed[step] = True


def is_step_complete(step: WorkflowStep) -> bool:
    """Check if a step is completed."""
    return st.session_state.step_completed.get(step, False)


def advance_to_next_step():
    """Advance to the next workflow step."""
    current = st.session_state.workflow_step

    if current == WorkflowStep.UPLOAD:
        mark_step_complete(WorkflowStep.UPLOAD)
        set_current_step(WorkflowStep.PROCESS_EDIT)
        st.session_state.scroll_to_step = "step-2"
    elif current == WorkflowStep.PROCESS_EDIT:
        mark_step_complete(WorkflowStep.PROCESS_EDIT)
        set_current_step(WorkflowStep.DOWNLOAD)
        st.session_state.scroll_to_step = "step-3"


def reset_workflow():
    """Reset workflow to initial state and clear all caches."""
    st.session_state.workflow_step = WorkflowStep.UPLOAD
    st.session_state.step_completed = {
        WorkflowStep.UPLOAD: False,
        WorkflowStep.PROCESS_EDIT: False,
        WorkflowStep.DOWNLOAD: False,
    }
    st.session_state.scroll_to_step = "step-1"

    # Clear all file caches
    if "processed_files" in st.session_state:
        st.session_state.processed_files = {}
    if "uploaded_files_cache" in st.session_state:
        st.session_state.uploaded_files_cache = {}


def can_access_step(step: WorkflowStep) -> bool:
    """Check if a step can be accessed (previous step completed)."""
    if step == WorkflowStep.UPLOAD:
        return True
    elif step == WorkflowStep.PROCESS_EDIT:
        return is_step_complete(WorkflowStep.UPLOAD)
    elif step == WorkflowStep.DOWNLOAD:
        return is_step_complete(WorkflowStep.PROCESS_EDIT)
    return False


def get_step_status(step: WorkflowStep) -> str:
    """Get step status for display."""
    if is_step_complete(step):
        return "✅ Complete"
    elif st.session_state.workflow_step == step:
        return "⏳ In Progress"
    elif can_access_step(step):
        return "📝 Ready"
    else:
        return "🔒 Locked"
