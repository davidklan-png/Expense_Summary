/**
 * Storybook Stories for Empty State Components
 *
 * Demonstrates all variants, sizes, and configurations
 */

import type { Meta, StoryObj } from '@storybook/react';
import {
  EmptyState,
  NoDocumentsEmptyState,
  NoSearchResultsEmptyState,
  ErrorEmptyState,
  FilteredEmptyState,
  EmptyStateWithHelp,
  DragDropEmptyState,
  GettingStartedEmptyState,
} from './EmptyState';
import { Upload, FileText, RefreshCw, Filter, Search } from 'lucide-react';
import React, { useState } from 'react';

// ============================================================================
// META
// ============================================================================

const meta: Meta<typeof EmptyState> = {
  title: 'Components/EmptyState',
  component: EmptyState,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component:
          'Professional empty state components for tax document management system with Japanese language support.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['no-documents', 'no-results', 'error', 'loading', 'success', 'filtered', 'offline'],
      description: 'Empty state variant',
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg'],
      description: 'Component size',
    },
    title: {
      control: 'text',
      description: 'Custom title (overrides default)',
    },
    description: {
      control: 'text',
      description: 'Custom description (overrides default)',
    },
  },
};

export default meta;
type Story = StoryObj<typeof EmptyState>;

// ============================================================================
// BASIC STORIES
// ============================================================================

export const Default: Story = {
  args: {
    variant: 'no-documents',
    size: 'md',
  },
  parameters: {
    docs: {
      description: {
        story: 'Default empty state without actions. Shows when no tax documents have been uploaded.',
      },
    },
  },
};

export const Loading: Story = {
  args: {
    variant: 'loading',
    size: 'md',
  },
  parameters: {
    docs: {
      description: {
        story: 'Loading state with animated spinner. Shows during data fetching.',
      },
    },
  },
};

export const Error: Story = {
  args: {
    variant: 'error',
    size: 'md',
    actions: [
      {
        label: '再試行',
        onClick: () => alert('Retry clicked'),
        variant: 'primary',
        icon: <RefreshCw className="w-5 h-5" />,
      },
    ],
  },
  parameters: {
    docs: {
      description: {
        story: 'Error state with retry action. Shows when data loading or processing fails.',
      },
    },
  },
};

// ============================================================================
// ALL VARIANTS
// ============================================================================

export const AllVariants: Story = {
  render: () => (
    <div className="space-y-12 p-8">
      <div>
        <h3 className="text-h4 font-semibold mb-4">No Documents</h3>
        <div className="border border-neutral-200 rounded-lg p-8 bg-white">
          <EmptyState
            variant="no-documents"
            actions={[
              {
                label: '書類をアップロード',
                onClick: () => console.log('Upload'),
                icon: <Upload className="w-5 h-5" />,
              },
            ]}
          />
        </div>
      </div>

      <div>
        <h3 className="text-h4 font-semibold mb-4">No Results</h3>
        <div className="border border-neutral-200 rounded-lg p-8 bg-white">
          <EmptyState
            variant="no-results"
            actions={[
              {
                label: '検索をクリア',
                onClick: () => console.log('Clear'),
                icon: <Search className="w-5 h-5" />,
              },
            ]}
          />
        </div>
      </div>

      <div>
        <h3 className="text-h4 font-semibold mb-4">Error</h3>
        <div className="border border-neutral-200 rounded-lg p-8 bg-white">
          <EmptyState
            variant="error"
            actions={[
              {
                label: '再試行',
                onClick: () => console.log('Retry'),
                icon: <RefreshCw className="w-5 h-5" />,
              },
            ]}
          />
        </div>
      </div>

      <div>
        <h3 className="text-h4 font-semibold mb-4">Loading</h3>
        <div className="border border-neutral-200 rounded-lg p-8 bg-white">
          <EmptyState variant="loading" />
        </div>
      </div>

      <div>
        <h3 className="text-h4 font-semibold mb-4">Success</h3>
        <div className="border border-neutral-200 rounded-lg p-8 bg-white">
          <EmptyState variant="success" />
        </div>
      </div>

      <div>
        <h3 className="text-h4 font-semibold mb-4">Filtered</h3>
        <div className="border border-neutral-200 rounded-lg p-8 bg-white">
          <EmptyState
            variant="filtered"
            actions={[
              {
                label: 'フィルターをリセット',
                onClick: () => console.log('Reset'),
                icon: <Filter className="w-5 h-5" />,
              },
            ]}
          />
        </div>
      </div>

      <div>
        <h3 className="text-h4 font-semibold mb-4">Offline</h3>
        <div className="border border-neutral-200 rounded-lg p-8 bg-white">
          <EmptyState variant="offline" />
        </div>
      </div>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'All available empty state variants in one view.',
      },
    },
  },
};

