# Optimistic UI State Diagram

Visual representation of the state flow for the Optimistic UI interface.

## State Flow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     OPTIMISTIC UI STATE FLOW                     │
└─────────────────────────────────────────────────────────────────┘

    ┌──────┐
    │ IDLE │ ◄──────────────────────────────────┐
    └──┬───┘                                     │
       │                                         │
       │ SUBMIT                                  │ RESET
       ▼                                         │
    ┌─────────────────────────────────────┐     │
    │          LOADING                     │     │
    │  ┌───────────────────────────────┐  │     │
    │  │  Phase 1: OPTIMISTIC (100ms)  │  │     │
    │  │  - Add user message           │  │     │
    │  │  - Add assistant placeholder  │  │     │
    │  └───────────────────────────────┘  │     │
    │             ▼                        │     │
    │  ┌───────────────────────────────┐  │     │
    │  │  Phase 2: RETRIEVING          │  │     │
    │  │  - Load documents (400ms ea)  │  │     │
    │  │  - Show in context pane       │  │     │
    │  └───────────────────────────────┘  │     │
    │             ▼                        │     │
    │  ┌───────────────────────────────┐  │     │
    │  │  Phase 3: REASONING           │  │     │
    │  │  - Process steps (600ms ea)   │  │     │
    │  │  - Show thinking process      │  │     │
    │  └───────────────────────────────┘  │     │
    │             ▼                        │     │
    │  ┌───────────────────────────────┐  │     │
    │  │  Phase 4: RESPONDING          │  │     │
    │  │  - Stream response (30ms/wd)  │  │     │
    │  │  - Update message content     │  │     │
    │  └───────────────────────────────┘  │     │
    │                                      │     │
    │  [2-second timer triggers skeletons] │     │
    └──┬─────────────────────────────┬────┘     │
       │                             │          │
       │ SUCCESS                     │ ERROR    │
       ▼                             ▼          │
    ┌────────────┐               ┌────────┐    │
    │ DISPLAYING │               │ ERROR  │    │
    │            │               │        │    │
    │ • Results  │               │ • Show │    │
    │ • History  │               │ • Retry├────┘
    └────────────┘               └────────┘
```

## State Transitions

### 1. IDLE → LOADING

**Trigger:** User submits query

**Actions:**
```typescript
✓ Set status = 'loading'
✓ Add user message (status: 'success')
✓ Add assistant message (status: 'optimistic', content: '')
✓ Start 2-second skeleton timer
✓ Clear previous results
```

### 2. LOADING (Phase Transitions)

#### Optimistic → Retrieving (100ms)

**Automatic transition after 100ms**

**Actions:**
```typescript
✓ Set loadingPhase = 'retrieving'
✓ Begin document retrieval
```

#### Retrieving → Reasoning

**Trigger:** All documents loaded

**Actions:**
```typescript
✓ Set loadingPhase = 'reasoning'
✓ Begin reasoning step processing
```

#### Reasoning → Responding

**Trigger:** All reasoning steps complete

**Actions:**
```typescript
✓ Set loadingPhase = 'responding'
✓ Begin response streaming
```

### 3. LOADING → DISPLAYING

**Trigger:** Response complete

**Actions:**
```typescript
✓ Set status = 'displaying'
✓ Mark assistant message (status: 'success')
✓ Hide skeleton loaders
✓ Clear skeleton timer
✓ Set loadingPhase = null
```

### 4. LOADING → ERROR

**Trigger:** Error during processing

**Actions:**
```typescript
✓ Set status = 'error'
✓ Mark assistant message (status: 'error')
✓ Set error message
✓ Hide skeleton loaders
✓ Clear skeleton timer
```

### 5. ERROR → LOADING (Retry)

**Trigger:** User clicks retry

**Actions:**
```typescript
✓ Set status = 'loading'
✓ Remove failed assistant message
✓ Add new assistant message (status: 'optimistic')
✓ Increment retry count
✓ Start 2-second skeleton timer
✓ Re-process with original query
```

### 6. DISPLAYING → IDLE (Reset)

**Trigger:** User resets

**Actions:**
```typescript
✓ Clear all messages
✓ Clear reasoning steps
✓ Clear retrieved documents
✓ Reset counters
```

## Skeleton Loader Flow

```
    User submits query
         │
         ▼
    Start 2-second timer
         │
         ├─────────────────────────────────────┐
         │                                     │
         │ Response < 2 seconds                │ Response > 2 seconds
         ▼                                     ▼
    Complete normally               Show skeleton loaders
    (no skeletons)                          │
                                            ▼
                                   Real content loads progressively
                                            │
                                            ▼
                                   Replace skeletons with content
```

## Message Status Flow

```
User Message:
    ┌─────────┐
    │ success │ (always success)
    └─────────┘

