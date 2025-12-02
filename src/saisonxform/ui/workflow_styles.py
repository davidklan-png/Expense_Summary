"""Workflow-specific CSS styles for three-step vertical layout.

Adds sticky header, step indicators, smooth scrolling, and progressive disclosure styles.
"""


def get_workflow_styles() -> str:
    """Get CSS styles for the three-step workflow layout."""
    return """
    <style>
    /* ===== WORKFLOW-SPECIFIC STYLES ===== */
    html {
        scroll-behavior: smooth;
    }

    /* Hide Streamlit elements for cleaner workflow */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main container with padding for sticky header */
    .main .block-container {
        padding-top: 120px !important;
        padding-bottom: 48px;
        max-width: 1200px;
    }

    /* ===== STICKY HEADER ===== */
    .sticky-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-bottom: 2px solid #dee2e6;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        z-index: 999;
        padding: 16px 24px;
    }

    .sticky-header-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        max-width: 1200px;
        margin: 0 auto;
        gap: 32px;
    }

    .header-left {
        flex-shrink: 0;
    }

    .header-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin: 0;
        line-height: 1.2;
    }

    .header-subtitle {
        font-size: 0.875rem;
        color: #6c757d;
        margin: 4px 0 0 0;
    }

    /* ===== STEP INDICATOR ===== */
    .step-indicator {
        display: flex;
        align-items: center;
        gap: 24px;
        flex: 1;
        justify-content: center;
    }

    .step-indicator-item {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .step-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        border: 2px solid;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.125rem;
        transition: all 0.3s ease;
    }

    .step-indicator-item.active .step-circle {
        transform: scale(1.1);
        box-shadow: 0 4px 12px rgba(31, 119, 180, 0.3);
    }

    .step-label {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }

    .step-name {
        font-size: 0.875rem;
        font-weight: 600;
        line-height: 1;
    }

    .step-status {
        font-size: 0.75rem;
        color: #6c757d;
        line-height: 1;
    }

    .step-connector {
        width: 40px;
        height: 2px;
        background: #dee2e6;
    }

    /* ===== RESET BUTTON ===== */
    .reset-button {
        background: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 8px 24px;
        font-size: 0.875rem;
        font-weight: 600;
        color: #6c757d;
        cursor: pointer;
        transition: all 0.2s ease;
        white-space: nowrap;
    }

    .reset-button:hover {
        background: #f8f9fa;
        border-color: #1f77b4;
        color: #1f77b4;
    }

    /* ===== SECTION CONTAINERS ===== */
    .workflow-section {
        margin-bottom: 64px;
        scroll-margin-top: 140px;
    }

    .section-header {
        margin-bottom: 32px;
    }

    .section-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 48px;
        height: 48px;
        background: #1f77b4;
        color: white;
        border-radius: 50%;
        font-weight: 700;
        font-size: 1.5rem;
        margin-right: 16px;
        box-shadow: 0 4px 8px rgba(31, 119, 180, 0.2);
    }

    .section-title {
        font-size: 2rem;
        font-weight: 700;
        color: #212529;
        margin: 16px 0;
        display: flex;
        align-items: center;
    }

    .section-description {
        font-size: 1rem;
        color: #6c757d;
        margin: 8px 0 24px 64px;
        line-height: 1.6;
    }

    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, #dee2e6 0%, transparent 100%);
        margin: 48px 0;
    }

    /* ===== UPLOAD ZONE ===== */
    .upload-container {
        background: linear-gradient(135deg, #f0f7ff 0%, #e6f2ff 100%);
        border: 3px dashed #1f77b4;
        border-radius: 16px;
        padding: 48px;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .upload-container:hover {
        background: linear-gradient(135deg, #e6f2ff 0%, #d9ebff 100%);
        border-color: #0056b3;
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(31, 119, 180, 0.2);
    }

    .upload-icon {
        font-size: 4rem;
        margin-bottom: 16px;
        opacity: 0.8;
    }

    .upload-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #212529;
        margin-bottom: 8px;
    }

    .upload-subtitle {
        font-size: 0.875rem;
        color: #6c757d;
    }

    /* ===== PROGRESS SECTION ===== */
    .progress-container {
        background: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 12px;
        padding: 24px;
        margin: 24px 0;
    }

    .progress-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
    }

    .progress-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: #212529;
    }

    .progress-count {
        font-size: 0.875rem;
        color: #6c757d;
    }

    /* ===== LOCKED SECTION ===== */
    .section-locked {
        opacity: 0.4;
        pointer-events: none;
        user-select: none;
        position: relative;
        min-height: 200px;
    }

    .section-locked::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(2px);
        border-radius: 16px;
        z-index: 1;
    }

    .section-locked::after {
        content: "🔒 Complete previous step to unlock";
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: #ffffff;
        padding: 16px 32px;
        border-radius: 12px;
        font-weight: 600;
        color: #6c757d;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 2;
        white-space: nowrap;
    }

    /* ===== CTA BUTTONS ===== */
    .cta-container {
        display: flex;
        justify-content: center;
        margin: 32px 0;
    }

    .cta-button {
        font-size: 1.125rem !important;
        padding: 16px 48px !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(31, 119, 180, 0.3) !important;
    }

    .cta-button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(31, 119, 180, 0.4) !important;
    }

    /* ===== FILE LIST ===== */
    .file-list {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 16px;
        margin: 16px 0;
    }

    .file-item {
        display: flex;
        align-items: center;
        padding: 12px;
        background: #ffffff;
        border-radius: 8px;
        margin-bottom: 8px;
        border: 1px solid #dee2e6;
    }

    .file-icon {
        font-size: 1.5rem;
        margin-right: 12px;
    }

    .file-name {
        flex: 1;
        font-weight: 500;
        color: #212529;
    }

    .file-status {
        font-size: 0.875rem;
        color: #28a745;
        font-weight: 600;
    }

    /* ===== RESPONSIVE DESIGN ===== */
    @media (max-width: 768px) {
        .sticky-header-content {
            flex-direction: column;
            gap: 16px;
            padding: 12px;
        }

        .step-indicator {
            flex-direction: column;
            gap: 12px;
        }

        .step-connector {
            width: 2px;
            height: 20px;
        }

        .main .block-container {
            padding-top: 240px !important;
        }

        .section-title {
            font-size: 1.5rem;
        }

        .section-number {
            width: 40px;
            height: 40px;
            font-size: 1.25rem;
        }

        .section-description {
            margin-left: 56px;
        }

        .upload-container {
            padding: 32px 16px;
        }

        .section-locked::after {
            font-size: 0.875rem;
            padding: 12px 24px;
        }
    }

    /* ===== ANIMATIONS ===== */
    @keyframes fadeSlideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .animate-in {
        animation: fadeSlideIn 0.4s ease-out;
    }

    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.6;
        }
    }

    .pulse {
        animation: pulse 2s ease-in-out infinite;
    }
    </style>
    """


def get_auto_scroll_script(target_id: str) -> str:
    """Get JavaScript for auto-scrolling to a section.

    Args:
        target_id: The HTML element ID to scroll to

    Returns:
        HTML script tag with scroll functionality
    """
    return f"""
    <script>
        setTimeout(function() {{
            const element = document.getElementById('{target_id}');
            if (element) {{
                element.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }}
        }}, 100);
    </script>
    """
