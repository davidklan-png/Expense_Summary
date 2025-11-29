# Empty State Components

Professional empty state components for tax document management system with Japanese language support.

## Features

- ✅ **7 Variants** - No documents, no results, error, loading, success, filtered, offline
- ✅ **Preset Components** - Ready-to-use components for common scenarios
- ✅ **3 Sizes** - Small, medium, large
- ✅ **Drag & Drop** - Interactive file upload empty state
- ✅ **Help Cards** - Educational content with icons
- ✅ **Getting Started** - Onboarding flow with steps
- ✅ **Japanese Support** - All text in Japanese (日本語対応)
- ✅ **Accessible** - WCAG AA compliant
- ✅ **Responsive** - Mobile-first design
- ✅ **Customizable** - Override all content and styling

## Quick Start

```tsx
import { NoDocumentsEmptyState } from './EmptyState';

function DocumentList() {
  const hasDocuments = documents.length > 0;

  if (!hasDocuments) {
    return (
      <NoDocumentsEmptyState
        onUpload={() => openFileUploader()}
        onViewSamples={() => showSampleDocuments()}
      />
    );
  }

  return <DocumentGrid documents={documents} />;
}
```

## Variants

### 1. No Documents

When no tax documents have been uploaded.

```tsx
<EmptyState
  variant="no-documents"
  actions={[
    {
      label: '書類をアップロード',
      onClick: handleUpload,
      variant: 'primary',
      icon: <Upload className="w-5 h-5" />,
    },
  ]}
/>
```

**Use When:**
- Initial state (no documents loaded)
- User deleted all documents
- Fresh session

### 2. No Results

When search or filter returns empty results.

```tsx
<EmptyState
  variant="no-results"
  title="「会議費」の検索結果が見つかりませんでした"
  actions={[
    {
      label: '検索をクリア',
      onClick: handleClearSearch,
    },
  ]}
/>
```

**Use When:**
- Search query returns no matches
- Filter combination too restrictive
- Misspelled search term

### 3. Error

When data loading or processing fails.

```tsx
<EmptyState
  variant="error"
  description="サーバーに接続できませんでした"
  actions={[
    {
      label: '再試行',
      onClick: handleRetry,
      icon: <RefreshCw className="w-5 h-5" />,
    },
  ]}
/>
```

**Use When:**
- Network error
- Server error (500, 502, etc.)
- File upload failed
- API timeout

### 4. Loading

When fetching data.

```tsx
<EmptyState variant="loading" size="md" />
```

**Use When:**
- Initial data fetch
- Refreshing data
- Loading more items
- Processing documents

### 5. Success

After successful operation.

```tsx
<EmptyState
  variant="success"
  title="アップロード完了"
  description="3件の書類が正常に処理されました"
  actions={[
    {
      label: '結果を見る',
      onClick: handleViewResults,
    },
  ]}
/>
```

**Use When:**
- Upload completed
- Processing finished
- Batch operation succeeded

### 6. Filtered

When active filters return no results.

```tsx
<EmptyState
  variant="filtered"
  actions={[
    {
      label: 'フィルターをリセット',
      onClick: handleResetFilters,
      icon: <Filter className="w-5 h-5" />,
    },
  ]}
/>
```

**Use When:**
- Multiple active filters
- Date range too narrow
- Category filter excludes all
- Tag combination too specific

### 7. Offline

When network connection lost.

```tsx
<EmptyState
  variant="offline"
  description="オフラインモードです。接続を確認してください。"
/>
```

**Use When:**
- Network disconnected
- PWA offline mode
- Connection timeout

## Preset Components

### NoDocumentsEmptyState

```tsx
<NoDocumentsEmptyState
  onUpload={() => openFileDialog()}
  onViewSamples={() => showSamples()}
/>
```

**Props:**
- `onUpload: () => void` - Upload button handler
- `onViewSamples?: () => void` - View samples button (optional)

### NoSearchResultsEmptyState

```tsx
<NoSearchResultsEmptyState
  searchTerm="会議費 2024"
  onClearSearch={() => clearSearch()}
  onResetFilters={() => resetAllFilters()}
/>
```

**Props:**
- `searchTerm?: string` - Current search query
- `onClearSearch: () => void` - Clear search handler
- `onResetFilters?: () => void` - Reset filters handler (optional)

### ErrorEmptyState

```tsx
<ErrorEmptyState
  onRetry={() => refetch()}
  errorMessage="ファイルが大きすぎます（最大10MB）"
/>
```

