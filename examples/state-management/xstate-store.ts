/**
 * XState Store - State Machine for Optimistic UI
 *
 * States: idle → loading → displaying → error → retry
 *
 * Features:
 * - Type-safe state transitions
 * - Predictable state flow
 * - Time-travel debugging
 * - Visual state charts
 */

import { createMachine, interpret, assign } from 'xstate';

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

export interface QueryContext {
  query: string;
  messages: Message[];
  reasoningSteps: ReasoningStep[];
  retrievedDocs: RetrievedDocument[];
  currentMessageId: string | null;
  error: string | null;
  retryCount: number;
  showSkeletons: boolean;
}

export type QueryEvent =
  | { type: 'SUBMIT'; query: string }
  | { type: 'DOCUMENT_LOADED'; document: RetrievedDocument }
  | { type: 'STEP_STARTED'; step: ReasoningStep }
  | { type: 'STEP_COMPLETED'; stepId: string; duration: number }
  | { type: 'RESPONSE_CHUNK'; content: string }
  | { type: 'SUCCESS' }
  | { type: 'ERROR'; error: string }
  | { type: 'RETRY' }
  | { type: 'RESET' }
  | { type: 'SHOW_SKELETONS' }
  | { type: 'HIDE_SKELETONS' };

// State Machine
export const queryMachine = createMachine<QueryContext, QueryEvent>(
  {
    id: 'query',
    initial: 'idle',
    context: {
      query: '',
      messages: [],
      reasoningSteps: [],
      retrievedDocs: [],
      currentMessageId: null,
      error: null,
      retryCount: 0,
      showSkeletons: false,
    },
    states: {
      // IDLE - Waiting for user input
      idle: {
        entry: ['resetSkeletons'],
        on: {
          SUBMIT: {
            target: 'loading',
            actions: ['setQuery', 'addUserMessage', 'addOptimisticAssistantMessage'],
          },
        },
      },

      // LOADING - Processing query with optimistic UI
      loading: {
        entry: ['startSkeletonTimer'],
        exit: ['clearSkeletonTimer'],
        on: {
          SHOW_SKELETONS: {
            actions: ['showSkeletons'],
          },
          DOCUMENT_LOADED: {
            target: 'loading.retrieving',
            actions: ['addDocument'],
          },
          STEP_STARTED: {
            target: 'loading.reasoning',
            actions: ['addReasoningStep'],
          },
          RESPONSE_CHUNK: {
            target: 'loading.responding',
            actions: ['appendResponseChunk'],
          },
          SUCCESS: {
            target: 'displaying',
          },
          ERROR: {
            target: 'error',
            actions: ['setError'],
          },
        },
        initial: 'optimistic',
        states: {
          // Optimistic state - Immediately after submit
          optimistic: {
            after: {
              100: { target: 'retrieving' },
            },
          },

          // Retrieving documents from vector database
          retrieving: {
            on: {
              DOCUMENT_LOADED: {
                actions: ['addDocument'],
              },
            },
          },

          // Processing reasoning steps
          reasoning: {
            on: {
              STEP_STARTED: {
                actions: ['addReasoningStep'],
              },
              STEP_COMPLETED: {
                actions: ['completeReasoningStep'],
              },
            },
          },

          // Streaming response
          responding: {
            on: {
              RESPONSE_CHUNK: {
                actions: ['appendResponseChunk'],
              },
            },
          },
        },
      },

      // DISPLAYING - Successfully showing results
      displaying: {
        entry: ['hideSkeletons', 'markMessageSuccess'],
        on: {
          SUBMIT: {
            target: 'loading',
            actions: ['setQuery', 'addUserMessage', 'addOptimisticAssistantMessage'],
          },
          RESET: {
            target: 'idle',
            actions: ['resetContext'],
          },
        },
      },

      // ERROR - Something went wrong
      error: {
        entry: ['hideSkeletons', 'markMessageError'],
        on: {
          RETRY: {
            target: 'loading',
            actions: ['incrementRetryCount', 'removeFailedMessage'],
          },
          RESET: {
            target: 'idle',
            actions: ['resetContext'],
          },
          SUBMIT: {
            target: 'loading',
            actions: ['setQuery', 'addUserMessage', 'addOptimisticAssistantMessage'],
          },
        },
      },
    },
  },
  {
    actions: {
      // Query actions
      setQuery: assign({
        query: (context, event) => (event.type === 'SUBMIT' ? event.query : context.query),
      }),

      // Message actions
      addUserMessage: assign({
        messages: (context, event) => {
          if (event.type !== 'SUBMIT') return context.messages;

          const userMessage: Message = {
            id: `user-${Date.now()}`,
            role: 'user',
            content: event.query,
            timestamp: new Date(),
            status: 'success',
          };

          return [...context.messages, userMessage];
        },
      }),

      addOptimisticAssistantMessage: assign({
        messages: (context) => {
          const assistantMessage: Message = {
            id: `assistant-${Date.now()}`,
            role: 'assistant',
            content: '',
            timestamp: new Date(),
            status: 'optimistic',
          };

          return [...context.messages, assistantMessage];
        },
        currentMessageId: () => `assistant-${Date.now()}`,
      }),

      appendResponseChunk: assign({
        messages: (context, event) => {
          if (event.type !== 'RESPONSE_CHUNK') return context.messages;

          return context.messages.map((msg) =>
            msg.id === context.currentMessageId
              ? {
                  ...msg,
                  content: msg.content + event.content,
                  status: 'pending' as const,
                }
              : msg
          );
        },
      }),

      markMessageSuccess: assign({
        messages: (context) =>
          context.messages.map((msg) =>
            msg.id === context.currentMessageId
              ? { ...msg, status: 'success' as const }
              : msg
          ),
      }),

      markMessageError: assign({
        messages: (context) =>
          context.messages.map((msg) =>
            msg.id === context.currentMessageId
              ? {
                  ...msg,
                  status: 'error' as const,
                  content: 'An error occurred while processing your request.',
                  error: context.error || 'Unknown error',
                }
              : msg
          ),
      }),

      removeFailedMessage: assign({
        messages: (context) =>
          context.messages.filter((msg) => msg.id !== context.currentMessageId),
      }),

      // Document actions
      addDocument: assign({
        retrievedDocs: (context, event) => {
          if (event.type !== 'DOCUMENT_LOADED') return context.retrievedDocs;
          return [...context.retrievedDocs, event.document];
        },
      }),

      // Reasoning step actions
      addReasoningStep: assign({
        reasoningSteps: (context, event) => {
          if (event.type !== 'STEP_STARTED') return context.reasoningSteps;

          const step = { ...event.step, status: 'processing' as const };
          const existing = context.reasoningSteps.find((s) => s.id === step.id);

          if (existing) {
            return context.reasoningSteps.map((s) =>
              s.id === step.id ? step : s
            );
          }

          return [...context.reasoningSteps, step];
        },
      }),

      completeReasoningStep: assign({
        reasoningSteps: (context, event) => {
          if (event.type !== 'STEP_COMPLETED') return context.reasoningSteps;

          return context.reasoningSteps.map((step) =>
            step.id === event.stepId
              ? {
                  ...step,
                  status: 'complete' as const,
                  duration: event.duration,
                }
              : step
          );
        },
      }),

      // Skeleton actions
      showSkeletons: assign({
        showSkeletons: true,
      }),

      hideSkeletons: assign({
        showSkeletons: false,
      }),

      resetSkeletons: assign({
        showSkeletons: false,
      }),

      startSkeletonTimer: () => {
        // Timer will be handled by the service
      },

      clearSkeletonTimer: () => {
        // Timer will be handled by the service
      },

      // Error actions
      setError: assign({
        error: (context, event) =>
          event.type === 'ERROR' ? event.error : context.error,
      }),

      incrementRetryCount: assign({
        retryCount: (context) => context.retryCount + 1,
      }),

      // Reset actions
      resetContext: assign({
        query: '',
        messages: [],
        reasoningSteps: [],
        retrievedDocs: [],
        currentMessageId: null,
        error: null,
        retryCount: 0,
        showSkeletons: false,
      }),
    },
  }
);

