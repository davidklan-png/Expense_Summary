# Optimistic UI Three-Pane Interface

A production-ready React component demonstrating optimistic UI patterns with 2-second skeleton loader fallback for AI chat applications.

## Features

- ⚡ **Optimistic UI** - Instant user feedback before server response
- ⏱️ **2-Second Skeleton Fallback** - Graceful degradation for slow responses
- 📊 **Progressive Loading** - Documents, reasoning steps, and responses load incrementally
- 🔄 **Error Recovery** - Retry failed messages with original context
- 🎨 **Smooth Animations** - Fade-in, slide-up, and pulse effects
- 💬 **Chat Interface** - Full conversation history with timestamps
- 🧠 **Reasoning Visualization** - Transparent AI thinking process
- 📚 **Context Display** - Retrieved documents with similarity scores
- 📋 **Copy to Clipboard** - Easy document content copying
- 🎯 **TypeScript** - Full type safety
- 🎨 **Design System** - Uses Saisonxform tokens

## Quick Start

### 1. Install Dependencies

```bash
npm install react react-dom lucide-react
npm install -D @types/react @types/react-dom typescript
npm install -D tailwindcss postcss autoprefixer
```

### 2. Setup Tailwind CSS

Use the included [tailwind.config.js](../tailwind.config.js):

```bash
cp tailwind.config.js my-app/tailwind.config.js
```

### 3. Import the Component

```tsx
import OptimisticUIInterface from './components/OptimisticUIInterface';

function App() {
  return <OptimisticUIInterface />;
}
```

## Architecture

### Component Structure

```
OptimisticUIInterface
├── Header (Title + Layout Toggle)
├── Three Panes (Horizontal/Vertical)
│   ├── Input Pane (Left/Top)
│   │   ├── Message List
│   │   │   ├── User Messages
│   │   │   ├── Assistant Messages
│   │   │   └── Skeleton Loader (after 2s)
│   │   └── Input Form
│   ├── Reasoning Pane (Middle)
│   │   ├── Step List
│   │   │   ├── Pending Steps
│   │   │   ├── Processing Steps (spinner)
│   │   │   ├── Complete Steps (checkmark)
│   │   │   └── Skeleton Loaders (after 2s)
│   │   └── Expandable Details
│   └── Context Pane (Right/Bottom)
│       ├── Document List
│       │   ├── Title + Source
│       │   ├── Similarity Score
│       │   ├── Content
│       │   ├── Highlighted Terms
│       │   └── Copy Button
│       └── Skeleton Loaders (after 2s)
```

## Optimistic UI Flow

### 1. User Submits Query

```typescript
handleSubmit() {
  // 1. Add user message immediately (optimistic)
  addMessage({ role: 'user', content: query, status: 'success' });

  // 2. Add placeholder assistant message (100ms delay)
  setTimeout(() => {
    addMessage({ role: 'assistant', content: '', status: 'optimistic' });
  }, 100);

  // 3. Start 2-second skeleton timer
  skeletonTimer = setTimeout(() => {
    if (isProcessing) showSkeletons = true;
  }, 2000);

  // 4. Process query
  await processQuery();
}
```

### 2. Progressive Processing

```typescript
async processQuery(query: string) {
  // Phase 1: Retrieve documents (400ms each)
  for (const doc of docs) {
    await delay(400);
    addDocument(doc);
  }

  // Phase 2: Show reasoning steps (600ms processing + 200ms complete)
  for (const step of steps) {
    step.status = 'processing';
    await delay(600);

    step.status = 'complete';
    step.duration = calculateDuration();
    await delay(200);
  }

  // Phase 3: Stream response (30ms per word)
  for (const word of words) {
    appendToMessage(word);
    await delay(30);
  }

  // Complete
  hideSkeletons();
}
```

### 3. Skeleton Fallback

If processing takes longer than 2 seconds:

```typescript
// After 2000ms
if (isProcessing) {
  // Show skeletons in all panes
  showSkeletons = true;

  // Skeletons appear while real content loads
  // Once real content arrives, skeletons disappear
}
```

## Message Status States

