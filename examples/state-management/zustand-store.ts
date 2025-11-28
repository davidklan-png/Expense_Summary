/**
 * Zustand Store - Lightweight State Management for Optimistic UI
 *
 * States: idle → loading → displaying → error → retry
 *
 * Features:
 * - Minimal boilerplate
 * - No providers needed
 * - DevTools support
 * - Middleware (persist, immer, devtools)
 */

import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

// Types
export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  status: 'optimistic' | 'pending' | 'success' | 'error';
  error?: string;
}

export interface ReasoningStep {
  id: string;
  step: number;
  title: string;
  content: string;
  status: 'pending' | 'processing' | 'complete' | 'error';
  duration?: number;
}

export interface RetrievedDocument {
  id: string;
  title: string;
  content: string;
  score: number;
  source: string;
  highlighted?: string[];
}

export type QueryStatus = 'idle' | 'loading' | 'displaying' | 'error';

export interface QueryState {
  // State
  status: QueryStatus;
  query: string;
  messages: Message[];
  reasoningSteps: ReasoningStep[];
  retrievedDocs: RetrievedDocument[];
  currentMessageId: string | null;
  error: string | null;
  retryCount: number;
  showSkeletons: boolean;
  loadingPhase: 'optimistic' | 'retrieving' | 'reasoning' | 'responding' | null;

  // Actions
  submitQuery: (query: string) => void;
  processQuery: (query: string) => Promise<void>;
  addDocument: (document: RetrievedDocument) => void;
  startReasoningStep: (step: ReasoningStep) => void;
  completeReasoningStep: (stepId: string, duration: number) => void;
  appendResponseChunk: (content: string) => void;
  markSuccess: () => void;
  markError: (error: string) => void;
  retry: () => void;
  reset: () => void;
  setLoadingPhase: (phase: 'optimistic' | 'retrieving' | 'reasoning' | 'responding') => void;
  showSkeletons: () => void;
  hideSkeletons: () => void;
}

// Initial state
const initialState = {
  status: 'idle' as QueryStatus,
  query: '',
  messages: [] as Message[],
  reasoningSteps: [] as ReasoningStep[],
  retrievedDocs: [] as RetrievedDocument[],
  currentMessageId: null as string | null,
  error: null as string | null,
  retryCount: 0,
  showSkeletons: false,
  loadingPhase: null as QueryState['loadingPhase'],
};

// Skeleton timer (outside store for side effects)
let skeletonTimer: NodeJS.Timeout | null = null;

const startSkeletonTimer = (callback: () => void) => {
  if (skeletonTimer) clearTimeout(skeletonTimer);
  skeletonTimer = setTimeout(callback, 2000);
};

const clearSkeletonTimer = () => {
  if (skeletonTimer) {
    clearTimeout(skeletonTimer);
    skeletonTimer = null;
  }
};