**Props:**
- `onRetry: () => void` - Retry button handler
- `errorMessage?: string` - Custom error message

### FilteredEmptyState

```tsx
<FilteredEmptyState
  onResetFilters={() => clearFilters()}
  activeFilterCount={3}
/>
```

**Props:**
- `onResetFilters: () => void` - Reset filters handler
- `activeFilterCount?: number` - Number of active filters

## Sizes

### Small (sm)

```tsx
<EmptyState variant="no-documents" size="sm" />
```

**Use In:**
- Sidebar panels
- Modal dialogs
- Compact views
- Mobile screens

### Medium (md) - Default

```tsx
<EmptyState variant="no-documents" size="md" />
```

**Use In:**
- Main content areas
- Standard layouts
- Default choice

### Large (lg)

```tsx
<EmptyState variant="no-documents" size="lg" />
```

**Use In:**
- Full-page empty states
- Landing pages
- First-time user experience
- Hero sections

## Advanced Components

### EmptyStateWithHelp

Empty state with educational help cards.

```tsx
<EmptyStateWithHelp
  variant="no-documents"
  actions={[
    {
      label: '書類をアップロード',
      onClick: handleUpload,
    },
  ]}
  helpCards={[
    {
      icon: <FileText className="w-6 h-6 text-primary-600" />,
      title: '対応形式',
      description: 'CSV、PDF、Excel（.xlsx）に対応',
    },
    {
      icon: <Database className="w-6 h-6 text-secondary-600" />,
      title: '自動分類',
      description: '会議費、接待費を自動分類',
    },
    {
      icon: <CheckCircle2 className="w-6 h-6 text-success" />,
      title: '簡単処理',
      description: 'ドラッグ&ドロップで簡単アップロード',
    },
  ]}
/>
```

**Props:**
- `variant` - Empty state variant
- `actions?` - Action buttons
- `helpCards?` - Array of help cards

### DragDropEmptyState

Interactive drag & drop upload area.

```tsx
const [isDragging, setIsDragging] = useState(false);

<div
  onDragEnter={() => setIsDragging(true)}
  onDragLeave={() => setIsDragging(false)}
>
  <DragDropEmptyState
    onFileDrop={(files) => handleUpload(files)}
    onBrowseClick={() => openFilePicker()}
    isDragging={isDragging}
    acceptedFormats={['CSV', 'PDF', 'Excel']}
  />
</div>
```

**Props:**
- `onFileDrop: (files: FileList) => void` - File drop handler
- `onBrowseClick: () => void` - Browse button handler
- `isDragging?: boolean` - Is user dragging files over
- `acceptedFormats?: string[]` - Accepted file formats

### GettingStartedEmptyState

Onboarding flow with numbered steps.

```tsx
<GettingStartedEmptyState
  onUpload={() => startUpload()}
  onViewDocs={() => openDocumentation()}
  onWatchTutorial={() => playVideo()}
/>
```

**Props:**
- `onUpload: () => void` - Upload button handler
- `onViewDocs: () => void` - View documentation handler
- `onWatchTutorial?: () => void` - Watch tutorial handler (optional)

## Customization

### Custom Content

```tsx
<EmptyState
  variant="no-documents"
  title="カスタムタイトル"
  description="カスタム説明文がここに入ります"
  actions={[
    {
      label: 'カスタムボタン',
      onClick: handleCustomAction,
    },
  ]}
/>
```

### Custom Illustration

```tsx
<EmptyState
  variant="no-documents"
  illustration={
    <div className="w-32 h-32 bg-gradient-to-br from-primary-400 to-primary-600 rounded-full" />
  }
/>
```

### Custom Styling

```tsx
<EmptyState
  variant="no-documents"
  className="bg-neutral-100 rounded-xl p-12"
/>
```

## Real-World Examples

### Document List Page

```tsx
function DocumentListPage() {
  const { data, isLoading, isError, refetch } = useDocuments();

  if (isLoading) {
    return <EmptyState variant="loading" size="lg" />;
  }

  if (isError) {
    return <ErrorEmptyState onRetry={refetch} />;
  }

  if (data.length === 0) {
    return (
      <NoDocumentsEmptyState
        onUpload={openUploadDialog}
        onViewSamples={showSamples}
      />
    );
  }

  return <DocumentGrid documents={data} />;
}
```

### Search Results

