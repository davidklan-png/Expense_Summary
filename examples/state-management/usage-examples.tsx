/**
 * State Management Usage Examples
 *
 * Demonstrates how to use XState, Redux, and Zustand stores
 * with the Optimistic UI interface
 */

import React from 'react';

// ============================================================================
// XSTATE USAGE
// ============================================================================

import { useQueryMachine } from './xstate-store';

export const XStateExample: React.FC = () => {
  const { state, send, context, stateName } = useQueryMachine();

  const handleSubmit = (query: string) => {
    send({ type: 'SUBMIT', query });
  };

  const handleRetry = () => {
    send({ type: 'RETRY' });
  };

  return (
    <div>
      <h2>XState Store</h2>
      <p>Current State: {stateName}</p>

      {/* Input Form */}
      <form onSubmit={(e) => {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        handleSubmit(formData.get('query') as string);
      }}>
        <input name="query" placeholder="Ask a question..." />
        <button type="submit" disabled={state.matches('loading')}>
          Submit
        </button>
      </form>

      {/* Messages */}
      <div>
        {context.messages.map((message) => (
          <div key={message.id}>
            <strong>{message.role}:</strong> {message.content}
            {message.status === 'error' && (
              <button onClick={handleRetry}>Retry</button>
            )}
          </div>
        ))}
      </div>

      {/* Skeletons */}
      {context.showSkeletons && <div>Loading skeletons...</div>}

      {/* Reasoning Steps */}
      <div>
        <h3>Reasoning Steps</h3>
        {context.reasoningSteps.map((step) => (
          <div key={step.id}>
            {step.step}. {step.title} - {step.status}
            {step.duration && <span> ({step.duration.toFixed(2)}s)</span>}
          </div>
        ))}
      </div>

      {/* Retrieved Documents */}
      <div>
        <h3>Retrieved Documents</h3>
        {context.retrievedDocs.map((doc) => (
          <div key={doc.id}>
            <h4>{doc.title}</h4>
            <p>{doc.content}</p>
            <span>Score: {(doc.score * 100).toFixed(0)}%</span>
          </div>
        ))}
      </div>
    </div>
  );
};

// ============================================================================
// REDUX USAGE
// ============================================================================

import { Provider } from 'react-redux';
import {
  store,
  useAppDispatch,
  useAppSelector,
  submitQuery,
  processQuery,
  retryQuery,
  selectQueryStatus,
  selectMessages,
  selectReasoningSteps,
  selectRetrievedDocs,
  selectShowSkeletons,
} from './redux-store';

