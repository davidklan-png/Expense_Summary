/**
 * Empty State Usage Examples
 *
 * Demonstrates all empty state variants and use cases
 */

import React, { useState } from 'react';
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
import { Upload, FileText, RefreshCw, Filter } from 'lucide-react';

// ============================================================================
// BASIC USAGE
// ============================================================================

export const BasicEmptyStateExample: React.FC = () => {
  return (
    <div className="space-y-8 p-8">
      <h2 className="text-h3 font-semibold">Basic Empty States</h2>

      {/* No Documents */}
      <div className="border border-neutral-200 rounded-lg p-8 bg-white">
        <EmptyState
          variant="no-documents"
          actions={[
            {
              label: '書類をアップロード',
              onClick: () => console.log('Upload clicked'),
              variant: 'primary',
              icon: <Upload className="w-5 h-5" />,
            },
          ]}
        />
      </div>

      {/* No Results */}
      <div className="border border-neutral-200 rounded-lg p-8 bg-white">
        <EmptyState
          variant="no-results"
          actions={[
            {
              label: '検索をクリア',
              onClick: () => console.log('Clear search'),
              variant: 'primary',
            },
          ]}
        />
      </div>

      {/* Error */}
      <div className="border border-neutral-200 rounded-lg p-8 bg-white">
        <EmptyState
          variant="error"
          actions={[
            {
              label: '再試行',
              onClick: () => console.log('Retry'),
              variant: 'primary',
              icon: <RefreshCw className="w-5 h-5" />,
            },
          ]}
        />
      </div>
    </div>
  );
};

// ============================================================================
// PRESET COMPONENTS
// ============================================================================

export const PresetEmptyStatesExample: React.FC = () => {
  return (
    <div className="space-y-8 p-8">
      <h2 className="text-h3 font-semibold">Preset Components</h2>

      {/* No Documents Preset */}
      <div className="border border-neutral-200 rounded-lg p-8 bg-white">
        <h3 className="text-h5 font-semibold mb-4">No Documents</h3>
        <NoDocumentsEmptyState
          onUpload={() => console.log('Upload')}
          onViewSamples={() => console.log('View samples')}
        />
      </div>

      {/* No Search Results */}
      <div className="border border-neutral-200 rounded-lg p-8 bg-white">
        <h3 className="text-h5 font-semibold mb-4">No Search Results</h3>
        <NoSearchResultsEmptyState
          searchTerm="会議費 2024"
          onClearSearch={() => console.log('Clear')}
          onResetFilters={() => console.log('Reset')}
        />
      </div>

      {/* Error */}
      <div className="border border-neutral-200 rounded-lg p-8 bg-white">
        <h3 className="text-h5 font-semibold mb-4">Error</h3>
        <ErrorEmptyState
          onRetry={() => console.log('Retry')}
          errorMessage="ネットワークエラー: サーバーに接続できませんでした"
        />
      </div>

      {/* Filtered */}
      <div className="border border-neutral-200 rounded-lg p-8 bg-white">
        <h3 className="text-h5 font-semibold mb-4">Filtered</h3>
        <FilteredEmptyState
          onResetFilters={() => console.log('Reset filters')}
          activeFilterCount={3}
        />
      </div>
    </div>
  );
};

// ============================================================================
// SIZES
// ============================================================================

export const EmptyStateSizesExample: React.FC = () => {
  return (
    <div className="space-y-8 p-8">
      <h2 className="text-h3 font-semibold">Empty State Sizes</h2>

      {/* Small */}
      <div className="border border-neutral-200 rounded-lg p-8 bg-white">
        <h3 className="text-h5 font-semibold mb-4">Small</h3>
        <EmptyState
          variant="no-documents"
          size="sm"
          actions={[
            {
              label: 'アップロード',
              onClick: () => console.log('Upload'),
            },
          ]}
        />
      </div>

      {/* Medium (Default) */}
      <div className="border border-neutral-200 rounded-lg p-8 bg-white">
        <h3 className="text-h5 font-semibold mb-4">Medium (Default)</h3>
        <EmptyState
          variant="no-documents"
          size="md"
          actions={[
            {
              label: 'アップロード',
              onClick: () => console.log('Upload'),
            },
          ]}
        />
      </div>

      {/* Large */}
      <div className="border border-neutral-200 rounded-lg p-8 bg-white">
        <h3 className="text-h5 font-semibold mb-4">Large</h3>
        <EmptyState
          variant="no-documents"
          size="lg"
          actions={[
            {
              label: 'アップロード',
              onClick: () => console.log('Upload'),
            },
          ]}
        />
      </div>
    </div>
  );
};