Assistant Message:
    ┌────────────┐        ┌─────────┐        ┌─────────┐
    │ optimistic │───────▶│ pending │───────▶│ success │
    └────────────┘        └─────────┘        └─────────┘
           │
           │ (on error)
           ▼
       ┌───────┐
       │ error │
       └───────┘
```

## Reasoning Step Status Flow

```
    ┌─────────┐        ┌────────────┐        ┌──────────┐
    │ pending │───────▶│ processing │───────▶│ complete │
    └─────────┘        └────────────┘        └──────────┘
                              │
                              │ (on error)
                              ▼
                          ┌───────┐
                          │ error │
                          └───────┘
```

## Timeline Diagram

```
Time (ms)  │ User Action │ Loading Phase │ UI State
═══════════╪═════════════╪═══════════════╪══════════════════════════
    0      │ Submit      │ optimistic    │ User msg appears
  100      │             │ retrieving    │ Assistant msg placeholder
  500      │             │ retrieving    │ Document 1 loads
  900      │             │ retrieving    │ Document 2 loads
 1300      │             │ retrieving    │ Document 3 loads
 1500      │             │ reasoning     │ Step 1 starts
 2000      │ [SKELETON TIMER TRIGGERS]   │ Show skeleton loaders
 2100      │             │ reasoning     │ Step 1 completes
 2300      │             │ reasoning     │ Step 2 starts
 2900      │             │ reasoning     │ Step 2 completes
 3100      │             │ reasoning     │ Step 3 starts
 3700      │             │ reasoning     │ Step 3 completes
 3900      │             │ reasoning     │ Step 4 starts
 4500      │             │ reasoning     │ Step 4 completes
 4700      │             │ responding    │ Response streaming starts
 5000      │             │ responding    │ Word-by-word appears
 6000      │             │ responding    │ Response complete
 6001      │             │ [null]        │ Status: displaying
           │             │               │ Hide skeletons
```

## Error Recovery Flow

```
                    ┌─────────────────────┐
                    │  Processing fails   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Mark as ERROR     │
                    │   Show error UI     │
                    └──────────┬──────────┘
                               │
                               │ User clicks Retry
                               ▼
                    ┌─────────────────────┐
                    │ Remove failed msg   │
                    │ Add new optimistic  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Re-process query   │
                    │  (same as initial)  │
                    └─────────────────────┘
```

## Progressive Loading Pattern

```
Documents:
    [────────────────────] Empty state
    [████────────────────] Doc 1 (400ms)
    [████████────────────] Doc 2 (800ms)
    [████████████────────] Doc 3 (1200ms)
    [████████████████████] Complete

Reasoning Steps:
    [────────────────────] Empty state
    [████────────────────] Step 1 processing (600ms)
    [█████───────────────] Step 1 complete (800ms)
    [█████████───────────] Step 2 processing (1400ms)
    [██████████──────────] Step 2 complete (1600ms)
    [██████████████──────] Step 3 processing (2200ms)
    [███████████████─────] Step 3 complete (2400ms)
    [███████████████████─] Step 4 processing (3000ms)
    [████████████████████] Step 4 complete (3200ms)

Response:
    [────────────────────] Empty
    [█───────────────────] "会議費と接待費の" (10%)
    [████────────────────] "分類についてお答え" (20%)
    [███████─────────────] "します。**会議費の" (35%)
    [██████████──────────] "定義:**会議費とは、" (50%)
    [█████████████───────] "会議に関連して通常" (65%)
    [████████████████────] "必要となる飲食代等" (80%)
    [███████████████████─] "の費用です。社内外" (95%)
    [████████████████████] Complete (100%)
```

## State Guards

### Can Submit Query?

```typescript
if (status === 'loading') {
  return false; // Already processing
}
if (!query.trim()) {
  return false; // Empty query
}
return true; // Can submit
```

### Can Retry?

```typescript
if (status !== 'error') {
  return false; // Only retry from error state
}
if (retryCount >= 3) {
  return false; // Max retries exceeded
}
return true; // Can retry
```

### Should Show Skeletons?

```typescript
if (status !== 'loading') {
  return false; // Not loading
}
if (timeElapsed < 2000) {
  return false; // Less than 2 seconds
}
return true; // Show skeletons
```

## XState Visualization

For XState implementation, you can visualize the state machine at:
**https://stately.ai/viz**

Paste this configuration:

```javascript
{
  id: 'query',
  initial: 'idle',
  states: {
    idle: {
      on: { SUBMIT: 'loading' }
    },
    loading: {
      initial: 'optimistic',
      states: {
        optimistic: { after: { 100: 'retrieving' } },
        retrieving: {},
        reasoning: {},
        responding: {}
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
}
```

## Related Files

- [XState Store](./xstate-store.ts)
- [Redux Store](./redux-store.ts)
- [Zustand Store](./zustand-store.ts)
- [Usage Examples](./usage-examples.tsx)
- [State Management README](./README.md)
