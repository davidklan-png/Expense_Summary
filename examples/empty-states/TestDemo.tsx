/**
 * Test Demo - Improved Empty State Components
 *
 * Interactive demonstration of all improvements
 */

import React, { useState } from 'react';
import {
  EmptyState,
  NoDocumentsEmptyState,
  NoSearchResultsEmptyState,
  ErrorEmptyState,
  FilteredEmptyState,
  EmptyStateWithHelp,
} from './EmptyState.improved';
import { Upload, FileText, RefreshCw, Check, X } from 'lucide-react';
import './animations.css';

export const TestDemo: React.FC = () => {
  const [activeTab, setActiveTab] = useState('improvements');
  const [testDisabled, setTestDisabled] = useState(false);

  const tabs = [
    { id: 'improvements', label: 'Key Improvements' },
    { id: 'sizes', label: 'Size Comparison' },
    { id: 'mobile', label: 'Mobile Test' },
    { id: 'accessibility', label: 'Accessibility' },
    { id: 'interactive', label: 'Interactive Demo' },
  ];

  return (
    <div className="min-h-screen bg-neutral-50">
      <div className="max-w-7xl mx-auto p-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-h2 font-bold text-neutral-900 mb-2">
            Empty State Components - Improved Version
          </h1>
          <p className="text-body text-neutral-600">
            All design evaluation improvements implemented and ready for testing
          </p>
        </div>

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
          {activeTab === 'improvements' && <ImprovementsTab />}
          {activeTab === 'sizes' && <SizesTab />}
          {activeTab === 'mobile' && <MobileTab />}
          {activeTab === 'accessibility' && <AccessibilityTab setTestDisabled={setTestDisabled} testDisabled={testDisabled} />}
          {activeTab === 'interactive' && <InteractiveTab />}
        </div>
      </div>
    </div>
  );
};

// ============================================================================
// TAB: KEY IMPROVEMENTS
// ============================================================================

const ImprovementsTab: React.FC = () => {
  return (
    <div className="space-y-8">
      <div className="bg-white rounded-lg p-6 border border-neutral-200">
        <h2 className="text-h4 font-semibold mb-4">✅ Implemented Improvements</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <ImprovementCard
            title="Button Gap: gap-4"
            description="Aligned with 8px grid (was gap-3/12px)"
            status="fixed"
          />
          <ImprovementCard
            title="Disabled States"
            description="Added disabled button styles with cursor-not-allowed"
            status="fixed"
          />
          <ImprovementCard
            title="Focus Indicators"
            description="Added focus:ring-2 for keyboard accessibility"
            status="fixed"
          />
          <ImprovementCard
            title="Mobile Layout"
            description="Full-width buttons on mobile, row on desktop"
            status="fixed"
          />
          <ImprovementCard
            title="Proportional Scaling"
            description="Consistent 1.5x and 2x ratios across sizes"
            status="fixed"
          />
          <ImprovementCard
            title="Responsive Icons"
            description="Icons scale with screen size (sm:w-16)"
            status="fixed"
          />
          <ImprovementCard
            title="Grid: 1→2→3 Columns"
            description="Smooth progression for help cards"
            status="fixed"
          />
          <ImprovementCard
            title="Entrance Animations"
            description="Fade-in and slide-up animations added"
            status="fixed"
          />
        </div>
      </div>

      {/* Example with all improvements */}
      <div className="bg-white rounded-lg p-8 border border-neutral-200">
        <h3 className="text-h5 font-semibold mb-6">Example with All Improvements</h3>
        <EmptyStateWithHelp
          variant="no-documents"
          actions={[
            {
              label: '書類をアップロード',
              onClick: () => alert('Upload clicked!'),
              variant: 'primary',
              icon: <Upload className="w-5 h-5" />,
            },
            {
              label: 'サンプルを見る',
              onClick: () => alert('Samples clicked!'),
              variant: 'secondary',
              icon: <FileText className="w-5 h-5" />,
            },
            {
              label: 'ドキュメント',
              onClick: () => alert('Docs clicked!'),
              variant: 'ghost',
            },
          ]}
        />
      </div>
    </div>
  );
};

// ============================================================================
// TAB: SIZE COMPARISON
// ============================================================================

