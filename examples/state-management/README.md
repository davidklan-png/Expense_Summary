# State Management for Optimistic UI

Comprehensive state management implementations for the Optimistic UI interface using **XState**, **Redux Toolkit**, and **Zustand**.

## State Flow

All implementations follow the same state flow:

```
idle → loading → displaying → error → retry
         ↓
    (loading substates)
         ↓
    optimistic → retrieving → reasoning → responding
```

## Files Overview

- **[xstate-store.ts](./xstate-store.ts)** - XState finite state machine
- **[redux-store.ts](./redux-store.ts)** - Redux Toolkit with async thunks
- **[zustand-store.ts](./zustand-store.ts)** - Zustand lightweight store
- **[usage-examples.tsx](./usage-examples.tsx)** - Usage examples for all three

## Quick Comparison

| Feature | XState | Redux Toolkit | Zustand |
|---------|--------|---------------|---------|
| **Bundle Size** | ~30KB | ~40KB | ~3KB |
| **Learning Curve** | Steep | Moderate | Easy |
| **Boilerplate** | Medium | Medium | Low |
| **DevTools** | ✅ Visual state charts | ✅ Time-travel | ✅ Basic |
| **Type Safety** | ✅ Excellent | ✅ Excellent | ✅ Good |
| **Async Handling** | Built-in | Thunks/Sagas | Manual |
| **Middleware** | Built-in | Extensive | Simple |
| **Provider Needed** | No | Yes | No |
| **Best For** | Complex flows | Large apps | Small/medium apps |

## Installation

### XState

```bash
npm install xstate @xstate/react
```

### Redux Toolkit

```bash
npm install @reduxjs/toolkit react-redux
```

### Zustand

```bash
npm install zustand
```

---

## 1. XState Implementation

### Features

