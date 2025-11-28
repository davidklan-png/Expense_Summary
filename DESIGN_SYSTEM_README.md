# Saisonxform Design System

## Overview

This design system provides a comprehensive foundation for the Saisonxform web interface, ensuring consistency, accessibility, and maintainability across all UI components.

## Files

- **[design-system.json](design-system.json)** - Complete design token specification in JSON format
- **[tailwind.config.js](tailwind.config.js)** - Tailwind CSS configuration extending the design tokens

## Design Principles

1. **Consistency through tokens** - Single source of truth for all design decisions
2. **Accessible by default** - WCAG AA compliant color contrasts and focus states
3. **Progressive disclosure** - Clear information hierarchy and user flows
4. **Clear visual hierarchy** - Proper use of typography, spacing, and elevation
5. **Responsive and mobile-friendly** - Adapts to all screen sizes

## Color System

### Primary Colors
- **Primary** (#1f77b4) - Main brand color for headers, primary actions, and key UI elements
- **Secondary** (#009688) - Teal/green for success states and positive feedback
- **Accent** (#FFC107) - Orange/amber for call-to-action and emphasis

### Semantic Colors
- **Success** (#28a745) - Positive feedback, completed actions
- **Error** (#dc3545) - Error states, negative feedback
- **Warning** (#ffc107) - Caution, important notices
- **Info** (#17a2b8) - Informational messages, hints

### Neutral Grays
Complete gray scale from 50 (lightest) to 900 (darkest) for text, borders, and backgrounds.

### Usage Examples

```python
# In Streamlit (custom CSS)
background_color = ColorTokens.primary_50
border_color = ColorTokens.primary_500
text_color = ColorTokens.text_primary
```

```css
/* In Tailwind */
.card {
  @apply bg-neutral-50 border border-neutral-300 rounded-lg shadow-sm;
}

.btn-primary {
  @apply bg-primary-500 text-white hover:bg-primary-600 rounded-md shadow-sm;
}
```

## Typography Scale

### Font Families
- **Sans-serif**: Inter, Segoe UI, Roboto, Helvetica Neue
- **Monospace**: Fira Code, Monaco, Consolas

### Type Hierarchy

| Level | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| H1 | 40px (2.5rem) | 700 | 1.2 | Main page title |
| H2 | 32px (2rem) | 600 | 1.3 | Section headers |
| H3 | 24px (1.5rem) | 600 | 1.4 | Subsection headers |
| H4 | 20px (1.25rem) | 600 | 1.5 | Card headers |
| H5 | 18px (1.125rem) | 600 | 1.5 | Small headers |
| H6 | 16px (1rem) | 600 | 1.5 | Tiny headers |
| Body | 16px (1rem) | 400 | 1.6 | Default body text |
| Body Small | 14px (0.875rem) | 400 | 1.5 | Small body text |
| Caption | 12px (0.75rem) | 400 | 1.4 | Captions, helper text |
| Button | 14px (0.875rem) | 600 | 1 | Button text |

## Spacing System

Based on an **8px baseline grid** for consistent vertical rhythm and spacing.

### Scale

| Token | Value | Pixels | Usage |
|-------|-------|--------|-------|
| xs | 0.25rem | 4px | Tight spacing |
| sm | 0.5rem | 8px | Small gaps |
| md | 1rem | 16px | Default spacing |
| lg | 1.5rem | 24px | Section spacing |
| xl | 2rem | 32px | Large spacing |
| 2xl | 3rem | 48px | Major sections |
| 3xl | 4rem | 64px | Page sections |

### Component Spacing

- **Button padding**: 24px horizontal, 10px vertical
- **Card padding**: 24px
- **Container padding**: 32px
- **Input padding**: 12px horizontal, 10px vertical

## Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| sm | 4px | Subtle rounded corners |
| md | 8px | Default border radius |
| lg | 12px | Cards and containers |
| xl | 16px | Modals and large elements |
| 2xl | 24px | Hero sections |
| full | 9999px | Pills and circular elements |

## Shadows

| Token | Usage |
|-------|-------|
| sm | Subtle elevation (1-2dp) |
| md | Default card shadow (4-6dp) |
| lg | Elevated cards (8-12dp) |
| xl | Modals and popovers (16-24dp) |
| 2xl | Maximum elevation (24dp+) |
| inner | Inset shadow for inputs |

## Component Specifications

### Card Variants

#### Default Card
```css
background: neutral-50
border: 1px solid neutral-300
border-radius: lg (12px)
padding: 24px
shadow: sm
```

#### Success Card
```css
background: success-light (#d4edda)
border: 2px solid success-border
border-left: 4px solid success (#28a745)
border-radius: md
padding: 16px
```

#### Error Card
```css
background: error-light (#f8d7da)
border: 2px solid error-border
border-left: 4px solid error (#dc3545)
border-radius: md
padding: 16px
```

#### Warning Card
```css
background: warning-light (#fff3cd)
border: 2px solid warning-border
border-left: 4px solid warning (#ffc107)
border-radius: md
padding: 16px
```

#### Info Card
```css
background: info-light (#d1ecf1)
border: 2px solid info-border
border-left: 4px solid info (#17a2b8)
border-radius: md
padding: 16px
```

### Button Variants

#### Primary Button
```css
background: primary-500
color: white
hover: primary-600
border-radius: md
padding: 10px 24px
font-weight: 600
shadow: sm → md (on hover)
```

#### Secondary Button
```css
background: neutral-100
color: text-primary
hover: neutral-200
border: 1px solid neutral-300
border-radius: md
```

#### Danger Button
```css
background: error
color: white
hover: error-dark
border-radius: md
```

### File Upload Zone
```css
background: primary-50
border: 2px dashed primary-500
border-radius: xl (16px)
padding: 32px
hover:
  background: primary-100
  border-color: primary-700
  shadow: md
transition: all 0.2s ease
```

## Accessibility

### WCAG Compliance
- **Level**: AA
- **Normal text contrast**: 4.5:1 minimum
- **Large text contrast**: 3:1 minimum
- **UI components contrast**: 3:1 minimum

### Focus Indicators
- **Color**: primary-500
- **Width**: 2px
- **Style**: solid
- **Offset**: 2px

### Color Contrast Verified
All color combinations in semantic states (success, error, warning, info) meet WCAG AA standards for contrast ratios.

## Implementation

### For Streamlit Applications

```python
# Create design token files in src/saisonxform/ui/tokens/
from saisonxform.ui.tokens.colors import ColorTokens
from saisonxform.ui.tokens.typography import Typography
from saisonxform.ui.tokens.spacing import Spacing

# Use in custom CSS
st.markdown(f"""
<style>
.custom-card {{
    background-color: {ColorTokens.neutral_50};
    border: 1px solid {ColorTokens.neutral_300};
    border-radius: {BorderRadius.lg};
    padding: {Spacing.card};
    box-shadow: {Shadows.sm};
}}
</style>
""", unsafe_allow_html=True)
```

### For Tailwind CSS Projects

```bash
# Install Tailwind and dependencies
npm install -D tailwindcss @tailwindcss/forms @tailwindcss/typography

# Use the included tailwind.config.js
npx tailwindcss -i ./src/input.css -o ./dist/output.css --watch
```

```html
<!-- Use Tailwind classes -->
<div class="bg-neutral-50 border border-neutral-300 rounded-lg shadow-sm p-card">
  <h3 class="text-h3 text-text-primary mb-sm">Card Title</h3>
  <p class="text-body text-text-secondary">Card content goes here...</p>
</div>
```

## Responsive Breakpoints

| Breakpoint | Width | Usage |
|------------|-------|-------|
| mobile | 640px | Mobile devices |
| tablet | 768px | Tablets |
| desktop | 1024px | Desktop screens |
| wide | 1280px | Wide screens |
| ultrawide | 1536px | Ultra-wide screens |

## Animation Guidelines

### Available Animations
- **fade-in**: 0.2s ease-out - For appearing elements
- **slide-up**: 0.3s ease-out - For bottom-to-top reveals
- **slide-down**: 0.3s ease-out - For top-to-bottom reveals
- **scale-in**: 0.2s ease-out - For zoom-in effects

### Transition Timing
- **Fast**: 0.1-0.2s - Micro-interactions (hover, focus)
- **Medium**: 0.2-0.3s - Component state changes
- **Slow**: 0.3-0.5s - Complex animations, page transitions

## Design Token Updates

When updating the design system:

1. **Update design-system.json** first (source of truth)
2. **Regenerate Tailwind config** from JSON if needed
3. **Update Python token files** in `src/saisonxform/ui/tokens/`
4. **Test all components** to ensure no breaking changes
5. **Document changes** in version history

## Version History

### v1.0.0 (2025-11-27)
- Initial design system specification
- Complete color palette with semantic variants
- Typography scale with 8 levels
- 8px baseline spacing system
- Shadow and border radius scales
- Component specifications for cards, buttons, inputs
- Accessibility guidelines (WCAG AA)
- Tailwind CSS configuration

## References

- [Saisonxform Web Interface](web_app.py)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [shadcn/ui](https://ui.shadcn.com/) - Design philosophy inspiration

## Support

For questions or suggestions about the design system:
- Open an issue in the repository
- Review the [design-system.json](design-system.json) for complete specifications
- Check the Tailwind config for implementation examples