const SizesTab: React.FC = () => {
  return (
    <div className="space-y-8">
      {/* Small */}
      <div className="bg-white rounded-lg p-6 border border-neutral-200">
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-h5 font-semibold">Small (sm)</h3>
          <code className="text-caption bg-neutral-100 px-2 py-1 rounded">
            Container: py-8 (32px)
          </code>
        </div>
        <EmptyState
          variant="no-documents"
          size="sm"
          actions={[
            {
              label: 'アップロード',
              onClick: () => alert('Small clicked'),
              icon: <Upload className="w-4 h-4" />,
            },
          ]}
        />
      </div>

      {/* Medium */}
      <div className="bg-white rounded-lg p-6 border border-neutral-200">
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-h5 font-semibold">Medium (md) - Default</h3>
          <code className="text-caption bg-neutral-100 px-2 py-1 rounded">
            Container: py-12 (48px = 1.5x)
          </code>
        </div>
        <EmptyState
          variant="no-documents"
          size="md"
          actions={[
            {
              label: 'アップロード',
              onClick: () => alert('Medium clicked'),
              icon: <Upload className="w-5 h-5" />,
            },
          ]}
        />
      </div>

      {/* Large */}
      <div className="bg-white rounded-lg p-6 border border-neutral-200">
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-h5 font-semibold">Large (lg)</h3>
          <code className="text-caption bg-neutral-100 px-2 py-1 rounded">
            Container: py-16 (64px = 2x)
          </code>
        </div>
        <EmptyState
          variant="no-documents"
          size="lg"
          actions={[
            {
              label: 'アップロード',
              onClick: () => alert('Large clicked'),
              icon: <Upload className="w-5 h-5" />,
            },
          ]}
        />
      </div>
    </div>
  );
};

// ============================================================================
// TAB: MOBILE TEST
// ============================================================================

const MobileTab: React.FC = () => {
  return (
    <div className="space-y-8">
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
        <p className="text-body-sm text-yellow-800">
          <strong>Tip:</strong> Resize your browser window or use DevTools mobile view to test responsive behavior
        </p>
      </div>

      <div className="bg-white rounded-lg p-6 border border-neutral-200">
        <h3 className="text-h5 font-semibold mb-4">Mobile Button Layout</h3>
        <p className="text-body-sm text-neutral-600 mb-6">
          Buttons stack vertically on mobile (&lt; 640px) and display horizontally on larger screens
        </p>
        <EmptyState
          variant="no-documents"
          actions={[
            {
              label: '書類をアップロード',
              onClick: () => {},
              variant: 'primary',
              icon: <Upload className="w-5 h-5" />,
            },
            {
              label: 'サンプルを見る',
              onClick: () => {},
              variant: 'secondary',
              icon: <FileText className="w-5 h-5" />,
            },
            {
              label: 'ヘルプを見る',
              onClick: () => {},
              variant: 'ghost',
            },
          ]}
        />
      </div>

      <div className="bg-white rounded-lg p-6 border border-neutral-200">
        <h3 className="text-h5 font-semibold mb-4">Responsive Icons</h3>
        <p className="text-body-sm text-neutral-600 mb-6">
          Icons are smaller on mobile (w-12) and larger on desktop (w-16)
        </p>
        <EmptyState variant="loading" size="md" />
      </div>
    </div>
  );
};

// ============================================================================
// TAB: ACCESSIBILITY
// ============================================================================

const AccessibilityTab: React.FC<{
  testDisabled: boolean;
  setTestDisabled: (value: boolean) => void;
}> = ({ testDisabled, setTestDisabled }) => {
  return (
    <div className="space-y-8">
      <div className="bg-white rounded-lg p-6 border border-neutral-200">
        <h3 className="text-h5 font-semibold mb-4">Keyboard Navigation Test</h3>
        <p className="text-body-sm text-neutral-600 mb-6">
          Press <kbd className="px-2 py-1 bg-neutral-100 border border-neutral-300 rounded text-caption">Tab</kbd> to navigate between buttons.
          Press <kbd className="px-2 py-1 bg-neutral-100 border border-neutral-300 rounded text-caption">Enter</kbd> or{' '}
          <kbd className="px-2 py-1 bg-neutral-100 border border-neutral-300 rounded text-caption">Space</kbd> to activate.
        </p>
        <EmptyState
          variant="no-documents"
          actions={[
            {
              label: 'Button 1 (Primary)',
              onClick: () => alert('Button 1 activated via keyboard!'),
              variant: 'primary',
            },
            {
              label: 'Button 2 (Secondary)',
              onClick: () => alert('Button 2 activated via keyboard!'),
              variant: 'secondary',
            },
            {
              label: 'Button 3 (Ghost)',
              onClick: () => alert('Button 3 activated via keyboard!'),
              variant: 'ghost',
            },
          ]}
        />
      </div>

      <div className="bg-white rounded-lg p-6 border border-neutral-200">
        <h3 className="text-h5 font-semibold mb-4">Disabled State Test</h3>
        <div className="mb-6">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={testDisabled}
              onChange={(e) => setTestDisabled(e.target.checked)}
              className="w-4 h-4"
            />
            <span className="text-body-sm">Enable disabled state</span>
          </label>
        </div>
        <EmptyState
          variant="error"
          actions={[
            {
              label: '再試行',
              onClick: () => alert('Retry clicked'),
              variant: 'primary',
              icon: <RefreshCw className="w-5 h-5" />,
              disabled: testDisabled,
            },
            {
              label: 'キャンセル',
              onClick: () => alert('Cancel clicked'),
              variant: 'secondary',
              disabled: testDisabled,
            },
          ]}
        />
      </div>

      <div className="bg-white rounded-lg p-6 border border-neutral-200">
        <h3 className="text-h5 font-semibold mb-4">ARIA & Screen Reader Support</h3>
        <ul className="space-y-2 text-body-sm text-neutral-700 mb-6">
          <li className="flex items-start gap-2">
            <Check className="w-5 h-5 text-success flex-shrink-0 mt-0.5" />
            <span><code>role="status"</code> announces state changes</span>
          </li>
          <li className="flex items-start gap-2">
            <Check className="w-5 h-5 text-success flex-shrink-0 mt-0.5" />
            <span><code>aria-live="polite"</code> for non-intrusive updates</span>
          </li>
          <li className="flex items-start gap-2">
            <Check className="w-5 h-5 text-success flex-shrink-0 mt-0.5" />
            <span>Semantic HTML structure (headings, buttons)</span>
          </li>
          <li className="flex items-start gap-2">
            <Check className="w-5 h-5 text-success flex-shrink-0 mt-0.5" />
            <span>Visible focus indicators (ring-2)</span>
          </li>
          <li className="flex items-start gap-2">
            <Check className="w-5 h-5 text-success flex-shrink-0 mt-0.5" />
            <span>WCAG AA contrast ratios exceeded</span>
          </li>
        </ul>
        <EmptyState variant="success" size="md" />
      </div>
    </div>
  );
};

