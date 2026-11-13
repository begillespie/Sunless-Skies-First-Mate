<div align="center">

<h6>⚜️ ─── ✦ 🧭 ۞ ⚓ ✦ ─── ⚜️</h6>

# 🚂 SUNLESS SKIES: FIRST MATE ENGINE 🚀
### *An Executive Officer AI Skill & Relational Telegraph Ledger for the High Wilderness*

<p>
  <img src="https://img.shields.io/badge/Engine_Core-v1.0.1-b8860b?style=for-the-badge&logo=steam" alt="Engine Core v1.0.1" />
  <img src="https://img.shields.io/badge/Data_Package-v1.1.2-2b3a42?style=for-the-badge&logo=json" alt="Data Package v1.1.2" />
  <img src="https://img.shields.io/badge/Logbook_Spec-v1.0.1-5c4033?style=for-the-badge&logo=markdown" alt="Logbook v1.0.1" />
  <img src="https://img.shields.io/badge/Frictionless_Data-Validated-2e8b57?style=for-the-badge&logo=python" alt="Frictionless Validated" />
</p>

<blockquote>
  <i>"Captains may fall to the dark, their hulls cracked upon the ice of Eleutheria or their minds unspooled by the Courtiers of the Blue Kingdom—yet the First Mate’s telegraphic records and bridge counsel endure."</i>
</blockquote>

<p>
  <a href="#-operational-mandate"><b>Operational Mandate</b></a> •
  <a href="#️-four-layer-architecture"><b>Architecture</b></a> •
  <a href="#-bridge-operations--usage"><b>Usage</b></a> •
  <a href="#-engineering-bay-environment--build"><b>Environment & Build</b></a> •
  <a href="#-deployment--telegraph-commissioning"><b>Deployment</b></a>
</p>

<h6>⚜️ ─── ✦ 🧭 ۞ ⚓ ✦ ─── ⚜️</h6>

</div>

---

## 📜 Operational Mandate

**Sunless Skies: First Mate Engine** (`sunless-skies-first-mate`) is a deterministic, out-of-game second-screen AI companion and relational state engine for Failbetter Games' Gothic-Victorian space RPG, *Sunless Skies*. 

Rather than relying on volatile conversational memory, the First Mate operates as a persistent **Executive Officer** backed by a 21-table live Google Sheet relational datastore (`Sunless_Skies_First_Mate_Engine`) governed by a strict **Frictionless Data Package** schema (`data/data_package.json`). The engine does not simulate RNG combat or hallucinate unprompted world state; it acts strictly upon explicit reports from the Captain's bridge to execute atomic inventory math, track branched quest completion graphs, calculate radial clock-face navigation trajectories, and render conditional Markdown logbooks (`src/logbook.md`).

---

## ⚙️ Four-Layer Architecture

The system is partitioned into four decoupled architectural layers governed by a 4-level semantic specification (`[Layer].[Subsystem].[Rule].[Details]` in `src/Sunless_Skies.md`):

