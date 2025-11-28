"""Component Showcase - Interactive demo of all UI components.

Run this file to see all available components and their variants in action.

Usage:
    streamlit run examples/component_showcase.py
"""

import sys
from pathlib import Path

import streamlit as st

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from saisonxform.ui import (
    Alert,
    Badge,
    Button,
    Card,
    Divider,
    FileUploadZone,
    Metric,
    SectionHeader,
    apply_global_styles,
)

# Apply global styles
apply_global_styles()

# Page configuration
st.set_page_config(
    page_title="Component Showcase",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Main header
st.markdown('<div class="main-header">🎨 Component Showcase</div>', unsafe_allow_html=True)
st.markdown("Interactive demonstration of all Saisonxform UI components")

# Sidebar navigation
with st.sidebar:
    SectionHeader.h3("Navigation", icon="🧭")
    component_section = st.radio(
        "Jump to section",
        [
            "Cards",
            "Alerts",
            "Badges",
            "Buttons",
            "Headers",
            "Metrics",
            "File Upload",
            "Dividers",
        ],
    )

# === CARDS SECTION ===
if component_section == "Cards":
    SectionHeader.h2("Cards", icon="🃏", subtitle="Container components for grouping content", divider=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Default Card")
        Card.default(
            content="This is a default card with neutral styling. Perfect for general content containers.",
            title="Default Card",
            icon="📄",
        )

        st.subheader("Success Card")
        Card.success(
            content="Operation completed successfully! The transaction has been processed.",
            title="Success",
        )

        st.subheader("Warning Card")
        Card.warning(
            content="Please review your settings before proceeding. Some configurations may need adjustment.",
            title="Warning",
        )

    with col2:
        st.subheader("Elevated Card")
        Card.default(
            content="This card has elevated shadow for more prominence. Use for featured content.",
            title="Elevated Card",
            icon="⬆️",
            elevated=True,
        )

        st.subheader("Error Card")
        Card.error(
            content="Failed to process request. Please check your input and try again.",
            title="Error",
        )

        st.subheader("Info Card")
        Card.info(
            content="Did you know? You can use keyboard shortcuts to speed up your workflow.",
            title="Pro Tip",
        )

# === ALERTS SECTION ===
elif component_section == "Alerts":
    SectionHeader.h2("Alerts", icon="🔔", subtitle="Inline notifications and messages", divider=True)

    st.subheader("Alert Variants")
    Alert.success("File uploaded successfully! Processing will begin shortly.")
    Alert.error("Connection failed. Please check your network settings.")
    Alert.warning("Your session will expire in 5 minutes. Save your work.")
    Alert.info("New update available. Click here to learn more.")

    st.subheader("Custom Icons")
    Alert.success("Payment received", icon="💰")
    Alert.warning("Low disk space", icon="💾")
    Alert.info("3 new messages", icon="📧")

# === BADGES SECTION ===
elif component_section == "Badges":
    SectionHeader.h2("Badges", icon="🏷️", subtitle="Labels and status indicators", divider=True)

    st.subheader("Badge Sizes")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Small**")
        Badge.primary("Small", size="sm")
    with col2:
        st.markdown("**Medium**")
        Badge.primary("Medium", size="md")
    with col3:
        st.markdown("**Large**")
        Badge.primary("Large", size="lg")

    Divider.render(spacing="lg")

    st.subheader("Badge Variants")
    st.markdown("**Default**")
    Badge.default("Default")
    Badge.default("Pending")
    Badge.default("Draft")

    st.markdown("**Primary**")
    Badge.primary("Primary")
    Badge.primary("Active")
    Badge.primary("New")

    st.markdown("**Success**")
    Badge.success("Success")
    Badge.success("Completed")
    Badge.success("Approved")

    st.markdown("**Error**")
    Badge.error("Error")
    Badge.error("Failed")
    Badge.error("Rejected")

    st.markdown("**Warning**")
    Badge.warning("Warning")
    Badge.warning("Pending Review")
    Badge.warning("Caution")

    st.markdown("**Info**")
    Badge.info("Info")
    Badge.info("Processing")
    Badge.info("Beta")

# === BUTTONS SECTION ===
elif component_section == "Buttons":
    SectionHeader.h2("Buttons", icon="🔘", subtitle="Interactive action triggers", divider=True)

    st.subheader("Button Variants")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Primary**")
        if Button.primary("Primary Button", key="btn_primary_1"):
            Alert.success("Primary button clicked!")

    with col2:
        st.markdown("**Secondary**")
        if Button.secondary("Secondary Button", key="btn_secondary_1"):
            Alert.info("Secondary button clicked!")

    with col3:
        st.markdown("**Danger**")
        if Button.danger("Danger Button", key="btn_danger_1"):
            Alert.error("Danger button clicked!")

    Divider.render(spacing="lg")

    st.subheader("Buttons with Icons")
    col1, col2, col3 = st.columns(3)

    with col1:
        Button.primary("Save", icon="💾", key="btn_save")

    with col2:
        Button.secondary("Cancel", icon="❌", key="btn_cancel")

    with col3:
        Button.danger("Delete", icon="🗑️", key="btn_delete")

    Divider.render(spacing="lg")

    st.subheader("Full Width Buttons")
    if Button.primary("Full Width Primary", icon="📊", key="btn_full_1", use_container_width=True):
        Alert.success("Full width button clicked!")

    if Button.secondary("Full Width Secondary", icon="⚙️", key="btn_full_2", use_container_width=True):
        Alert.info("Configuration opened")

# === HEADERS SECTION ===
elif component_section == "Headers":
    SectionHeader.h2("Section Headers", icon="📑", subtitle="Hierarchical content organization", divider=True)

    SectionHeader.h1("H1 Header", icon="🔷", subtitle="Main page title level")
    st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")

    SectionHeader.h2("H2 Header", icon="🔶", subtitle="Major section header")
    st.markdown("Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")

    SectionHeader.h3("H3 Header", icon="🟨", subtitle="Subsection header")
    st.markdown("Ut enim ad minim veniam, quis nostrud exercitation ullamco.")

    SectionHeader.h3("Header with Divider", icon="➖", divider=True)
    st.markdown("Headers can include automatic dividers for clear section separation.")

# === METRICS SECTION ===
elif component_section == "Metrics":
    SectionHeader.h2("Metrics", icon="📊", subtitle="Key performance indicators and statistics", divider=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        Metric.render(
            label="Total Users",
            value="1,234",
            delta="+12% vs last month",
            help_text="Active users this month",
        )

    with col2:
        Metric.render(
            label="Revenue",
            value="$45.2K",
            delta="+8.5%",
            help_text="Monthly recurring revenue",
        )

    with col3:
        Metric.render(
            label="Conversion Rate",
            value="3.24%",
            delta="+0.5%",
            help_text="Visitor to customer conversion",
        )

    with col4:
        Metric.render(
            label="Satisfaction",
            value="4.8/5.0",
            help_text="Average customer rating",
        )

# === FILE UPLOAD SECTION ===
elif component_section == "File Upload":
    SectionHeader.h2("File Upload Zone", icon="📁", subtitle="Drag-and-drop file upload interface", divider=True)

    st.subheader("Standard File Upload")
    uploaded_files = FileUploadZone.render(
        label="Drag and drop CSV files here",
        accept_multiple=True,
        accepted_types=["csv"],
        help_text="Supports multiple CSV files up to 200MB each",
        key="upload_standard",
    )

    if uploaded_files:
        Alert.success(f"Uploaded {len(uploaded_files)} file(s) successfully!")
        for file in uploaded_files:
            Badge.success(file.name, size="sm")

    Divider.render(spacing="lg")

    st.subheader("Image Upload")
    uploaded_images = FileUploadZone.render(
        label="Upload images",
        accept_multiple=True,
        accepted_types=["png", "jpg", "jpeg"],
        help_text="PNG, JPG, JPEG formats supported",
        key="upload_images",
    )

    if uploaded_images:
        Alert.info(f"{len(uploaded_images)} image(s) ready for processing")

# === DIVIDERS SECTION ===
elif component_section == "Dividers":
    SectionHeader.h2("Dividers", icon="➖", subtitle="Visual section separators", divider=True)

    st.subheader("Small Spacing")
    st.markdown("Content above")
    Divider.render(spacing="sm")
    st.markdown("Content below")

    st.subheader("Medium Spacing (Default)")
    st.markdown("Content above")
    Divider.render(spacing="md")
    st.markdown("Content below")

    st.subheader("Large Spacing")
    st.markdown("Content above")
    Divider.render(spacing="lg")
    st.markdown("Content below")

    st.subheader("Custom Color")
    st.markdown("Content above")
    Divider.render(spacing="md", color="#1f77b4", thickness="2px")
    st.markdown("Content below with custom blue divider")

# === COMBINED EXAMPLE ===
Divider.render(spacing="lg")
SectionHeader.h2("Combined Example", icon="🎭", subtitle="Real-world usage demonstration", divider=True)

col1, col2 = st.columns([2, 1])

with col1:
    Card.default(
        content="""
        <p>This example shows how multiple components work together to create a cohesive interface:</p>
        <ul>
            <li>Semantic cards for different states</li>
            <li>Alerts for user feedback</li>
            <li>Badges for status indicators</li>
            <li>Consistent spacing and typography</li>
        </ul>
        """,
        title="Dashboard Overview",
        icon="📊",
        elevated=True,
    )

    Alert.info("System update completed. All services are operational.")

with col2:
    st.markdown("**File Status**")
    Badge.success("Processed", size="sm")
    Badge.warning("Pending", size="sm")
    Badge.error("Failed", size="sm")

    Metric.render(
        label="Files Processed",
        value="847",
        delta="+23 today",
    )

# Footer
st.markdown("---")
st.caption("💡 Tip: Check the sidebar to navigate between component categories")