```typescript
type MessageStatus = 'optimistic' | 'pending' | 'success' | 'error';

'optimistic' - Just added, waiting for processing to start
'pending'    - Currently being processed (typing animation)
'success'    - Completed successfully
'error'      - Failed with error (shows retry button)
```

## Reasoning Step States

```typescript
type StepStatus = 'pending' | 'processing' | 'complete' | 'error';

'pending'    - Waiting to start (gray circle with number)
'processing' - Currently running (blue spinner)
'complete'   - Finished (green checkmark + duration)
'error'      - Failed (red X icon)
```

## Key Components

### MessageSkeleton

Animated placeholder for chat messages:

```tsx
<MessageSkeleton />
// Renders:
// ████████████  (pulse animation)
// ████████████████
// ████████
```

### ReasoningStepSkeleton

Placeholder for reasoning steps:

```tsx
<ReasoningStepSkeleton />
// Renders:
// ⚪ ████████████  (pulse animation)
//    ████
```

### DocumentSkeleton

Placeholder for retrieved documents:

```tsx
<DocumentSkeleton />
// Renders:
// ████████████  █████
// ████████████████████████████
// ████████████████████████
// ██████████████████
```

## Timer Management

### Skeleton Fallback Timer

```typescript
// Start on submit
skeletonTimerRef.current = setTimeout(() => {
  if (isProcessing) setShowSkeletons(true);
}, 2000);

// Clear on completion
if (skeletonTimerRef.current) {
  clearTimeout(skeletonTimerRef.current);
}
```

### Processing Timeout Timer

```typescript
// Optional: Set max processing time
processingTimerRef.current = setTimeout(() => {
  if (isProcessing) {
    setError('Request timed out');
    setIsProcessing(false);
  }
}, 30000); // 30 seconds
```

### Cleanup on Unmount

```typescript
useEffect(() => {
  return () => {
    if (skeletonTimerRef.current) clearTimeout(skeletonTimerRef.current);
    if (processingTimerRef.current) clearTimeout(processingTimerRef.current);
  };
}, []);
```

## Error Handling

### Display Error State

```tsx
{message.status === 'error' && (
  <>
    <AlertCircle className="w-4 h-4 text-error" />
    <span>Error</span>
    <p>{message.content}</p>
    <button onClick={() => retryMessage(message.id)}>
      <RefreshCw /> Retry
    </button>
  </>
)}
```

### Retry Logic

```typescript
const retryMessage = (messageId: string) => {
  // 1. Find failed message and previous user message
  const message = messages.find(m => m.id === messageId);
  const userMessage = messages[messageIndex - 1];

  // 2. Remove failed message
  removeMessage(messageId);

  // 3. Pre-fill input with original query
  setInputValue(userMessage.content);

  // 4. Focus input for user to resubmit
  inputRef.current?.focus();
};
```

## Progressive Loading Techniques

### 1. Document Loading (One at a Time)

```typescript
const docs = fetchDocuments();

for (let i = 0; i < docs.length; i++) {
  await delay(400); // Stagger loading
  setRetrievedDocs(prev => [...prev, docs[i]]);
}
```

### 2. Reasoning Steps (Sequential)

```typescript
for (let i = 0; i < steps.length; i++) {
  // Start processing
  steps[i].status = 'processing';
  setReasoningSteps([...steps]);
  await delay(600);

  // Mark complete
  steps[i].status = 'complete';
  steps[i].duration = Math.random() * 1.5 + 0.5;
  setReasoningSteps([...steps]);
  await delay(200);
}
```

### 3. Response Streaming (Word by Word)

```typescript
const words = response.split(' ');
let currentContent = '';

for (let i = 0; i < words.length; i++) {
  currentContent += (i > 0 ? ' ' : '') + words[i];

  updateMessage(messageId, currentContent);

  await delay(30); // 30ms per word for smooth streaming
}
```

## Animations

### CSS Classes

```css
/* Fade in animation */
.animate-fade-in {
  animation: fadeIn 0.3s ease-in;
}

/* Slide up animation */
.animate-slide-up {
  animation: slideUp 0.3s ease-out;
}

/* Pulse animation (built-in Tailwind) */
.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Spin animation (built-in Tailwind) */
.animate-spin {
  animation: spin 1s linear infinite;
}
```

