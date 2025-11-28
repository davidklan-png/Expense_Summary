/**
 * Optimistic UI Three-Pane Interface
 *
 * Features:
 * - Optimistic message rendering (instant feedback)
 * - 2-second fallback skeleton loaders
 * - Progressive loading states
 * - Error recovery with rollback
 * - Smooth transitions and animations
 *
 * Based on Saisonxform Design System
 */

import React, { useState, useRef, useEffect } from 'react';
import {
  Send,
  Loader2,
  MessageSquare,
  Brain,
  FileText,
  Settings,
  ChevronDown,
  ChevronUp,
  Copy,
  Check,
  Sparkles,
  Zap,
  Database,
  Search,
  XCircle,
  AlertCircle,
  RefreshCw,
} from 'lucide-react';

// Types
interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  status: 'optimistic' | 'pending' | 'success' | 'error';
  error?: string;
}

interface ReasoningStep {
  id: string;
  step: number;
  title: string;
  content: string;
  status: 'pending' | 'processing' | 'complete' | 'error';
  duration?: number;
}

interface RetrievedDocument {
  id: string;
  title: string;
  content: string;
  score: number;
  source: string;
  highlighted?: string[];
}

// Skeleton Loader Components
const MessageSkeleton: React.FC = () => (
  <div className="flex justify-start animate-fade-in">
    <div className="max-w-[85%] bg-neutral-100 rounded-lg p-3 space-y-2">
      <div className="h-4 bg-neutral-200 rounded w-48 animate-pulse" />
      <div className="h-4 bg-neutral-200 rounded w-64 animate-pulse" />
      <div className="h-4 bg-neutral-200 rounded w-32 animate-pulse" />
    </div>
  </div>
);

const ReasoningStepSkeleton: React.FC = () => (
  <div className="bg-white border border-neutral-300 rounded-lg p-3 animate-pulse">
    <div className="flex items-center gap-3">
      <div className="w-6 h-6 bg-neutral-200 rounded-full" />
      <div className="flex-1 space-y-2">
        <div className="h-4 bg-neutral-200 rounded w-32" />
        <div className="h-3 bg-neutral-200 rounded w-16" />
      </div>
    </div>
  </div>
);

const DocumentSkeleton: React.FC = () => (
  <div className="border border-neutral-300 rounded-lg p-4 animate-pulse">
    <div className="flex justify-between mb-3">
      <div className="space-y-2 flex-1">
        <div className="h-4 bg-neutral-200 rounded w-48" />
        <div className="h-3 bg-neutral-200 rounded w-32" />
      </div>
      <div className="h-6 w-16 bg-neutral-200 rounded" />
    </div>
    <div className="space-y-2">
      <div className="h-3 bg-neutral-200 rounded w-full" />
      <div className="h-3 bg-neutral-200 rounded w-full" />
      <div className="h-3 bg-neutral-200 rounded w-3/4" />
    </div>
  </div>
);