// ============================================================================
// TAB: INTERACTIVE DEMO
// ============================================================================

const InteractiveTab: React.FC = () => {
  const [state, setState] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [attempts, setAttempts] = useState(0);

  const handleUpload = () => {
    setState('loading');
    setAttempts(attempts + 1);
    setTimeout(() => {
      if (Math.random() > 0.3) {
        setState('success');
      } else {
        setState('error');
      }
    }, 2000);
  };

  const handleReset = () => {
    setState('idle');
  };

  return (
    <div className="space-y-8">
      <div className="bg-white rounded-lg p-6 border border-neutral-200">
        <div className="mb-6">
          <h3 className="text-h5 font-semibold mb-2">Interactive State Machine</h3>
          <p className="text-body-sm text-neutral-600">
            Current State: <strong className="text-primary-600">{state.toUpperCase()}</strong>
            {' | '}
            Attempts: <strong>{attempts}</strong>
          </p>
        </div>

        <div className="min-h-96 bg-neutral-50 rounded-lg p-8 border-2 border-dashed border-neutral-300">
          {state === 'idle' && (
            <NoDocumentsEmptyState
              onUpload={handleUpload}
              onViewSamples={() => alert('View samples')}
            />
          )}

          {state === 'loading' && (
            <EmptyState variant="loading" size="lg" />
          )}

          {state === 'success' && (
            <EmptyState
              variant="success"
              size="lg"
              title="アップロード完了!"
              description="書類が正常に処理されました。"
              actions={[
                {
                  label: '続けてアップロード',
                  onClick: handleUpload,
                  variant: 'primary',
                  icon: <Upload className="w-5 h-5" />,
                },
                {
                  label: 'リセット',
                  onClick: handleReset,
                  variant: 'secondary',
                },
              ]}
            />
          )}

          {state === 'error' && (
            <ErrorEmptyState
              onRetry={handleUpload}
              errorMessage="ファイルのアップロードに失敗しました。もう一度お試しください。"
            />
          )}
        </div>
      </div>
    </div>
  );
};

// ============================================================================
// IMPROVEMENT CARD
// ============================================================================

const ImprovementCard: React.FC<{
  title: string;
  description: string;
  status: 'fixed' | 'pending';
}> = ({ title, description, status }) => {
  return (
    <div className="flex items-start gap-3 p-4 bg-neutral-50 rounded-lg border border-neutral-200">
      <div className={`
        w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0
        ${status === 'fixed' ? 'bg-success-light' : 'bg-neutral-200'}
      `}>
        {status === 'fixed' ? (
          <Check className="w-4 h-4 text-success" />
        ) : (
          <X className="w-4 h-4 text-neutral-500" />
        )}
      </div>
      <div className="flex-1">
        <h4 className="text-body-sm font-semibold text-neutral-900 mb-1">
          {title}
        </h4>
        <p className="text-caption text-neutral-600">
          {description}
        </p>
      </div>
    </div>
  );
};

export default TestDemo;