<table>
  <thead>
    <tr>
      <th align="left">Layer</th>
      <th align="left">Subsystem Scope</th>
      <th align="left">Technical Guarantees & Invariants</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top"><b>1. Memory & Datastore</b><br><sub><code>State Continuity</code></sub></td>
      <td valign="top">21 Google Sheet tabs governed by 5 strict CRUD Permission Classes (<code>Class A</code> through <code>Class E</code>).</td>
      <td valign="top">
        • <b>Logical NULL Equivalence:</b> Logical <code>null</code> strictly equals physical empty string <code>""</code>.<br>
        • <b>Baseline Guardrail:</b> <code>fuel</code> and <code>supplies</code> rows in <code>State_Inventory</code> are permanent and never deleted at <code>0</code> quantity.<br>
        • <b>Two-Tier Circuit Breaker:</b> Halts execution and suppresses logbook rendering on datastore lock or FK/bounds violation.
      </td>
    </tr>
    <tr>
      <td valign="top"><b>2. Brain & Planning</b><br><sub><code>Kinetic FSM & Routing</code></sub></td>
      <td valign="top">Deterministic 4-state closed navigation loop and radial clock-bearing geometry.</td>
      <td valign="top">
        • <b>Kinetic Loop:</b> <code>docked</code> ➔ <code>departing</code> ➔ <code>enroute</code> ➔ <code>arriving</code> ➔ <code>docked</code>.<br>
        • <b>Departure Guards:</b> Enforces Hold Capacity, Consumable Reserves, Platform Parent Waypoints, and Transit Relay Tolls/Permits before cast-off.<br>
        • <b>Anti-Zig-Zag Geometry:</b> Computes angular displacement $\Delta\theta = \min(\vert{}c_1 - c_2\vert{}, 12 - \vert{}c_1 - c_2\vert{})$ across <code>center</code>, <code>inner</code>, <code>middle</code>, and <code>outer</code> rings.
      </td>
    </tr>
    <tr>
      <td valign="top"><b>3. Tools & Logistics</b><br><sub><code>Math & Task Graph</code></sub></td>
      <td valign="top">7-Step Atomic Transaction Pipeline, MAC accounting, and polymorphic quest graphs.</td>
      <td valign="top">
        • <b>Three Storage Loci:</b> Separates Volumetric Hold (<code>1 unit = 1 slot</code>, contraband concealed in <code>hidden_slots</code> first), Hub Bank (<code>0 slots</code>, service-gated), and Personal Locker (weightless possessions/curios).<br>
        • <b>Moving Average Cost (MAC):</b> Recalculates across <code>hold_qty + bank_qty</code> on purchase/salvage; invariant on sale or transfer.<br>
        • <b>Quest Completion Graph:</b> Supports Atomic tasks (<code>ACT-XXXX</code>), Sequential Blocking Chains, and Parallel Fan-In Checklists (<code>ACT-XXXX.YY</code>) with priority-ordered cargo earmarking.
      </td>
    </tr>
    <tr>
      <td valign="top"><b>4. Response Synthesis</b><br><sub><code>Persona & Logbook</code></sub></td>
      <td valign="top">Dynamic vitals demeanor and modal Markdown presentation.</td>
      <td valign="top">
        • <b>Modal Rendering:</b> Renders the full visual Captain's Log (<code>logbook.md</code>) <i>only</i> upon port departure (<code>departing</code> ➔ <code>enroute</code>) or explicit request; delivers taut Bridge Micro-Briefings during <code>arriving</code>, <code>docked</code>, and <code>enroute</code> turns.<br>
        • <b>Zero Meta-Leakage:</b> Translates all database operations into authentic High Wilderness terminology; caps missing telemetry queries at <b>1 question per turn</b>.
      </td>
    </tr>
  </tbody>
</table>

<details>
<summary><b>🔎 View Datastore Permission Class Topology (21 Tables)</b></summary>
<br>

| Permission Class | CRUD Rights | Lifecycle Mandate | Included Sheet Tabs |
| :---: | :---: | :--- | :--- |
| **Class A** | `-R--` | **Immutable Reference & Lookups:** Authoritative game definitions and domain enums. Zero agent mutation rights. | `Lkup_BridgeSlots`, `Lkup_LocationTypes`, `Lkup_Possessions`, `Lkup_Regions`, `Lkup_ServiceTypes`, `Lkup_TransitPermits`, `Ref_Compatibility_Contract`, `Ref_Goods`, `Ref_Locations`, `Ref_Location_Goods`, `Ref_Location_Services`, `Ref_Officers`, `Ref_TransitTolls` |
| **Class B** | `CRUD` | **Dynamic Entity State:** Active campaign collections created, updated, or deleted dynamically (with permanent `fuel`/`supplies` retention). | `State_Inventory`, `State_Officers`, `State_Navigation_Itinerary`, `State_Discovered_Locations` |
| **Class C** | `CR--` | **Append-Only Audit Logs:** Chronological navigation ledger incremented (`leg_index + 1`) on every port arrival. | `State_Navigation_History` |
| **Class D** | `CRUD` | **Lifecycle-Governed Ephemeral State:** `State_Action` retains terminal rows (`completed`, `cancelled`, `failed`) permanently; `State_Bazaar_Stock` sweeps rows where `expiration_epoch <= current_epoch` or `qty_available == 0`. | `State_Action`, `State_Bazaar_Stock` |
| **Class E** | `-RU-` | **Fixed-Row Scalar Registry:** Pre-initialized EAV singleton table (`session`, `captain`, `crew`, `locomotive`). Only `property_value` may be mutated. | `State_Scalars` |