// Main Component
const OptimisticUIInterface: React.FC = () => {
  // State
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [reasoningSteps, setReasoningSteps] = useState<ReasoningStep[]>([]);
  const [retrievedDocs, setRetrievedDocs] = useState<RetrievedDocument[]>([]);
  const [showSkeletons, setShowSkeletons] = useState(false);
  const [expandedSteps, setExpandedSteps] = useState<Set<string>>(new Set());
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [paneLayout, setPaneLayout] = useState<'horizontal' | 'vertical'>('horizontal');

  const inputRef = useRef<HTMLTextAreaElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const skeletonTimerRef = useRef<NodeJS.Timeout | null>(null);
  const processingTimerRef = useRef<NodeJS.Timeout | null>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Cleanup timers on unmount
  useEffect(() => {
    return () => {
      if (skeletonTimerRef.current) clearTimeout(skeletonTimerRef.current);
      if (processingTimerRef.current) clearTimeout(processingTimerRef.current);
    };
  }, []);

  // Optimistic submit handler
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isProcessing) return;

    const userMessageId = `user-${Date.now()}`;
    const assistantMessageId = `assistant-${Date.now() + 1}`;

    // 1. OPTIMISTIC: Immediately add user message
    const userMessage: Message = {
      id: userMessageId,
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
      status: 'success', // User messages are always successful
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsProcessing(true);

    // 2. OPTIMISTIC: Add pending assistant message after 100ms (feels instant)
    setTimeout(() => {
      const assistantMessage: Message = {
        id: assistantMessageId,
        role: 'assistant',
        content: '', // Empty for now
        timestamp: new Date(),
        status: 'optimistic',
      };
      setMessages((prev) => [...prev, assistantMessage]);
    }, 100);

    // 3. SKELETON FALLBACK: Show skeletons after 2 seconds if still processing
    skeletonTimerRef.current = setTimeout(() => {
      if (isProcessing) {
        setShowSkeletons(true);
      }
    }, 2000);

    // 4. Start actual processing
    try {
      await processQuery(inputValue, assistantMessageId);
    } catch (error) {
      // Error handling: Update message status
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === assistantMessageId
            ? {
                ...msg,
                status: 'error',
                content: 'Sorry, an error occurred while processing your request.',
                error: error instanceof Error ? error.message : 'Unknown error',
              }
            : msg
        )
      );
      setShowSkeletons(false);
    } finally {
      setIsProcessing(false);
      if (skeletonTimerRef.current) {
        clearTimeout(skeletonTimerRef.current);
      }
    }
  };

  // Process query with progressive updates
  const processQuery = async (query: string, messageId: string): Promise<void> => {
    // Simulate network delay (replace with actual API call)
    await new Promise((resolve) => setTimeout(resolve, 500));

    // 1. Start context retrieval (can show immediately)
    const docs: RetrievedDocument[] = [
      {
        id: '1',
        title: '会議費の定義と税務処理',
        content: '会議費とは、会議に関連して通常必要となる飲食代等の費用をいいます。税務上、社内外を問わず、会議に際して供与される茶菓子、弁当、飲料等の費用は会議費として処理することができます。',
        score: 0.94,
        source: '国税庁通達 第9章',
        highlighted: ['会議費', '税務処理', '飲食代'],
      },
      {
        id: '2',
        title: '接待費の判定基準',
        content: '接待飲食費は、得意先や仕入先等、社外の者との飲食費に限られます。1人当たり5,000円以下（税抜）の飲食費については、交際費等から除外することができます。',
        score: 0.87,
        source: '法人税法施行令 第37条',
        highlighted: ['接待費', '5,000円', '判定基準'],
      },
      {
        id: '3',
        title: '出席者の記録要件',
        content: '会議費として処理するためには、①出席者の氏名、②会議の目的、③会議の日時、場所、④費用の金額を記録する必要があります。',
        score: 0.82,
        source: '国税庁FAQ Q&A',
        highlighted: ['出席者', '記録要件', '会議費'],
      },
    ];

    // Progressive document loading (one at a time)
    for (let i = 0; i < docs.length; i++) {
      await new Promise((resolve) => setTimeout(resolve, 400));
      setRetrievedDocs((prev) => [...prev, docs[i]]);
    }

    // 2. Show reasoning steps progressively
    const steps: ReasoningStep[] = [
      {
        id: 'step1',
        step: 1,
        title: 'クエリ分析',
        content: 'ユーザーの質問を分析し、会議費と接待費の分類に関する質問であることを特定しました。',
        status: 'pending',
      },
      {
        id: 'step2',
        step: 2,
        title: 'コンテキスト検索',
        content: 'ベクトルデータベースから関連する税務規定を3件取得しました（類似度スコア: 0.94, 0.87, 0.82）。',
        status: 'pending',
      },
      {
        id: 'step3',
        step: 3,
        title: '情報統合',
        content: '取得した文書から会議費の定義、判定基準、記録要件を抽出し、統合しています。',
        status: 'pending',
      },
      {
        id: 'step4',
        step: 4,
        title: '回答生成',
        content: '統合した情報をもとに、わかりやすい日本語で回答を生成しています。',
        status: 'pending',
      },
    ];

    // Process steps one at a time
    for (let i = 0; i < steps.length; i++) {
      steps[i].status = 'processing';
      setReasoningSteps([...steps]);
      await new Promise((resolve) => setTimeout(resolve, 600));

      steps[i].status = 'complete';
      steps[i].duration = Math.random() * 1.5 + 0.5;
      setReasoningSteps([...steps]);
      await new Promise((resolve) => setTimeout(resolve, 200));
    }

    // 3. Generate final response (streaming simulation)
    const fullResponse = `会議費と接待費の分類についてお答えします。

**会議費の定義:**
会議費とは、会議に関連して通常必要となる飲食代等の費用です。社内外を問わず、会議に際して供与される茶菓子、弁当、飲料等の費用は会議費として処理できます。

**接待費との違い:**
接待飲食費は、得意先や仕入先等、社外の者との飲食費に限られます。1人当たり5,000円以下（税抜）の飲食費については、交際費等から除外することができます。

**必要な記録:**
会議費として処理するためには、以下の記録が必要です：
1. 出席者の氏名
2. 会議の目的
3. 会議の日時、場所
4. 費用の金額

これらの記録を適切に保管することで、税務調査時の説明資料として活用できます。`;

    // Stream response word by word (smoother UX)
    const words = fullResponse.split(' ');
    let currentContent = '';

    for (let i = 0; i < words.length; i++) {
      currentContent += (i > 0 ? ' ' : '') + words[i];
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === messageId
            ? {
                ...msg,
                content: currentContent,
                status: 'pending',
              }
            : msg
        )
      );
      await new Promise((resolve) => setTimeout(resolve, 30)); // 30ms per word
    }

    // Mark as complete
    setMessages((prev) =>
      prev.map((msg) =>
        msg.id === messageId
          ? {
              ...msg,
              status: 'success',
            }
          : msg
      )
    );

    // Hide skeletons
    setShowSkeletons(false);
  };

  // Retry failed message
  const retryMessage = (messageId: string) => {
    const message = messages.find((m) => m.id === messageId);
    if (!message || message.role !== 'assistant') return;

    // Find the user message that triggered this
    const messageIndex = messages.findIndex((m) => m.id === messageId);
    const userMessage = messages[messageIndex - 1];

    if (!userMessage || userMessage.role !== 'user') return;

    // Remove failed message
    setMessages((prev) => prev.filter((m) => m.id !== messageId));

    // Retry with the original query
    setInputValue(userMessage.content);
    setTimeout(() => {
      inputRef.current?.focus();
    }, 100);
  };

  // Toggle step expansion
  const toggleStep = (stepId: string) => {
    const newExpanded = new Set(expandedSteps);
    if (newExpanded.has(stepId)) {
      newExpanded.delete(stepId);
    } else {
      newExpanded.add(stepId);
    }
    setExpandedSteps(newExpanded);
  };

  // Copy to clipboard
  const copyToClipboard = async (text: string, id: string) => {
    await navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="flex h-screen bg-neutral-50">
      {/* Main Container */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="h-16 bg-white border-b border-neutral-300 flex items-center justify-between px-6 shadow-sm">
          <div className="flex items-center gap-3">
            <Sparkles className="w-6 h-6 text-primary-500" />
            <h1 className="text-h4 font-semibold text-neutral-900">AI Assistant</h1>
            <span className="px-2 py-1 bg-success-light text-success-dark text-xs font-semibold rounded-full">
              Optimistic UI
            </span>
          </div>

          <button
            onClick={() => setPaneLayout(paneLayout === 'horizontal' ? 'vertical' : 'horizontal')}
            className="p-2 rounded-lg hover:bg-neutral-100 transition-colors"
          >
            <Settings className="w-5 h-5 text-neutral-600" />
          </button>
        </header>

        {/* Three Panes */}
        <div className={`flex-1 flex ${paneLayout === 'horizontal' ? 'flex-row' : 'flex-col'} overflow-hidden`}>
          {/* LEFT/TOP PANE - Input & Conversation */}
          <div className={`${paneLayout === 'horizontal' ? 'w-1/3' : 'h-1/3'} bg-white border-r border-b border-neutral-300 flex flex-col`}>
            {/* Pane Header */}
            <div className="h-14 border-b border-neutral-300 flex items-center px-4">
              <MessageSquare className="w-5 h-5 text-primary-500 mr-2" />
              <h2 className="text-body font-semibold text-neutral-900">Conversation</h2>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((message) => (
                <div key={message.id}>
                  {message.role === 'user' ? (
                    <div className="flex justify-end">
                      <div className="max-w-[85%] bg-primary-500 text-white rounded-lg p-3">
                        <p className="text-body-sm whitespace-pre-wrap">{message.content}</p>
                        <span className="text-xs opacity-70 mt-1 block">
                          {message.timestamp.toLocaleTimeString()}
                        </span>
                      </div>
                    </div>
                  ) : (
                    <div className="flex justify-start">
                      <div
                        className={`
                          max-w-[85%] rounded-lg p-3
                          ${message.status === 'error'
                            ? 'bg-error-light border border-error-border'
                            : 'bg-neutral-100'
                          }
                        `}
                      >
                        {message.status === 'optimistic' || message.status === 'pending' ? (
                          <div className="flex items-center gap-2 text-neutral-600">
                            <Loader2 className="w-4 h-4 animate-spin" />
                            <span className="text-body-sm">Thinking...</span>
                          </div>
                        ) : message.status === 'error' ? (
                          <>
                            <div className="flex items-center gap-2 text-error mb-2">
                              <AlertCircle className="w-4 h-4" />
                              <span className="text-body-sm font-medium">Error</span>
                            </div>
                            <p className="text-body-sm text-neutral-700">{message.content}</p>
                            <button
                              onClick={() => retryMessage(message.id)}
                              className="
                                mt-2 px-3 py-1 bg-error text-white rounded
                                hover:bg-error-dark transition-colors
                                text-xs font-medium flex items-center gap-1
                              "
                            >
                              <RefreshCw className="w-3 h-3" />
                              Retry
                            </button>
                          </>
                        ) : (
                          <>
                            <p className="text-body-sm text-neutral-900 whitespace-pre-wrap">
                              {message.content}
                            </p>
                            <span className="text-xs text-neutral-600 mt-1 block">
                              {message.timestamp.toLocaleTimeString()}
                            </span>
                          </>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              ))}

              {/* Skeleton loader after 2s */}
              {showSkeletons && isProcessing && (
                <MessageSkeleton />
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input Form */}
            <form onSubmit={handleSubmit} className="border-t border-neutral-300 p-4">
              <div className="flex gap-2">
                <textarea
                  ref={inputRef}
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleSubmit(e);
                    }
                  }}
                  placeholder="Ask me anything..."
                  className="
                    flex-1 px-4 py-3 rounded-lg
                    border border-neutral-300
                    focus:outline-none focus:ring-2 focus:ring-primary-500
                    resize-none text-body
                  "
                  rows={2}
                  disabled={isProcessing}
                />
                <button
                  type="submit"
                  disabled={isProcessing || !inputValue.trim()}
                  className="
                    px-6 py-3 bg-primary-500 text-white rounded-lg
                    hover:bg-primary-600 disabled:bg-neutral-300
                    transition-colors flex items-center gap-2
                    font-semibold
                  "
                >
                  <Send className="w-5 h-5" />
                </button>
              </div>
            </form>
          </div>

          {/* MIDDLE PANE - Reasoning */}
          <div className={`${paneLayout === 'horizontal' ? 'w-1/3' : 'h-1/3'} bg-neutral-50 border-r border-b border-neutral-300 flex flex-col`}>
            <div className="h-14 bg-white border-b border-neutral-300 flex items-center px-4">
              <Brain className="w-5 h-5 text-accent-600 mr-2" />
              <h2 className="text-body font-semibold text-neutral-900">Reasoning</h2>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-3">
              {reasoningSteps.length === 0 && !showSkeletons ? (
                <div className="flex flex-col items-center justify-center h-full text-center">
                  <Zap className="w-12 h-12 text-neutral-300 mb-3" />
                  <p className="text-body text-neutral-600">
                    Reasoning steps will appear here
                  </p>
                </div>
              ) : (
                <>
                  {reasoningSteps.map((step) => (
                    <div
                      key={step.id}
                      className="bg-white border border-neutral-300 rounded-lg overflow-hidden"
                    >
                      <div
                        onClick={() => toggleStep(step.id)}
                        className="p-3 cursor-pointer hover:bg-neutral-50 transition-colors flex items-center justify-between"
                      >
                        <div className="flex items-center gap-3 flex-1">
                          {step.status === 'processing' && (
                            <Loader2 className="w-6 h-6 text-accent-600 animate-spin" />
                          )}
                          {step.status === 'complete' && (
                            <Check className="w-6 h-6 text-success p-1 bg-success-light rounded-full" />
                          )}
                          {step.status === 'pending' && (
                            <div className="w-6 h-6 rounded-full bg-neutral-200 flex items-center justify-center">
                              <span className="text-xs text-neutral-600">{step.step}</span>
                            </div>
                          )}

                          <div className="flex-1">
                            <h3 className="text-body-sm font-semibold text-neutral-900">
                              {step.title}
                            </h3>
                            {step.duration && (
                              <span className="text-caption text-neutral-600">
                                {step.duration.toFixed(2)}s
                              </span>
                            )}
                          </div>
                        </div>

                        {expandedSteps.has(step.id) ? (
                          <ChevronUp className="w-5 h-5 text-neutral-400" />
                        ) : (
                          <ChevronDown className="w-5 h-5 text-neutral-400" />
                        )}
                      </div>

                      {expandedSteps.has(step.id) && (
                        <div className="px-3 pb-3 border-t border-neutral-200 pt-3">
                          <p className="text-body-sm text-neutral-700">{step.content}</p>
                        </div>
                      )}
                    </div>
                  ))}

                  {/* Show skeleton if still processing after 2s */}
                  {showSkeletons && isProcessing && reasoningSteps.length < 4 && (
                    <>
                      <ReasoningStepSkeleton />
                      <ReasoningStepSkeleton />
                    </>
                  )}
                </>
              )}
            </div>
          </div>

          {/* RIGHT/BOTTOM PANE - Retrieved Context */}
          <div className={`${paneLayout === 'horizontal' ? 'flex-1' : 'flex-1'} bg-white flex flex-col`}>
            <div className="h-14 border-b border-neutral-300 flex items-center justify-between px-4">
              <div className="flex items-center gap-2">
                <Database className="w-5 h-5 text-secondary-600" />
                <h2 className="text-body font-semibold text-neutral-900">Retrieved Context</h2>
                {retrievedDocs.length > 0 && (
                  <span className="px-2 py-0.5 bg-secondary-100 text-secondary-700 text-xs font-semibold rounded-full">
                    {retrievedDocs.length}
                  </span>
                )}
              </div>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-3">
              {retrievedDocs.length === 0 && !showSkeletons ? (
                <div className="flex flex-col items-center justify-center h-full text-center">
                  <Search className="w-12 h-12 text-neutral-300 mb-3" />
                  <p className="text-body text-neutral-600">
                    Retrieved documents will appear here
                  </p>
                </div>
              ) : (
                <>
                  {retrievedDocs.map((doc) => (
                    <div
                      key={doc.id}
                      className="border border-neutral-300 rounded-lg p-4 hover:shadow-md transition-shadow animate-slide-up"
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex-1">
                          <h3 className="text-body font-semibold text-neutral-900 mb-1">
                            {doc.title}
                          </h3>
                          <div className="flex items-center gap-2 text-caption text-neutral-600">
                            <FileText className="w-3 h-3" />
                            <span>{doc.source}</span>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <div className="px-2 py-1 bg-success-light text-success-dark text-xs font-semibold rounded">
                            {(doc.score * 100).toFixed(0)}%
                          </div>
                          <button
                            onClick={() => copyToClipboard(doc.content, doc.id)}
                            className="p-1 rounded hover:bg-neutral-100 transition-colors"
                          >
                            {copiedId === doc.id ? (
                              <Check className="w-4 h-4 text-success" />
                            ) : (
                              <Copy className="w-4 h-4 text-neutral-600" />
                            )}
                          </button>
                        </div>
                      </div>

                      <p className="text-body-sm text-neutral-700 leading-relaxed">
                        {doc.content}
                      </p>

                      {doc.highlighted && doc.highlighted.length > 0 && (
                        <div className="mt-3 flex flex-wrap gap-2">
                          {doc.highlighted.map((term, idx) => (
                            <span
                              key={idx}
                              className="px-2 py-1 bg-warning-light text-warning-dark text-xs font-medium rounded"
                            >
                              {term}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}

                  {/* Show skeleton if still processing after 2s */}
                  {showSkeletons && isProcessing && retrievedDocs.length < 3 && (
                    <>
                      <DocumentSkeleton />
                      <DocumentSkeleton />
                    </>
                  )}
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OptimisticUIInterface;