// ============================================================================
// SIZES
// ============================================================================

export const SmallSize: Story = {
  args: {
    variant: 'no-documents',
    size: 'sm',
    actions: [
      {
        label: 'アップロード',
        onClick: () => console.log('Upload'),
      },
    ],
  },
  parameters: {
    docs: {
      description: {
        story: 'Small size for compact spaces like sidebars or modals.',
      },
    },
  },
};

export const MediumSize: Story = {
  args: {
    variant: 'no-documents',
    size: 'md',
    actions: [
      {
        label: 'アップロード',
        onClick: () => console.log('Upload'),
      },
    ],
  },
  parameters: {
    docs: {
      description: {
        story: 'Medium size (default) for standard layouts.',
      },
    },
  },
};

export const LargeSize: Story = {
  args: {
    variant: 'no-documents',
    size: 'lg',
    actions: [
      {
        label: 'アップロード',
        onClick: () => console.log('Upload'),
      },
    ],
  },
  parameters: {
    docs: {
      description: {
        story: 'Large size for full-page empty states or hero sections.',
      },
    },
  },
};

// ============================================================================
// WITH ACTIONS
// ============================================================================

export const WithSingleAction: Story = {
  args: {
    variant: 'no-documents',
    actions: [
      {
        label: '書類をアップロード',
        onClick: () => alert('Upload clicked'),
        variant: 'primary',
        icon: <Upload className="w-5 h-5" />,
      },
    ],
  },
  parameters: {
    docs: {
      description: {
        story: 'Empty state with a single primary action button.',
      },
    },
  },
};

export const WithMultipleActions: Story = {
  args: {
    variant: 'no-documents',
    actions: [
      {
        label: '書類をアップロード',
        onClick: () => alert('Upload clicked'),
        variant: 'primary',
        icon: <Upload className="w-5 h-5" />,
      },
      {
        label: 'サンプルを見る',
        onClick: () => alert('View samples clicked'),
        variant: 'secondary',
        icon: <FileText className="w-5 h-5" />,
      },
      {
        label: 'ドキュメント',
        onClick: () => alert('Docs clicked'),
        variant: 'ghost',
      },
    ],
  },
  parameters: {
    docs: {
      description: {
        story: 'Empty state with multiple action buttons of different variants.',
      },
    },
  },
};

// ============================================================================
// CUSTOM CONTENT
// ============================================================================

export const CustomTitle: Story = {
  args: {
    variant: 'no-documents',
    title: 'カスタムタイトルがここに入ります',
    actions: [
      {
        label: '開始',
        onClick: () => console.log('Start'),
      },
    ],
  },
  parameters: {
    docs: {
      description: {
        story: 'Empty state with custom title overriding the default.',
      },
    },
  },
};

export const CustomDescription: Story = {
  args: {
    variant: 'no-documents',
    description: 'これはカスタムの説明文です。デフォルトの説明文を上書きしています。',
    actions: [
      {
        label: '開始',
        onClick: () => console.log('Start'),
      },
    ],
  },
  parameters: {
    docs: {
      description: {
        story: 'Empty state with custom description overriding the default.',
      },
    },
  },
};

export const CustomTitleAndDescription: Story = {
  args: {
    variant: 'no-documents',
    title: 'まだ何もありません',
    description: '最初のステップとして、税務書類をアップロードしてください。CSV、PDF、Excelファイルに対応しています。',
    actions: [
      {
        label: '今すぐアップロード',
        onClick: () => console.log('Upload now'),
        variant: 'primary',
      },
    ],
  },
  parameters: {
    docs: {
      description: {
        story: 'Empty state with both custom title and description.',
      },
    },
  },
};

// ============================================================================
// PRESET COMPONENTS
// ============================================================================

export const PresetNoDocuments: Story = {
  render: () => (
    <div className="border border-neutral-200 rounded-lg p-8 bg-white">
      <NoDocumentsEmptyState
        onUpload={() => alert('Upload clicked')}
        onViewSamples={() => alert('View samples clicked')}
      />
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'Preset component for no documents state with upload and view samples actions.',
      },
    },
  },
};

export const PresetNoSearchResults: Story = {
  render: () => (
    <div className="border border-neutral-200 rounded-lg p-8 bg-white">
      <NoSearchResultsEmptyState
        searchTerm="会議費 2024"
        onClearSearch={() => alert('Clear search clicked')}
        onResetFilters={() => alert('Reset filters clicked')}
      />
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'Preset component for no search results with search term displayed.',
      },
    },
  },
};