### Usage

```tsx
// Fade in new messages
<div className="animate-fade-in">

// Slide up documents
<div className="animate-slide-up">

// Pulse skeleton loaders
<div className="animate-pulse">

// Spin processing indicators
<Loader2 className="animate-spin" />
```

## Integration with Backend API

Replace the simulated processing with actual API calls:

```typescript
const processQuery = async (query: string, messageId: string) => {
  try {
    // 1. Call document retrieval API
    const docs = await fetch('/api/retrieve', {
      method: 'POST',
      body: JSON.stringify({ query }),
    }).then(r => r.json());

    // Add documents progressively
    for (const doc of docs) {
      setRetrievedDocs(prev => [...prev, doc]);
      await delay(100); // Smooth UX
    }

    // 2. Call reasoning API (streaming)
    const response = await fetch('/api/reason', {
      method: 'POST',
      body: JSON.stringify({ query, documents: docs }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    // Stream reasoning steps
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const data = JSON.parse(chunk);

      if (data.type === 'step') {
        updateReasoningStep(data.step);
      } else if (data.type === 'response') {
        appendToMessage(messageId, data.content);
      }
    }

    // 3. Mark complete
    updateMessage(messageId, { status: 'success' });

  } catch (error) {
    updateMessage(messageId, {
      status: 'error',
      content: 'An error occurred',
      error: error.message,
    });
  } finally {
    setShowSkeletons(false);
  }
};
```

## Customization

### Adjust Skeleton Delay

```typescript
// Change from 2 seconds to 1 second
setTimeout(() => {
  if (isProcessing) setShowSkeletons(true);
}, 1000); // 1 second
```

### Adjust Loading Speeds

```typescript
// Faster document loading
await delay(200); // Instead of 400ms

// Slower response streaming
await delay(50); // Instead of 30ms
```

### Custom Skeleton Components

```tsx
const CustomSkeleton: React.FC = () => (
  <div className="animate-pulse space-y-3">
    <div className="h-6 bg-gradient-to-r from-neutral-200 to-neutral-300 rounded" />
    <div className="h-4 bg-gradient-to-r from-neutral-200 to-neutral-300 rounded w-3/4" />
  </div>
);
```

## Best Practices

### 1. Always Clear Timers

```typescript
useEffect(() => {
  return () => {
    // ALWAYS clear timers on unmount
    if (skeletonTimerRef.current) clearTimeout(skeletonTimerRef.current);
  };
}, []);
```

### 2. Use Status States

```typescript
// Good - Clear status tracking
message.status = 'optimistic' | 'pending' | 'success' | 'error';

// Bad - Boolean flags
isLoading = true;
hasError = false;
isOptimistic = true;
```

### 3. Progressive Enhancement

```typescript
// Good - Show content as it arrives
for (const item of items) {
  addItem(item);
  await delay(100);
}

// Bad - Wait for everything
const items = await fetchAll();
setItems(items);
```

### 4. Graceful Degradation

```typescript
// Show skeletons after delay
setTimeout(() => {
  if (isProcessing) setShowSkeletons(true);
}, 2000);

// Don't show skeletons immediately - feels janky
setShowSkeletons(true);
```

## Performance Optimizations

### 1. Memoize Components

```tsx
const MessageItem = React.memo(({ message }: { message: Message }) => {
  return <div>{message.content}</div>;
});
```

### 2. Virtualize Long Lists

```tsx
import { FixedSizeList } from 'react-window';

<FixedSizeList
  height={600}
  itemCount={messages.length}
  itemSize={80}
>
  {({ index }) => <MessageItem message={messages[index]} />}
</FixedSizeList>
```

### 3. Debounce Input

```typescript
const debouncedSubmit = useMemo(
  () => debounce(handleSubmit, 300),
  []
);
```

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Related Files

- [Three-Pane Interface](./three_pane_ai_interface.tsx) - Base implementation
- [React Layout](./react_layout.tsx) - Layout structure
- [Tailwind Config](../tailwind.config.js) - Design tokens
- [Design System](../design-system.json) - Token specification

## License

Part of the Saisonxform project.
