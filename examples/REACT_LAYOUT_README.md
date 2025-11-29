# React Layout Component

A fully responsive React + Tailwind CSS layout component matching the Saisonxform design system.

## Features

- ✅ **Collapsible Sidebar** - Desktop sidebar with toggle, mobile overlay
- ✅ **Responsive Header** - Breadcrumb navigation and action buttons
- ✅ **Split-Pane Layout** - Query input on left, results on right
- ✅ **Status Footer** - Real-time connection status and statistics
- ✅ **Mobile-First** - Fully responsive from 320px to 4K
- ✅ **Design System Integration** - Uses Saisonxform Tailwind config
- ✅ **Icon System** - Lucide React icons
- ✅ **TypeScript** - Full type safety

## Quick Start

### 1. Install Dependencies

```bash
npm install react react-dom lucide-react
npm install -D @types/react @types/react-dom typescript
npm install -D tailwindcss postcss autoprefixer
```

### 2. Setup Tailwind CSS

Use the included [tailwind.config.js](../tailwind.config.js) from the Saisonxform design system.

```bash
# Initialize Tailwind (if not already done)
npx tailwindcss init -p

# Copy Saisonxform Tailwind config
cp tailwind.config.js my-app/tailwind.config.js
```

### 3. Import the Component

```tsx
import MainLayout from './components/MainLayout';

function App() {
  return <MainLayout />;
}

export default App;
```

## Component Structure

```
MainLayout
├── Sidebar (Collapsible)
│   ├── Header (Logo + Toggle)
│   ├── Navigation (Links)
│   └── Footer (User Profile)
├── Mobile Sidebar (Overlay)
├── Main Content
│   ├── Header (Breadcrumbs + Actions)
│   ├── Split Pane
│   │   ├── Query Input (Left)
│   │   │   ├── Search Bar
│   │   │   ├── Filters
│   │   │   └── Action Buttons
│   │   └── Results (Right)
│   │       ├── Results Header
│   │       └── Result Cards
│   └── Footer (Status Bar)
```

## Responsive Breakpoints

| Breakpoint | Width | Layout Changes |
|------------|-------|----------------|
| Mobile | < 768px | Sidebar hidden, burger menu, stacked panes |
| Tablet | 768px - 1024px | Sidebar visible, stacked panes |
| Desktop | > 1024px | Full layout, side-by-side panes |

## Customization

### Sidebar Items

Edit the `sidebarItems` array:

```tsx
const sidebarItems = [
  { icon: Home, label: 'Dashboard', href: '#', badge: null },
  { icon: FileText, label: 'Documents', href: '#', badge: '12' },
  // Add more items...
];
```

### Breadcrumbs

Edit the `breadcrumbs` array:

```tsx
const breadcrumbs: BreadcrumbItem[] = [
  { label: 'Home', href: '/' },
  { label: 'Dashboard', href: '/dashboard' },
  { label: 'Current Page', href: '/current' },
];
```

### Color Scheme

All colors are defined in the Tailwind config using design tokens:

```tsx
// Primary action button
className="bg-primary-500 hover:bg-primary-600"

// Success badge
className="bg-success-light text-success-dark"

// Neutral backgrounds
className="bg-neutral-50 border-neutral-300"
```

## Usage Examples

### Basic Implementation

```tsx
import MainLayout from './components/MainLayout';

function App() {
  return (
    <MainLayout>
      {/* Optional: Override default content */}
    </MainLayout>
  );
}
```

### With Routing (React Router)

```tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MainLayout from './components/MainLayout';

function App() {
  return (
    <BrowserRouter>
      <MainLayout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/documents" element={<Documents />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </MainLayout>
    </BrowserRouter>
  );
}
```

### With State Management

```tsx
import { useState } from 'react';
import MainLayout from './components/MainLayout';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [results, setResults] = useState([]);

  return (
    <MainLayout
      onSearch={(query) => {
        setSearchQuery(query);
        // Fetch results...
      }}
      results={results}
    />
  );
}
```

## Key Features Explained

### 1. Collapsible Sidebar

- **Desktop**: Toggles between 256px (w-64) and 80px (w-20)
- **Mobile**: Slides in as overlay
- **Animation**: Smooth 300ms transition

```tsx
const [sidebarOpen, setSidebarOpen] = useState(true);

<aside className={`${sidebarOpen ? 'w-64' : 'w-20'} transition-all duration-300`}>
```

### 2. Mobile Menu

- Triggered by hamburger icon on mobile
- Full-screen overlay with slide-in animation
- Close on backdrop click or X button

```tsx
const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

<div className="fixed inset-0 bg-black/50 z-40 md:hidden">
  <aside className="absolute left-0 w-64 bg-white">
```