export const PresetError: Story = {
  render: () => (
    <div className="border border-neutral-200 rounded-lg p-8 bg-white">
      <ErrorEmptyState
        onRetry={() => alert('Retry clicked')}
        errorMessage="ネットワークエラー: サーバーに接続できませんでした（タイムアウト）"
      />
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'Preset error component with custom error message.',
      },
    },
  },
};

export const PresetFiltered: Story = {
  render: () => (
    <div className="border border-neutral-200 rounded-lg p-8 bg-white">
      <FilteredEmptyState
        onResetFilters={() => alert('Reset filters clicked')}
        activeFilterCount={3}
      />
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'Preset filtered component showing active filter count.',
      },
    },
  },
};

// ============================================================================
// ADVANCED COMPONENTS
// ============================================================================

export const WithHelpCards: Story = {
  render: () => (
    <div className="border border-neutral-200 rounded-lg p-8 bg-neutral-50 min-w-[900px]">
      <EmptyStateWithHelp
        variant="no-documents"
        actions={[
          {
            label: '書類をアップロード',
            onClick: () => alert('Upload clicked'),
            variant: 'primary',
            icon: <Upload className="w-5 h-5" />,
          },
          {
            label: 'ドキュメントを見る',
            onClick: () => alert('View docs clicked'),
            variant: 'secondary',
            icon: <FileText className="w-5 h-5" />,
          },
        ]}
      />
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'Empty state with educational help cards below.',
      },
    },
  },
};

export const DragAndDrop: Story = {
  render: () => {
    const [isDragging, setIsDragging] = useState(false);

    return (
      <div
        className="border border-neutral-200 rounded-lg p-8 bg-white min-w-[600px]"
        onDragEnter={() => setIsDragging(true)}
        onDragLeave={() => setIsDragging(false)}
      >
        <DragDropEmptyState
          onFileDrop={(files) => {
            alert(`Dropped ${files.length} file(s)`);
            setIsDragging(false);
          }}
          onBrowseClick={() => alert('Browse clicked')}
          isDragging={isDragging}
          acceptedFormats={['CSV', 'PDF', 'Excel']}
        />
      </div>
    );
  },
  parameters: {
    docs: {
      description: {
        story: 'Interactive drag and drop upload zone. Try dragging files over it!',
      },
    },
  },
};

export const GettingStarted: Story = {
  render: () => (
    <div className="border border-neutral-200 rounded-lg p-8 bg-neutral-50 min-w-[900px]">
      <GettingStartedEmptyState
        onUpload={() => alert('Upload clicked')}
        onViewDocs={() => alert('View docs clicked')}
        onWatchTutorial={() => alert('Watch tutorial clicked')}
      />
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'Getting started component with numbered steps and multiple actions.',
      },
    },
  },
};

// ============================================================================
// INTERACTIVE DEMO
// ============================================================================

export const InteractiveStateMachine: Story = {
  render: () => {
    const [state, setState] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

    const handleUpload = () => {
      setState('loading');
      setTimeout(() => {
        setState('success');
      }, 2000);
    };

    const handleError = () => {
      setState('error');
    };

    const handleReset = () => {
      setState('idle');
    };

    return (
      <div className="space-y-4">
        <div className="flex gap-2">
          <button
            onClick={handleUpload}
            className="px-4 py-2 bg-primary-500 text-white rounded hover:bg-primary-600"
          >
            Simulate Upload
          </button>
          <button
            onClick={handleError}
            className="px-4 py-2 bg-error text-white rounded hover:bg-error-dark"
          >
            Trigger Error
          </button>
          <button
            onClick={handleReset}
            className="px-4 py-2 bg-neutral-500 text-white rounded hover:bg-neutral-600"
          >
            Reset
          </button>
        </div>

        <div className="border border-neutral-200 rounded-lg p-8 bg-white min-h-96">
          {state === 'idle' && (
            <NoDocumentsEmptyState
              onUpload={handleUpload}
              onViewSamples={() => alert('View samples')}
            />
          )}

          {state === 'loading' && <EmptyState variant="loading" size="lg" />}

          {state === 'success' && (
            <EmptyState
              variant="success"
              size="lg"
              actions={[
                {
                  label: '続けてアップロード',
                  onClick: handleUpload,
                  icon: <Upload className="w-5 h-5" />,
                },
              ]}
            />
          )}

          {state === 'error' && (
            <ErrorEmptyState
              onRetry={handleUpload}
              errorMessage="ファイルのアップロードに失敗しました"
            />
          )}
        </div>
      </div>
    );
  },
  parameters: {
    docs: {
      description: {
        story: 'Interactive state machine demo. Click buttons to transition between states.',
      },
    },
  },
};

