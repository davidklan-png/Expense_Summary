/**
 * Redux Toolkit Store - Optimistic UI State Management
 *
 * States: idle → loading → displaying → error → retry
 *
 * Features:
 * - Immutable state updates
 * - Redux DevTools support
 * - Time-travel debugging
 * - Middleware support (thunks, sagas)
 */

import { createSlice, configureStore, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

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
}

// Initial State
const initialState: QueryState = {
  status: 'idle',
  query: '',
  messages: [],
  reasoningSteps: [],
  retrievedDocs: [],
  currentMessageId: null,
  error: null,
  retryCount: 0,
  showSkeletons: false,
  loadingPhase: null,
};

// Async Thunk - Process Query
export const processQuery = createAsyncThunk<
  void,
  string,
  { state: { query: QueryState } }
>(
  'query/processQuery',
  async (queryText, { dispatch, rejectWithValue }) => {
    try {
      // Simulate API delay
      await new Promise((resolve) => setTimeout(resolve, 500));

      // Phase 1: Retrieve documents
      dispatch(setLoadingPhase('retrieving'));

      const docs: RetrievedDocument[] = [
        {
          id: '1',
          title: '会議費の定義と税務処理',
          content: '会議費とは、会議に関連して通常必要となる飲食代等の費用をいいます。',
          score: 0.94,
          source: '国税庁通達 第9章',
          highlighted: ['会議費', '税務処理'],
        },
        {
          id: '2',
          title: '接待費の判定基準',
          content: '接待飲食費は、得意先や仕入先等、社外の者との飲食費に限られます。',
          score: 0.87,
          source: '法人税法施行令 第37条',
          highlighted: ['接待費', '判定基準'],
        },
        {
          id: '3',
          title: '出席者の記録要件',
          content: '会議費として処理するためには、出席者の氏名等を記録する必要があります。',
          score: 0.82,
          source: '国税庁FAQ Q&A',
          highlighted: ['出席者', '記録要件'],
        },
      ];

      for (const doc of docs) {
        await new Promise((resolve) => setTimeout(resolve, 400));
        dispatch(addDocument(doc));
      }

      // Phase 2: Reasoning steps
      dispatch(setLoadingPhase('reasoning'));

      const steps: ReasoningStep[] = [
        {
          id: 'step1',
          step: 1,
          title: 'クエリ分析',
          content: 'ユーザーの質問を分析しています。',
          status: 'pending',
        },
        {
          id: 'step2',
          step: 2,
          title: 'コンテキスト検索',
          content: 'ベクトルデータベースから関連文書を検索しています。',
          status: 'pending',
        },
        {
          id: 'step3',
          step: 3,
          title: '情報統合',
          content: '取得した情報を統合しています。',
          status: 'pending',
        },
        {
          id: 'step4',
          step: 4,
          title: '回答生成',
          content: '最終的な回答を生成しています。',
          status: 'pending',
        },
      ];

      for (const step of steps) {
        dispatch(startReasoningStep(step));
        await new Promise((resolve) => setTimeout(resolve, 600));

        dispatch(
          completeReasoningStep({
            stepId: step.id,
            duration: Math.random() * 1.5 + 0.5,
          })
        );
        await new Promise((resolve) => setTimeout(resolve, 200));
      }

      // Phase 3: Stream response
      dispatch(setLoadingPhase('responding'));

      const response = `会議費と接待費の分類についてお答えします。

**会議費の定義:**
会議費とは、会議に関連して通常必要となる飲食代等の費用です。

**接待費との違い:**
接待飲食費は、得意先や仕入先等、社外の者との飲食費に限られます。

**必要な記録:**
会議費として処理するためには、出席者の氏名、会議の目的等を記録する必要があります。`;

      const words = response.split(' ');

      for (const word of words) {
        dispatch(appendResponseChunk(word + ' '));
        await new Promise((resolve) => setTimeout(resolve, 30));
      }

      // Mark as complete
      dispatch(markQuerySuccess());
    } catch (error) {
      return rejectWithValue(
        error instanceof Error ? error.message : 'Unknown error'
      );
    }
  }
);

