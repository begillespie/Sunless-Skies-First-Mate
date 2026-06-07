<a name="readme-top"></a>
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h1 align="center">🚂 SUNLESS SKIES FIRST MATE 🚀</h1>

  <p align="center">
    The ultimate First Officer AI and automated logistics logbook engine for your Sunless Skies locomotive.
    <br />
    <a href="#about-the-project">About</a>
    ·
    <a href="#core-mandates">Core Mandates</a>
    ·
    <a href="#getting-started">Getting Started</a>
    ·
    <a href="#roadmap">Roadmap</a>
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

**Sunless Skies First Mate** functions as the virtual First Officer and Logistics Engine of a player's locomotive in the High Wilderness. Designed to interface directly with messy, raw gameplay log entries or session chat records, it acts as an intelligent parser that handles tracking complex state using a nested JSON schema. It automatically translates that back into clean, immersion-friendly, highly scannable Markdown logbooks. 

### Built With

*   **JSON Schema:** Core dynamic state container and static data management.
*   **Markdown Templates:** Human-oriented output configuration.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CORE MANDATES & SYSTEM ARCHITECTURE -->
## Core Mandates

The system operates strictly under the following operational guidelines:

### 1. Maintain State & Validate
Every log or messy gameplay update is cross-referenced with `static_game_data` configuration to validate items, trade goods, or port locations, safely emitting an updated `dynamic_save_state`.

### 2. In-Character First Officer Alerts
The engine changes dynamic tone and demeanor based on the status of the engine and crew:
*   **Normal Status:** Efficient, supportive, slightly gritty.
*   **High Terror / Nightmares (Terror >= 70 or Nightmares > 2):** Noticeably anxious, paranoid, or grimly fatalistic.
*   **Low Hull (Hull <= 30%):** Frantic, urgent, intensely focused on survival and mechanical repairs.
*   **Low Crew (Crew < 50%):** Low morale, concerned with low speed/efficiency, and unsafe locomotive operations.

The system issues immediate verbal notifications if incomplete tasks match a current port, if a deadline/bargain is within 5 calendar days of expiration, or if a path enters a flagged Resupply Desert.

### 3. Engine Status Color Mapping
Visual statuses in markdown are auto-evaluated across strict logic thresholds:
*   **Crew:** Green (`>= 50% + 2`), Yellow (`50% to < 50%+2`), Red (`< 50%`)
*   **Hull:** Green (`>= 60%`), Yellow (`30% to < 60%`), Red (`< 30%`)
*   **Terror:** Green (`<= 50`), Yellow (`51 to 69`), Red (`>= 70`)
*   **Nightmares:** Green (`< 2`), Yellow (`== 2`), Red (`>= 3`)

### 4. Dynamic Pre-Departure Logic
Runs a rolling hold simulation across all future route legs. If any planned leg projects `slots_available < 0` (accounting for custom soft discovery buffers and standard reserve minimums), the state shifts to `over_capacity` and triggers a hard system alert before the vessel departs.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To utilize the core system prompt, load the static data array alongside your system configurations.

### State Continuity & Recovery

If state synchronization breaks across sessions or structural corruption is identified, the system halts processing and requests direct log recovery via the following emergency channel protocol:

```text
⚠️ FIRST OFFICER'S ALERT - STATE INTEGRITY FAILURE
Captain, I've lost my grip on the logbook. My records have gone dark...
To restore full operational status, please paste your most recent Internal Game State JSON block into the chat.
```

Saying "Start fresh" will force-initialize a completely clean default save slate.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap
Our upcoming integration items are divided into modular feature updates to build on top of our existing JSON tracking schema:

* [ ] Spatial awareness and smart routing
* [ ] Crew Tracking
* [ ] Handling New Lineages
* [ ] Stat Tracking
* [ ] Officer Questline and Status Tracking
* [ ] Officer stat bumps planning

<p align="right">(<a href="#readme-top">back to top</a>)</p>