// ============================================================================
// REAL-WORLD SCENARIOS
// ============================================================================

export const DocumentListEmpty: Story = {
  render: () => (
    <div className="border border-neutral-200 rounded-lg p-8 bg-white">
      <NoDocumentsEmptyState
        onUpload={() => alert('Upload document')}
        onViewSamples={() => alert('View sample documents')}
      />
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'Real-world: Empty document list page.',
      },
    },
  },
};

export const SearchNoResults: Story = {
  render: () => (
    <div className="border border-neutral-200 rounded-lg p-8 bg-white">
      <NoSearchResultsEmptyState
        searchTerm="接待費 2023年12月"
        onClearSearch={() => alert('Clear search')}
        onResetFilters={() => alert('Reset filters')}
      />
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'Real-world: Search returned no results.',
      },
    },
  },
};

export const NetworkError: Story = {
  render: () => (
    <div className="border border-neutral-200 rounded-lg p-8 bg-white">
      <ErrorEmptyState
        onRetry={() => alert('Retrying...')}
        errorMessage="ネットワークエラー: インターネット接続を確認してください"
      />
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'Real-world: Network connection failed.',
      },
    },
  },
};

export const FilteredNoMatches: Story = {
  render: () => (
    <div className="border border-neutral-200 rounded-lg p-8 bg-white">
      <FilteredEmptyState onResetFilters={() => alert('Filters reset')} activeFilterCount={5} />
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'Real-world: Active filters with no matching results.',
      },
    },
  },
};

// ============================================================================
// EDGE CASES
// ============================================================================

export const NoActions: Story = {
  args: {
    variant: 'success',
    actions: [],
  },
  parameters: {
    docs: {
      description: {
        story: 'Edge case: Empty state with no action buttons.',
      },
    },
  },
};

export const VeryLongTitle: Story = {
  args: {
    variant: 'no-documents',
    title: 'これは非常に長いタイトルです。テキストが折り返されることを確認するために、十分な長さのテキストを用意しています。',
    actions: [
      {
        label: 'アップロード',
        onClick: () => console.log('Upload'),
      },
    ],
  },
  parameters: {
    docs: {
      description: {
        story: 'Edge case: Very long title to test text wrapping.',
      },
    },
  },
};

export const VeryLongDescription: Story = {
  args: {
    variant: 'no-documents',
    description:
      'これは非常に長い説明文です。複数行にわたってテキストが表示されることを確認するために、十分な長さのテキストを用意しています。この説明文は、最大幅を超えた場合に適切に折り返されることをテストするためのものです。',
    actions: [
      {
        label: 'アップロード',
        onClick: () => console.log('Upload'),
      },
    ],
  },
  parameters: {
    docs: {
      description: {
        story: 'Edge case: Very long description to test text wrapping.',
      },
    },
  },
};

// ============================================================================
// ACCESSIBILITY
// ============================================================================

export const AccessibilityTest: Story = {
  render: () => (
    <div className="space-y-4">
      <p className="text-body text-neutral-700 max-w-2xl">
        This story demonstrates accessibility features:
      </p>
      <ul className="list-disc pl-6 text-body-sm text-neutral-600 space-y-1">
        <li>
          <strong>role="status"</strong> - Announces state changes to screen readers
        </li>
        <li>
          <strong>aria-live="polite"</strong> - Non-intrusive announcements
        </li>
        <li>
          <strong>Keyboard Navigation</strong> - All buttons are keyboard accessible
        </li>
        <li>
          <strong>Focus Indicators</strong> - Visible focus rings on interactive elements
        </li>
        <li>
          <strong>Color Contrast</strong> - Meets WCAG AA standards (4.5:1 minimum)
        </li>
      </ul>

      <div className="border border-neutral-200 rounded-lg p-8 bg-white">
        <NoDocumentsEmptyState
          onUpload={() => alert('Upload (keyboard accessible)')}
          onViewSamples={() => alert('View samples (keyboard accessible)')}
        />
      </div>

      <p className="text-body-sm text-neutral-600">
        Try tabbing through the buttons with your keyboard and pressing Enter or Space.
      </p>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'Demonstrates accessibility features and keyboard navigation.',
      },
    },
    a11y: {
      config: {
        rules: [
          {
            id: 'color-contrast',
            enabled: true,
          },
          {
            id: 'button-name',
            enabled: true,
          },
        ],
      },
    },
  },
};