// ============================================================================
// WITH HELP CARDS
// ============================================================================

export const EmptyStateWithHelpExample: React.FC = () => {
  return (
    <div className="space-y-8 p-8">
      <h2 className="text-h3 font-semibold">Empty State with Help Cards</h2>

      <div className="border border-neutral-200 rounded-lg p-8 bg-neutral-50">
        <EmptyStateWithHelp
          variant="no-documents"
          actions={[
            {
              label: '書類をアップロード',
              onClick: () => console.log('Upload'),
              variant: 'primary',
              icon: <Upload className="w-5 h-5" />,
            },
            {
              label: 'ドキュメントを見る',
              onClick: () => console.log('View docs'),
              variant: 'secondary',
              icon: <FileText className="w-5 h-5" />,
            },
          ]}
        />
      </div>
    </div>
  );
};

// ============================================================================
// DRAG & DROP
// ============================================================================

export const DragDropEmptyStateExample: React.FC = () => {
  const [isDragging, setIsDragging] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<string[]>([]);

  const handleFileDrop = (files: FileList) => {
    const fileNames = Array.from(files).map((f) => f.name);
    setUploadedFiles(fileNames);
    setIsDragging(false);
    console.log('Files dropped:', fileNames);
  };

  const handleBrowseClick = () => {
    console.log('Browse clicked');
    // Open file picker
  };

  return (
    <div className="space-y-8 p-8">
      <h2 className="text-h3 font-semibold">Drag & Drop Empty State</h2>

      <div className="border border-neutral-200 rounded-lg p-8 bg-white">
        <div
          onDragEnter={() => setIsDragging(true)}
          onDragLeave={() => setIsDragging(false)}
        >
          <DragDropEmptyState
            onFileDrop={handleFileDrop}
            onBrowseClick={handleBrowseClick}
            isDragging={isDragging}
            acceptedFormats={['CSV', 'PDF', 'Excel']}
          />
        </div>

        {uploadedFiles.length > 0 && (
          <div className="mt-4">
            <h4 className="text-body font-semibold mb-2">Uploaded Files:</h4>
            <ul className="space-y-1">
              {uploadedFiles.map((file, index) => (
                <li key={index} className="text-body-sm text-neutral-600">
                  ✓ {file}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

// ============================================================================
// GETTING STARTED
// ============================================================================

export const GettingStartedExample: React.FC = () => {
  return (
    <div className="space-y-8 p-8">
      <h2 className="text-h3 font-semibold">Getting Started Empty State</h2>

      <div className="border border-neutral-200 rounded-lg p-8 bg-neutral-50">
        <GettingStartedEmptyState
          onUpload={() => console.log('Upload')}
          onViewDocs={() => console.log('View docs')}
          onWatchTutorial={() => console.log('Watch tutorial')}
        />
      </div>
    </div>
  );
};

// ============================================================================
// INTERACTIVE DEMO
// ============================================================================

export const InteractiveEmptyStateDemo: React.FC = () => {
  const [currentState, setCurrentState] = useState<
    'no-documents' | 'loading' | 'error' | 'success' | 'filtered'
  >('no-documents');

  const handleUpload = () => {
    setCurrentState('loading');
    setTimeout(() => {
      setCurrentState('success');
    }, 2000);
  };

  const handleError = () => {
    setCurrentState('error');
  };

  const handleFilter = () => {
    setCurrentState('filtered');
  };

  const handleReset = () => {
    setCurrentState('no-documents');
  };

  return (
    <div className="space-y-8 p-8">
      <h2 className="text-h3 font-semibold">Interactive Demo</h2>

      {/* Controls */}
      <div className="flex flex-wrap gap-2">
        <button
          onClick={() => setCurrentState('no-documents')}
          className="px-4 py-2 bg-white border border-neutral-300 rounded hover:bg-neutral-50"
        >
          No Documents
        </button>
        <button
          onClick={handleUpload}
          className="px-4 py-2 bg-white border border-neutral-300 rounded hover:bg-neutral-50"
        >
          Simulate Upload
        </button>
        <button
          onClick={handleError}
          className="px-4 py-2 bg-white border border-neutral-300 rounded hover:bg-neutral-50"
        >
          Show Error
        </button>
        <button
          onClick={handleFilter}
          className="px-4 py-2 bg-white border border-neutral-300 rounded hover:bg-neutral-50"
        >
          Apply Filters
        </button>
        <button
          onClick={handleReset}
          className="px-4 py-2 bg-primary-500 text-white rounded hover:bg-primary-600"
        >
          Reset
        </button>
      </div>

      {/* Empty State Display */}
      <div className="border border-neutral-200 rounded-lg p-8 bg-white min-h-96">
        {currentState === 'no-documents' && (
          <NoDocumentsEmptyState
            onUpload={handleUpload}
            onViewSamples={() => console.log('View samples')}
          />
        )}

        {currentState === 'loading' && (
          <EmptyState variant="loading" size="lg" />
        )}

        {currentState === 'success' && (
          <EmptyState
            variant="success"
            size="lg"
            actions={[
              {
                label: '続けてアップロード',
                onClick={handleUpload},
                variant: 'primary',
                icon: <Upload className="w-5 h-5" />,
              },
            ]}
          />
        )}

        {currentState === 'error' && (
          <ErrorEmptyState
            onRetry={handleUpload}
            errorMessage="ファイルのアップロードに失敗しました"
          />
        )}

        {currentState === 'filtered' && (
          <FilteredEmptyState
            onResetFilters={handleReset}
            activeFilterCount={2}
          />
        )}
      </div>
    </div>
  );
};

// ============================================================================
// SHOWCASE
// ============================================================================

export const EmptyStateShowcase: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('basic');

  const tabs = [
    { id: 'basic', label: 'Basic' },
    { id: 'presets', label: 'Presets' },
    { id: 'sizes', label: 'Sizes' },
    { id: 'help', label: 'With Help' },
    { id: 'dragdrop', label: 'Drag & Drop' },
    { id: 'getting-started', label: 'Getting Started' },
    { id: 'interactive', label: 'Interactive' },
  ];

  return (
    <div className="min-h-screen bg-neutral-50">
      <div className="max-w-7xl mx-auto p-8">
        <h1 className="text-h2 font-bold text-neutral-900 mb-8">
          Empty State Component Showcase
        </h1>

        {/* Tabs */}
        <div className="flex flex-wrap gap-2 mb-8 border-b border-neutral-200">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`
                px-4 py-2 text-body font-medium
                border-b-2 transition-colors
                ${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-neutral-600 hover:text-neutral-900'
                }
              `}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Content */}
        <div>
          {activeTab === 'basic' && <BasicEmptyStateExample />}
          {activeTab === 'presets' && <PresetEmptyStatesExample />}
          {activeTab === 'sizes' && <EmptyStateSizesExample />}
          {activeTab === 'help' && <EmptyStateWithHelpExample />}
          {activeTab === 'dragdrop' && <DragDropEmptyStateExample />}
          {activeTab === 'getting-started' && <GettingStartedExample />}
          {activeTab === 'interactive' && <InteractiveEmptyStateDemo />}
        </div>
      </div>
    </div>
  );
};

export default EmptyStateShowcase;
