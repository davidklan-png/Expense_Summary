## Saisonxform UI Components

A comprehensive atomic component library implementing the Saisonxform design system for Streamlit applications.

## Features

- 🎨 **Design Token Based** - All components use centralized design tokens for consistency
- ♿ **Accessible** - WCAG AA compliant colors and focus states
- 📦 **Atomic Design** - Reusable, composable components
- 🎯 **Type Safe** - Full type hints for better IDE support
- 🚀 **Production Ready** - Battle-tested in real applications
- 📱 **Responsive** - Adapts to all screen sizes

## Quick Start

### Installation

The component library is part of the saisonxform package:

```python
from saisonxform.ui import (
    Card, Alert, Badge, Button,
    SectionHeader, Metric, FileUploadZone,
    apply_global_styles
)

# Apply global styles first
apply_global_styles()
```

### Basic Usage

```python
import streamlit as st
from saisonxform.ui import Card, Alert, Button, apply_global_styles

apply_global_styles()

st.title("My App")

# Use components
Card.success(
    content="File processed successfully!",
    title="Success",
    icon="✅"
)

Alert.info("New update available")

if Button.primary("Save Changes", icon="💾"):
    Alert.success("Changes saved!")
```

## Component Reference

### Card

Container component for grouping related content.

**Variants:** `default`, `success`, `error`, `warning`, `info`

```python
# Default card
Card.default(
    content="This is a card",
    title="Card Title",
    icon="📄",
    elevated=False  # Use elevated shadow
)

# Semantic cards
Card.success("Operation completed!", title="Success")
Card.error("Something went wrong", title="Error")
Card.warning("Please review settings", title="Warning")
Card.info("Did you know...", title="Pro Tip")
```

**Props:**
- `content` (str): Card content (supports HTML)
- `variant` (str): Style variant
- `title` (str, optional): Card title
- `icon` (str, optional): Emoji icon
- `elevated` (bool): Use elevated shadow

### Alert

Inline notification component for user feedback.

**Variants:** `success`, `error`, `warning`, `info`

```python
Alert.success("File uploaded successfully!")
Alert.error("Connection failed")
Alert.warning("Session expiring soon")
Alert.info("3 new messages")

# Custom icon
Alert.success("Payment received", icon="💰")
```

**Props:**
- `message` (str): Alert message
- `variant` (str): Style variant
- `icon` (str, optional): Custom emoji icon
- `dismissible` (bool): Show dismiss button (future)
- `key` (str, optional): Streamlit key

### Badge

Label and status indicator component.

**Variants:** `default`, `primary`, `success`, `error`, `warning`, `info`
**Sizes:** `sm`, `md`, `lg`

```python
Badge.primary("New", size="sm")
Badge.success("Completed", size="md")
Badge.error("Failed", size="lg")
Badge.warning("Pending")
Badge.info("Beta")
```

**Props:**
- `text` (str): Badge text
- `variant` (str): Color variant
- `size` (str): Badge size

### Button

Interactive action trigger (wrapper around Streamlit button).

**Variants:** `primary`, `secondary`, `danger`, `ghost`

```python
if Button.primary("Save", icon="💾", key="btn_save"):
    # Handle click
    pass

if Button.secondary("Cancel", key="btn_cancel"):
    pass

if Button.danger("Delete", icon="🗑️", key="btn_delete"):
    pass

# Full width
Button.primary("Submit", use_container_width=True)
```

**Props:**
- `label` (str): Button text
- `variant` (str): Style variant
- `icon` (str, optional): Emoji icon
- `key` (str, optional): Streamlit key
- `disabled` (bool): Disable button
- `use_container_width` (bool): Expand to container width

**Returns:** `bool` - True if button was clicked

### SectionHeader

Header component with optional icon and subtitle.

**Levels:** `1`, `2`, `3`, `4`, `5`, `6`

