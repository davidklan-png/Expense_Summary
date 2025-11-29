/**
 * Empty State Component
 *
 * Professional empty state UI for tax document management system
 *
 * Features:
 * - Multiple variants (no-documents, no-results, error, loading)
 * - Call-to-action buttons
 * - Helpful illustrations
 * - Responsive design
 * - Accessibility compliant
 */

import React from 'react';
import {
  FileText,
  Search,
  Upload,
  AlertCircle,
  FolderOpen,
  Database,
  Filter,
  RefreshCw,
  Download,
  Plus,
  ArrowRight,
  CheckCircle2,
} from 'lucide-react';

// Types
export type EmptyStateVariant =
  | 'no-documents'
  | 'no-results'
  | 'error'
  | 'loading'
  | 'success'
  | 'filtered'
  | 'offline';

export interface EmptyStateAction {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary' | 'ghost';
  icon?: React.ReactNode;
}

export interface EmptyStateProps {
  variant: EmptyStateVariant;
  title?: string;
  description?: string;
  actions?: EmptyStateAction[];
  illustration?: React.ReactNode;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

// Default configurations for each variant
const VARIANT_CONFIG: Record<
  EmptyStateVariant,
  {
    icon: React.ComponentType<{ className?: string }>;
    title: string;
    description: string;
    iconColor: string;
    iconBgColor: string;
  }
> = {
  'no-documents': {
    icon: FileText,
    title: '書類がアップロードされていません',
    description:
      '税務書類をアップロードして開始してください。CSV、PDF、Excel形式に対応しています。',
    iconColor: 'text-primary-600',
    iconBgColor: 'bg-primary-50',
  },
  'no-results': {
    icon: Search,
    title: '検索結果が見つかりませんでした',
    description:
      '別のキーワードで検索するか、フィルターを調整してください。',
    iconColor: 'text-neutral-600',
    iconBgColor: 'bg-neutral-100',
  },
  error: {
    icon: AlertCircle,
    title: 'エラーが発生しました',
    description:
      'データの読み込み中に問題が発生しました。もう一度お試しください。',
    iconColor: 'text-error',
    iconBgColor: 'bg-error-light',
  },
  loading: {
    icon: RefreshCw,
    title: '読み込み中...',
    description: 'データを取得しています。しばらくお待ちください。',
    iconColor: 'text-primary-600',
    iconBgColor: 'bg-primary-50',
  },
  success: {
    icon: CheckCircle2,
    title: '処理が完了しました',
    description: 'すべての書類が正常に処理されました。',
    iconColor: 'text-success',
    iconBgColor: 'bg-success-light',
  },
  filtered: {
    icon: Filter,
    title: 'フィルター条件に一致する書類がありません',
    description: 'フィルターを変更するか、リセットしてください。',
    iconColor: 'text-warning-dark',
    iconBgColor: 'bg-warning-light',
  },
  offline: {
    icon: AlertCircle,
    title: 'オフラインです',
    description:
      'インターネット接続を確認してください。オンラインに戻ると自動的に再接続します。',
    iconColor: 'text-error',
    iconBgColor: 'bg-error-light',
  },
};

const SIZE_CONFIG = {
  sm: {
    container: 'py-8',
    icon: 'w-12 h-12',
    iconWrapper: 'w-16 h-16',
    title: 'text-h5',
    description: 'text-body-sm',
    buttonPadding: 'px-4 py-2',
    buttonText: 'text-body-sm',
  },
  md: {
    container: 'py-12',
    icon: 'w-16 h-16',
    iconWrapper: 'w-24 h-24',
    title: 'text-h4',
    description: 'text-body',
    buttonPadding: 'px-6 py-2.5',
    buttonText: 'text-body',
  },
  lg: {
    container: 'py-16',
    icon: 'w-20 h-20',
    iconWrapper: 'w-32 h-32',
    title: 'text-h3',
    description: 'text-body',
    buttonPadding: 'px-8 py-3',
    buttonText: 'text-body',
  },
};

export const EmptyState: React.FC<EmptyStateProps> = ({
  variant,
  title,
  description,
  actions = [],
  illustration,
  size = 'md',
  className = '',
}) => {
  const config = VARIANT_CONFIG[variant];
  const sizeConfig = SIZE_CONFIG[size];
  const Icon = config.icon;

  const displayTitle = title || config.title;
  const displayDescription = description || config.description;

  return (
    <div
      className={`
        flex flex-col items-center justify-center text-center
        ${sizeConfig.container}
        ${className}
      `}
      role="status"
      aria-live="polite"
    >
      {/* Icon or Illustration */}
      <div className="mb-6">
        {illustration || (
          <div
            className={`
              ${sizeConfig.iconWrapper}
              ${config.iconBgColor}
              rounded-full flex items-center justify-center
              ${variant === 'loading' ? 'animate-pulse' : ''}
            `}
          >
            <Icon
              className={`
                ${sizeConfig.icon}
                ${config.iconColor}
                ${variant === 'loading' ? 'animate-spin' : ''}
              `}
            />
          </div>
        )}
      </div>

      {/* Title */}
      <h3
        className={`
          ${sizeConfig.title}
          font-semibold text-neutral-900 mb-2
        `}
      >
        {displayTitle}
      </h3>

      {/* Description */}
      <p
        className={`
          ${sizeConfig.description}
          text-neutral-600 max-w-md mb-6
        `}
      >
        {displayDescription}
      </p>

      {/* Actions */}
      {actions.length > 0 && (
        <div className="flex flex-wrap items-center justify-center gap-3">
          {actions.map((action, index) => (
            <button
              key={index}
              onClick={action.onClick}
              className={`
                ${sizeConfig.buttonPadding}
                ${sizeConfig.buttonText}
                rounded-lg font-semibold
                transition-all duration-200
                flex items-center gap-2
                ${
                  action.variant === 'primary' || !action.variant
                    ? 'bg-primary-500 text-white hover:bg-primary-600 shadow-sm hover:shadow-md'
                    : action.variant === 'secondary'
                    ? 'bg-white border border-neutral-300 text-neutral-700 hover:bg-neutral-50'
                    : 'bg-transparent text-primary-600 hover:bg-primary-50'
                }
              `}
            >
              {action.icon}
              {action.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

// ============================================================================
// PRESET COMPONENTS
// ============================================================================

export const NoDocumentsEmptyState: React.FC<{
  onUpload: () => void;
  onViewSamples?: () => void;
}> = ({ onUpload, onViewSamples }) => {
  return (
    <EmptyState
      variant="no-documents"
      actions={[
        {
          label: '書類をアップロード',
          onClick: onUpload,
          variant: 'primary',
          icon: <Upload className="w-5 h-5" />,
        },
        ...(onViewSamples
          ? [
              {
                label: 'サンプルを見る',
                onClick: onViewSamples,
                variant: 'secondary' as const,
                icon: <FileText className="w-5 h-5" />,
              },
            ]
          : []),
      ]}
    />
  );
};

export const NoSearchResultsEmptyState: React.FC<{
  onClearSearch: () => void;
  onResetFilters?: () => void;
  searchTerm?: string;
}> = ({ onClearSearch, onResetFilters, searchTerm }) => {
  return (
    <EmptyState
      variant="no-results"
      title={
        searchTerm
          ? `「${searchTerm}」の検索結果が見つかりませんでした`
          : '検索結果が見つかりませんでした'
      }
      actions={[
        {
          label: '検索をクリア',
          onClick: onClearSearch,
          variant: 'primary',
          icon: <Search className="w-5 h-5" />,
        },
        ...(onResetFilters
          ? [
              {
                label: 'フィルターをリセット',
                onClick: onResetFilters,
                variant: 'secondary' as const,
                icon: <RefreshCw className="w-5 h-5" />,
              },
            ]
          : []),
      ]}
    />
  );
};

export const ErrorEmptyState: React.FC<{
  onRetry: () => void;
  errorMessage?: string;
}> = ({ onRetry, errorMessage }) => {
  return (
    <EmptyState
      variant="error"
      description={
        errorMessage ||
        'データの読み込み中に問題が発生しました。もう一度お試しください。'
      }
      actions={[
        {
          label: '再試行',
          onClick: onRetry,
          variant: 'primary',
          icon: <RefreshCw className="w-5 h-5" />,
        },
      ]}
    />
  );
};

export const FilteredEmptyState: React.FC<{
  onResetFilters: () => void;
  activeFilterCount?: number;
}> = ({ onResetFilters, activeFilterCount }) => {
  return (
    <EmptyState
      variant="filtered"
      description={
        activeFilterCount
          ? `${activeFilterCount}個のフィルターが適用されています。フィルターを変更するか、リセットしてください。`
          : 'フィルター条件に一致する書類がありません。フィルターを変更するか、リセットしてください。'
      }
      actions={[
        {
          label: 'フィルターをリセット',
          onClick: onResetFilters,
          variant: 'primary',
          icon: <Filter className="w-5 h-5" />,
        },
      ]}
    />
  );
};

// ============================================================================
// ADVANCED EMPTY STATE WITH HELP CARDS
// ============================================================================

export interface HelpCard {
  icon: React.ReactNode;
  title: string;
  description: string;
}

export const EmptyStateWithHelp: React.FC<{
  variant: EmptyStateVariant;
  actions?: EmptyStateAction[];
  helpCards?: HelpCard[];
}> = ({ variant, actions, helpCards }) => {
  const defaultHelpCards: HelpCard[] = [
    {
      icon: <FileText className="w-6 h-6 text-primary-600" />,
      title: '対応形式',
      description: 'CSV、PDF、Excel（.xlsx）ファイルに対応しています。',
    },
    {
      icon: <Database className="w-6 h-6 text-secondary-600" />,
      title: '自動分類',
      description: '会議費、接待費などを自動的に分類します。',
    },
    {
      icon: <CheckCircle2 className="w-6 h-6 text-success" />,
      title: '簡単処理',
      description: 'ドラッグ&ドロップで簡単にアップロードできます。',
    },
  ];

  return (
    <div className="space-y-8">
      <EmptyState variant={variant} actions={actions} size="lg" />

      {/* Help Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-4xl mx-auto">
        {(helpCards || defaultHelpCards).map((card, index) => (
          <div
            key={index}
            className="
              bg-white border border-neutral-200 rounded-lg p-6
              hover:shadow-md transition-shadow
            "
          >
            <div className="mb-3">{card.icon}</div>
            <h4 className="text-body font-semibold text-neutral-900 mb-2">
              {card.title}
            </h4>
            <p className="text-body-sm text-neutral-600">{card.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

// ============================================================================
// DRAG & DROP EMPTY STATE
// ============================================================================

export const DragDropEmptyState: React.FC<{
  onFileDrop: (files: FileList) => void;
  onBrowseClick: () => void;
  acceptedFormats?: string[];
  isDragging?: boolean;
}> = ({
  onFileDrop,
  onBrowseClick,
  acceptedFormats = ['CSV', 'PDF', 'Excel'],
  isDragging = false,
}) => {
  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files) {
      onFileDrop(e.dataTransfer.files);
    }
  };

  return (
    <div
      onDragOver={handleDragOver}
      onDrop={handleDrop}
      className={`
        border-2 border-dashed rounded-xl p-12
        transition-all duration-200
        ${
          isDragging
            ? 'border-primary-500 bg-primary-50'
            : 'border-neutral-300 bg-white hover:border-primary-400 hover:bg-neutral-50'
        }
      `}
    >
      <div className="flex flex-col items-center text-center">
        <div
          className={`
            w-20 h-20 rounded-full flex items-center justify-center mb-4
            ${isDragging ? 'bg-primary-100' : 'bg-neutral-100'}
          `}
        >
          <Upload
            className={`
              w-10 h-10
              ${isDragging ? 'text-primary-600' : 'text-neutral-600'}
            `}
          />
        </div>

        <h3 className="text-h4 font-semibold text-neutral-900 mb-2">
          {isDragging
            ? 'ここにファイルをドロップ'
            : 'ファイルをドラッグ&ドロップ'}
        </h3>

        <p className="text-body text-neutral-600 mb-4">
          または
        </p>

        <button
          onClick={onBrowseClick}
          className="
            px-6 py-2.5 bg-primary-500 text-white rounded-lg
            hover:bg-primary-600 transition-colors
            font-semibold text-body
            shadow-sm hover:shadow-md
          "
        >
          ファイルを選択
        </button>

        <p className="text-body-sm text-neutral-500 mt-4">
          対応形式: {acceptedFormats.join('、')}
        </p>
      </div>
    </div>
  );
};

// ============================================================================
// GETTING STARTED EMPTY STATE
// ============================================================================

export const GettingStartedEmptyState: React.FC<{
  onUpload: () => void;
  onViewDocs: () => void;
  onWatchTutorial?: () => void;
}> = ({ onUpload, onViewDocs, onWatchTutorial }) => {
  const steps = [
    {
      number: 1,
      title: '書類をアップロード',
      description: 'CSV、PDF、Excelファイルをアップロード',
      icon: <Upload className="w-6 h-6" />,
    },
    {
      number: 2,
      title: '自動分類',
      description: 'AIが会議費と接待費を自動分類',
      icon: <Database className="w-6 h-6" />,
    },
    {
      number: 3,
      title: '確認・出力',
      description: '結果を確認してダウンロード',
      icon: <Download className="w-6 h-6" />,
    },
  ];

  return (
    <div className="space-y-8 py-12">
      {/* Header */}
      <div className="text-center">
        <div className="w-24 h-24 bg-primary-50 rounded-full flex items-center justify-center mx-auto mb-4">
          <FileText className="w-12 h-12 text-primary-600" />
        </div>
        <h2 className="text-h3 font-semibold text-neutral-900 mb-2">
          税務書類処理システムへようこそ
        </h2>
        <p className="text-body text-neutral-600 max-w-2xl mx-auto">
          会議費と接待費の分類を自動化し、税務処理を効率化します。
          まずは書類をアップロードして開始しましょう。
        </p>
      </div>

      {/* Steps */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
        {steps.map((step, index) => (
          <div key={step.number} className="relative">
            <div className="bg-white border border-neutral-200 rounded-lg p-6 h-full">
              <div className="flex items-start gap-4">
                <div className="w-10 h-10 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center font-semibold flex-shrink-0">
                  {step.number}
                </div>
                <div className="flex-1">
                  <h3 className="text-body font-semibold text-neutral-900 mb-1">
                    {step.title}
                  </h3>
                  <p className="text-body-sm text-neutral-600">
                    {step.description}
                  </p>
                </div>
              </div>
            </div>

            {/* Arrow */}
            {index < steps.length - 1 && (
              <div className="hidden md:block absolute top-1/2 -right-3 transform -translate-y-1/2">
                <ArrowRight className="w-6 h-6 text-neutral-300" />
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Actions */}
      <div className="flex flex-wrap items-center justify-center gap-3">
        <button
          onClick={onUpload}
          className="
            px-8 py-3 bg-primary-500 text-white rounded-lg
            hover:bg-primary-600 transition-colors
            font-semibold text-body
            shadow-sm hover:shadow-md
            flex items-center gap-2
          "
        >
          <Upload className="w-5 h-5" />
          書類をアップロード
        </button>

        <button
          onClick={onViewDocs}
          className="
            px-8 py-3 bg-white border border-neutral-300 text-neutral-700 rounded-lg
            hover:bg-neutral-50 transition-colors
            font-semibold text-body
            flex items-center gap-2
          "
        >
          <FileText className="w-5 h-5" />
          ドキュメントを見る
        </button>

        {onWatchTutorial && (
          <button
            onClick={onWatchTutorial}
            className="
              px-8 py-3 bg-transparent text-primary-600 rounded-lg
              hover:bg-primary-50 transition-colors
              font-semibold text-body
            "
          >
            チュートリアルを見る
          </button>
        )}
      </div>
    </div>
  );
};

export default EmptyState;