// Store
export const useQueryStore = create<QueryState>()(
  devtools(
    immer((set, get) => ({
      ...initialState,

      // Submit query (optimistic update)
      submitQuery: (query: string) => {
        set((state) => {
          state.status = 'loading';
          state.query = query;
          state.error = null;
          state.showSkeletons = false;
          state.loadingPhase = 'optimistic';

          // Add user message
          const userMessage: Message = {
            id: `user-${Date.now()}`,
            role: 'user',
            content: query,
            timestamp: new Date(),
            status: 'success',
          };
          state.messages.push(userMessage);

          // Add optimistic assistant message
          const assistantMessage: Message = {
            id: `assistant-${Date.now()}`,
            role: 'assistant',
            content: '',
            timestamp: new Date(),
            status: 'optimistic',
          };
          state.messages.push(assistantMessage);
          state.currentMessageId = assistantMessage.id;

          // Clear previous data
          state.reasoningSteps = [];
          state.retrievedDocs = [];
        });

        // Start skeleton timer
        startSkeletonTimer(() => {
          if (get().status === 'loading') {
            get().showSkeletons();
          }
        });

        // Process query
        get().processQuery(query);
      },

      // Process query (async)
      processQuery: async (query: string) => {
        try {
          // Simulate API delay
          await new Promise((resolve) => setTimeout(resolve, 500));

          // Phase 1: Retrieve documents
          get().setLoadingPhase('retrieving');

          const docs: RetrievedDocument[] = [
            {
              id: '1',
              title: '会議費の定義と税務処理',
              content:
                '会議費とは、会議に関連して通常必要となる飲食代等の費用をいいます。税務上、社内外を問わず、会議に際して供与される茶菓子、弁当、飲料等の費用は会議費として処理することができます。',
              score: 0.94,
              source: '国税庁通達 第9章',
              highlighted: ['会議費', '税務処理', '飲食代'],
            },
            {
              id: '2',
              title: '接待費の判定基準',
              content:
                '接待飲食費は、得意先や仕入先等、社外の者との飲食費に限られます。1人当たり5,000円以下（税抜）の飲食費については、交際費等から除外することができます。',
              score: 0.87,
              source: '法人税法施行令 第37条',
              highlighted: ['接待費', '5,000円', '判定基準'],
            },
            {
              id: '3',
              title: '出席者の記録要件',
              content:
                '会議費として処理するためには、①出席者の氏名、②会議の目的、③会議の日時、場所、④費用の金額を記録する必要があります。',
              score: 0.82,
              source: '国税庁FAQ Q&A',
              highlighted: ['出席者', '記録要件', '会議費'],
            },
          ];

          for (const doc of docs) {
            await new Promise((resolve) => setTimeout(resolve, 400));
            get().addDocument(doc);
          }

          // Phase 2: Reasoning steps
          get().setLoadingPhase('reasoning');

          const steps: ReasoningStep[] = [
            {
              id: 'step1',
              step: 1,
              title: 'クエリ分析',
              content:
                'ユーザーの質問を分析し、会議費と接待費の分類に関する質問であることを特定しました。',
              status: 'pending',
            },
            {
              id: 'step2',
              step: 2,
              title: 'コンテキスト検索',
              content:
                'ベクトルデータベースから関連する税務規定を3件取得しました（類似度スコア: 0.94, 0.87, 0.82）。',
              status: 'pending',
            },
            {
              id: 'step3',
              step: 3,
              title: '情報統合',
              content:
                '取得した文書から会議費の定義、判定基準、記録要件を抽出し、統合しています。',
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

          for (const step of steps) {
            get().startReasoningStep(step);
            await new Promise((resolve) => setTimeout(resolve, 600));

            get().completeReasoningStep(step.id, Math.random() * 1.5 + 0.5);
            await new Promise((resolve) => setTimeout(resolve, 200));
          }

          // Phase 3: Stream response
          get().setLoadingPhase('responding');

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

          const words = fullResponse.split(' ');

          for (const word of words) {
            get().appendResponseChunk(word + ' ');
            await new Promise((resolve) => setTimeout(resolve, 30));
          }

          // Mark as complete
          get().markSuccess();
        } catch (error) {
          get().markError(error instanceof Error ? error.message : 'Unknown error');
        }
      },

      // Set loading phase
      setLoadingPhase: (phase) => {
        set((state) => {
          state.loadingPhase = phase;
        });
      },

      // Add document
      addDocument: (document) => {
        set((state) => {
          state.retrievedDocs.push(document);
        });
      },

      // Start reasoning step
      startReasoningStep: (step) => {
        set((state) => {
          const existingIndex = state.reasoningSteps.findIndex((s) => s.id === step.id);

          if (existingIndex >= 0) {
            state.reasoningSteps[existingIndex] = {
              ...step,
              status: 'processing',
            };
          } else {
            state.reasoningSteps.push({
              ...step,
              status: 'processing',
            });
          }
        });
      },

      // Complete reasoning step
      completeReasoningStep: (stepId, duration) => {
        set((state) => {
          const step = state.reasoningSteps.find((s) => s.id === stepId);
          if (step) {
            step.status = 'complete';
            step.duration = duration;
          }
        });
      },

      // Append response chunk
      appendResponseChunk: (content) => {
        set((state) => {
          const message = state.messages.find((m) => m.id === state.currentMessageId);
          if (message) {
            message.content += content;
            message.status = 'pending';
          }
        });
      },

      // Mark success
      markSuccess: () => {
        clearSkeletonTimer();

        set((state) => {
          state.status = 'displaying';
          state.showSkeletons = false;
          state.loadingPhase = null;

          const message = state.messages.find((m) => m.id === state.currentMessageId);
          if (message) {
            message.status = 'success';
          }
        });
      },

      // Mark error
      markError: (error) => {
        clearSkeletonTimer();

        set((state) => {
          state.status = 'error';
          state.error = error;
          state.showSkeletons = false;
          state.loadingPhase = null;

          const message = state.messages.find((m) => m.id === state.currentMessageId);
          if (message) {
            message.status = 'error';
            message.content = 'An error occurred while processing your request.';
            message.error = error;
          }
        });
      },

      // Retry
      retry: () => {
        set((state) => {
          state.status = 'loading';
          state.error = null;
          state.retryCount += 1;
          state.showSkeletons = false;
          state.loadingPhase = 'optimistic';

          // Remove failed message
          state.messages = state.messages.filter((m) => m.id !== state.currentMessageId);

          // Add new optimistic assistant message
          const assistantMessage: Message = {
            id: `assistant-${Date.now()}`,
            role: 'assistant',
            content: '',
            timestamp: new Date(),
            status: 'optimistic',
          };
          state.messages.push(assistantMessage);
          state.currentMessageId = assistantMessage.id;

          // Clear previous data
          state.reasoningSteps = [];
          state.retrievedDocs = [];
        });

        // Start skeleton timer
        startSkeletonTimer(() => {
          if (get().status === 'loading') {
            get().showSkeletons();
          }
        });

        // Retry with original query
        get().processQuery(get().query);
      },

      // Reset
      reset: () => {
        clearSkeletonTimer();
        set(initialState);
      },

      // Skeletons
      showSkeletons: () => {
        set((state) => {
          state.showSkeletons = true;
        });
      },

      hideSkeletons: () => {
        set((state) => {
          state.showSkeletons = false;
        });
      },
    })),
    { name: 'query-store' }
  )
);

// Selectors
export const selectQueryStatus = (state: QueryState) => state.status;
export const selectMessages = (state: QueryState) => state.messages;
export const selectReasoningSteps = (state: QueryState) => state.reasoningSteps;
export const selectRetrievedDocs = (state: QueryState) => state.retrievedDocs;
export const selectShowSkeletons = (state: QueryState) => state.showSkeletons;
export const selectError = (state: QueryState) => state.error;
export const selectLoadingPhase = (state: QueryState) => state.loadingPhase;

// Computed selectors
export const selectUserMessages = (state: QueryState) =>
  state.messages.filter((m) => m.role === 'user');

export const selectAssistantMessages = (state: QueryState) =>
  state.messages.filter((m) => m.role === 'assistant');

export const selectActiveReasoningSteps = (state: QueryState) =>
  state.reasoningSteps.filter((s) => s.status === 'processing');

export const selectCompletedReasoningSteps = (state: QueryState) =>
  state.reasoningSteps.filter((s) => s.status === 'complete');

export const selectIsLoading = (state: QueryState) => state.status === 'loading';

export const selectHasError = (state: QueryState) => state.status === 'error';

// React Hooks for common patterns
export const useQueryStatus = () => useQueryStore(selectQueryStatus);
export const useMessages = () => useQueryStore(selectMessages);
export const useReasoningSteps = () => useQueryStore(selectReasoningSteps);
export const useRetrievedDocs = () => useQueryStore(selectRetrievedDocs);
export const useShowSkeletons = () => useQueryStore(selectShowSkeletons);
export const useIsLoading = () => useQueryStore(selectIsLoading);
export const useHasError = () => useQueryStore(selectHasError);

// Actions hook
export const useQueryActions = () => {
  const submitQuery = useQueryStore((state) => state.submitQuery);
  const retry = useQueryStore((state) => state.retry);
  const reset = useQueryStore((state) => state.reset);

  return { submitQuery, retry, reset };
};