```tsx
function SearchResults({ query, results, filters }) {
  const hasActiveFilters = Object.keys(filters).length > 0;

  if (results.length === 0 && query) {
    return (
      <NoSearchResultsEmptyState
        searchTerm={query}
        onClearSearch={() => setQuery('')}
        onResetFilters={hasActiveFilters ? () => resetFilters() : undefined}
      />
    );
  }

  if (results.length === 0 && hasActiveFilters) {
    return (
      <FilteredEmptyState
        onResetFilters={() => resetFilters()}
        activeFilterCount={Object.keys(filters).length}
      />
    );
  }

  return <ResultsList results={results} />;
}
```

### Upload Zone

```tsx
function UploadZone() {
  const [isDragging, setIsDragging] = useState(false);
  const { upload, isUploading, error } = useFileUpload();

  if (isUploading) {
    return <EmptyState variant="loading" title="アップロード中..." />;
  }

  if (error) {
    return (
      <ErrorEmptyState
        onRetry={() => upload(lastFiles)}
        errorMessage={error.message}
      />
    );
  }

  return (
    <div
      onDragEnter={() => setIsDragging(true)}
      onDragLeave={() => setIsDragging(false)}
    >
      <DragDropEmptyState
        onFileDrop={(files) => upload(files)}
        onBrowseClick={() => openFilePicker()}
        isDragging={isDragging}
      />
    </div>
  );
}
```

### First-Time User Experience

```tsx
function Dashboard() {
  const { documents, isFirstVisit } = useDocuments();

  if (isFirstVisit && documents.length === 0) {
    return (
      <GettingStartedEmptyState
        onUpload={openUpload}
        onViewDocs={openDocs}
        onWatchTutorial={playTutorial}
      />
    );
  }

  return <DashboardContent documents={documents} />;
}
```

## Accessibility

All empty states follow WCAG AA guidelines:

- **Role & ARIA** - `role="status"` and `aria-live="polite"`
- **Keyboard Navigation** - All buttons are keyboard accessible
- **Focus Indicators** - Visible focus rings (Tailwind defaults)
- **Color Contrast** - Minimum 4.5:1 ratio
- **Screen Readers** - Semantic HTML structure

## Best Practices

### 1. Always Provide Actions

```tsx
// Good - Clear next step
<EmptyState
  variant="no-documents"
  actions={[{ label: '書類をアップロード', onClick: handleUpload }]}
/>

// Bad - No way forward
<EmptyState variant="no-documents" />
```

### 2. Use Appropriate Size

```tsx
// Good - Large for full page
<div className="h-screen">
  <EmptyState variant="no-documents" size="lg" />
</div>

// Good - Small for sidebar
<aside className="w-64">
  <EmptyState variant="no-documents" size="sm" />
</aside>
```

### 3. Match Variant to Context

```tsx
// Good - Error variant for errors
if (error) {
  return <EmptyState variant="error" />;
}

// Bad - Generic variant
if (error) {
  return <EmptyState variant="no-documents" />;
}
```

### 4. Provide Context

```tsx
// Good - Specific error message
<ErrorEmptyState
  errorMessage="ファイルサイズが10MBを超えています"
  onRetry={handleRetry}
/>

// OK - Generic message
<ErrorEmptyState onRetry={handleRetry} />
```

### 5. Progressive Disclosure

```tsx
// Good - Start simple, add help if needed
const [showHelp, setShowHelp] = useState(false);

{showHelp ? (
  <EmptyStateWithHelp variant="no-documents" />
) : (
  <NoDocumentsEmptyState onUpload={handleUpload} />
)}
```

## Testing

```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { NoDocumentsEmptyState } from './EmptyState';

test('renders no documents empty state', () => {
  render(
    <NoDocumentsEmptyState
      onUpload={jest.fn()}
    />
  );

  expect(screen.getByText('書類がアップロードされていません')).toBeInTheDocument();
});

test('calls onUpload when button clicked', () => {
  const handleUpload = jest.fn();

  render(
    <NoDocumentsEmptyState onUpload={handleUpload} />
  );

  fireEvent.click(screen.getByText('書類をアップロード'));

  expect(handleUpload).toHaveBeenCalledTimes(1);
});
```

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Related Files

- [Empty State Component](./EmptyState.tsx) - Main component
- [Usage Examples](./EmptyStateExamples.tsx) - Interactive examples
- [Design System](../../design-system.json) - Design tokens

## License

Part of the Saisonxform project.