// Slice
const querySlice = createSlice({
  name: 'query',
  initialState,
  reducers: {
    // Submit query
    submitQuery: (state, action: PayloadAction<string>) => {
      state.status = 'loading';
      state.query = action.payload;
      state.error = null;
      state.showSkeletons = false;
      state.loadingPhase = 'optimistic';

      // Add user message
      const userMessage: Message = {
        id: `user-${Date.now()}`,
        role: 'user',
        content: action.payload,
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
    },

    // Loading phase
    setLoadingPhase: (
      state,
      action: PayloadAction<'optimistic' | 'retrieving' | 'reasoning' | 'responding'>
    ) => {
      state.loadingPhase = action.payload;
    },

    // Documents
    addDocument: (state, action: PayloadAction<RetrievedDocument>) => {
      state.retrievedDocs.push(action.payload);
    },

    // Reasoning steps
    startReasoningStep: (state, action: PayloadAction<ReasoningStep>) => {
      const existingIndex = state.reasoningSteps.findIndex(
        (s) => s.id === action.payload.id
      );

      if (existingIndex >= 0) {
        state.reasoningSteps[existingIndex] = {
          ...action.payload,
          status: 'processing',
        };
      } else {
        state.reasoningSteps.push({
          ...action.payload,
          status: 'processing',
        });
      }
    },

    completeReasoningStep: (
      state,
      action: PayloadAction<{ stepId: string; duration: number }>
    ) => {
      const step = state.reasoningSteps.find((s) => s.id === action.payload.stepId);
      if (step) {
        step.status = 'complete';
        step.duration = action.payload.duration;
      }
    },

    // Response streaming
    appendResponseChunk: (state, action: PayloadAction<string>) => {
      const message = state.messages.find((m) => m.id === state.currentMessageId);
      if (message) {
        message.content += action.payload;
        message.status = 'pending';
      }
    },

    // Success
    markQuerySuccess: (state) => {
      state.status = 'displaying';
      state.showSkeletons = false;
      state.loadingPhase = null;

      const message = state.messages.find((m) => m.id === state.currentMessageId);
      if (message) {
        message.status = 'success';
      }
    },

    // Error
    markQueryError: (state, action: PayloadAction<string>) => {
      state.status = 'error';
      state.error = action.payload;
      state.showSkeletons = false;
      state.loadingPhase = null;

      const message = state.messages.find((m) => m.id === state.currentMessageId);
      if (message) {
        message.status = 'error';
        message.content = 'An error occurred while processing your request.';
        message.error = action.payload;
      }
    },

    // Retry
    retryQuery: (state) => {
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
    },

    // Skeletons
    showSkeletons: (state) => {
      state.showSkeletons = true;
    },

    hideSkeletons: (state) => {
      state.showSkeletons = false;
    },

    // Reset
    resetQuery: () => initialState,
  },

  extraReducers: (builder) => {
    builder
      .addCase(processQuery.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(processQuery.fulfilled, (state) => {
        state.status = 'displaying';
      })
      .addCase(processQuery.rejected, (state, action) => {
        state.status = 'error';
        state.error = action.payload as string;
      });
  },
});

// Actions
export const {
  submitQuery,
  setLoadingPhase,
  addDocument,
  startReasoningStep,
  completeReasoningStep,
  appendResponseChunk,
  markQuerySuccess,
  markQueryError,
  retryQuery,
  showSkeletons,
  hideSkeletons,
  resetQuery,
} = querySlice.actions;

// Store
export const store = configureStore({
  reducer: {
    query: querySlice.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        // Ignore timestamp fields
        ignoredActions: ['query/submitQuery'],
        ignoredPaths: ['query.messages', 'query.reasoningSteps'],
      },
    }),
});

// Middleware for 2-second skeleton timer
let skeletonTimer: NodeJS.Timeout | null = null;

store.subscribe(() => {
  const state = store.getState().query;

  // Start timer when entering loading state
  if (state.status === 'loading' && !skeletonTimer) {
    skeletonTimer = setTimeout(() => {
      if (store.getState().query.status === 'loading') {
        store.dispatch(showSkeletons());
      }
    }, 2000);
  }

  // Clear timer when leaving loading state
  if (state.status !== 'loading' && skeletonTimer) {
    clearTimeout(skeletonTimer);
    skeletonTimer = null;
  }
});

// Types
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// React Hooks
import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux';

export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;

// Selectors
export const selectQueryStatus = (state: RootState) => state.query.status;
export const selectMessages = (state: RootState) => state.query.messages;
export const selectReasoningSteps = (state: RootState) => state.query.reasoningSteps;
export const selectRetrievedDocs = (state: RootState) => state.query.retrievedDocs;
export const selectShowSkeletons = (state: RootState) => state.query.showSkeletons;
export const selectError = (state: RootState) => state.query.error;
export const selectLoadingPhase = (state: RootState) => state.query.loadingPhase;

// Memoized selectors
import { createSelector } from '@reduxjs/toolkit';

export const selectUserMessages = createSelector([selectMessages], (messages) =>
  messages.filter((m) => m.role === 'user')
);

export const selectAssistantMessages = createSelector([selectMessages], (messages) =>
  messages.filter((m) => m.role === 'assistant')
);

export const selectActiveReasoningSteps = createSelector(
  [selectReasoningSteps],
  (steps) => steps.filter((s) => s.status === 'processing')
);

export const selectCompletedReasoningSteps = createSelector(
  [selectReasoningSteps],
  (steps) => steps.filter((s) => s.status === 'complete')
);

export const selectIsLoading = createSelector(
  [selectQueryStatus],
  (status) => status === 'loading'
);

export const selectHasError = createSelector(
  [selectQueryStatus],
  (status) => status === 'error'
);