### 3. Split Pane

- **Desktop (lg+)**: Side-by-side (50/50)
- **Mobile/Tablet**: Stacked vertically
- Independent scrolling for each pane

```tsx
<main className="flex-1 flex flex-col lg:flex-row">
  <div className="lg:w-1/2">Query Input</div>
  <div className="flex-1">Results</div>
</main>
```

### 4. Breadcrumb Navigation

- Shows current location hierarchy
- Hover states on clickable items
- Last item highlighted
- Chevron separators

```tsx
{breadcrumbs.map((item, index) => (
  <>
    <a href={item.href}>{item.label}</a>
    {index < breadcrumbs.length - 1 && <ChevronRight />}
  </>
))}
```

### 5. Status Footer

- Connection status indicator with pulse animation
- Last update timestamp
- File and record counts
- Responsive: Hides less important info on mobile

```tsx
<footer className="h-12 bg-white border-t flex items-center justify-between">
  <span className="flex items-center gap-2">
    <span className="w-2 h-2 bg-success rounded-full animate-pulse" />
    Connected
  </span>
</footer>
```

## Tailwind Classes Explained

### Layout Classes

```tsx
// Flex container filling screen height
"flex h-screen overflow-hidden"

// Sidebar with transition
"w-64 transition-all duration-300 flex-shrink-0"

// Main content area
"flex-1 flex flex-col overflow-hidden"
```

### Responsive Classes

```tsx
// Hidden on mobile, visible on desktop
"hidden md:flex"

// Column on mobile, row on desktop
"flex-col lg:flex-row"

// Different widths per breakpoint
"w-full lg:w-1/2"
```

### Interactive States

```tsx
// Hover effects
"hover:bg-primary-50 hover:text-primary-700"

// Focus states (accessibility)
"focus:outline-none focus:ring-2 focus:ring-primary-500"

// Active states
"transition-colors duration-200"
```

### Design System Colors

```tsx
// Primary colors
"bg-primary-500 text-primary-700"

// Semantic colors
"bg-success-light text-success-dark"

// Neutral grays
"bg-neutral-50 text-neutral-900 border-neutral-300"
```

## Accessibility

- ✅ **Keyboard Navigation** - Tab through all interactive elements
- ✅ **Focus Indicators** - Visible focus rings (ring-2)
- ✅ **ARIA Labels** - All buttons have aria-label
- ✅ **Semantic HTML** - Proper nav, aside, main, footer
- ✅ **Color Contrast** - WCAG AA compliant (4.5:1 minimum)

## Performance Optimizations

1. **React.memo** - Wrap components to prevent unnecessary re-renders
2. **useMemo** - Cache expensive computations
3. **Lazy Loading** - Code-split routes
4. **Virtual Scrolling** - For large result lists (use react-window)

```tsx
import { memo, useMemo } from 'react';

const ResultCard = memo(({ data }) => {
  return <div>{data.title}</div>;
});
```

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Dependencies

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "lucide-react": "^0.294.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "typescript": "^5.0.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0"
  }
}
```

## File Structure

```
src/
├── components/
│   └── MainLayout.tsx       # Main layout component
├── types/
│   └── index.ts             # TypeScript interfaces
├── App.tsx                  # App entry point
├── index.css                # Tailwind imports
└── main.tsx                 # React DOM render

config/
├── tailwind.config.js       # Tailwind configuration
├── postcss.config.js        # PostCSS configuration
└── tsconfig.json            # TypeScript configuration
```

## Integration with Existing Apps

### Next.js

```tsx
// pages/_app.tsx
import MainLayout from '../components/MainLayout';
import '../styles/globals.css';

function MyApp({ Component, pageProps }) {
  return (
    <MainLayout>
      <Component {...pageProps} />
    </MainLayout>
  );
}
```

### Vite

```tsx
// src/main.tsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import MainLayout from './components/MainLayout';
import './index.css';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <MainLayout />
  </StrictMode>
);
```

## Troubleshooting

### Tailwind Classes Not Working

1. Ensure `tailwind.config.js` includes component paths:
   ```js
   content: ['./src/**/*.{js,jsx,ts,tsx}']
   ```

2. Import Tailwind in your CSS:
   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```

### Icons Not Displaying

Install lucide-react:
```bash
npm install lucide-react
```

### TypeScript Errors

Ensure types are installed:
```bash
npm install -D @types/react @types/react-dom
```

## Related Files

- [Tailwind Config](../tailwind.config.js) - Design system configuration
- [Design System JSON](../design-system.json) - Complete token specification
- [Component Showcase](./component_showcase.py) - Streamlit components

## License

Part of the Saisonxform project.