</details>

---

## 🧭 Bridge Operations & Usage

Once the skill is active and linked to your `Sunless_Skies_First_Mate_Engine` Google Sheet, communicate with your First Mate in natural language or clipped bridge commands as you play:

### 1. Session Handshake & Lineage Continuity
* On initial connection, the First Mate silently inspects `State_Scalars`. If `first_mate_name` is unpopulated, they generate and permanently record a gritty Victorian identity that persists across all future captains.
* If `captain_name` is empty (a fresh campaign or a new heir assuming command after a fatal voyage), the First Mate will greet you on the bridge and request your name before logging turn operations.

### 2. Typical Bridge Commands
* **Arrival & Mooring (`enroute` ➔ `arriving` ➔ `docked`):**
  > *"We've sighted Port Avon at 2 o'clock. burned 2 fuel and 1 crate of supplies on the leg from New Winchester. Mooring lines secured."*
  * **Engine Action:** Advances `current_epoch` (`1 Jan 1905` base anchor), logs leg to `State_Navigation_History`, shifts `State_Navigation_Itinerary`, charts `port_avon` at clock bearing `2`, sweeps expired bazaar bargains, deducts consumables, and delivers an atmospheric port micro-briefing with active local objectives.
* **Bazaar Commerce & Hub Banking (`docked`):**
  > *"Bazaar has a bargain on 4 Bronzewood at 55 Sovereigns each. Buy all 4, stow 2 in the New Winchester bank vault, and pick up a Prospect requiring 3 Bronzewood for Magdalene's."*
  * **Engine Action:** Updates `bazaar_reset_epoch = current_epoch + 30`, computes weighted Moving Average Cost (`MAC`), splits `hold_qty` and `bank_qty`, creates `ACT-XXXX` (`action_type = 'prospect'`), and evaluates inventory readiness (`active` $\leftrightarrow$ `ready`).
* **Course Plotting & Departure (`docked` ➔ `departing` ➔ `enroute`):**
  > *"Plot a course for Magdalene's via Polmear & Plenty's, top off fuel to 6 barrels at standard price, and cast off."*
  * **Engine Action:** Runs the 4 **Departure Guards**, updates `last_location_visited_key`, renders the complete **Captain's Logbook (`logbook.md`)** with resupply badges (`🟢`/`🟡`/`🔴`) and tactical Concept of Maneuver, and transitions `navigation_state` to `enroute`.

---

## 🔧 Engineering Bay: Environment & Build

The repository includes an automated validation and packaging pipeline designed for **Ubuntu / WSL (Windows Subsystem for Linux)** and **GitHub Actions CI/CD**.

### Repository Structure

```text
Sunless_Skies_First_Mate/
├─ .github/workflows/
│  └─ skill-pipeline.yml               # CI/CD: Frictionless validation + GitHub Release packaging
├─ data/
│  ├─ data_package.json                # Authoritative Frictionless Data Package schema
│  └─ tables/                          # Seed CSVs for Class A Reference & Class E Scalar tables
│     ├─ Ref_Compatibility_Contract.csv
│     ├─ Ref_Goods.csv
│     ├─ Ref_Location_Goods.csv
│     ├─ Ref_Location_Services.csv
│     ├─ Ref_Locations.csv
│     ├─ Ref_Officers.csv
│     ├─ Ref_TransitTolls.csv
│     └─ State_Scalars.csv
├─ scripts/
│  └─ build_skill.sh                   # Validates contract versions, schemas, and packages dist/
├─ src/
│  ├─ SKILL.md                         # Agent Skill entrypoint & YAML frontmatter
│  ├─ Sunless_Skies.md                 # 4-level X.Y.Z.W system instruction specification
│  └─ logbook.md                       # Conditional Markdown Captain's Log template
├─ test/
│  ├─ State_Scalars.csv
│  ├─ test_cases.md
│  └─ test_runner.md
├─ .gitattributes                      # Enforces LF line endings across Windows/WSL
├─ .gitignore
├─ Makefile                            # Developer CLI wrapper & .venv stamp-file bootstrapper
└─ requirements-dev.txt                # Pinned Python validation dependencies (frictionless)

```

