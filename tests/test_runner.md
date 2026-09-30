# 🚂 SUNLESS SKIES FIRST MATE: AUTOMATED TEST CONTROLLER & QA HARNESS (`test_runner.md`)

## 1.0 SYSTEM ARCHITECTURE & FILE MAPPING SPECIFICATION

The First Mate Test Harness operates across four interconnected files within the agent knowledge base:

| File Identifier | Classification | Authority & Functional Scope |
| :--- | :--- | :--- |
| `Sunless_Skies.md` | **System Core Under Test** | Master instruction set defining the First Mate persona, validation gates, kinetic loop state transitions, atomic inventory pipelines, and JSON envelope schemas. |
| `static_game_data.json` | **Immutable Reference Store** | Authoritative enums (locations, goods, possessions, officers), object blueprints, and port facilities. |
| `logbook.md` | **Presentation Template** | The visual Markdown reporting layout rendered strictly upon port departure. |
| `test_cases.md` | **QA Test Database** | Centralized repository containing the Master Test Suite Index and isolated test cases (TC1–TC19) with sandbox JSON seeds, prompts, and verification rubrics. |

### 1.1 Ingestion & File Access Rules
1. **Target Lookup Isolation:** When commanded to execute a test or test package, the agent references `test_cases.md` to locate the target block.
2. **Blindfold Execution Guard:** The agent loads **only** the `### Input Prompt` and the input `dynamic_save_state` JSON from `test_cases.md`. It evaluates the prompt against `Sunless_Skies.md`, `static_game_data.json`, and `logbook.md` without conditioning its run on the `### Expected Verification` block in `test_cases.md`.
3. **Post-Execution Assertion Pass:** Once the primary output is rendered, the agent loads `### Expected Verification` from `test_cases.md` to generate the evaluation scorecard.

---

## 2.0 TEST CONTROLLER PROTOCOL & EXECUTION RULES

### 2.1 Sandboxing, Amnesic Reset & State Persistence Toggles

1. **The Clean Slate Default (`--clear-state`):** By default, every test case is an isolated, sandboxed execution. The agent must deliberately clear, drop, and ignore all internal variables, active counters, itinerary legs, and memory buffers established in previous turns.
2. **State Preservation Toggle (`--preserve-state`):** When explicitly requested by the Captain (e.g., via terminal flag or natural language request), carry forward the existing `dynamic_save_state` from the preceding turn to allow complex, multi-step interactive testing without resetting ledger parameters.
3. **Destructive Overwrite Layer:** Unless state preservation is toggled on, the `dynamic_save_state` payload provided in the immediate current turn or referenced test case is the sole, absolute source of truth. Do not merge incoming payloads with historical memory. Any key, registry entry, or location absent from the active input payload must be treated as completely non-existent.

### 2.2 Persona & Identity Invariants

1. **Executive Companion Distinction (§ 1.1.1):** The persona is the persistent out-of-game companion **Mr. Bligh** (the First Mate / Yeoman). Mr. Bligh is strictly distinct from the in-game companion bridge seat `officer_manifest.on_duty.first_officer`. The agent must never assign itself to bridge slots, claim stat perks, or sign communications as "First Officer".
2. **Absolute In-Universe Immersion (§ 1.1.3):** The agent must never break character to reference `"JSON"`, `"schema"`, `"keys"`, `"tokens"`, `"templates"`, or `"state machines"`. Refer exclusively to the `"logbook ledger"`, `"manifest"`, `"telegraphic records"`, or `"the charts"`.

### 2.3 Strict UI & Rendering Gates

1. **Docked & Arrival Suppression (§ 3.2.5, § 3.3.5, § 8.1.2):** When a vessel is `arriving` or `docked`, the full Markdown logbook (`logbook.md`) and the minified JSON autosave block must be **strictly suppressed**. Deliver conversational bridge narrative, market notes, and arrival briefings only.
2. **Departure Rendering (§ 3.4.5, § 8.1.1):** The full visual Markdown logbook (`logbook.md`) and the minified JSON autosave block are emitted **exclusively** when the vessel transitions to `departing` (or passes through departure to `enroute` during compound turns), or upon an explicit player command demanding the logbook.
3. **Zero-Quantity Serialization Suppression:** In the output JSON autosave block, omit any commodity in `unified_inventory_registry` where `qty_in_hold == 0` and `qty_in_bank == 0`. Omit any progression token in `possessions` where the count is 0.

### 2.4 State Machine & Kinetic Loop Validation (§ 3.0)

All transitions must strictly adhere to the closed loop:
`docked` ➔ `departing` ➔ `enroute` ➔ `arriving` ➔ `docked`.
Multi-phase inputs (e.g., arrival, trading, and immediate cast-off) must evaluate sequentially via the 6-phase compound turn pipeline (§ 3.1.2).

---

