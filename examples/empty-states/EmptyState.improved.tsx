/**
 * Empty State Component - IMPROVED VERSION
 *
 * All design evaluation improvements implemented:
 * ✅ Fixed button gap (gap-4 for 8px grid alignment)
 * ✅ Added disabled states
 * ✅ Added focus indicators
 * ✅ Improved mobile button layout
 * ✅ Proportional size scaling
 * ✅ Responsive icon sizes
 * ✅ Improved grid responsiveness
 * ✅ Entrance animations
 * ✅ Explicit font weights
 */

import React from 'react';
import {
  FileText,
  Search,
  Upload,
  AlertCircle,
  Database,
  Filter,
  RefreshCw,
  Download,
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
  disabled?: boolean;
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
    description: '別のキーワードで検索するか、フィルターを調整してください。',
    iconColor: 'text-neutral-600',
    iconBgColor: 'bg-neutral-100',
  },
  error: {
    icon: AlertCircle,
    title: 'エラーが発生しました',
    description: 'データの読み込み中に問題が発生しました。もう一度お試しください。',
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

// IMPROVED: Proportional size scaling with 8px grid alignment
const SIZE_CONFIG = {
  sm: {
    container: 'py-8',          // 32px (base)
    icon: 'w-10 h-10 sm:w-12 sm:h-12',          // 40-48px (responsive)
    iconWrapper: 'w-14 h-14 sm:w-16 sm:h-16',   // 56-64px (responsive)
    iconMargin: 'mb-4',         // 16px
    title: 'text-h5',           // 20px
    titleMargin: 'mb-1.5',      // 6px
    description: 'text-caption', // 12px (improved contrast ratio)
    descMargin: 'mb-4',         // 16px
    buttonPadding: 'px-4 py-2',
    buttonText: 'text-body-sm',
    buttonMinWidth: 'min-w-[120px] sm:min-w-[140px]',
  },
  md: {
    container: 'py-12',         // 48px (1.5x)
    icon: 'w-14 h-14 sm:w-16 sm:h-16',          // 56-64px (responsive)
    iconWrapper: 'w-20 h-20 sm:w-24 sm:h-24',   // 80-96px (responsive)
    iconMargin: 'mb-6',         // 24px (1.5x)
    title: 'text-h4',           // 24px
    titleMargin: 'mb-2',        // 8px
    description: 'text-body',   // 16px
    descMargin: 'mb-6',         // 24px (1.5x)
    buttonPadding: 'px-6 py-2.5',
    buttonText: 'text-body',
    buttonMinWidth: 'min-w-[140px] sm:min-w-[160px]',
  },
  lg: {
    container: 'py-16',         // 64px (2x)
    icon: 'w-20 h-20 sm:w-24 sm:h-24',          // 80-96px (responsive)
    iconWrapper: 'w-28 h-28 sm:w-32 sm:h-32',   // 112-128px (responsive)
    iconMargin: 'mb-8',         // 32px (2x)
    title: 'text-h3',           // 30px
    titleMargin: 'mb-3',        // 12px
    description: 'text-body',   // 16px
    descMargin: 'mb-8',         // 32px (2x)
    buttonPadding: 'px-8 py-3',
    buttonText: 'text-body',
    buttonMinWidth: 'min-w-[160px] sm:min-w-[180px]',
  },
};

// IMPROVED: Content width hierarchy
const CONTENT_WIDTH = {
  text: 'max-w-md',      // 448px - Optimal reading width
  actions: 'max-w-lg',   // 512px - Button groups
  cards: 'max-w-4xl',    // 896px - Help cards grid
  hero: 'max-w-2xl',     // 672px - Hero descriptions
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

  // IMPROVED: Helper function for button styles
  const getButtonStyles = (buttonVariant: 'primary' | 'secondary' | 'ghost' = 'primary', disabled = false) => {
    const baseStyles = `
      ${sizeConfig.buttonPadding}
      ${sizeConfig.buttonText}
      ${sizeConfig.buttonMinWidth}
      rounded-lg font-semibold
      transition-all duration-200
      flex items-center justify-center gap-2
      focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2
      focus-visible:ring-2 focus-visible:ring-primary-500
    `;

    if (buttonVariant === 'primary') {
      return `${baseStyles} bg-primary-500 text-white hover:bg-primary-600 shadow-sm hover:shadow-md
        disabled:bg-neutral-300 disabled:text-neutral-500 disabled:cursor-not-allowed disabled:shadow-none`;
    } else if (buttonVariant === 'secondary') {
      return `${baseStyles} bg-white border border-neutral-300 text-neutral-700 hover:bg-neutral-50
        disabled:bg-neutral-100 disabled:text-neutral-400 disabled:border-neutral-200 disabled:cursor-not-allowed`;
    } else {
      return `${baseStyles} bg-transparent text-primary-600 hover:bg-primary-50
        disabled:text-neutral-400 disabled:hover:bg-transparent disabled:cursor-not-allowed`;
    }
  };

  return (
    <div
      className={`
        flex flex-col items-center justify-center text-center
        ${sizeConfig.container}
        ${className}
        animate-fade-in
      `}
      role="status"
      aria-live="polite"
    >
      {/* Icon or Illustration */}
      <div className={sizeConfig.iconMargin}>
        {illustration || (
          <div
            className={`
              ${sizeConfig.iconWrapper}
              ${config.iconBgColor}
              rounded-full flex items-center justify-center
              ${variant === 'loading' ? 'animate-pulse-scale' : ''}
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

      {/* Title - IMPROVED: Explicit font weight */}
      <h3
        className={`
          ${sizeConfig.title}
          ${sizeConfig.titleMargin}
          font-semibold text-neutral-900
        `}
      >
        {displayTitle}
      </h3>

      {/* Description - IMPROVED: Explicit font weight and max-width */}
      <p
        className={`
          ${sizeConfig.description}
          ${sizeConfig.descMargin}
          font-normal text-neutral-600
          ${CONTENT_WIDTH.text}
        `}
      >
        {displayDescription}
      </p>

      {/* Actions - IMPROVED: gap-4 for 8px grid, mobile responsive layout */}
      {actions.length > 0 && (
        <div className={`flex flex-col sm:flex-row items-stretch sm:items-center justify-center gap-4 ${CONTENT_WIDTH.actions} w-full px-4 sm:px-0`}>
          {actions.map((action, index) => (
            <button
              key={index}
              onClick={action.onClick}
              disabled={action.disabled}
              className={getButtonStyles(action.variant, action.disabled)}
            >
              {action.icon}
              <span className="truncate">{action.label}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

// ============================================================================
// PRESET COMPONENTS (IMPROVED)
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
// ADVANCED COMPONENTS (IMPROVED)
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

      {/* IMPROVED: Grid with responsive columns (1→2→3) */}
      <div className={`grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 ${CONTENT_WIDTH.cards} mx-auto px-4 sm:px-0`}>
        {(helpCards || defaultHelpCards).map((card, index) => (
          <div
            key={index}
            className="
              bg-white border border-neutral-200 rounded-lg p-6
              hover:shadow-md transition-shadow
              animate-slide-up
            "
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <div className="mb-3">{card.icon}</div>
            <h4 className="text-body font-semibold text-neutral-900 mb-2">
              {card.title}
            </h4>
            <p className="text-body-sm font-normal text-neutral-600">{card.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

// Export improved version as default
export default EmptyState;