### Prerequisites (Ubuntu / WSL)

Ensure Python 3.10+ and the `venv` module are present in your WSL environment:

```bash
sudo apt-get update && sudo apt-get install -y python3 python3-venv make

```

*(No external `jq` or `zip` binaries are required; JSON validation, version extraction, and `.zip` archiving are handled natively via Python's standard `json` and `zipfile` modules).*

### Build & Validation Targets (`Makefile`)

The `Makefile` uses an idempotent stamp-file pattern (`.venv/.installed`) that automatically bootstraps a local Python virtual environment and installs `requirements-dev.txt` (`frictionless`) on first run:

| Command | Action |
| --- | --- |
| make all | Runs `validate` followed by `build` (default target). |
| make venv | Creates `.venv/` and installs `frictionless` if missing or if `requirements-dev.txt` changed. |
| make validate | Validates JSON syntax, verifies subsystem version alignment against `Ref_Compatibility_Contract.csv`, and validates all `data/tables/*.csv` against `data/data_package.json` using `.venv/bin/frictionless`. |
| make build | Runs all validation gates, normalizes `LF` line endings, stages `dist/sunless-skies-first-mate/`, and produces `dist/sunless-skies-first-mate.zip` + `.sha256` checksum. |
| make clean | Removes `dist/` build artifacts while preserving `.venv/` for fast rebuilds. |
| make clean-all | Removes both `dist/` and `.venv/`. |

### Version Compatibility Contract (`Ref_Compatibility_Contract.csv`)

Subsystem versions are governed by `data/tables/Ref_Compatibility_Contract.csv` (`current_version >= minimum_version`). Each source artifact declares its own `@subsystem` and `@version` header, which `scripts/build_skill.sh` cross-checks at build time and the AI agent verifies at runtime (Gate `1.3.1.1`).

---

## 🚀 Deployment & Telegraph Commissioning

### 1. Commissioning the Google Sheet Datastore

1. Create a Google Sheet named **`Sunless_Skies_First_Mate_Engine`** in your Google Drive.
2. Import the Class A and Class E seed CSVs from `data/tables/*.csv` as individual tabs matching their exact resource names in `data/data_package.json`.
3. Initialize the remaining Class B, C, and D tabs (`State_Action`, `State_Bazaar_Stock`, `State_Discovered_Locations`, `State_Inventory`, `State_Navigation_History`, `State_Navigation_Itinerary`, `State_Officers`) using the column headers and starter rows defined in the `"data"` arrays of `data/data_package.json`.

### 2. Packaging & Deploying the Agent Skill

To build the deployable skill package locally:

```bash
make all

```

This outputs a self-contained skill directory and archive in `dist/`:

```text
dist/
├─ sunless-skies-first-mate/
│  ├─ SKILL.md
│  └─ references/
│     ├─ Sunless_Skies.md
│     ├─ logbook.md
│     └─ data_package.json
├─ sunless-skies-first-mate.zip
└─ sunless-skies-first-mate.zip.sha256

```

### 3. Automated GitHub Releases (CI/CD)

Every push or pull request to `main` triggers `.github/workflows/skill-pipeline.yml`, running `make all` on `ubuntu-latest` and attaching the built `.zip` as a CI preview artifact. To publish an official versioned release to GitHub Releases:

```bash
git tag -a v1.0.1 -m "Release v1.0.1"
git push origin main --tags

```

---

*Respectfully submitted,*

### 🪶 ***The First Mate's Office***

*Executive Officer's Telegraph & Chart Room*