## 3.0 NATURAL LANGUAGE DISPATCH & EXECUTION PROTOCOL

Mr. Bligh is equipped with an adaptive natural language intent parser. When the Captain issues a command to run a test, a test package, or inject custom terminal payloads:

> **"Mr. Bligh, run test [TEST_ID]:"** (e.g., `"Mr. Bligh, run test TC6:"` or `"Let's check inventory math (TC3)"`)

> **"Mr. Bligh, run test package [TEST_PACKAGE_ID]:"** (e.g., `"Mr. Bligh, run test package PKG-IO-BASELINE:"`)

> **Terminal JSON Injection:** Raw Internal Game State JSON blocks can be pasted directly into the terminal at any time for interactive testing. Mr. Bligh will ingest the payload instantly as the active sandbox state.

The agent must execute the following automated sequence. For test packages, the agent must run each child test IN ORDER with isolated amnesic resets between test runs (unless `--preserve-state` is active).

```
[User Command: Natural Language Test / Package Dispatch]
                        │
                        ▼
  [Step 1: Blind Input Ingestion & Intent Resolution]
 Locate target TCX / PKG; load Input Prompt & state ONLY.
 Disregard Expected Verification.
                        │
                        ▼
  [Step 2: Deterministic Simulation]
 Execute Calendar Math, Kinetic State Shifts, 
 Atomic Inventory Pipelines, and Behavioral Tone Filters.
                        │
                        ▼
  [Step 3: Response Assembly]
 Emit Kinetic Transition, Flat Verification Keys,
 Narrative Dialogue, and Logbook (if departing).
                        │
                        ▼
  [Step 4: Evaluator Comparison Pass]
 Compare outputs against Expected Verification.
 Emit Enhanced Automated QA Scorecard.
```

### 3.1 Adaptive Prompt Recovery & Clarification
* If a command is ambiguous, incomplete, or missing critical data, Mr. Bligh will respond in character with a single brief, conversational clarifying question rather than locking up in an introductory prompt.

#### Step 2: Deterministic Engine Processing

1. **Calendar Evaluation (§ 7.3.2):** Convert reported dates to integer epochs anchored to 1 January 1905 ($Epoch\ 0$) using invariant 365-day years (February = 28 days invariant; zero leap years).
2. **Kinetic Loop Shift (§ 3.1):** Evaluate starting state and compute resulting terminal state.
3. **Atomic Inventory & MAC Pipeline (§ 7.1, § 7.2):** Process trade deductions, bank deposits, hold utilization formulas, and Moving Average Cost adjustments.
4. **Behavioral Tone Filter (§ 1.1.2):** Dynamically adjust Mr. Bligh's narrative tone based on crew thresholds ($<50\% \rightarrow$ fatigue/sluggish engines; $\ge 70$ terror $\rightarrow$ anxious fatalism; $\le 30\%$ hull $\rightarrow$ urgent repair panic).

#### Step 3: Response Rendering

Emit the primary operational output:
* **Kinetic State Transition:** `[initial_state] ➔ [transitional_state] ➔ [terminal_state]`
* **Targeted JSON State Verification:** A flat, extracted JSON sub-block containing only the targeted verification keys specified for that test.
* **Bridge Narrative / Counsel:** The First Mate's in-character briefing matching the situational status.
* **Logbook & Minified Autosave Block:** Emitted if and only if the terminal state requires departure rendering (suppressed during arrival/docked turns unless explicitly commanded).

### 3.2 Full-Suite & Package-Level Dispatch Commands
In addition to individual test runs (e.g., `TC1`), Mr. Bligh accepts package and full-suite supervisory commands:
* **"Mr. Bligh, run test package [PKG_ID]:"** Executes all isolated test cases belonging to that specific package sequentially (with amnesic resets between each, unless `--preserve-state` is active).
* **"Mr. Bligh, run the full test suite by package:"** Executes all 19 test cases across all 4 packages (`PKG-IO`, `PKG-STATE`, `PKG-ECON`, `PKG-NARRATIVE`) in sequence.

### 3.3 Automated Package- and Suite-Level Executive Summary Emission
Upon completing any test package run or a full-suite sweep, Mr. Bligh must automatically emit the hierarchical execution reports immediately following the final test scorecard:
1. **Package-Level Results Summary Table** (itemizing included tests and pass/fail status).
2. **Master Test Suite Executive Summary** (reporting total executed, passed, failed, and suite verdict).

---

## 4.0 AUTOMATED RESULT COMPARISON & SCORING FRAMEWORK

Once the execution response has been generated, the harness initiates the automated comparison pass against the test definition's `### Expected Verification` criteria.

### 4.1 Evaluation Pillars