```python
SectionHeader.h1("Main Title", icon="🎯", subtitle="Optional subtitle")
SectionHeader.h2("Section", icon="📊", divider=True)
SectionHeader.h3("Subsection", subtitle="Description")

# Or use render with level
SectionHeader.render(
    text="Custom Header",
    level=2,
    icon="🔷",
    subtitle="Supporting text",
    divider=False
)
```

**Props:**
- `text` (str): Header text
- `level` (int): Heading level (1-6)
- `icon` (str, optional): Emoji icon
- `subtitle` (str, optional): Subtitle text
- `divider` (bool): Show divider below

### Metric

Key performance indicator display.

```python
Metric.render(
    label="Total Users",
    value="1,234",
    delta="+12% vs last month",
    delta_color="normal",  # normal, inverse, off
    help_text="Active users this month"
)
```

**Props:**
- `label` (str): Metric label
- `value` (str): Metric value
- `delta` (str, optional): Change indicator
- `delta_color` (str): Delta color scheme
- `help_text` (str, optional): Help text

### FileUploadZone

Styled file upload component with drag-and-drop.

```python
uploaded_files = FileUploadZone.render(
    label="Drag and drop CSV files here",
    accept_multiple=True,
    accepted_types=["csv"],
    help_text="Supports multiple files",
    key="upload_csv"
)

if uploaded_files:
    for file in uploaded_files:
        st.write(file.name)
```

**Props:**
- `label` (str): Upload zone label
- `accept_multiple` (bool): Allow multiple files
- `accepted_types` (list, optional): Accepted file extensions
- `help_text` (str, optional): Help text
- `key` (str, optional): Streamlit key

**Returns:** Uploaded file(s) or None

### Divider

Horizontal divider for section separation.

```python
Divider.render(spacing="md")  # sm, md, lg
Divider.render(spacing="lg", color="#1f77b4", thickness="2px")
```

**Props:**
- `spacing` (str): Vertical spacing (sm, md, lg)
- `color` (str, optional): Custom color (hex)
- `thickness` (str): Border thickness

## Design Tokens

All components use centralized design tokens for consistency.

### Colors

```python
from saisonxform.ui.tokens import ColorTokens

# Primary colors
ColorTokens.primary_500    # Main brand color
ColorTokens.secondary_500  # Accent color
ColorTokens.accent_500     # CTA color

# Semantic colors
ColorTokens.success        # Success state
ColorTokens.error          # Error state
ColorTokens.warning        # Warning state
ColorTokens.info           # Info state

# Neutral grays
ColorTokens.neutral_50     # Lightest
ColorTokens.neutral_900    # Darkest

# Text colors
ColorTokens.text_primary
ColorTokens.text_secondary
ColorTokens.text_disabled
```

### Typography

```python
from saisonxform.ui.tokens import Typography

# Font families
Typography.font_sans  # Sans-serif stack
Typography.font_mono  # Monospace stack

# Sizes
Typography.h1_size   # 2.5rem (40px)
Typography.h2_size   # 2rem (32px)
Typography.body_size # 1rem (16px)
# ... and more
```

### Spacing

```python
from saisonxform.ui.tokens import Spacing

# 8px baseline grid
Spacing.xs    # 4px
Spacing.sm    # 8px
Spacing.md    # 16px
Spacing.lg    # 24px
Spacing.xl    # 32px
Spacing.xxl   # 48px
Spacing.xxxl  # 64px

# Component-specific
Spacing.card_padding       # 24px
Spacing.button_padding_x   # 24px
Spacing.button_padding_y   # 10px
```

### Effects

```python
from saisonxform.ui.tokens import BorderRadius, Shadows

# Border radius
BorderRadius.sm    # 4px
BorderRadius.md    # 8px
BorderRadius.lg    # 12px
BorderRadius.xl    # 16px
BorderRadius.full  # 9999px (pills)

# Shadows
Shadows.sm   # Subtle elevation
Shadows.md   # Default card shadow
Shadows.lg   # Elevated cards
Shadows.xl   # Modals
Shadows.xxl  # Maximum elevation
```

## Global Styles

Apply global styles to your Streamlit app:

```python
from saisonxform.ui import apply_global_styles

# At the top of your app
apply_global_styles()
```

This applies:
- Typography styles
- Button enhancements
- Table styling
- Input field styling
- Tab styling
- Scrollbar styling
- Utility classes
- Animations

## Examples

### Complete Page Example

```python
import streamlit as st
from saisonxform.ui import (
    Card, Alert, Badge, Button, SectionHeader,
    Metric, FileUploadZone, apply_global_styles
)

apply_global_styles()

st.set_page_config(page_title="Dashboard", layout="wide")

# Header
SectionHeader.h1("Dashboard", icon="📊", subtitle="Overview of your data")

# Metrics row
col1, col2, col3, col4 = st.columns(4)
with col1:
    Metric.render("Total Users", "1,234", "+12%")
with col2:
    Metric.render("Revenue", "$45.2K", "+8.5%")
with col3:
    Metric.render("Conversion", "3.24%", "+0.5%")
with col4:
    Metric.render("Satisfaction", "4.8/5.0")

# File upload section
SectionHeader.h2("Upload Data", icon="📁", divider=True)
uploaded = FileUploadZone.render(
    label="Drag and drop CSV files",
    accepted_types=["csv"],
    key="upload_main"
)

if uploaded:
    Alert.success(f"Uploaded {len(uploaded)} file(s)")

# Status cards
SectionHeader.h2("Recent Activity", icon="📝", divider=True)
col1, col2 = st.columns(2)

with col1:
    Card.success(
        content="All systems operational",
        title="System Status",
        icon="✅"
    )

with col2:
    Card.warning(
        content="3 files pending review",
        title="Pending Actions",
        icon="⚠️"
    )

# Action buttons
if Button.primary("Process Files", icon="🚀", key="process"):
    Alert.info("Processing started...")
```

### Form Example

```python
SectionHeader.h2("User Settings", icon="⚙️", divider=True)

with st.form("settings_form"):
    st.text_input("Name")
    st.text_input("Email")
    st.selectbox("Role", ["Admin", "User", "Guest"])

    col1, col2 = st.columns(2)
    with col1:
        submit = st.form_submit_button("Save Changes", type="primary")
    with col2:
        cancel = st.form_submit_button("Cancel")

    if submit:
        Alert.success("Settings saved successfully!")
    if cancel:
        Alert.info("Changes discarded")
```

## Component Showcase

Run the interactive component showcase:

```bash
streamlit run examples/component_showcase.py
```

This demonstrates all components with all their variants and usage examples.

## Best Practices

1. **Always apply global styles first**
   ```python
   apply_global_styles()  # At top of your app
   ```

2. **Use semantic variants**
   ```python
   # Good - clear intent
   Card.success("Operation completed")
   Alert.error("Failed to save")

   # Avoid - unclear purpose
   Card.render(..., variant="success")
   ```

3. **Provide clear labels**
   ```python
   # Good
   Button.primary("Save Changes", icon="💾")

   # Avoid
   Button.primary("OK")
   ```

4. **Use consistent spacing**
   ```python
   SectionHeader.h2("Section", divider=True)
   # Content...
   Divider.render(spacing="lg")
   SectionHeader.h2("Next Section", divider=True)
   ```

5. **Provide feedback for actions**
   ```python
   if Button.primary("Delete", icon="🗑️"):
       # Show feedback
       Alert.success("Item deleted")
       # Or error
       Alert.error("Failed to delete item")
   ```

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Accessibility

All components follow WCAG AA guidelines:
- Color contrast ratios meet minimum requirements
- Semantic HTML structure
- Keyboard navigation support (via Streamlit)
- Focus indicators on interactive elements

## Related Documentation

- [Design System JSON](../../../design-system.json)
- [Tailwind Config](../../../tailwind.config.js)
- [Design System README](../../../DESIGN_SYSTEM_README.md)
- [Component Showcase](../../../examples/component_showcase.py)

## Support

For issues or questions:
- Check the component showcase for usage examples
- Review the design system documentation
- Open an issue in the repository