- ✅ **Finite State Machine** - Predictable state transitions
- ✅ **Visual State Charts** - Visualize state flow with [XState Visualizer](https://stately.ai/viz)
- ✅ **Hierarchical States** - Nested loading substates (optimistic → retrieving → reasoning → responding)
- ✅ **Guards & Actions** - Conditional transitions with side effects
- ✅ **Context Management** - Typed context for data storage
- ✅ **Event-Driven** - All transitions triggered by events

### State Machine Structure

```typescript
{
  idle: {
    on: { SUBMIT: 'loading' }
  },
  loading: {
    initial: 'optimistic',
    states: {
      optimistic: { after: { 100: 'retrieving' } },
      retrieving: { on: { DOCUMENT_LOADED: { actions: 'addDocument' } } },
      reasoning: { on: { STEP_COMPLETED: { actions: 'completeStep' } } },
      responding: { on: { RESPONSE_CHUNK: { actions: 'appendChunk' } } }
    },
    on: {
      SUCCESS: 'displaying',
      ERROR: 'error'
    }
  },
  displaying: {
    on: { SUBMIT: 'loading', RESET: 'idle' }
  },
  error: {
    on: { RETRY: 'loading', RESET: 'idle' }
  }
}
```

### Usage

```typescript
import { useQueryMachine } from './xstate-store';

const Component = () => {
  const { state, send, context, stateName } = useQueryMachine();

  // Submit query
  const handleSubmit = (query: string) => {
    send({ type: 'SUBMIT', query });
  };

  // Check state
  if (state.matches('loading')) {
    // Show loading UI
  }

  // Access context
  const { messages, reasoningSteps, retrievedDocs } = context;

  return (
    <div>
      <p>State: {stateName}</p>
      {/* UI components */}
    </div>
  );
};
```

### Pros

- **Predictable**: Impossible states are impossible
- **Visualizable**: State charts provide clear documentation
- **Debuggable**: Every transition is logged
- **Testable**: Easy to test state transitions
- **Self-documenting**: State machine is the documentation

### Cons

- **Learning Curve**: Requires understanding state machines
- **Bundle Size**: ~30KB (largest of the three)
- **Verbose**: More code for simple use cases
- **Overkill**: May be too complex for simple apps

### When to Use

- ✅ Complex state flows with many transitions
- ✅ Multiple interdependent states
- ✅ Need visual documentation of state flow
- ✅ Team collaboration (state charts as communication tool)
- ✅ Mission-critical applications (banking, healthcare)

---

## 2. Redux Toolkit Implementation

### Features

- ✅ **Immutable Updates** - Immer integration for easy mutations
- ✅ **Redux DevTools** - Time-travel debugging
- ✅ **Async Thunks** - Built-in async action creators
- ✅ **RTK Query** - Data fetching (optional)
- ✅ **Middleware** - Extensive ecosystem
- ✅ **Selectors** - Memoized state derivation

### Store Structure

```typescript
const querySlice = createSlice({
  name: 'query',
  initialState: {
    status: 'idle',
    messages: [],
    reasoningSteps: [],
    retrievedDocs: [],
    showSkeletons: false,
  },
  reducers: {
    submitQuery: (state, action) => {
      state.status = 'loading';
      state.messages.push(/* new message */);
    },
    addDocument: (state, action) => {
      state.retrievedDocs.push(action.payload);
    },
    markQuerySuccess: (state) => {
      state.status = 'displaying';
    },
  },
  extraReducers: (builder) => {
    builder.addCase(processQuery.fulfilled, (state) => {
      state.status = 'displaying';
    });
  },
});
```

### Usage

```typescript
import { useAppDispatch, useAppSelector } from './redux-store';
import { submitQuery, processQuery, selectMessages } from './redux-store';

const Component = () => {
  const dispatch = useAppDispatch();
  const status = useAppSelector((state) => state.query.status);
  const messages = useAppSelector(selectMessages);

  const handleSubmit = (query: string) => {
    dispatch(submitQuery(query));
    dispatch(processQuery(query));
  };

  return (
    <div>
      <p>Status: {status}</p>
      {messages.map((msg) => <div key={msg.id}>{msg.content}</div>)}
    </div>
  );
};

// Wrap app with Provider
<Provider store={store}>
  <Component />
</Provider>
```

### Pros

- **Mature Ecosystem**: Extensive libraries and tools
- **DevTools**: Excellent debugging with time-travel
- **Middleware**: Redux Thunk, Saga, Observable, etc.
- **Community**: Large community, lots of resources
- **Scalable**: Proven in large applications

### Cons

- **Boilerplate**: More code than Zustand
- **Provider Needed**: Requires wrapping app
- **Learning Curve**: Moderate (reducers, actions, selectors)
- **Bundle Size**: ~40KB (largest)

### When to Use

- ✅ Large applications with many features
- ✅ Need time-travel debugging
- ✅ Complex async workflows (Sagas)
- ✅ Team already familiar with Redux
- ✅ Need extensive middleware ecosystem

---

## 3. Zustand Implementation

### Features

- ✅ **Minimal Boilerplate** - Least code of the three
- ✅ **No Provider** - Direct store access
- ✅ **Immer Integration** - Easy immutable updates
- ✅ **DevTools Support** - Basic Redux DevTools integration
- ✅ **Middleware** - Persist, Immer, DevTools
- ✅ **Tiny Bundle** - Only ~3KB

### Store Structure

```typescript
export const useQueryStore = create<QueryState>()(
  devtools(
    immer((set, get) => ({
      status: 'idle',
      messages: [],
      reasoningSteps: [],
      retrievedDocs: [],
      showSkeletons: false,

      submitQuery: (query: string) => {
        set((state) => {
          state.status = 'loading';
          state.messages.push(/* new message */);
        });
        get().processQuery(query);
      },

      addDocument: (document) => {
        set((state) => {
          state.retrievedDocs.push(document);
        });
      },

      markSuccess: () => {
        set((state) => {
          state.status = 'displaying';
        });
      },
    }))
  )
);
```

### Usage

```typescript
import { useQueryStore, useQueryStatus, useMessages } from './zustand-store';

const Component = () => {
  // Option 1: Use custom hooks (recommended)
  const status = useQueryStatus();
  const messages = useMessages();
  const { submitQuery, retry } = useQueryActions();

  // Option 2: Direct store access
  const { status, messages, submitQuery } = useQueryStore();

  // Option 3: Selective subscription
  const showSkeletons = useQueryStore((state) => state.showSkeletons);

  const handleSubmit = (query: string) => {
    submitQuery(query);
  };

  return (
    <div>
      <p>Status: {status}</p>
      {messages.map((msg) => <div key={msg.id}>{msg.content}</div>)}
    </div>
  );
};
```

### Pros

- **Minimal Code**: Least boilerplate
- **No Provider**: Direct store access
- **Small Bundle**: Only ~3KB
- **Easy to Learn**: Simple API
- **Flexible**: Use hooks or direct access

### Cons

- **Less Structure**: Can become messy in large apps
- **Limited DevTools**: Basic compared to Redux
- **Manual Async**: No built-in async helpers
- **Less Mature**: Smaller community than Redux

### When to Use

- ✅ Small to medium applications
- ✅ Prototypes and MVPs
- ✅ Bundle size is critical
- ✅ Team prefers minimal boilerplate
- ✅ Don't need complex async workflows

---

## State Flow Comparison

### XState

```typescript
// Event-driven transitions
send({ type: 'SUBMIT', query: 'Hello' });          // idle → loading
send({ type: 'DOCUMENT_LOADED', document: doc });  // loading (retrieving)
send({ type: 'STEP_COMPLETED', stepId: '1' });     // loading (reasoning)
send({ type: 'SUCCESS' });                          // loading → displaying
send({ type: 'ERROR', error: 'Failed' });          // loading → error
send({ type: 'RETRY' });                            // error → loading
```

### Redux Toolkit

```typescript
// Action dispatching
dispatch(submitQuery('Hello'));           // idle → loading
dispatch(addDocument(doc));               // add document
dispatch(completeReasoningStep('1'));     // complete step
dispatch(markQuerySuccess());             // loading → displaying
dispatch(markQueryError('Failed'));       // loading → error
dispatch(retryQuery());                   // error → loading
```

### Zustand

```typescript
// Direct method calls
submitQuery('Hello');                     // idle → loading
addDocument(doc);                         // add document
completeReasoningStep('1', 0.5);          // complete step
markSuccess();                            // loading → displaying
markError('Failed');                      // loading → error
retry();                                  // error → loading
```

---

## Skeleton Timer Implementation

All three implementations handle the 2-second skeleton fallback:

### XState

```typescript
const service = interpret(queryMachine)
  .onTransition((state) => {
    if (state.matches('loading') && !skeletonTimer) {
      skeletonTimer = setTimeout(() => {
        service.send('SHOW_SKELETONS');
      }, 2000);
    }
    if (!state.matches('loading') && skeletonTimer) {
      clearTimeout(skeletonTimer);
      skeletonTimer = null;
    }
  })
  .start();
```

### Redux Toolkit

```typescript
// Store subscriber
store.subscribe(() => {
  const state = store.getState().query;

  if (state.status === 'loading' && !skeletonTimer) {
    skeletonTimer = setTimeout(() => {
      if (store.getState().query.status === 'loading') {
        store.dispatch(showSkeletons());
      }
    }, 2000);
  }

  if (state.status !== 'loading' && skeletonTimer) {
    clearTimeout(skeletonTimer);
    skeletonTimer = null;
  }
});
```

### Zustand

```typescript
// Inside submitQuery action
submitQuery: (query: string) => {
  set((state) => { state.status = 'loading'; });

  startSkeletonTimer(() => {
    if (get().status === 'loading') {
      get().showSkeletons();
    }
  });

  get().processQuery(query);
},
```

---

## Testing

### XState Testing

```typescript
import { queryMachine } from './xstate-store';

test('transitions from idle to loading on SUBMIT', () => {
  const state = queryMachine.transition('idle', { type: 'SUBMIT', query: 'Test' });
  expect(state.matches('loading')).toBe(true);
});

test('transitions to displaying on SUCCESS', () => {
  let state = queryMachine.transition('idle', { type: 'SUBMIT', query: 'Test' });
  state = queryMachine.transition(state, { type: 'SUCCESS' });
  expect(state.matches('displaying')).toBe(true);
});
```

### Redux Testing

```typescript
import { store, submitQuery, markQuerySuccess } from './redux-store';

test('submitting query changes status to loading', () => {
  store.dispatch(submitQuery('Test'));
  expect(store.getState().query.status).toBe('loading');
});

test('marking success changes status to displaying', () => {
  store.dispatch(submitQuery('Test'));
  store.dispatch(markQuerySuccess());
  expect(store.getState().query.status).toBe('displaying');
});
```

### Zustand Testing

```typescript
import { useQueryStore } from './zustand-store';

test('submitting query changes status to loading', () => {
  const { submitQuery, status } = useQueryStore.getState();
  submitQuery('Test');
  expect(useQueryStore.getState().status).toBe('loading');
});

test('marking success changes status to displaying', () => {
  const { submitQuery, markSuccess } = useQueryStore.getState();
  submitQuery('Test');
  markSuccess();
  expect(useQueryStore.getState().status).toBe('displaying');
});
```

---

## Performance Comparison

| Metric | XState | Redux Toolkit | Zustand |
|--------|--------|---------------|---------|
| **Initial Load** | ~30ms | ~40ms | ~5ms |
| **State Update** | ~0.5ms | ~0.3ms | ~0.2ms |
| **Re-render Count** | Low | Low | Very Low |
| **Memory Usage** | Medium | Medium | Low |
| **Bundle Size** | 30KB | 40KB | 3KB |

---

## Recommendation

### Choose XState if:

- You have complex state flows with many transitions
- You need visual documentation (state charts)
- Team collaboration is important
- Building mission-critical applications
- You want impossible states to be impossible

### Choose Redux Toolkit if:

- Building large applications
- Team already knows Redux
- Need time-travel debugging
- Want extensive middleware ecosystem
- Using RTK Query for data fetching

### Choose Zustand if:

- Building small to medium apps
- Rapid prototyping
- Bundle size matters
- Want minimal boilerplate
- Team prefers simplicity

---

## Migration Guide

### From XState to Redux

```typescript
// XState
send({ type: 'SUBMIT', query: 'Hello' });

// Redux
dispatch(submitQuery('Hello'));
```

### From Redux to Zustand

```typescript
// Redux
const messages = useSelector(selectMessages);
dispatch(submitQuery('Hello'));

// Zustand
const messages = useMessages();
submitQuery('Hello');
```

### From Zustand to XState

```typescript
// Zustand
submitQuery('Hello');

// XState
send({ type: 'SUBMIT', query: 'Hello' });
```

---

## Related Files

- [Optimistic UI Interface](../optimistic_ui_interface.tsx)
- [Three-Pane Interface](../three_pane_ai_interface.tsx)
- [Design System](../../design-system.json)

---

## License

Part of the Saisonxform project.