// Service factory with skeleton timer
export const createQueryService = () => {
  let skeletonTimer: NodeJS.Timeout | null = null;

  const service = interpret(queryMachine)
    .onTransition((state) => {
      // Start 2-second skeleton timer when entering loading state
      if (state.matches('loading') && !skeletonTimer) {
        skeletonTimer = setTimeout(() => {
          service.send('SHOW_SKELETONS');
        }, 2000);
      }

      // Clear skeleton timer when leaving loading state
      if (!state.matches('loading') && skeletonTimer) {
        clearTimeout(skeletonTimer);
        skeletonTimer = null;
      }
    })
    .start();

  return service;
};

// Utility: Get current state name
export const getStateName = (state: any): string => {
  if (state.matches('idle')) return 'idle';
  if (state.matches('loading.optimistic')) return 'loading (optimistic)';
  if (state.matches('loading.retrieving')) return 'loading (retrieving)';
  if (state.matches('loading.reasoning')) return 'loading (reasoning)';
  if (state.matches('loading.responding')) return 'loading (responding)';
  if (state.matches('displaying')) return 'displaying';
  if (state.matches('error')) return 'error';
  return 'unknown';
};

// React Hook
export const useQueryMachine = () => {
  const [state, setState] = React.useState(queryMachine.initialState);
  const serviceRef = React.useRef<ReturnType<typeof createQueryService> | null>(null);

  React.useEffect(() => {
    serviceRef.current = createQueryService();

    const subscription = serviceRef.current.subscribe((newState) => {
      setState(newState);
    });

    return () => {
      subscription.unsubscribe();
      serviceRef.current?.stop();
    };
  }, []);

  return {
    state,
    send: (event: QueryEvent) => serviceRef.current?.send(event),
    context: state.context,
    stateName: getStateName(state),
  };
};

// Export types
export type QueryState = ReturnType<typeof queryMachine.transition>;
export type QueryService = ReturnType<typeof createQueryService>;