const ReduxComponent: React.FC = () => {
  const dispatch = useAppDispatch();
  const status = useAppSelector(selectQueryStatus);
  const messages = useAppSelector(selectMessages);
  const reasoningSteps = useAppSelector(selectReasoningSteps);
  const retrievedDocs = useAppSelector(selectRetrievedDocs);
  const showSkeletons = useAppSelector(selectShowSkeletons);

  const handleSubmit = (query: string) => {
    dispatch(submitQuery(query));
    dispatch(processQuery(query));
  };

  const handleRetry = () => {
    dispatch(retryQuery());
    const lastQuery = messages[messages.length - 2]?.content || '';
    dispatch(processQuery(lastQuery));
  };

  return (
    <div>
      <h2>Redux Toolkit Store</h2>
      <p>Current Status: {status}</p>

      {/* Input Form */}
      <form onSubmit={(e) => {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        handleSubmit(formData.get('query') as string);
      }}>
        <input name="query" placeholder="Ask a question..." />
        <button type="submit" disabled={status === 'loading'}>
          Submit
        </button>
      </form>

      {/* Messages */}
      <div>
        {messages.map((message) => (
          <div key={message.id}>
            <strong>{message.role}:</strong> {message.content}
            {message.status === 'error' && (
              <button onClick={handleRetry}>Retry</button>
            )}
          </div>
        ))}
      </div>

      {/* Skeletons */}
      {showSkeletons && <div>Loading skeletons...</div>}

      {/* Reasoning Steps */}
      <div>
        <h3>Reasoning Steps</h3>
        {reasoningSteps.map((step) => (
          <div key={step.id}>
            {step.step}. {step.title} - {step.status}
            {step.duration && <span> ({step.duration.toFixed(2)}s)</span>}
          </div>
        ))}
      </div>

      {/* Retrieved Documents */}
      <div>
        <h3>Retrieved Documents</h3>
        {retrievedDocs.map((doc) => (
          <div key={doc.id}>
            <h4>{doc.title}</h4>
            <p>{doc.content}</p>
            <span>Score: {(doc.score * 100).toFixed(0)}%</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export const ReduxExample: React.FC = () => (
  <Provider store={store}>
    <ReduxComponent />
  </Provider>
);

// ============================================================================
// ZUSTAND USAGE
// ============================================================================

import {
  useQueryStore,
  useQueryStatus,
  useMessages,
  useReasoningSteps,
  useRetrievedDocs,
  useShowSkeletons,
  useQueryActions,
} from './zustand-store';

export const ZustandExample: React.FC = () => {
  const status = useQueryStatus();
  const messages = useMessages();
  const reasoningSteps = useReasoningSteps();
  const retrievedDocs = useRetrievedDocs();
  const showSkeletons = useShowSkeletons();
  const { submitQuery, retry } = useQueryActions();

  const handleSubmit = (query: string) => {
    submitQuery(query);
  };

  return (
    <div>
      <h2>Zustand Store</h2>
      <p>Current Status: {status}</p>

      {/* Input Form */}
      <form onSubmit={(e) => {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        handleSubmit(formData.get('query') as string);
      }}>
        <input name="query" placeholder="Ask a question..." />
        <button type="submit" disabled={status === 'loading'}>
          Submit
        </button>
      </form>

      {/* Messages */}
      <div>
        {messages.map((message) => (
          <div key={message.id}>
            <strong>{message.role}:</strong> {message.content}
            {message.status === 'error' && (
              <button onClick={retry}>Retry</button>
            )}
          </div>
        ))}
      </div>

      {/* Skeletons */}
      {showSkeletons && <div>Loading skeletons...</div>}

      {/* Reasoning Steps */}
      <div>
        <h3>Reasoning Steps</h3>
        {reasoningSteps.map((step) => (
          <div key={step.id}>
            {step.step}. {step.title} - {step.status}
            {step.duration && <span> ({step.duration.toFixed(2)}s)</span>}
          </div>
        ))}
      </div>

      {/* Retrieved Documents */}
      <div>
        <h3>Retrieved Documents</h3>
        {retrievedDocs.map((doc) => (
          <div key={doc.id}>
            <h4>{doc.title}</h4>
            <p>{doc.content}</p>
            <span>Score: {(doc.score * 100).toFixed(0)}%</span>
          </div>
        ))}
      </div>
    </div>
  );
};

// ============================================================================
// ZUSTAND - DIRECT STORE ACCESS (Advanced)
// ============================================================================

export const ZustandDirectExample: React.FC = () => {
  // Access entire store (causes re-render on any state change)
  const { status, messages, submitQuery, retry } = useQueryStore();

  // Or use selectors for granular updates
  const showSkeletons = useQueryStore((state) => state.showSkeletons);
  const loadingPhase = useQueryStore((state) => state.loadingPhase);

  return (
    <div>
      <h2>Zustand (Direct Access)</h2>
      <p>Status: {status}</p>
      <p>Loading Phase: {loadingPhase}</p>
      <p>Show Skeletons: {showSkeletons ? 'Yes' : 'No'}</p>

      <button onClick={() => submitQuery('Test query')}>
        Submit Query
      </button>

      {messages.map((msg) => (
        <div key={msg.id}>{msg.content}</div>
      ))}
    </div>
  );
};

// ============================================================================
// COMPARISON DEMO
// ============================================================================

export const ComparisonDemo: React.FC = () => {
  const [activeLibrary, setActiveLibrary] = React.useState<'xstate' | 'redux' | 'zustand'>('zustand');

  return (
    <div>
      <h1>State Management Comparison</h1>

      {/* Tabs */}
      <div>
        <button onClick={() => setActiveLibrary('xstate')}>XState</button>
        <button onClick={() => setActiveLibrary('redux')}>Redux</button>
        <button onClick={() => setActiveLibrary('zustand')}>Zustand</button>
      </div>

      {/* Active Library */}
      {activeLibrary === 'xstate' && <XStateExample />}
      {activeLibrary === 'redux' && <ReduxExample />}
      {activeLibrary === 'zustand' && <ZustandExample />}
    </div>
  );
};

// ============================================================================
// TESTING HELPERS
// ============================================================================

// XState Testing
export const testXStateMachine = () => {
  const { state, send } = useQueryMachine();

  // Test state transitions
  console.log('Initial:', state.value); // 'idle'

  send({ type: 'SUBMIT', query: 'Test query' });
  console.log('After submit:', state.value); // 'loading'

  send({ type: 'SUCCESS' });
  console.log('After success:', state.value); // 'displaying'

  send({ type: 'ERROR', error: 'Test error' });
  console.log('After error:', state.value); // 'error'

  send({ type: 'RETRY' });
  console.log('After retry:', state.value); // 'loading'
};

// Redux Testing
export const testReduxStore = () => {
  const { getState, dispatch } = store;

  console.log('Initial:', getState().query.status); // 'idle'

  dispatch(submitQuery('Test query'));
  console.log('After submit:', getState().query.status); // 'loading'

  dispatch(markQuerySuccess());
  console.log('After success:', getState().query.status); // 'displaying'
};

// Zustand Testing
export const testZustandStore = () => {
  const store = useQueryStore.getState();

  console.log('Initial:', store.status); // 'idle'

  store.submitQuery('Test query');
  console.log('After submit:', store.status); // 'loading'

  store.markSuccess();
  console.log('After success:', store.status); // 'displaying'
};