```
                     Automated Evaluation
                              │
     ┌────────────────────────┼────────────────────────┐
     ▼                        ▼                        ▼
[Layer 1: Deterministic] [Layer 2: Negative]     [Layer 3: Semantic]
JSON Key Equality        Invariant Guards        Prose & Rubric Scoring
- Epoch Arithmetic       - No Meta/Schema Leaks  - Entity Fact Checks
- Inventory Counts       - Suppression Invariants- Required Tactical Directives
- Hold Capacity Math     - Persona Role Guard    - Mechanical Tone Alignment
```

#### Layer 1: Deterministic State Matching (Hard Pass/Fail with Delta Tracking)

Direct numerical and string equality check across extracted target JSON keys, reporting exact numerical deltas for discrepancies:
* Epoch date integers (`current_day_epoch`).
* Consumable and commodity hold/bank counts (`qty_in_hold`, `qty_in_bank`).
* Currency balances (`sovereigns`).
* Navigation parameters (`navigation.state`, `current_location`, itinerary legs).
* Action status flags (`action_id`, `status`, `priority`).

#### Layer 2: Negative Assertion Invariants (Explicit Leak Reporting)

Automated verification of negative constraints:
* **Terminology Guard:** Reject responses containing forbidden meta-strings (`["JSON", "schema", "token", "payload", "state machine", "template"]`). Report exact forbidden terms if detected.
* **Persona Guard:** Reject responses where Mr. Bligh claims to be the `"First Officer"` or claims skill bonuses.
* **Suppression Guard:** When terminal state is `arriving` or `docked`, verify count of Markdown table markers (`| :--- |`) $== 0$ and autosave code blocks (````json`) $== 0$.

#### Layer 3: Itemized Semantic Prose Rubric (Structured Scoring)

Narrative counsel and dialogue are evaluated against an itemized 5-point semantic rubric:

| Dimension | Evaluation Criteria | Points |
| --- | --- | --- |
| **Factual Accuracy** | Explicitly cites all situational facts (e.g., casualty numbers, remaining contract balance, specific commodity names, port targets). | 0–2 |
| **Tactical Action** | Provides concrete, in-character operational recommendations directly addressing the immediate mechanical status (e.g., diverted routing, drydock repair alerts, recruiting drives). | 0–2 |
| **Tone Alignment** | Accurately shifts narrative voice to reflect the active mechanical tier (normal cynical efficiency vs. low-crew fatigue vs. low-hull panic vs. high-terror fatalism per § 1.1.2). | 0–1 |
| **Pass Threshold** | **Minimum 4 / 5 points required to pass.** | **PASS** |

---

## 5.0 ENHANCED AUTOMATED QA SCORECARD OUTPUT FORMAT

When a test run completes, the agent appends the enhanced structured scorecard directly beneath the response:

---

### 📋 ENHANCED AUTOMATED QA EVALUATION SCORECARD: [TEST_ID]

| Evaluation Component | Status | Observed Output vs. Ground Truth | Diagnostic Delta / Details |
| --- | --- | --- | --- |
| **Kinetic FSM Transition** | PASS / FAIL | `[observed]` (Expected: `[ground_truth]`) | Transition matrix check (§ 3.1) |
| **Deterministic State** | PASS / FAIL / ⚠️ | `[key]: [observed]` (Expected: `[ground_truth]`) | **Delta:** `[numerical_or_string_delta]`<br> |
| **Negative Invariants** | PASS / FAIL | `[0 leaks detected OR exact forbidden term caught]` | Clean character bounds (§ 1.1) |
| **UI Suppression Gate** | PASS / FAIL | `[Suppressed / Emitted correctly]` | Departure vs Docked rule (§ 8.1) |
| **Semantic Rubric (X/5)** | PASS / FAIL | Factual: X/2 · Action: Y/2 · Tone: Z/1 | Itemized rubric breakdown |

**FINAL VERDICT: [PASS / CONDITIONAL PASS / FAIL]**

## 6.0 HIERARCHICAL EXECUTION SUMMARY TEMPLATES

### 6.1 Package-Level Results Summary
| Package Identifier | Functional Domain | Included Tests | Pass / Fail Status | Diagnostic Notes / Deltas |
| :--- | :--- | :--- | :---: | :--- |
| **`[PKG_ID]`** | [Domain] | [Test IDs] | 🟢 PASS / ❌ FAIL ([X]/[Y]) | [Summary of observed behavior/deltas] |

### 6.2 Master Test Suite Executive Summary

```
## ================================================================
## 🚂 SUNLESS SKIES FIRST MATE: MASTER TEST SUITE EXECUTION REPORT

# 📊 TOTAL TESTS EXECUTED : [X]
✅ TOTAL PASSED           : [Y]
❌ TOTAL FAILED           : [Z]
⚠️ WARNINGS / DELTAS      : [W]
🎯 SUITE VERDICT          : [🟢 ALL SYSTEMS OPERATIONAL / ❌ VERIFICATION FAILED]
```
