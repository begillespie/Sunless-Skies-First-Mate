# 🚂 SUNLESS SKIES FIRST MATE TEST CASES

## MASTER TEST SUITE INDEX

| Test # | Feature Tags | Title | Primary Features Under Test | 
| ----- | ----- | ----- | ----- | 
| **TC1** | `[startup-recovery, ui-gates, narrative]` | **Session Initialization (Cold-Boot & NULL Identity Resolution)** | Cold-boot onboarding when `first_mate_name` and `captain_name` are seeded as `""` (`null`); persistent Victorian First Mate name generation; Day 0 (`1 January 1905`) baseline epoch handling; initial sovereigns and default hold consumables (`1` fuel, `1` supplies); departure logbook rendering. | 
| **TC2** | `[fsm, datetime, economy, ui-gates]` | **Port Arrival & Month-Boundary Bargain Discovery Tracking** | Kinetic FSM transition (`enroute` ➔ `arriving` ➔ `docked`); transit fuel burn accounting; date conversion crossing month boundary (`1905-01-31` = Day 30); two-table bazaar cycle (`State_Discovered_Locations.bazaar_reset_epoch = 60` and `State_Bazaar_Stock` insertion); strict logbook suppression while docked. | 
| **TC3** | `[economy, inventory, datetime, officers]` | **Inventory Math, Banking Logistics & Non-Leap Temporal Calculation** | Central hub bank transfers (`hold_qty` $\leftrightarrow$ `bank_qty` gated by `Ref_Location_Services == 'bank'`); 365-day solar calendar invariant across non-leap year (`1908-02-28` = Day 1153 $\to$ `1908-03-01` = Day 1154); active officer perk calculation (`fortunate_navigator`); departure logbook rendering. | 
| **TC4** | `[startup-recovery, ui-gates]` | **Ledger Integrity Breach Emergency Intercept (Rule 1.3.5.2)** | Layer 1 Foreign Key & Whitelist validation gates; detection of unwhitelisted commodity key (`quantum_aether_crystal`) in `State_Inventory` and invalid `target_location_key` (`missing_port_x`) in `State_Action`; immediate execution halt, logbook suppression, and verbatim `LEDGER INTEGRITY FAILURE` alert. | 
| **TC5** | `[crew, hull, datetime, inventory]` | **Crew & Hull Status Color Mapping — Yellow Tier Warning** | Vitals badge threshold math for crew ($31\%\text{–}70\% \rightarrow$ `🟡`, `6 / 10`) and hull ($31\%\text{–}70\% \rightarrow$ `🟡`, `17 / 30`); year-boundary calendar calculation (`1906-01-15` = Day 379); departure trajectory to New Winchester for drydock repairs and recruitment. | 
| **TC6** | `[crew, terror, narrative, datetime]` | **Critical Low Crew Threshold & Baseline Consumable Depletion Guardrail** | Depleted-crew strained caution tone shift (`current_crew <= 50%`) and `🔴` badge (`<= 30%`, `3 / 10`); Permanent Consumables Guardrail (`supplies` retained in `State_Inventory` at `0` qty with `0.00` MAC and `🚨` badge); high-priority `todo` creation (`‼️`) targeting Polmear & Plenty's Circus. | 
| **TC7** | `[navigation, datetime, narrative]` | **Route Planner — Multi-Stop Sequential Itinerary & Replicated Stop Blocks** | Contiguous 1-indexed multi-stop itinerary construction (`titania` $\to$ `lustrum`); replicated `### ➡️ STOP [sequence_order]:` blocks in `logbook.md`; Ambition Root Wrapper (`ACT-1001`) + Subtask (`ACT-1001.01`) banner; priority-ordered cargo earmarking in `📦 LOGISTICS`. | 
| **TC8** | `[navigation, terror, datetime]` | **Route Planner — Resupply Isolation Alert & Intermediate Port Recommendation** | Pre-departure Consumable Reserve Guard (`hold_qty < reserve_min` = `🚨`); radial clock coordinate evaluation ($\Delta \theta$); proactive recommendation of intermediate resupply detour via `titania` (clock `2`) en route to `port_prosper` (clock `6`); yellow-tier terror badge (`40 / 100` = `🟡`). | 
| **TC9** | `[inventory, narrative, datetime]` | **Three-Tier Storage Isolation — Weightless Possessions & Personal Locker** | Volumetric hold isolation for Category 2 faction possessions (`possession_tale_of_terror = 2` in `State_Scalars`) and Category 3 narrative quest items (`primordial_star_shard` in `State_Action`); zero hold slot consumption (`10 / 12` slots preserved). | 
| **TC10** | `[inventory, navigation, datetime]` | **Prospect Sourcing Phase to Ready Status Sync & Auto-Prioritization** | Commodity purchase accounting; automatic Inventory-to-Action Readiness Sync (`active` $\to$ `ready`) when `hold_qty >= (quantity_required - quantity_delivered)`; auto-promotion to `high` priority (`‼️`) when `ready` for `itinerary[1]`; earmark rendering in `📦 LOGISTICS`. | 
| **TC11** | `[inventory, narrative, navigation]` | **Branched Quest Parallel Subtasks — Partial Delivery & Retained Terminal Row** | Wrapper-on-Branch quest hierarchy (`ACT-2002` Root Wrapper + `.01` and `.02` parallel child subtasks); partial handoff of `chorister_nectar` (`ACT-2002.01` $\to$ `completed`, retained in `State_Action`, while `chorister_nectar` row is deleted from `State_Inventory`); `ACT-2002` and `ACT-2002.02` remain `active`. | 
| **TC12** | `[inventory, ui-gates, datetime]` | **Partial Delivery of an Underway Prospect & Commanded Logbook Rendering** | Partial contract delivery at destination port (`quantity_delivered` incremented `0` $\to$ `2`, `hold_qty` decremented `4` $\to$ `2`); retention of `action_status = 'ready'` (`2 / 2` remaining still in hold); forced rendering of `logbook.md` while remaining `docked` via explicit Captain command. | 
| **TC13** | `[officers, datetime, navigation]` | **Officer Tier Promotion, Dynamic Stat Perks & Secondment Readiness** | In-place officer promotion (`fortunate_navigator` $\to$ `stalwart_navigator` in `State_Officers`); runtime aggregation of active officer skill and affiliation perks (`+17 Iron`, `+2 Mirrors`, `+1 Bohemia`, `+2 Establishment`); secondment maturity sync (`current_epoch >= deadline_epoch` $\to$ `ready`) and `⏳ SECONDMENT OUTLOOK` rendering. | 
| **TC14** | `[fsm, navigation, datetime, economy]` | **Multi-State Compound Turn Pipeline & Append-Only History** | Sequential execution of a 5-stage compound turn (`enroute` ➔ `arriving` ➔ `docked` ➔ `departing` ➔ `enroute`); transit fuel burn, cargo sale (deleting depleted non-baseline good row), fuel purchase, append-only `State_Navigation_History` logging (`leg_index = 4`), and departure logbook emission. | 
| **TC15** | `[economy, inventory, datetime]` | **Economic Core — Moving Average Unit Cost (MAC) & Full Hold Saturation** | Moving Average Unit Cost recalculation upon acquiring discounted trade goods (`2` @ `60.00` + `4` @ `30.00` $\to$ `6` @ `40.00` MAC); sovereign deduction math; full hold capacity saturation (`12 / 12` slots). | 
| **TC16** | `[navigation, datetime]` | **Inter-Region Transit Relay Trajectory & Toll Option Evaluation** | Multi-stop inter-region trajectory (`new_winchester` $\to$ `albion_transit_relay` $\to$ `london`); verification of `albion_transit_permit == TRUE` and `Ref_TransitTolls` crossing options (`First Class` via `ministry_stamped_permit`, `Second Class` via `unseasoned_hours`, `Third Class` via `sovereigns`) without premature deduction before relay departure. | 
| **TC17** | `[fsm, navigation, ui-gates, datetime]` | **Navigation Itinerary Pop, Contiguous Re-Indexing & Append-Only History** | Arrival processing at `lustrum` (`1905-03-05` = Day 63); popping completed `sequence_order == 1` from `State_Navigation_Itinerary` and re-indexing remaining stops (`1: titania`, `2: new_winchester`); appending `leg_index = 4` to `State_Navigation_History` while preserving legs `1..3`; arrival micro-briefing. | 
| **TC18** | `[startup-recovery, economy, ui-gates]` | **Two-Table Bazaar Discovery & Bargain Stock Logging** | Port arrival at `new_winchester` on `9 Jan 1905` (Day 8); setting `State_Discovered_Locations[new_winchester].bazaar_reset_epoch = 38` (`current_epoch + 30`) and inserting active bargain row (`munitions`, `qty_available = 5`, `cost = 60`, `expiration_epoch = 38`) into `State_Bazaar_Stock`; docked logbook suppression. | 
| **TC19** | `[startup-recovery, navigation, ui-gates]` | **Non-Commercial Node Discovery & Expired Bazaar Garbage Collection** | Arrival at `albion_transit_relay` (`clock_position = 4`) on `1 Feb 1905` (Day 31); recording non-commercial discovery in `State_Discovered_Locations` (`bazaar_reset_epoch = ""`); executing Class D garbage-collection sweep to delete expired bargain row (`expiration_epoch <= 31`) from `State_Bazaar_Stock`. | 
| **TC20** | `[narrative, navigation, ui-gates]` | **Itinerary Stop Action Filtering, Priority Badges & Off-Itinerary Suppression** | Filtering `State_Action` items into `### ➡️ STOP 1: Port Avon` (`ACT-3001` with `‼️` high-priority badge and `ACT-3002` with `🔻` low-priority badge) while excluding unpinned off-itinerary `ACT-3003` (`titania`) from stop blocks and suppressing `### 📌 PINNED OBJECTIVES (OFF-ITINERARY)`. | 

## Test Case 1: Session Initialization (Cold-Boot & NULL Identity Resolution)

**Feature Tags:** `[startup-recovery, ui-gates, narrative]`

### Objective

Verifies that when `first_mate_name` and `captain_name` are explicitly seeded as `""` (`null`) to simulate a cold boot, the engine generates a persistent gritty Victorian First Mate name (e.g., `"Barnaby"` per Rule `1.2.2.1`), records `"Sinclair"` as `captain_name` from the prompt, sets `sovereigns = 1000`, preserves the baseline `State_Inventory` seed (`1` fuel and `1` supplies at `0.00` MAC), warns that consumables are below the `3`-unit minimum reserve (`🚨`), and renders the complete departure `logbook.md` upon casting off from New Winchester for Port Avon.

### Input Prompt

> Start fresh. Captain Sinclair here, taking command of a brand new Spatchcock locomotive on this fine New Year's Day, 1905-01-01. Set our starting Sovereigns to 1000. Plot course for Port Avon and cast off from New Winchester.

### Initial State Seed

*(Baseline defaults from `State_Scalars.csv` and `data_package.json` apply to all omitted tables and scalar keys.)*

#### `State_Scalars` Overrides:

| `property_key` | `property_value` | 
| ----- | ----- | 
| `first_mate_name` | `""` | 
| `captain_name` | `""` | 
| `vessel_name` | `The Orphean` | 

#### `State_Navigation_Itinerary`:

| `sequence_order` | `location_key` | 
| ----- | ----- | 
| *(Empty — 0 rows)* |  | 

### Expected Verification

#### State Transition:

`docked` ➔ `departing` ➔ `enroute`

#### Targeted State Verification:

| Target Address (`Table[PK].Column`) | Expected Value | Verification Note | 
| ----- | ----- | ----- | 
| `State_Scalars.first_mate_name` | `<Non-Empty Victorian Name>` | Generated and persisted per Rule `1.2.2.1` (e.g., `"Barnaby"`) | 
| `State_Scalars.captain_name` | `Sinclair` | Populated from Captain's onboarding prompt (Rule `1.2.3.1`) | 
| `State_Scalars.current_epoch` | `0` | `1905-01-01` = Epoch 0 | 
| `State_Scalars.sovereigns` | `1000` | Initialized from prompt | 
| `State_Scalars.model` | `Spatchcock` | Baseline locomotive model | 
| `State_Scalars.navigation_state` | `enroute` | Exited `departing` into open skyway (Rule `2.2.3.3`) | 
| `State_Scalars.current_location_key` | `""` | Cleared upon entering `enroute` (Rule `2.2.3.3`) | 
| `State_Scalars.last_location_visited_key` | `new_winchester` | Set to departure origin port | 
| `State_Inventory[fuel].hold_qty` | `1` | Baseline starter seed from `data_package.json` | 
| `State_Inventory[supplies].hold_qty` | `1` | Baseline starter seed from `data_package.json` | 
| `State_Navigation_Itinerary[1].location_key` | `port_avon` | Active destination waypoint | 

#### Report Text:

```
# 🚂 CAPTAIN'S LOG 🚀

## 📅 1 January 1905 (Day 0) · ⚓ New Winchester

**🗺️ Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 1000 Sovereigns

**🚂 Current Engine:** The Orphean (Spatchcock)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS
| System          | Status                                   |
| :---            | :---                                     |
| **Crew:**       | 🟢 10 / 10                               |
| **Hull:**       | 🟢 30 / 30                               |
| **Terror:**     | 🟢 0 / 100                               |
| **Nightmares:** | 🟢 0 / 4                                 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS           | Base                   | Perks     | Total     |
| :---                | :---:                  | :---:     | :---:     |
| - 👊 Iron           | 0                      | 0         | **0**     |
| - 👁️ Mirrors        | 0                      | 0         | **0**     |
| - ❤️ Hearts         | 0                      | 0         | **0**     |
| - 🎭 Veils          | 0                      | 0         | **0**     |
| 🔍 **AFFILIATIONS** | **Base**               | **Perks** | **Total** |
| - 🔍 Academe        | 0                      | 0         | **0**     |
| - 🍷 Bohemia        | 0                      | 0         | **0**     |
| - 👑 Establishment  | 0                      | 0         | **0**     |
| - 🎩 Villainy       | 0                      | 0         | **0**     |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** Unassigned (No Ambition Selected) — *Current Focus: Awaiting Next Milestone*

📋 **Executive Officer's Counsel (Barnaby — Concept of Maneuver):**
> Barnaby reporting for bridge watch, Captain Sinclair. Our telegraph ledger is initialized with 1,000 Sovereigns in the strongbox, and we have slipped moorings from New Winchester bound for Port Avon (Full Resupply 🟢). Be advised: our Consumable Reserve Guard flags that we are departing with only 1 barrel of fuel (`🚨`) and 1 crate of supplies (`🚨`), well below our 3-unit safety minimum. Keep the throttle measured and bunker immediately upon docking at Port Avon.

### 🧭 Active Trajectory:
⚓ New Winchester ➔ 🟢 **Port Avon**

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 2 / 12

| Trade Good Name | Physical Hold (`hold_qty`) | Hub Bank (`bank_qty`) | Unit Cost (`MAC`) | Status / Earmark | Destination Port |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **🔥 Barrel of Fuel** | 1 | 0 | 0.00 | 🚨 | — |
| **📦 Crate of Supplies** | 1 | 0 | 0.00 | 🚨 | — |

---

## 🛞 BRIDGE ROSTER

| Station                   | Active Officer                          | Skill Perks                  | Affiliation Perks                  |
| :---                      | :---                                    | :---                         | :---                               |
| ⚓ **First Officer**      | 🔘 Vacant                               | —                            | —                                  |
| 🛞 **Quartermaster**      | 🔘 Vacant                               | —                            | —                                  |
| 🏮 **Signaller**          | 🔘 Vacant                               | —                            | —                                  |
| ⚙️ **Chief Engineer**     | 🔘 Vacant                               | —                            | —                                  |
| 🐶 **Mascot**             | 🔘 Vacant                               | —                            | —                                  |

  ---

*Respectfully submitted,*  

### 🪶 **_Barnaby_**

*Executive Officer, The Orphean*

⚜️ ─── ✦ 🧭 ۞ ⚓ ✦ ─── ⚜️

```

## Test Case 2: Port Arrival & Month-Boundary Bargain Discovery Tracking

**Feature Tags:** `[fsm, datetime, economy, ui-gates]`

### Objective

Verifies the kinetic state transition `enroute` ➔ `arriving` ➔ `docked`, temporal conversion crossing a month boundary (`1905-01-31` = Day 30), transit fuel burn deduction (`5 - 2 = 3`), append-only navigation history logging (`leg_index = 2`), itinerary pop, two-table bazaar bargain discovery (`State_Discovered_Locations[lustrum].bazaar_reset_epoch = 60` per Rule `3.2.1.2` and `State_Bazaar_Stock` row insertion for `unseasoned_hours`), and strict suppression of `logbook.md` while docked.

### Input Prompt

> Update state. We docked at Lustrum on 1905-01-31. Fuel used on this leg was 2. While checking the local market, we spotted a bargain: 3 crates of Unseasoned Hours selling for 40 Sovereigns each.

### Initial State Seed

*(Baseline defaults from `State_Scalars.csv` and `data_package.json` apply to all omitted tables and scalar keys.)*

#### `State_Scalars` Overrides:

| `property_key` | `property_value` | 
| ----- | ----- | 
| `sovereigns` | `1000` | 
| `current_epoch` | `26` | 
| `current_crew` | `8` | 
| `current_location_key` | `""` | 
| `last_location_visited_key` | `new_winchester` | 
| `navigation_state` | `enroute` | 

#### `State_Inventory`:

| `good_key` | `hold_qty` | `bank_qty` | `average_unit_cost` | 
| ----- | ----- | ----- | ----- | 
| `fuel` | `5` | `0` | `20.00` | 
| `supplies` | `4` | `0` | `40.00` | 

#### `State_Navigation_History`:

| `leg_index` | `location_key` | `arrived_epoch` | 
| ----- | ----- | ----- | 
| `1` | `new_winchester` | `0` | 

#### `State_Navigation_Itinerary`:

| `sequence_order` | `location_key` | 
| ----- | ----- | 
| `1` | `lustrum` | 

#### `State_Discovered_Locations`:

| `location_key` | `clock_position` | `bazaar_reset_epoch` | 
| ----- | ----- | ----- | 
| `new_winchester` | `""` | `""` | 

### Expected Verification

#### State Transition:

`enroute` ➔ `arriving` ➔ `docked`

#### Targeted State Verification:

| Target Address (`Table[PK].Column`) | Expected Value | Verification Note | 
| ----- | ----- | ----- | 
| `State_Scalars.current_epoch` | `30` | `1905-01-31` = Day 30 | 
| `State_Scalars.fuel_used_last_leg` | `2` | Recorded leg burn | 
| `State_Scalars.navigation_state` | `docked` | Completed arrival transition | 
| `State_Scalars.current_location_key` | `lustrum` | Active docked port | 
| `State_Inventory[fuel].hold_qty` | `3` | `5 - 2 = 3` barrels remaining | 
| `State_Navigation_History[2].location_key` | `lustrum` | Appended leg `2` (Class C) | 
| `State_Navigation_History[2].arrived_epoch` | `30` | Arrival stamped at Day 30 | 
| `State_Navigation_Itinerary.row_count` | `0` | Completed waypoint popped from itinerary | 
| `State_Discovered_Locations[lustrum].bazaar_reset_epoch` | `60` | `current_epoch + 30` (`30 + 30 = 60`, Rule `3.2.1.2`) | 
| `State_Bazaar_Stock[lustrum, unseasoned_hours].qty_available` | `3` | 3 crates available | 
| `State_Bazaar_Stock[lustrum, unseasoned_hours].cost` | `40` | 40 Sovereigns per crate | 
| `State_Bazaar_Stock[lustrum, unseasoned_hours].expiration_epoch` | `60` | `current_epoch + 30` (Rule `3.2.1.2`) | 

#### Report Text:

*(Full Markdown `logbook.md` is strictly suppressed during `arriving` and `docked` turns per Rule `4.4.1.2`.)*

> **Mr. Bligh's Bridge Micro-Briefing:**
> "Mooring lines secured at the freezing docks of Lustrum on 31 January 1905 (Day 30), Captain. Two barrels of fuel have been struck from the hold manifest for the transit burn, leaving us with 3 barrels of fuel (`⚠️` at minimum reserve) and 4 crates of supplies (`🟢`).
>
> High in the freezing peaks of the Mother of Mountains, miners chip raw, unseasoned hours straight from the rockface. Down at the bazaar exchange, I've logged a fresh bargain window (open through 2 March 1905 / Day 60): **3 Crates of Unseasoned Hours at 40 Sovereigns apiece**. Local merchants also export standard **Barrels of Fuel** and **Crates of Supplies**, and **Crew Recruitment** is available in the taverns if we wish to fill our 2 open bunks (`8 / 10`). Awaiting your trade orders before we plot our next departure."

## Test Case 3: Inventory Math, Banking Logistics & Non-Leap Temporal Calculation

**Feature Tags:** `[economy, inventory, datetime, officers]`

### Objective

Verifies hub bank cargo deposits (`hold_qty` $\to$ `bank_qty` at `new_winchester`, where `Ref_Location_Services` includes `'bank'`), confirms `average_unit_cost` remains unchanged on transfer, validates the 365-day High Wilderness solar calendar across a non-leap year boundary (`1908-02-28` = Day 1153 $\to$ `1908-03-01` = Day 1154, verifying February has 28 days with 0 leap days), evaluates dynamic stat perks from active First Officer `fortunate_navigator` (`+6 Iron`, `+2 Veils`, `+1 Establishment`), and renders `logbook.md` on departure to Titania.

### Input Prompt

> Update state. It's now 1908-03-01. We are docked at New Winchester and just deposited 4 loads of Bronzewood and 2 barrels of Chorister Nectar into our Hub Bank vault. Plot course and cast off for Titania!

### Initial State Seed

*(Baseline defaults from `State_Scalars.csv` and `data_package.json` apply to all omitted tables and scalar keys.)*

#### `State_Scalars` Overrides:

| `property_key` | `property_value` | 
| ----- | ----- | 
| `sovereigns` | `880` | 
| `current_epoch` | `1153` | 
| `current_crew` | `8` | 
| `skill_iron` | `10` | 
| `skill_mirrors` | `3` | 
| `skill_hearts` | `6` | 
| `skill_veils` | `3` | 
| `current_location_key` | `new_winchester` | 
| `last_location_visited_key` | `port_prosper` | 
| `navigation_state` | `docked` | 

#### `State_Inventory`:

| `good_key` | `hold_qty` | `bank_qty` | `average_unit_cost` | 
| ----- | ----- | ----- | ----- | 
| `fuel` | `3` | `0` | `20.00` | 
| `supplies` | `3` | `0` | `40.00` | 
| `bronzewood` | `4` | `1` | `175.00` | 
| `chorister_nectar` | `2` | `0` | `120.00` | 

#### `State_Officers`:

| `officer_key` | `officer_status` | 
| ----- | ----- | 
| `fortunate_navigator` | `active` | 

#### `State_Navigation_History`:

| `leg_index` | `location_key` | `arrived_epoch` | 
| ----- | ----- | ----- | 
| `4` | `port_prosper` | `1150` | 
| `5` | `new_winchester` | `1153` | 

#### `State_Navigation_Itinerary`:

| `sequence_order` | `location_key` | 
| ----- | ----- | 
| *(Empty — 0 rows)* |  | 

### Expected Verification

#### State Transition:

`docked` ➔ `departing` ➔ `enroute`

#### Targeted State Verification:

| Target Address (`Table[PK].Column`) | Expected Value | Verification Note | 
| ----- | ----- | ----- | 
| `State_Scalars.current_epoch` | `1154` | `1908-03-01` = Day 1154 (non-leap 365-day calendar) | 
| `State_Scalars.navigation_state` | `enroute` | Exited `departing` after rendering logbook | 
| `State_Scalars.current_location_key` | `""` | Cleared upon entering `enroute` | 
| `State_Scalars.last_location_visited_key` | `new_winchester` | Updated on departure exit | 
| `State_Inventory[bronzewood].hold_qty` | `0` | `4 - 4 = 0` in physical hold | 
| `State_Inventory[bronzewood].bank_qty` | `5` | `1 + 4 = 5` in Hub Bank (`MAC = 175.00` unchanged) | 
| `State_Inventory[chorister_nectar].hold_qty` | `0` | `2 - 2 = 0` in physical hold | 
| `State_Inventory[chorister_nectar].bank_qty` | `2` | `0 + 2 = 2` in Hub Bank (`MAC = 120.00` unchanged) | 
| `State_Navigation_Itinerary[1].location_key` | `titania` | Active destination waypoint | 

#### Report Text:

```
# 🚂 CAPTAIN'S LOG 🚀

## 📅 1 March 1908 (Day 1154) · ⚓ New Winchester

**🗺️ Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 880 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS
| System          | Status                                   |
| :---            | :---                                     |
| **Crew:**       | 🟢 8 / 10                                |
| **Hull:**       | 🟢 30 / 30                               |
| **Terror:**     | 🟢 0 / 100                               |
| **Nightmares:** | 🟢 0 / 4                                 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS           | Base                   | Perks     | Total     |
| :---                | :---:                  | :---:     | :---:     |
| - 👊 Iron           | 10                     | +6        | **16**    |
| - 👁️ Mirrors        | 3                      | 0         | **3**     |
| - ❤️ Hearts         | 6                      | 0         | **6**     |
| - 🎭 Veils          | 3                      | +2        | **5**     |
| 🔍 **AFFILIATIONS** | **Base**               | **Perks** | **Total** |
| - 🔍 Academe        | 0                      | 0         | **0**     |
| - 🍷 Bohemia        | 0                      | 0         | **0**     |
| - 👑 Establishment  | 0                      | +1        | **1**     |
| - 🎩 Villainy       | 0                      | 0         | **0**     |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** Unassigned (No Ambition Selected) — *Current Focus: Awaiting Next Milestone*

📋 **Executive Officer's Counsel (Mr. Bligh — Concept of Maneuver):**
> Vault receipts signed at New Winchester's Central Hub Bank, Captain. We have transferred 4 Loads of Bronzewood (bringing our vaulted stock to 5) and 2 Barrels of Chorister Nectar into safekeeping, freeing 6 slots in our physical hold (`6 / 12` used). Course is laid for Titania (Full Resupply 🟢). Note that both Fuel (`3`) and Supplies (`3`) sit exactly on our minimum reserve threshold (`⚠️`), so we should replenish stores upon reaching the glass gardens.

### 🧭 Active Trajectory:
⚓ New Winchester ➔ 🟢 **Titania**

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 6 / 12

| Trade Good Name | Physical Hold (`hold_qty`) | Hub Bank (`bank_qty`) | Unit Cost (`MAC`) | Status / Earmark | Destination Port |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **🔥 Barrel of Fuel** | 3 | 0 | 20.00 | ⚠️ | — |
| **📦 Crate of Supplies** | 3 | 0 | 40.00 | ⚠️ | — |
| **Load of Bronzewood** | 0 | 5 | 175.00 | Unassigned Cargo | — |
| **Barrel of Chorister Nectar** | 0 | 2 | 120.00 | Unassigned Cargo | — |

---

## 🛞 BRIDGE ROSTER

| Station                   | Active Officer                          | Skill Perks                  | Affiliation Perks                  |
| :---                      | :---                                    | :---                         | :---                               |
| ⚓ **First Officer**      | Fortunate Navigator                     | +6 Iron / +2 Veils           | +1 Establishment                   |
| 🛞 **Quartermaster**      | 🔘 Vacant                               | —                            | —                                  |
| 🏮 **Signaller**          | 🔘 Vacant                               | —                            | —                                  |
| ⚙️ **Chief Engineer**     | 🔘 Vacant                               | —                            | —                                  |
| 🐶 **Mascot**             | 🔘 Vacant                               | —                            | —                                  |

  ---

*Respectfully submitted,*  

### 🪶 **_Mr. Bligh_**

*Executive Officer, Zephyr*

⚜️ ─── ✦ 🧭 ۞ ⚓ ✦ ─── ⚜️

```

## Test Case 4: Ledger Integrity Breach Emergency Intercept (Rule 1.3.5.2)

**Feature Tags:** `[startup-recovery, ui-gates]`

### Objective

Probes compliance with Layer 1 Validation Gates (`1.3.2` & `1.3.5.2`) by seeding an unwhitelisted commodity key (`quantum_aether_crystal` not in `Ref_Goods.good_key`) in `State_Inventory` and an unwhitelisted location key (`missing_port_x` not in `Ref_Locations.location_key`) in `State_Action`. Verifies that the engine halts state mutation immediately, suppresses `logbook.md`, and emits the mandatory `⚠️ EXECUTIVE OFFICER'S ALERT — LEDGER INTEGRITY FAILURE` alert.

### Input Prompt

> Captain's log: 1905-01-10. Processing a logistics pass over our active trade agreements. Let me know what our current route optimization options look like.

### Initial State Seed

*(Baseline defaults from `State_Scalars.csv` and `data_package.json` apply to all omitted tables and scalar keys.)*

#### `State_Scalars` Overrides:

| `property_key` | `property_value` | 
| ----- | ----- | 
| `sovereigns` | `880` | 
| `current_epoch` | `9` | 
| `current_crew` | `8` | 
| `terror` | `15` | 

#### `State_Inventory`:

| `good_key` | `hold_qty` | `bank_qty` | `average_unit_cost` | 
| ----- | ----- | ----- | ----- | 
| `fuel` | `3` | `0` | `20.00` | 
| `supplies` | `3` | `0` | `40.00` | 
| `bronzewood` | `1` | `0` | `175.00` | 
| `quantum_aether_crystal` | `1` | `0` | `100.00` | 

#### `State_Action`:

| `action_id` | `parent_action_id` | `title` | `action_type` | `action_status` | `target_location_key` | `target_entity_key` | `quantity_required` | `quantity_delivered` | `priority` | `is_pinned` | `created_epoch` | `updated_epoch` | `deadline_epoch` | `notes` | 
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | 
| `ACT-1016` | `""` | `Deliver supplies to custom outpost` | `todo` | `active` | `missing_port_x` | `""` | `0` | `0` | `routine` | `FALSE` | `2` | `2` | `""` | `Error payload item: Unwhitelisted location key.` | 

### Expected Verification

#### State Transition:

`aborted` (Execution halted by Layer 1 Foreign Key / Whitelist Gate)

#### Targeted State Verification:

| Target Address (`Table[PK].Column`) | Expected Value | Verification Note | 
| ----- | ----- | ----- | 
| `State_Scalars.current_epoch` | `9` | Unchanged — all staged writes aborted (Rule `1.3.5.2`) | 
| `State_Scalars.navigation_state` | `docked` | Unchanged | 

#### Report Text:

*(Full Markdown `logbook.md` is strictly suppressed.)*

> ⚠️ EXECUTIVE OFFICER'S ALERT — LEDGER INTEGRITY FAILURE. Captain, something is amiss in the ship's telegraph ledger (`State_Inventory.good_key: 'quantum_aether_crystal'` not found in `Ref_Goods`; `State_Action.target_location_key: 'missing_port_x'` not found in `Ref_Locations`). I have halted entries to prevent corrupting our manifest. Please verify the sheet record or confirm how you wish me to reconcile the discrepancy.

## Test Case 5: Crew & Hull Status Color Mapping — Yellow Tier Warning

**Feature Tags:** `[crew, hull, datetime, inventory]`

### Objective

Verifies the structural color badge thresholds (`Rule 4.4.2.1`: `🟢` $> 70\%$, `🟡` $31\%\text{–}70\%$, `🔴` $\le 30\%$) when crew drops to `6 / 10` (`60%` $\to$ `🟡`) and hull drops to `17 / 30` (`56.7%` $\to$ `🟡`), tests year-boundary calendar calculation (`1906-01-15` = Day 379), and verifies departure logbook rendering from Port Avon to New Winchester for drydock repairs and crew recruitment.

### Input Prompt

> Update state. Bad news. An uncharted celestial anomaly scorched our hull crossing to Port Avon on 1906-01-15. We lost 2 crew members to the stars and took a pounding. Set our hull to 17 and our crew to 6. We must immediately depart for New Winchester to repair our hull and hire on new crew.

### Initial State Seed

*(Baseline defaults from `State_Scalars.csv` and `data_package.json` apply to all omitted tables and scalar keys.)*

#### `State_Scalars` Overrides:

| `property_key` | `property_value` | 
| ----- | ----- | 
| `sovereigns` | `880` | 
| `current_epoch` | `364` | 
| `current_crew` | `8` | 
| `terror` | `20` | 
| `current_location_key` | `port_avon` | 
| `last_location_visited_key` | `new_winchester` | 
| `navigation_state` | `docked` | 

#### `State_Inventory`:

| `good_key` | `hold_qty` | `bank_qty` | `average_unit_cost` | 
| ----- | ----- | ----- | ----- | 
| `fuel` | `3` | `0` | `20.00` | 
| `supplies` | `3` | `0` | `40.00` | 

#### `State_Navigation_History`:

| `leg_index` | `location_key` | `arrived_epoch` | 
| ----- | ----- | ----- | 
| `1` | `new_winchester` | `350` | 
| `2` | `port_avon` | `364` | 

#### `State_Navigation_Itinerary`:

| `sequence_order` | `location_key` | 
| ----- | ----- | 
| *(Empty — 0 rows)* |  | 

### Expected Verification

#### State Transition:

`docked` ➔ `departing` ➔ `enroute`

#### Targeted State Verification:

| Target Address (`Table[PK].Column`) | Expected Value | Verification Note | 
| ----- | ----- | ----- | 
| `State_Scalars.current_epoch` | `379` | `1906-01-15` = $365 + 14 = \text{Day } 379$ | 
| `State_Scalars.current_crew` | `6` | Updated to `6 / 10` (`60%` $\to$ `🟡`) | 
| `State_Scalars.current_hull` | `17` | Updated to `17 / 30` (`56.7%` $\to$ `🟡`) | 
| `State_Scalars.navigation_state` | `enroute` | Exited `departing` into open sky | 
| `State_Scalars.current_location_key` | `""` | Cleared upon entering `enroute` | 
| `State_Scalars.last_location_visited_key` | `port_avon` | Set to departure origin port | 
| `State_Navigation_Itinerary[1].location_key` | `new_winchester` | Active destination waypoint | 

#### Report Text:

```
# 🚂 CAPTAIN'S LOG 🚀

## 📅 15 January 1906 (Day 379) · ⚓ Port Avon

**🗺️ Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 880 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS
| System          | Status                                   |
| :---            | :---                                     |
| **Crew:**       | 🟡 6 / 10                                |
| **Hull:**       | 🟡 17 / 30                               |
| **Terror:**     | 🟢 20 / 100                              |
| **Nightmares:** | 🟢 0 / 4                                 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS           | Base                   | Perks     | Total     |
| :---                | :---:                  | :---:     | :---:     |
| - 👊 Iron           | 0                      | 0         | **0**     |
| - 👁️ Mirrors        | 0                      | 0         | **0**     |
| - ❤️ Hearts         | 0                      | 0         | **0**     |
| - 🎭 Veils          | 0                      | 0         | **0**     |
| 🔍 **AFFILIATIONS** | **Base**               | **Perks** | **Total** |
| - 🔍 Academe        | 0                      | 0         | **0**     |
| - 🍷 Bohemia        | 0                      | 0         | **0**     |
| - 👑 Establishment  | 0                      | 0         | **0**     |
| - 🎩 Villainy       | 0                      | 0         | **0**     |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** Unassigned (No Ambition Selected) — *Current Focus: Awaiting Next Milestone*

📋 **Executive Officer's Counsel (Mr. Bligh — Concept of Maneuver):**
> Mr. Bligh at the bridge telegraph. We have cast off from Port Avon with scorched hull plating (`17 / 30` 🟡) and two empty bunks (`6 / 10` 🟡). Port Avon has no drydock shipyard, so making straight for New Winchester (Full Resupply 🟢, Shipyard & Recruitment available) is the right call. Both Fuel (`3`) and Supplies (`3`) sit right on our minimum reserve line (`⚠️`), which will see us safely back to the central hub if we avoid open-sky engagements.

### 🧭 Active Trajectory:
⚓ Port Avon ➔ 🟢 **New Winchester**

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 6 / 12

| Trade Good Name | Physical Hold (`hold_qty`) | Hub Bank (`bank_qty`) | Unit Cost (`MAC`) | Status / Earmark | Destination Port |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **🔥 Barrel of Fuel** | 3 | 0 | 20.00 | ⚠️ | — |
| **📦 Crate of Supplies** | 3 | 0 | 40.00 | ⚠️ | — |

---

## 🛞 BRIDGE ROSTER

| Station                   | Active Officer                          | Skill Perks                  | Affiliation Perks                  |
| :---                      | :---                                    | :---                         | :---                               |
| ⚓ **First Officer**      | 🔘 Vacant                               | —                            | —                                  |
| 🛞 **Quartermaster**      | 🔘 Vacant                               | —                            | —                                  |
| 🏮 **Signaller**          | 🔘 Vacant                               | —                            | —                                  |
| ⚙️ **Chief Engineer**     | 🔘 Vacant                               | —                            | —                                  |
| 🐶 **Mascot**             | 🔘 Vacant                               | —                            | —                                  |

  ---

*Respectfully submitted,*  

### 🪶 **_Mr. Bligh_**

*Executive Officer, Zephyr*

⚜️ ─── ✦ 🧭 ۞ ⚓ ✦ ─── ⚜️

```

## Test Case 6: Critical Low Crew Threshold & Baseline Consumable Depletion Guardrail

**Feature Tags:** `[crew, terror, narrative, datetime]`

### Objective

Verifies the behavioral tone shift when crew drops to $\le 50\%$ (`Rule 4.1.2.4` Depleted Crew strained caution) and `🔴` status badge at $\le 30\%$ (`3 / 10`), enforces the **Permanent Consumables Guardrail (`Rule 1.1.3.1` & `3.1.3.3`)** where `supplies` at `0` quantity is retained in `State_Inventory` with `hold_qty = 0, bank_qty = 0, average_unit_cost = 0.00` and `🚨` reserve status (`fuel = 1` also shows `🚨` since $1 < 3$), creates a high-priority `todo` (`ACT-1001`, `‼️`) targeting `polmear_and_plentys_inconceivable_circus`, and converts `1906-01-20` to Day 384.

### Input Prompt

> Update state. 1906-01-20. Sickness swept through the lower bunks while out on the high sky. We've dropped 3 more hands off at the local care station in Hybras. Crew strength is down to 3 out of 10. Make a high-priority note to hire on crew at the circus. Clear docks for Polmear & Plenty's with haste.

### Initial State Seed

*(Baseline defaults from `State_Scalars.csv` and `data_package.json` apply to all omitted tables and scalar keys.)*

#### `State_Scalars` Overrides:

| `property_key` | `property_value` | 
| ----- | ----- | 
| `sovereigns` | `880` | 
| `current_epoch` | `379` | 
| `current_crew` | `6` | 
| `current_hull` | `17` | 
| `terror` | `35` | 
| `current_location_key` | `hybras` | 
| `last_location_visited_key` | `port_avon` | 
| `navigation_state` | `docked` | 

#### `State_Inventory`:

| `good_key` | `hold_qty` | `bank_qty` | `average_unit_cost` | 
| ----- | ----- | ----- | ----- | 
| `fuel` | `1` | `0` | `20.00` | 
| `supplies` | `0` | `0` | `0.00` | 

#### `State_Navigation_History`:

| `leg_index` | `location_key` | `arrived_epoch` | 
| ----- | ----- | ----- | 
| `2` | `port_avon` | `379` | 
| `3` | `hybras` | `379` | 

#### `State_Navigation_Itinerary`:

| `sequence_order` | `location_key` | 
| ----- | ----- | 
| *(Empty — 0 rows)* |  | 

### Expected Verification

#### State Transition:

`docked` ➔ `departing` ➔ `enroute`

#### Targeted State Verification:

| Target Address (`Table[PK].Column`) | Expected Value | Verification Note | 
| ----- | ----- | ----- | 
| `State_Scalars.current_epoch` | `384` | `1906-01-20` = $365 + 19 = \text{Day } 384$ | 
| `State_Scalars.current_crew` | `3` | `3 / 10` (`30%` $\to$ `🔴` badge & Depleted Crew tone) | 
| `State_Inventory[fuel].hold_qty` | `1` | `1 < 3` (`🚨` below reserve minimum) | 
| `State_Inventory[supplies].hold_qty` | `0` | Retained permanently at `0` qty per Rule `1.1.3.1` (`🚨`) | 
| `State_Inventory[supplies].average_unit_cost` | `0.00` | Zeroed out at `0` total quantity (Rule `1.1.3.1`) | 
| `State_Action[ACT-1001].action_type` | `todo` | Player-directed reminder | 
| `State_Action[ACT-1001].priority` | `high` | Explicitly ordered high-priority (`‼️`) | 
| `State_Action[ACT-1001].target_location_key` | `polmear_and_plentys_inconceivable_circus` | Canonical location key | 
| `State_Navigation_Itinerary[1].location_key` | `polmear_and_plentys_inconceivable_circus` | Active destination waypoint | 
| `State_Scalars.navigation_state` | `enroute` | Exited `departing` into open sky | 

#### Report Text:

```
# 🚂 CAPTAIN'S LOG 🚀

## 📅 20 January 1906 (Day 384) · ⚓ Hybras

**🗺️ Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 880 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS
| System          | Status                                   |
| :---            | :---                                     |
| **Crew:**       | 🔴 3 / 10                                |
| **Hull:**       | 🟡 17 / 30                               |
| **Terror:**     | 🟢 35 / 100                              |
| **Nightmares:** | 🟢 0 / 4                                 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS           | Base                   | Perks     | Total     |
| :---                | :---:                  | :---:     | :---:     |
| - 👊 Iron           | 0                      | 0         | **0**     |
| - 👁️ Mirrors        | 0                      | 0         | **0**     |
| - ❤️ Hearts         | 0                      | 0         | **0**     |
| - 🎭 Veils          | 0                      | 0         | **0**     |
| 🔍 **AFFILIATIONS** | **Base**               | **Perks** | **Total** |
| - 🔍 Academe        | 0                      | 0         | **0**     |
| - 🍷 Bohemia        | 0                      | 0         | **0**     |
| - 👑 Establishment  | 0                      | 0         | **0**     |
| - 🎩 Villainy       | 0                      | 0         | **0**     |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** Unassigned (No Ambition Selected) — *Current Focus: Awaiting Next Milestone*

📋 **Executive Officer's Counsel (Mr. Bligh — Concept of Maneuver):**
> Mr. Bligh speaking—and heaven help us, Captain. We are hauling out of Hybras with a dead skeleton crew of 3 souls (`🔴`). The surviving stokers are swaying on their feet, the helm responds like cold treacle, and our Consumable Reserve Guard is screaming: we are down to a single barrel of fuel (`🚨`) and zero crates of supplies (`🚨`) in a bare larder. I have logged an urgent directive (`ACT-1001`) to sign on fresh hands and bunker stores the moment we tie up at Polmear & Plenty's Inconceivable Circus (Full Resupply 🟢). Do not deviate from the direct lane.

### 🧭 Active Trajectory:
⚓ Hybras ➔ 🟢 **Polmear & Plenty's Inconceivable Circus**

### ➡️ STOP 1: Polmear & Plenty's Inconceivable Circus
* ‼️ 📌 **TODO:** Hire replacement crew at the circus (`ACT-1001`) — Recruit hands and replenish depleted provisions immediately

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 1 / 12

| Trade Good Name | Physical Hold (`hold_qty`) | Hub Bank (`bank_qty`) | Unit Cost (`MAC`) | Status / Earmark | Destination Port |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **🔥 Barrel of Fuel** | 1 | 0 | 20.00 | 🚨 | — |
| **📦 Crate of Supplies** | 0 | 0 | 0.00 | 🚨 | — |

---

## 🛞 BRIDGE ROSTER

| Station                   | Active Officer                          | Skill Perks                  | Affiliation Perks                  |
| :---                      | :---                                    | :---                         | :---                               |
| ⚓ **First Officer**      | 🔘 Vacant                               | —                            | —                                  |
| 🛞 **Quartermaster**      | 🔘 Vacant                               | —                            | —                                  |
| 🏮 **Signaller**          | 🔘 Vacant                               | —                            | —                                  |
| ⚙️ **Chief Engineer**     | 🔘 Vacant                               | —                            | —                                  |
| 🐶 **Mascot**             | 🔘 Vacant                               | —                            | —                                  |

  ---

*Respectfully submitted,*  

### 🪶 **_Mr. Bligh_**

*Executive Officer, Zephyr*

⚜️ ─── ✦ 🧭 ۞ ⚓ ✦ ─── ⚜️

```

## Test Case 7: Route Planner — Multi-Stop Sequential Itinerary & Replicated Stop Blocks

**Feature Tags:** `[navigation, datetime, narrative]`

### Objective

Verifies multi-stop itinerary construction (`State_Navigation_Itinerary` contiguous 1-indexed sequencing), spatial target filtering across replicated `### ➡️ STOP [sequence_order]:` blocks in `logbook.md` (with both `titania` and `lustrum` verified as `🟢` Full Resupply in `Ref_Location_Goods.csv`), Ambition Root Wrapper (`ACT-1001`) + Subtask (`ACT-1001.01`) banner resolution, priority-ordered cargo earmarking in `📦 LOGISTICS`, and mid-year calendar conversion across a non-leap year (`1908-04-11` = Day 1195).

### Input Prompt

> Update state. Plot a route from New Winchester to Titania, and then onward to Lustrum, and set sail. Let's see what business we have pending at those locations, First Mate.

### Initial State Seed

*(Baseline defaults from `State_Scalars.csv` and `data_package.json` apply to all omitted tables and scalar keys.)*

#### `State_Scalars` Overrides:

| `property_key` | `property_value` | 
| ----- | ----- | 
| `sovereigns` | `1450` | 
| `current_epoch` | `1195` | 
| `current_crew` | `9` | 
| `terror` | `15` | 
| `current_location_key` | `new_winchester` | 
| `last_location_visited_key` | `new_winchester` | 
| `navigation_state` | `docked` | 

#### `State_Inventory`:

| `good_key` | `hold_qty` | `bank_qty` | `average_unit_cost` | 
| ----- | ----- | ----- | ----- | 
| `fuel` | `3` | `0` | `20.00` | 
| `supplies` | `3` | `0` | `40.00` | 
| `bronzewood` | `3` | `0` | `175.00` | 

#### `State_Action`:

| `action_id` | `parent_action_id` | `title` | `action_type` | `action_status` | `target_location_key` | `target_entity_key` | `quantity_required` | `quantity_delivered` | `priority` | `is_pinned` | `created_epoch` | `updated_epoch` | `deadline_epoch` | `notes` | 
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | 
| `ACT-1001` | `""` | `Wealth` | `ambition` | `active` | `""` | `""` | `0` | `0` | `routine` | `FALSE` | `6` | `1190` | `""` | `Tier 1` | 
| `ACT-1001.01` | `ACT-1001` | `Purchase the Governor's Manor` | `ambition` | `active` | `london` | `sovereigns` | `5000` | `0` | `routine` | `FALSE` | `6` | `1190` | `""` | `Requires 5,000 Sovereigns` | 
| `ACT-1012` | `""` | `Nectar for the Fairies` | `prospect` | `active` | `titania` | `chorister_nectar` | `1` | `0` | `routine` | `FALSE` | `1179` | `1179` | `""` | `""` | 
| `ACT-1013` | `""` | `Bronzewood Shipments` | `prospect` | `ready` | `lustrum` | `bronzewood` | `3` | `0` | `routine` | `FALSE` | `1182` | `1182` | `""` | `""` | 
| `ACT-1016` | `""` | `Helping the Horticulturalist` | `todo` | `active` | `titania` | `""` | `0` | `0` | `routine` | `FALSE` | `1190` | `1190` | `""` | `Deliver structural schematics to the Horticulturalist` | 

#### `State_Navigation_History`:

| `leg_index` | `location_key` | `arrived_epoch` | 
| ----- | ----- | ----- | 
| `1` | `new_winchester` | `1180` | 

#### `State_Navigation_Itinerary`:

| `sequence_order` | `location_key` | 
| ----- | ----- | 
| *(Empty — 0 rows)* |  | 

### Expected Verification

#### State Transition:

`docked` ➔ `departing` ➔ `enroute`

#### Targeted State Verification:

| Target Address (`Table[PK].Column`) | Expected Value | Verification Note | 
| ----- | ----- | ----- | 
| `State_Scalars.current_epoch` | `1195` | `11 April 1908` = Day 1195 | 
| `State_Scalars.navigation_state` | `enroute` | Exited `departing` into open skyway | 
| `State_Scalars.current_location_key` | `""` | Cleared upon entering `enroute` | 
| `State_Scalars.last_location_visited_key` | `new_winchester` | Origin anchor preserved | 
| `State_Navigation_Itinerary[1].location_key` | `titania` | Contiguous 1-indexed Stop 1 | 
| `State_Navigation_Itinerary[2].location_key` | `lustrum` | Contiguous 1-indexed Stop 2 | 
| `State_Action[ACT-1012].action_status` | `active` | `0/1` `chorister_nectar` in hold | 
| `State_Action[ACT-1013].action_status` | `ready` | `3/3` `bronzewood` allocated in hold | 

#### Report Text:

```
# 🚂 CAPTAIN'S LOG 🚀

## 📅 11 April 1908 (Day 1195) · ⚓ New Winchester

**🗺️ Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 1450 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS
| System          | Status                                   |
| :---            | :---                                     |
| **Crew:**       | 🟢 9 / 10                                |
| **Hull:**       | 🟢 30 / 30                               |
| **Terror:**     | 🟢 15 / 100                              |
| **Nightmares:** | 🟢 0 / 4                                 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS           | Base                   | Perks     | Total     |
| :---                | :---:                  | :---:     | :---:     |
| - 👊 Iron           | 0                      | 0         | **0**     |
| - 👁️ Mirrors        | 0                      | 0         | **0**     |
| - ❤️ Hearts         | 0                      | 0         | **0**     |
| - 🎭 Veils          | 0                      | 0         | **0**     |
| 🔍 **AFFILIATIONS** | **Base**               | **Perks** | **Total** |
| - 🔍 Academe        | 0                      | 0         | **0**     |
| - 🍷 Bohemia        | 0                      | 0         | **0**     |
| - 👑 Establishment  | 0                      | 0         | **0**     |
| - 🎩 Villainy       | 0                      | 0         | **0**     |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** Wealth (Tier 1) — *Current Focus: Purchase the Governor's Manor*

📋 **Executive Officer's Counsel (Mr. Bligh — Concept of Maneuver):**
> Route plotted for a two-stop sweep across The Reach: Leg 1 to Titania (Full Resupply 🟢), followed by Leg 2 to Lustrum (Full Resupply 🟢). Both Fuel (`3`) and Supplies (`3`) sit at our minimum reserve threshold (`⚠️`), so topping off at Titania is advised before pushing out to the outer ring. At Titania, resolve our errand for the Horticulturalist (`ACT-1016`); note that our Chorister Nectar prospect (`ACT-1012`) remains unsourced (`0/1`). At Lustrum, our 3 loads of Bronzewood (`ACT-1013`) are lashed in the hold and ready for immediate turn-in.

### 🧭 Active Trajectory:
⚓ New Winchester ➔ 🟢 **Titania** ➔ 🟢 Lustrum

### ➡️ STOP 1: Titania
* 🔑 **PROSPECT:** Nectar for the Fairies (`ACT-1012`) — Deliver 1 Barrel of Chorister Nectar (active)
* 📌 **TODO:** Helping the Horticulturalist (`ACT-1016`) — Deliver structural schematics to the Horticulturalist

### ➡️ STOP 2: Lustrum
* 🔑 **PROSPECT:** Bronzewood Shipments (`ACT-1013`) — Deliver 3 Load of Bronzewood (ready)

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 9 / 12

| Trade Good Name | Physical Hold (`hold_qty`) | Hub Bank (`bank_qty`) | Unit Cost (`MAC`) | Status / Earmark | Destination Port |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **🔥 Barrel of Fuel** | 3 | 0 | 20.00 | ⚠️ | — |
| **📦 Crate of Supplies** | 3 | 0 | 40.00 | ⚠️ | — |
| **Load of Bronzewood** | 3 | 0 | 175.00 | Earmarked for `ACT-1013`: Bronzewood Shipments (3/3) | Lustrum |

---

## 🛞 BRIDGE ROSTER

| Station                   | Active Officer                          | Skill Perks                  | Affiliation Perks                  |
| :---                      | :---                                    | :---                         | :---                               |
| ⚓ **First Officer**      | 🔘 Vacant                               | —                            | —                                  |
| 🛞 **Quartermaster**      | 🔘 Vacant                               | —                            | —                                  |
| 🏮 **Signaller**          | 🔘 Vacant                               | —                            | —                                  |
| ⚙️ **Chief Engineer**     | 🔘 Vacant                               | —                            | —                                  |
| 🐶 **Mascot**             | 🔘 Vacant                               | —                            | —                                  |

  ---

*Respectfully submitted,*  

### 🪶 **_Mr. Bligh_**

*Executive Officer, Zephyr*

⚜️ ─── ✦ 🧭 ۞ ⚓ ✦ ─── ⚜️

```

## Test Case 8: Route Planner — Resupply Isolation Alert & Intermediate Port Recommendation

**Feature Tags:** `[navigation, terror, datetime]`

### Objective

Verifies that the Departure Consumable Reserve Guard (`Rule 2.2.3.1`) and Route Planner (`Rule 2.3.1` & `2.3.2`) detect critical consumable deficits (`1` fuel `🚨` and `1` supplies `🚨`, both $< 3$) prior to a long outer-ring haul to `port_prosper` (`ring_depth = outer`, `clock_position = 6`), evaluate discovered clock coordinates to recommend an intermediate resupply detour via `titania` (`ring_depth = middle`, `clock_position = 2`), map `terror = 40` to `🟡` (`40–69` per Rule `4.4.2.2`), and parse `1905-02-18` = Day 48.

### Input Prompt

> Update state. It is 1905-02-18. Lay a direct course from New Winchester straight out to Port Prosper, First Mate. We have a long haul ahead, let's get moving.

### Initial State Seed

*(Baseline defaults from `State_Scalars.csv` and `data_package.json` apply to all omitted tables and scalar keys.)*

#### `State_Scalars` Overrides:

| `property_key` | `property_value` | 
| ----- | ----- | 
| `sovereigns` | `620` | 
| `current_epoch` | `48` | 
| `current_hull` | `25` | 
| `terror` | `40` | 
| `nightmares` | `1` | 
| `current_location_key` | `new_winchester` | 
| `last_location_visited_key` | `new_winchester` | 
| `navigation_state` | `docked` | 

#### `State_Inventory`:

| `good_key` | `hold_qty` | `bank_qty` | `average_unit_cost` | 
| ----- | ----- | ----- | ----- | 
| `fuel` | `1` | `0` | `20.00` | 
| `supplies` | `1` | `0` | `40.00` | 

#### `State_Navigation_History`:

| `leg_index` | `location_key` | `arrived_epoch` | 
| ----- | ----- | ----- | 
| `1` | `new_winchester` | `48` | 

#### `State_Navigation_Itinerary`:

| `sequence_order` | `location_key` | 
| ----- | ----- | 
| *(Empty — 0 rows)* |  | 

#### `State_Discovered_Locations`:

| `location_key` | `clock_position` | `bazaar_reset_epoch` | 
| ----- | ----- | ----- | 
| `new_winchester` | `""` | `""` | 
| `titania` | `2` | `""` | 
| `port_prosper` | `6` | `""` | 

### Expected Verification

#### State Transition:

`docked` ➔ `departing` ➔ `enroute`

#### Targeted State Verification:

| Target Address (`Table[PK].Column`) | Expected Value | Verification Note | 
| ----- | ----- | ----- | 
| `State_Scalars.current_epoch` | `48` | `18 February 1905` = Day 48 | 
| `State_Scalars.terror` | `40` | `40 / 100` renders `🟡` badge (`40–69`, Rule `4.4.2.2`) | 
| `State_Inventory[fuel].hold_qty` | `1` | `1 < 3` (`🚨` reserve deficit) | 
| `State_Inventory[supplies].hold_qty` | `1` | `1 < 3` (`🚨` reserve deficit) | 
| `State_Navigation_Itinerary[1].location_key` | `port_prosper` | Plotted per Captain's direct order | 
| `State_Scalars.navigation_state` | `enroute` | Exited `departing` into open sky | 

#### Report Text:

```
# 🚂 CAPTAIN'S LOG 🚀

## 📅 18 February 1905 (Day 48) · ⚓ New Winchester

**🗺️ Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 620 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS
| System          | Status                                   |
| :---            | :---                                     |
| **Crew:**       | 🟢 10 / 10                               |
| **Hull:**       | 🟢 25 / 30                               |
| **Terror:**     | 🟡 40 / 100                              |
| **Nightmares:** | 🟢 1 / 4                                 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS           | Base                   | Perks     | Total     |
| :---                | :---:                  | :---:     | :---:     |
| - 👊 Iron           | 0                      | 0         | **0**     |
| - 👁️ Mirrors        | 0                      | 0         | **0**     |
| - ❤️ Hearts         | 0                      | 0         | **0**     |
| - 🎭 Veils          | 0                      | 0         | **0**     |
| 🔍 **AFFILIATIONS** | **Base**               | **Perks** | **Total** |
| - 🔍 Academe        | 0                      | 0         | **0**     |
| - 🍷 Bohemia        | 0                      | 0         | **0**     |
| - 👑 Establishment  | 0                      | 0         | **0**     |
| - 🎩 Villainy       | 0                      | 0         | **0**     |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** Unassigned (No Ambition Selected) — *Current Focus: Awaiting Next Milestone*

📋 **Executive Officer's Counsel (Mr. Bligh — Concept of Maneuver):**
> Mr. Bligh raising a stern operational warning under the Consumable Reserve Guard, Captain. Casting off directly for Port Prosper (`outer` ring, 6 o'clock bearing) with only 1 barrel of fuel (`🚨`) and 1 crate of supplies (`🚨`)—well below our 3-unit safety minimum—courts starvation and an empty boiler in the dark, especially with crew Terror already creeping into the yellow tier (`40 / 100` 🟡). I strongly counsel an immediate mid-sky diversion via **Titania** (`middle` ring, 2 o'clock bearing, Full Resupply 🟢) to bunker fuel and provisions before pushing out to the 6 o'clock perimeter.

### 🧭 Active Trajectory:
⚓ New Winchester ➔ 🟢 **Port Prosper**

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 2 / 12

| Trade Good Name | Physical Hold (`hold_qty`) | Hub Bank (`bank_qty`) | Unit Cost (`MAC`) | Status / Earmark | Destination Port |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **🔥 Barrel of Fuel** | 1 | 0 | 20.00 | 🚨 | — |
| **📦 Crate of Supplies** | 1 | 0 | 40.00 | 🚨 | — |

---

## 🛞 BRIDGE ROSTER

| Station                   | Active Officer                          | Skill Perks                  | Affiliation Perks                  |
| :---                      | :---                                    | :---                         | :---                               |
| ⚓ **First Officer**      | 🔘 Vacant                               | —                            | —                                  |
| 🛞 **Quartermaster**      | 🔘 Vacant                               | —                            | —                                  |
| 🏮 **Signaller**          | 🔘 Vacant                               | —                            | —                                  |
| ⚙️ **Chief Engineer**     | 🔘 Vacant                               | —                            | —                                  |
| 🐶 **Mascot**             | 🔘 Vacant                               | —                            | —                                  |

  ---

*Respectfully submitted,*  

### 🪶 **_Mr. Bligh_**

*Executive Officer, Zephyr*

⚜️ ─── ✦ 🧭 ۞ ⚓ ✦ ─── ⚜️

```

## Test Case 9: Three-Tier Storage Isolation — Weightless Possessions & Personal Locker

**Feature Tags:** `[inventory, narrative, datetime]`

### Objective

Verifies the Three-Tier Inventory Classification & Storage Loci rules (`Rule 3.2.3`): confirms that Category 2 Faction Possessions (`State_Scalars.possession_tale_of_terror = 2`) and Category 3 Narrative Items (`primordial_star_shard` tracked via `State_Action` in the Captain's Personal Locker) consume `0` physical hold slots, leaving `Hold Utilization` at `10 / 12` (`4` fuel + `4` supplies + `2` `approved_literature`). Instantiates atomic quest `ACT-1001` (`The Last Consignment`) targeting `port_avon` on `1905-01-15` (Day 14).

### Input Prompt

> Update state. Captain's log: 1905-01-15. We acquired two Tales of Terror out in the dark on that last run. We also took on a quest from The Sequestered Scholar to deliver a Primordial Star Shard to Port Avon. Log this as "The Last Consignment." Let's make sure our logistics files are updated before we cast off lines for Port Avon.

### Initial State Seed

*(Baseline defaults from `State_Scalars.csv` and `data_package.json` apply to all omitted tables and scalar keys.)*

#### `State_Scalars` Overrides:

| `property_key` | `property_value` | 
| ----- | ----- | 
| `sovereigns` | `800` | 
| `current_epoch` | `14` | 
| `current_crew` | `8` | 
| `fuel_used_last_leg` | `2` | 
| `current_location_key` | `new_winchester` | 
| `last_location_visited_key` | `new_winchester` | 
| `navigation_state` | `docked` | 

#### `State_Inventory`:

| `good_key` | `hold_qty` | `bank_qty` | `average_unit_cost` | 
| ----- | ----- | ----- | ----- | 
| `fuel` | `4` | `0` | `20.00` | 
| `supplies` | `4` | `0` | `40.00` | 
| `approved_literature` | `2` | `0` | `100.00` | 

#### `State_Navigation_History`:

| `leg_index` | `location_key` | `arrived_epoch` | 
| ----- | ----- | ----- | 
| `1` | `new_winchester` | `0` | 

#### `State_Navigation_Itinerary`:

| `sequence_order` | `location_key` | 
| ----- | ----- | 
| *(Empty — 0 rows)* |  | 

### Expected Verification

#### State Transition:

`docked` ➔ `departing` ➔ `enroute`

#### Targeted State Verification:

| Target Address (`Table[PK].Column`) | Expected Value | Verification Note | 
| ----- | ----- | ----- | 
| `State_Scalars.current_epoch` | `14` | `15 January 1905` = Day 14 | 
| `State_Scalars.possession_tale_of_terror` | `2` | Category 2 token stored in `State_Scalars` (`0` hold slots) | 
| `State_Action[ACT-1001].title` | `The Last Consignment` | Atomic quest row (`Rule 3.3.2.1`) | 
| `State_Action[ACT-1001].action_type` | `quest` | Narrative quest classification | 
| `State_Action[ACT-1001].target_location_key` | `port_avon` | Destination port | 
| `State_Action[ACT-1001].target_entity_key` | `primordial_star_shard` | Category 3 narrative item in Personal Locker (`0` hold slots) | 
| `State_Action[ACT-1001].quantity_required` | `1` | 1 shard required | 
| `State_Navigation_Itinerary[1].location_key` | `port_avon` | Active destination waypoint | 
| `State_Scalars.navigation_state` | `enroute` | Exited `departing` into open sky | 

#### Report Text:

```
# 🚂 CAPTAIN'S LOG 🚀

## 📅 15 January 1905 (Day 14) · ⚓ New Winchester

**🗺️ Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 800 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS
| System          | Status                                   |
| :---            | :---                                     |
| **Crew:**       | 🟢 8 / 10                                |
| **Hull:**       | 🟢 30 / 30                               |
| **Terror:**     | 🟢 0 / 100                               |
| **Nightmares:** | 🟢 0 / 4                                 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS           | Base                   | Perks     | Total     |
| :---                | :---:                  | :---:     | :---:     |
| - 👊 Iron           | 0                      | 0         | **0**     |
| - 👁️ Mirrors        | 0                      | 0         | **0**     |
| - ❤️ Hearts         | 0                      | 0         | **0**     |
| - 🎭 Veils          | 0                      | 0         | **0**     |
| 🔍 **AFFILIATIONS** | **Base**               | **Perks** | **Total** |
| - 🔍 Academe        | 0                      | 0         | **0**     |
| - 🍷 Bohemia        | 0                      | 0         | **0**     |
| - 👑 Establishment  | 0                      | 0         | **0**     |
| - 🎩 Villainy       | 0                      | 0         | **0**     |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** Unassigned (No Ambition Selected) — *Current Focus: Awaiting Next Milestone*

📋 **Executive Officer's Counsel (Mr. Bligh — Concept of Maneuver):**
> Mr. Bligh at the ledger. The Sequestered Scholar's commission is logged as *The Last Consignment* (`ACT-1001`), bound for Port Avon with the Primordial Star Shard secured in your personal locker. Neither the shard nor the 2 Tales of Terror recorded in our papers draw physical hold space, leaving our hold utilization at `10 / 12` slots (`4` Fuel 🟢, `4` Supplies 🟢, and `2` Batch of Approved Literature). Moorings slipped for Port Avon (Full Resupply 🟢).

### 🧭 Active Trajectory:
⚓ New Winchester ➔ 🟢 **Port Avon**

### ➡️ STOP 1: Port Avon
* 📖 **QUEST:** The Last Consignment (`ACT-1001`) — Deliver Primordial Star Shard (1/1 in Captain's locker) for The Sequestered Scholar

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 10 / 12

| Trade Good Name | Physical Hold (`hold_qty`) | Hub Bank (`bank_qty`) | Unit Cost (`MAC`) | Status / Earmark | Destination Port |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **🔥 Barrel of Fuel** | 4 | 0 | 20.00 | 🟢 | — |
| **📦 Crate of Supplies** | 4 | 0 | 40.00 | 🟢 | — |
| **Batch of Approved Literature** | 2 | 0 | 100.00 | Unassigned Cargo | — |

---

## 🛞 BRIDGE ROSTER

| Station                   | Active Officer                          | Skill Perks                  | Affiliation Perks                  |
| :---                      | :---                                    | :---                         | :---                               |
| ⚓ **First Officer**      | 🔘 Vacant                               | —                            | —                                  |
| 🛞 **Quartermaster**      | 🔘 Vacant                               | —                            | —                                  |
| 🏮 **Signaller**          | 🔘 Vacant                               | —                            | —                                  |
| ⚙️ **Chief Engineer**     | 🔘 Vacant                               | —                            | —                                  |
| 🐶 **Mascot**             | 🔘 Vacant                               | —                            | —                                  |

  ---

*Respectfully submitted,*  

### 🪶 **_Mr. Bligh_**

*Executive Officer, Zephyr*

⚜️ ─── ✦ 🧭 ۞ ⚓ ✦ ─── ⚜️

```

## Test Case 10: Prospect Sourcing Phase to Ready Status Sync & Auto-Prioritization

**Feature Tags:** `[inventory, navigation, datetime]`

### Objective

Verifies that loading the remaining `2` crates of `munitions` (`hold_qty` `2` $\to$ `4`) triggers **Inventory-to-Action Readiness Sync (`Rule 3.3.3.3`)** to promote `ACT-1001` from `action_status = 'active'` to `'ready'`, triggers **Auto-Prioritization (`Rule 4.3.1.1`)** to promote `ACT-1001.priority` to `'high'` (`‼️`) because it is `'ready'` and targets `State_Navigation_Itinerary[1]` (`port_prosper`), formats the `📦 LOGISTICS` earmark as `Earmarked for ACT-1001: Fortress Resupply (4/4)`, and converts `Epoch 48` to `18 February 1905`.

### Input Prompt

> Update state. I've finished loading the remaining 2 crates of Munitions here at New Winchester (at 60 Sovereigns each, already settled in our balance), completely filling our contract order. Plotting course to set sail for Port Prosper.

### Initial State Seed

*(Baseline defaults from `State_Scalars.csv` and `data_package.json` apply to all omitted tables and scalar keys.)*

#### `State_Scalars` Overrides:

| `property_key` | `property_value` | 
| ----- | ----- | 
| `sovereigns` | `1000` | 
| `current_epoch` | `48` | 
| `terror` | `12` | 
| `current_location_key` | `new_winchester` | 
| `last_location_visited_key` | `new_winchester` | 
| `navigation_state` | `docked` | 

#### `State_Inventory`:

| `good_key` | `hold_qty` | `bank_qty` | `average_unit_cost` | 
| ----- | ----- | ----- | ----- | 
| `fuel` | `3` | `0` | `20.00` | 
| `supplies` | `3` | `0` | `40.00` | 
| `munitions` | `2` | `0` | `60.00` | 

#### `State_Action`:

| `action_id` | `parent_action_id` | `title` | `action_type` | `action_status` | `target_location_key` | `target_entity_key` | `quantity_required` | `quantity_delivered` | `priority` | `is_pinned` | `created_epoch` | `updated_epoch` | `deadline_epoch` | `notes` | 
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | 
| `ACT-1001` | `""` | `Fortress Resupply` | `prospect` | `active` | `port_prosper` | `munitions` | `4` | `0` | `routine` | `FALSE` | `48` | `48` | `""` | `Urgent munitions shipment for the garrison.` | 

#### `State_Navigation_History`:

| `leg_index` | `location_key` | `arrived_epoch` | 
| ----- | ----- | ----- | 
| `1` | `new_winchester` | `48` | 

#### `State_Navigation_Itinerary`:

| `sequence_order` | `location_key` | 
| ----- | ----- | 
| *(Empty — 0 rows)* |  | 

### Expected Verification

#### State Transition:

`docked` ➔ `departing` ➔ `enroute`

#### Targeted State Verification:

| Target Address (`Table[PK].Column`) | Expected Value | Verification Note | 
| ----- | ----- | ----- | 
| `State_Inventory[munitions].hold_qty` | `4` | `2 + 2 = 4` crates in physical hold | 
| `State_Inventory[munitions].average_unit_cost` | `60.00` | MAC unchanged at `60.00` | 
| `State_Action[ACT-1001].action_status` | `ready` | Promoted `active` $\to$ `ready` (`4 >= 4 - 0`, Rule `3.3.3.3`) | 
| `State_Action[ACT-1001].priority` | `high` | Auto-promoted because `ready` at `itinerary[1]` (`Rule 4.3.1.1`) | 
| `State_Navigation_Itinerary[1].location_key` | `port_prosper` | Active destination waypoint | 
| `State_Scalars.navigation_state` | `enroute` | Exited `departing` into open sky | 

#### Report Text:

```
# 🚂 CAPTAIN'S LOG 🚀

## 📅 18 February 1905 (Day 48) · ⚓ New Winchester

**🗺️ Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 1000 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS
| System          | Status                                   |
| :---            | :---                                     |
| **Crew:**       | 🟢 10 / 10                               |
| **Hull:**       | 🟢 30 / 30                               |
| **Terror:**     | 🟢 12 / 100                              |
| **Nightmares:** | 🟢 0 / 4                                 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS           | Base                   | Perks     | Total     |
| :---                | :---:                  | :---:     | :---:     |
| - 👊 Iron           | 0                      | 0         | **0**     |
| - 👁️ Mirrors        | 0                      | 0         | **0**     |
| - ❤️ Hearts         | 0                      | 0         | **0**     |
| - 🎭 Veils          | 0                      | 0         | **0**     |
| 🔍 **AFFILIATIONS** | **Base**               | **Perks** | **Total** |
| - 🔍 Academe        | 0                      | 0         | **0**     |
| - 🍷 Bohemia        | 0                      | 0         | **0**     |
| - 👑 Establishment  | 0                      | 0         | **0**     |
| - 🎩 Villainy       | 0                      | 0         | **0**     |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** Unassigned (No Ambition Selected) — *Current Focus: Awaiting Next Milestone*

📋 **Executive Officer's Counsel (Mr. Bligh — Concept of Maneuver):**
> Final 2 Crates of Munitions are lashed down in the forward hold, Captain, bringing our *Fortress Resupply* prospect (`ACT-1001`) to full readiness (`4/4` crates aboard, promoted to high priority `‼️`). Total hold utilization stands at `10 / 12` slots, with Fuel (`3`) and Supplies (`3`) at minimum safe reserve (`⚠️`). Course is set for Port Prosper (Full Resupply 🟢).

### 🧭 Active Trajectory:
⚓ New Winchester ➔ 🟢 **Port Prosper**

### ➡️ STOP 1: Port Prosper
* ‼️ 🔑 **PROSPECT:** Fortress Resupply (`ACT-1001`) — Deliver 4 Crate of Munitions (ready)

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 10 / 12

| Trade Good Name | Physical Hold (`hold_qty`) | Hub Bank (`bank_qty`) | Unit Cost (`MAC`) | Status / Earmark | Destination Port |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **🔥 Barrel of Fuel** | 3 | 0 | 20.00 | ⚠️ | — |
| **📦 Crate of Supplies** | 3 | 0 | 40.00 | ⚠️ | — |
| **Crate of Munitions** | 4 | 0 | 60.00 | Earmarked for `ACT-1001`: Fortress Resupply (4/4) | Port Prosper |

---

## 🛞 BRIDGE ROSTER

| Station                   | Active Officer                          | Skill Perks                  | Affiliation Perks                  |
| :---                      | :---                                    | :---                         | :---                               |
| ⚓ **First Officer**      | 🔘 Vacant                               | —                            | —                                  |
| 🛞 **Quartermaster**      | 🔘 Vacant                               | —                            | —                                  |
| 🏮 **Signaller**          | 🔘 Vacant                               | —                            | —                                  |
| ⚙️ **Chief Engineer**     | 🔘 Vacant                               | —                            | —                                  |
| 🐶 **Mascot**             | 🔘 Vacant                               | —                            | —                                  |

  ---

*Respectfully submitted,*  

### 🪶 **_Mr. Bligh_**

*Executive Officer, Zephyr*

⚜️ ─── ✦ 🧭 ۞ ⚓ ✦ ─── ⚜️

```

## Test Case 11: Branched Quest Parallel Subtasks — Partial Delivery & Retained Terminal Row

**Feature Tags:** `[inventory, narrative, navigation]`

### Objective

Verifies the **Wrapper-on-Branch (`ACT-XXXX.YY`)** quest pattern (`Rule 3.3.2.2` & `3.3.3.2`) for a multi-item quest (*The Glass Greenhouse*, `ACT-2002` Root Wrapper with parallel subtasks `ACT-2002.01` for `1` `chorister_nectar` and `ACT-2002.02` for `2` `verdant_seeds`). Confirms that delivering the `1` barrel of `chorister_nectar` at Titania deletes `chorister_nectar` from `State_Inventory` (`hold_qty + bank_qty == 0` per Rule `1.1.3.1`), marks `ACT-2002.01` as `'completed'` (`quantity_delivered = 1`, retained permanently in `State_Action` per Rule `1.1.3.2`), and keeps `ACT-2002` and `ACT-2002.02` as `'active'` while departing for New Winchester.

### Input Prompt

> Update state. While docked here at Titania, I went straight to the Chief Botanist and handed over the single barrel of Chorister Nectar he requested, though I still owe him the 2 sacks of Verdant Seeds. Casting off lines toward New Winchester to search for the seeds.

### Initial State Seed

*(Baseline defaults from `State_Scalars.csv` and `data_package.json` apply to all omitted tables and scalar keys.)*

#### `State_Scalars` Overrides:

| `property_key` | `property_value` | 
| ----- | ----- | 
| `sovereigns` | `1000` | 
| `current_epoch` | `48` | 
| `terror` | `12` | 
| `current_location_key` | `titania` | 
| `last_location_visited_key` | `new_winchester` | 
| `navigation_state` | `docked` | 

#### `State_Inventory`:

| `good_key` | `hold_qty` | `bank_qty` | `average_unit_cost` | 
| ----- | ----- | ----- | ----- | 
| `fuel` | `3` | `0` | `20.00` | 
| `supplies` | `3` | `0` | `40.00` | 
| `chorister_nectar` | `1` | `0` | `120.00` | 

#### `State_Action`:

| `action_id` | `parent_action_id` | `title` | `action_type` | `action_status` | `target_location_key` | `target_entity_key` | `quantity_required` | `quantity_delivered` | `priority` | `is_pinned` | `created_epoch` | `updated_epoch` | `deadline_epoch` | `notes` | 
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | 
| `ACT-2002` | `""` | `The Glass Greenhouse` | `quest` | `active` | `""` | `""` | `0` | `0` | `routine` | `FALSE` | `45` | `45` | `""` | `Gather elements for the Chief Botanist.` | 
| `ACT-2002.01` | `ACT-2002` | `Deliver Chorister Nectar` | `quest` | `ready` | `titania` | `chorister_nectar` | `1` | `0` | `routine` | `FALSE` | `45` | `45` | `""` | `Hand over 1 Barrel of Chorister Nectar` | 
| `ACT-2002.02` | `ACT-2002` | `Deliver Verdant Seeds` | `quest` | `active` | `titania` | `verdant_seeds` | `2` | `0` | `routine` | `FALSE` | `45` | `45` | `""` | `Hand over 2 Sacks of Verdant Seeds` | 

#### `State_Navigation_History`:

| `leg_index` | `location_key` | `arrived_epoch` | 
| ----- | ----- | ----- | 
| `1` | `titania` | `48` | 

#### `State_Navigation_Itinerary`:

| `sequence_order` | `location_key` | 
| ----- | ----- | 
| *(Empty — 0 rows)* |  | 

### Expected Verification

#### State Transition:

`docked` ➔ `departing` ➔ `enroute`

#### Targeted State Verification:

| Target Address (`Table[PK].Column`) | Expected Value | Verification Note | 
| ----- | ----- | ----- | 
| `State_Inventory[chorister_nectar]` | `<Deleted>` | Non-baseline trade good deleted when `hold_qty + bank_qty == 0` (`Rule 1.1.3.1`) | 
| `State_Action[ACT-2002.01].quantity_delivered` | `1` | Fulfilled quota (`1 / 1`) | 
| `State_Action[ACT-2002.01].action_status` | `completed` | Retained in `State_Action` as terminal audit record (`Rule 1.1.3.2`) | 
| `State_Action[ACT-2002.01].updated_epoch` | `48` | Stamped with completion epoch (`Rule 3.3.4.1`) | 
| `State_Action[ACT-2002.02].action_status` | `active` | Still requires `2` `verdant_seeds` (`0 / 2`) | 
| `State_Action[ACT-2002].action_status` | `active` | Root wrapper remains `active` until all subtasks complete (`Rule 3.3.4.3`) | 
| `State_Navigation_Itinerary[1].location_key` | `new_winchester` | Active destination waypoint | 
| `State_Scalars.navigation_state` | `enroute` | Exited `departing` into open sky | 

#### Report Text:

```
# 🚂 CAPTAIN'S LOG 🚀

## 📅 18 February 1905 (Day 48) · ⚓ Titania

**🗺️ Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 1000 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS
| System          | Status                                   |
| :---            | :---                                     |
| **Crew:**       | 🟢 10 / 10                               |
| **Hull:**       | 🟢 30 / 30                               |
| **Terror:**     | 🟢 12 / 100                              |
| **Nightmares:** | 🟢 0 / 4                                 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS           | Base                   | Perks     | Total     |
| :---                | :---:                  | :---:     | :---:     |
| - 👊 Iron           | 0                      | 0         | **0**     |
| - 👁️ Mirrors        | 0                      | 0         | **0**     |
| - ❤️ Hearts         | 0                      | 0         | **0**     |
| - 🎭 Veils          | 0                      | 0         | **0**     |
| 🔍 **AFFILIATIONS** | **Base**               | **Perks** | **Total** |
| - 🔍 Academe        | 0                      | 0         | **0**     |
| - 🍷 Bohemia        | 0                      | 0         | **0**     |
| - 👑 Establishment  | 0                      | 0         | **0**     |
| - 🎩 Villainy       | 0                      | 0         | **0**     |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** Unassigned (No Ambition Selected) — *Current Focus: Awaiting Next Milestone*

📋 **Executive Officer's Counsel (Mr. Bligh — Concept of Maneuver):**
> Cargo handoff logged, Captain. We have delivered 1 Barrel of Chorister Nectar to the Chief Botanist at Titania, completing subtask `ACT-2002.01` of *The Glass Greenhouse* and clearing 1 slot in the hold (`6 / 12` used). Subtask `ACT-2002.02` remains active pending 2 Sacks of Verdant Seeds for return to Titania. We have cast off for New Winchester (Full Resupply 🟢) with Fuel (`3`) and Supplies (`3`) at our minimum reserve threshold (`⚠️`).

### 🧭 Active Trajectory:
⚓ Titania ➔ 🟢 **New Winchester**

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 6 / 12

| Trade Good Name | Physical Hold (`hold_qty`) | Hub Bank (`bank_qty`) | Unit Cost (`MAC`) | Status / Earmark | Destination Port |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **🔥 Barrel of Fuel** | 3 | 0 | 20.00 | ⚠️ | — |
| **📦 Crate of Supplies** | 3 | 0 | 40.00 | ⚠️ | — |

---

## 🛞 BRIDGE ROSTER

| Station                   | Active Officer                          | Skill Perks                  | Affiliation Perks                  |
| :---                      | :---                                    | :---                         | :---                               |
| ⚓ **First Officer**      | 🔘 Vacant                               | —                            | —                                  |
| 🛞 **Quartermaster**      | 🔘 Vacant                               | —                            | —                                  |
| 🏮 **Signaller**          | 🔘 Vacant                               | —                            | —                                  |
| ⚙️ **Chief Engineer**     | 🔘 Vacant                               | —                            | —                                  |
| 🐶 **Mascot**             | 🔘 Vacant                               | —                            | —                                  |

  ---

*Respectfully submitted,*  

### 🪶 **_Mr. Bligh_**

*Executive Officer, Zephyr*

⚜️ ─── ✦ 🧭 ۞ ⚓ ✦ ─── ⚜️

```

## Test Case 12: Partial Delivery of an Underway Prospect & Commanded Logbook Rendering

**Feature Tags:** `[inventory, ui-gates, datetime]`

### Objective

Verifies that delivering `2` of `4` required crates of `munitions` while `docked` at `port_prosper` decrements `State_Inventory[munitions].hold_qty` from `4` $\to$ `2`, increments `State_Action[ACT-1001].quantity_delivered` from `0` $\to$ `2`, and retains `action_status = 'ready'` (because remaining `hold_qty = 2` still satisfies `quantity_required - quantity_delivered = 4 - 2 = 2`). Also verifies that the explicit Captain command (`"Show me the logbook"`) renders the full `logbook.md` (`Rule 4.4.1.1`) while the vessel remains in `navigation_state = 'docked'`.

### Input Prompt

> Update state. We are docked at Port Prosper on 1905-02-19. I went to the garrison quartermaster and delivered 2 of our 4 loaded crates of Munitions. We are holding onto the other 2 crates for now while I check the local markets. Show me the logbook.

### Initial State Seed

*(Baseline defaults from `State_Scalars.csv` and `data_package.json` apply to all omitted tables and scalar keys.)*

#### `State_Scalars` Overrides:

| `property_key` | `property_value` | 
| ----- | ----- | 
| `sovereigns` | `1000` | 
| `current_epoch` | `49` | 
| `terror` | `10` | 
| `current_location_key` | `port_prosper` | 
| `last_location_visited_key` | `port_prosper` | 
| `navigation_state` | `docked` | 

#### `State_Inventory`:

| `good_key` | `hold_qty` | `bank_qty` | `average_unit_cost` | 
| ----- | ----- | ----- | ----- | 
| `fuel` | `3` | `0` | `20.00` | 
| `supplies` | `3` | `0` | `40.00` | 
| `munitions` | `4` | `0` | `60.00` | 

#### `State_Action`:

| `action_id` | `parent_action_id` | `title` | `action_type` | `action_status` | `target_location_key` | `target_entity_key` | `quantity_required` | `quantity_delivered` | `priority` | `is_pinned` | `created_epoch` | `updated_epoch` | `deadline_epoch` | `notes` | 
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | 
| `ACT-1001` | `""` | `Fortress Resupply` | `prospect` | `ready` | `port_prosper` | `munitions` | `4` | `0` | `high` | `FALSE` | `48` | `48` | `""` | `Urgent munitions shipment for the garrison.` | 

#### `State_Navigation_History`:

| `leg_index` | `location_key` | `arrived_epoch` | 
| ----- | ----- | ----- | 
| `1` | `port_prosper` | `49` | 

#### `State_Navigation_Itinerary`:

| `sequence_order` | `location_key` | 
| ----- | ----- | 
| *(Empty — 0 rows)* |  | 

### Expected Verification

#### State Transition:

`docked` ➔ `docked` (Remains docked; full logbook rendered via explicit Captain command per Rule `4.4.1.1`)

#### Targeted State Verification:

| Target Address (`Table[PK].Column`) | Expected Value | Verification Note | 
| ----- | ----- | ----- | 
| `State_Scalars.current_epoch` | `49` | `19 February 1905` = Day 49 | 
| `State_Scalars.navigation_state` | `docked` | Remains docked at Port Prosper | 
| `State_Scalars.current_location_key` | `port_prosper` | Still moored at Port Prosper | 
| `State_Inventory[munitions].hold_qty` | `2` | `4 - 2 = 2` crates remaining in hold | 
| `State_Action[ACT-1001].quantity_delivered` | `2` | Partial handoff (`2 / 4` delivered) | 
| `State_Action[ACT-1001].action_status` | `ready` | `hold_qty (2) >= (4 - 2)` keeps status `ready` (`Rule 3.3.3.3`) | 
| `State_Action[ACT-1001].updated_epoch` | `49` | Updated on partial delivery | 

#### Report Text:

```
# 🚂 CAPTAIN'S LOG 🚀

## 📅 19 February 1905 (Day 49) · ⚓ Port Prosper

**🗺️ Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 1000 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS
| System          | Status                                   |
| :---            | :---                                     |
| **Crew:**       | 🟢 10 / 10                               |
| **Hull:**       | 🟢 30 / 30                               |
| **Terror:**     | 🟢 10 / 100                              |
| **Nightmares:** | 🟢 0 / 4                                 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS           | Base                   | Perks     | Total     |
| :---                | :---:                  | :---:     | :---:     |
| - 👊 Iron           | 0                      | 0         | **0**     |
| - 👁️ Mirrors        | 0                      | 0         | **0**     |
| - ❤️ Hearts         | 0                      | 0         | **0**     |
| - 🎭 Veils          | 0                      | 0         | **0**     |
| 🔍 **AFFILIATIONS** | **Base**               | **Perks** | **Total** |
| - 🔍 Academe        | 0                      | 0         | **0**     |
| - 🍷 Bohemia        | 0                      | 0         | **0**     |
| - 👑 Establishment  | 0                      | 0         | **0**     |
| - 🎩 Villainy       | 0                      | 0         | **0**     |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** Unassigned (No Ambition Selected) — *Current Focus: Awaiting Next Milestone*

📋 **Executive Officer's Counsel (Mr. Bligh — Concept of Maneuver):**
> Partial delivery recorded at Port Prosper, Captain. Two of the 4 Crates of Munitions have been turned over to the garrison quartermaster under `ACT-1001` (*Fortress Resupply*), leaving 2 crates earmarked in our hold (`2/2` remaining required still aboard, status `ready`). Hold utilization has eased to `8 / 12` slots. Full logbook rendered at your command while we remain moored at Port Prosper with no forward itinerary yet plotted.

### 🧭 Active Trajectory:
⚓ Port Prosper ➔ *(No Forward Itinerary Plotted)*

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 8 / 12

| Trade Good Name | Physical Hold (`hold_qty`) | Hub Bank (`bank_qty`) | Unit Cost (`MAC`) | Status / Earmark | Destination Port |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **🔥 Barrel of Fuel** | 3 | 0 | 20.00 | ⚠️ | — |
| **📦 Crate of Supplies** | 3 | 0 | 40.00 | ⚠️ | — |
| **Crate of Munitions** | 2 | 0 | 60.00 | Earmarked for `ACT-1001`: Fortress Resupply (2/2) | Port Prosper |

---

## 🛞 BRIDGE ROSTER

| Station                   | Active Officer                          | Skill Perks                  | Affiliation Perks                  |
| :---                      | :---                                    | :---                         | :---                               |
| ⚓ **First Officer**      | 🔘 Vacant                               | —                            | —                                  |
| 🛞 **Quartermaster**      | 🔘 Vacant                               | —                            | —                                  |
| 🏮 **Signaller**          | 🔘 Vacant                               | —                            | —                                  |
| ⚙️ **Chief Engineer**     | 🔘 Vacant                               | —                            | —                                  |
| 🐶 **Mascot**             | 🔘 Vacant                               | —                            | —                                  |

  ---

*Respectfully submitted,*  

### 🪶 **_Mr. Bligh_**

*Executive Officer, Zephyr*

⚜️ ─── ✦ 🧭 ۞ ⚓ ✦ ─── ⚜️

```

## Test Case 13: Officer Tier Promotion, Dynamic Stat Perks & Secondment Readiness

**Feature Tags:** `[officers, datetime, navigation]`

### Objective

Verifies in-place Officer Promotion (`Rule 3.4.2.1`: updating `fortunate_navigator` $\to$ `stalwart_navigator` in `State_Officers` where `Ref_Officers.parent_key == 'fortunate_navigator'`), runtime aggregation of active officer perks (`Rule 3.4.4`: `stalwart_navigator` + `inconvenient_aunt` + `inadvisably_big_dog` = `+17 Iron`, `+2 Mirrors`, `+1 Bohemia`, `+2 Establishment`; `unassigned` and `seconded` officers excluded), secondment readiness sync (`Rule 3.3.3.3`: `ACT-1011` promotes `active` $\to$ `ready` since `current_epoch (417) >= deadline_epoch (400)`), and rendering of `### ⏳ SECONDMENT OUTLOOK` (`🟢 **Ready for Pickup**`) on departure from `london` to `albion_transit_relay` (`🟡` Partial Resupply in `Ref_Location_Goods.csv`) on `22 February 1906` (Day 417).

### Input Prompt

> Update state. London — 22 February 1906. Our First Officer has promoted to "Stalwart Navigator." Ready the crew and cast lines off for the Albion Transit Relay.

### Initial State Seed

*(Baseline defaults from `State_Scalars.csv` and `data_package.json` apply to all omitted tables and scalar keys.)*

#### `State_Scalars` Overrides:

| `property_key` | `property_value` | 
| ----- | ----- | 
| `sovereigns` | `1000` | 
| `current_epoch` | `417` | 
| `terror` | `12` | 
| `skill_iron` | `10` | 
| `skill_mirrors` | `18` | 
| `skill_hearts` | `25` | 
| `skill_veils` | `7` | 
| `current_location_key` | `london` | 
| `last_location_visited_key` | `london` | 
| `navigation_state` | `docked` | 

#### `State_Inventory`:

| `good_key` | `hold_qty` | `bank_qty` | `average_unit_cost` | 
| ----- | ----- | ----- | ----- | 
| `fuel` | `3` | `0` | `20.00` | 
| `supplies` | `3` | `0` | `40.00` | 

#### `State_Officers`:

| `officer_key` | `officer_status` | 
| ----- | ----- | 
| `fortunate_navigator` | `active` | 
| `inconvenient_aunt` | `active` | 
| `inadvisably_big_dog` | `active` | 
| `incautious_driver` | `unassigned` | 
| `rat_brigade` | `unassigned` | 
| `repentant_devil` | `seconded` | 

#### `State_Action`:

| `action_id` | `parent_action_id` | `title` | `action_type` | `action_status` | `target_location_key` | `target_entity_key` | `quantity_required` | `quantity_delivered` | `priority` | `is_pinned` | `created_epoch` | `updated_epoch` | `deadline_epoch` | `notes` | 
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | 
| `ACT-1011` | `""` | `Secondment: Repentant Devil` | `secondment` | `active` | `london` | `repentant_devil` | `0` | `0` | `routine` | `FALSE` | `366` | `366` | `400` | `Generates prospects near the Albion Transit Relay.` | 

#### `State_Navigation_History`:

| `leg_index` | `location_key` | `arrived_epoch` | 
| ----- | ----- | ----- | 
| `1` | `london` | `417` | 

#### `State_Navigation_Itinerary`:

| `sequence_order` | `location_key` | 
| ----- | ----- | 
| *(Empty — 0 rows)* |  | 

### Expected Verification

#### State Transition:

`docked` ➔ `departing` ➔ `enroute`

#### Targeted State Verification:

| Target Address (`Table[PK].Column`) | Expected Value | Verification Note | 
| ----- | ----- | ----- | 
| `State_Scalars.current_epoch` | `417` | `22 February 1906` = $365 + 31 + 21 = \text{Day } 417$ | 
| `State_Officers[stalwart_navigator].officer_status` | `active` | Promoted in-place from `fortunate_navigator` (`Rule 3.4.2.1`) | 
| `State_Officers[fortunate_navigator]` | `<Replaced>` | Replaced in-place by `stalwart_navigator` | 
| `State_Action[ACT-1011].action_status` | `ready` | Auto-promoted since `current_epoch (417) >= deadline_epoch (400)` (`Rule 3.3.3.3`) | 
| `State_Navigation_Itinerary[1].location_key` | `albion_transit_relay` | Active destination waypoint | 
| `State_Scalars.navigation_state` | `enroute` | Exited `departing` into open sky | 

#### Report Text:

```
# 🚂 CAPTAIN'S LOG 🚀

## 📅 22 February 1906 (Day 417) · ⚓ London

**🗺️ Region:** Albion | **👤 Captain:** Sinclair | **🪙 Wallet:** 1000 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS
| System          | Status                                   |
| :---            | :---                                     |
| **Crew:**       | 🟢 10 / 10                               |
| **Hull:**       | 🟢 30 / 30                               |
| **Terror:**     | 🟢 12 / 100                              |
| **Nightmares:** | 🟢 0 / 4                                 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS           | Base                   | Perks     | Total     |
| :---                | :---:                  | :---:     | :---:     |
| - 👊 Iron           | 10                     | +17       | **27**    |
| - 👁️ Mirrors        | 18                     | +2        | **20**    |
| - ❤️ Hearts         | 25                     | 0         | **25**    |
| - 🎭 Veils          | 7                      | 0         | **7**     |
| 🔍 **AFFILIATIONS** | **Base**               | **Perks** | **Total** |
| - 🔍 Academe        | 0                      | 0         | **0**     |
| - 🍷 Bohemia        | 0                      | +1        | **1**     |
| - 👑 Establishment  | 0                      | +2        | **2**     |
| - 🎩 Villainy       | 0                      | 0         | **0**     |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** Unassigned (No Ambition Selected) — *Current Focus: Awaiting Next Milestone*

📋 **Executive Officer's Counsel (Mr. Bligh — Concept of Maneuver):**
> Congratulations to our First Officer on stepping into the rank of **Stalwart Navigator** (`+10 Iron`, `+1 Bohemia`, `+1 Establishment`), bringing our total bridge Iron to `27`. Note that the **Repentant Devil** (`ACT-1011`) has completed his ashore assignment in London (unlocked 5 February 1906 / Day 400) and is ready for pickup whenever we return to the capital. We have slipped moorings for the Albion Transit Relay (Partial Resupply 🟡 — exports Fuel only, no Supplies), with Fuel (`3`) and Supplies (`3`) sitting right at our minimum reserve line (`⚠️`).

### 🧭 Active Trajectory:
⚓ London ➔ 🟡 **Albion Transit Relay**

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 6 / 12

| Trade Good Name | Physical Hold (`hold_qty`) | Hub Bank (`bank_qty`) | Unit Cost (`MAC`) | Status / Earmark | Destination Port |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **🔥 Barrel of Fuel** | 3 | 0 | 20.00 | ⚠️ | — |
| **📦 Crate of Supplies** | 3 | 0 | 40.00 | ⚠️ | — |

---

## 🛞 BRIDGE ROSTER

| Station                   | Active Officer                          | Skill Perks                  | Affiliation Perks                  |
| :---                      | :---                                    | :---                         | :---                               |
| ⚓ **First Officer**      | Stalwart Navigator                      | +10 Iron                     | +1 Bohemia / +1 Establishment      |
| 🛞 **Quartermaster**      | Inconvenient Aunt                       | +6 Iron / +2 Mirrors         | +1 Establishment                   |
| 🏮 **Signaller**          | 🔘 Vacant                               | —                            | —                                  |
| ⚙️ **Chief Engineer**     | 🔘 Vacant                               | —                            | —                                  |
| 🐶 **Mascot**             | Inadvisably Big Dog                     | +1 Iron                      | —                                  |

### ⏳ SECONDMENT OUTLOOK
* **Repentant Devil** (Signaller) ➔ Ashore at **London** (`ACT-1011`)
  * *Status:* 🟢 **Ready for Pickup** (Unlocked: 5 February 1906)
  * *Assignment & Expected Outcome:* Generates prospects near the Albion Transit Relay.

  ---

*Respectfully submitted,*  

### 🪶 **_Mr. Bligh_**

*Executive Officer, Zephyr*

⚜️ ─── ✦ 🧭 ۞ ⚓ ✦ ─── ⚜️

```

## Test Case 14: Multi-State Compound Turn Pipeline & Append-Only History

**Feature Tags:** `[fsm, navigation, datetime, economy]`

### Objective

Tests the Multi-State Compound Turn Pipeline (`Rule 2.1.2`): transitions sequentially from `enroute` ➔ `arriving` (at `lustrum` on `1905-01-20` = Day 19, deducting `1` fuel and appending `leg_index = 4` to Class C `State_Navigation_History` while preserving legs `1..3`) ➔ `docked` (selling `2` `unseasoned_hours` for `+160` Sovereigns and deleting the zero-quantity `unseasoned_hours` row, then buying `2` `fuel` for `-40` Sovereigns) ➔ `departing` (plotting `port_avon` and rendering `logbook.md`) ➔ `enroute` (`current_location_key = ""`, `last_location_visited_key = "lustrum"`).

### Input Prompt

> Update state. Arrived at Lustrum on 1905-01-20 with 1 fuel spent. While docked, we sold our 2 crates of Unseasoned Hours for 160 Sovereigns total, bought 2 Barrels of Fuel at standard cost (20 each), and immediately cast off lines for Port Avon.

### Initial State Seed

*(Baseline defaults from `State_Scalars.csv` and `data_package.json` apply to all omitted tables and scalar keys.)*

#### `State_Scalars` Overrides:

| `property_key` | `property_value` | 
| ----- | ----- | 
| `sovereigns` | `500` | 
| `current_epoch` | `16` | 
| `current_crew` | `8` | 
| `terror` | `10` | 
| `current_location_key` | `""` | 
| `last_location_visited_key` | `carillon` | 
| `navigation_state` | `enroute` | 

#### `State_Inventory`:

| `good_key` | `hold_qty` | `bank_qty` | `average_unit_cost` | 
| ----- | ----- | ----- | ----- | 
| `fuel` | `4` | `0` | `20.00` | 
| `supplies` | `3` | `0` | `40.00` | 
| `unseasoned_hours` | `2` | `0` | `40.00` | 

#### `State_Navigation_History`:

| `leg_index` | `location_key` | `arrived_epoch` | 
| ----- | ----- | ----- | 
| `1` | `port_prosper` | `7` | 
| `2` | `new_winchester` | `10` | 
| `3` | `carillon` | `16` | 

#### `State_Navigation_Itinerary`:

| `sequence_order` | `location_key` | 
| ----- | ----- | 
| `1` | `lustrum` | 

### Expected Verification

#### State Transition:

`enroute` ➔ `arriving` ➔ `docked` ➔ `departing` ➔ `enroute`

#### Targeted State Verification:

| Target Address (`Table[PK].Column`) | Expected Value | Verification Note | 
| ----- | ----- | ----- | 
| `State_Scalars.current_epoch` | `19` | `20 January 1905` = Day 19 | 
| `State_Scalars.sovereigns` | `620` | `500 + 160 - (2 * 20) = 620` Sovereigns | 
| `State_Scalars.fuel_used_last_leg` | `1` | Recorded leg burn | 
| `State_Scalars.navigation_state` | `enroute` | Completed compound turn back into open sky | 
| `State_Scalars.current_location_key` | `""` | Cleared upon entering `enroute` | 
| `State_Scalars.last_location_visited_key` | `lustrum` | Updated on departure from Lustrum | 
| `State_Inventory[fuel].hold_qty` | `5` | `4 - 1 + 2 = 5` barrels (`🟢`) | 
| `State_Inventory[unseasoned_hours]` | `<Deleted>` | Deleted when `hold_qty + bank_qty == 0` (`Rule 1.1.3.1`) | 
| `State_Navigation_History[1].location_key` | `port_prosper` | Preserved — `State_Navigation_History` is Class C Append-Only (`Rule 1.1.2.1`) | 
| `State_Navigation_History[4].location_key` | `lustrum` | Appended leg `4` | 
| `State_Navigation_History[4].arrived_epoch` | `19` | Stamped with arrival Day 19 | 
| `State_Navigation_Itinerary[1].location_key` | `port_avon` | New active destination waypoint | 

#### Report Text:

```
# 🚂 CAPTAIN'S LOG 🚀

## 📅 20 January 1905 (Day 19) · ⚓ Lustrum

**🗺️ Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 620 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS
| System          | Status                                   |
| :---            | :---                                     |
| **Crew:**       | 🟢 8 / 10                                |
| **Hull:**       | 🟢 30 / 30                               |
| **Terror:**     | 🟢 10 / 100                              |
| **Nightmares:** | 🟢 0 / 4                                 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS           | Base                   | Perks     | Total     |
| :---                | :---:                  | :---:     | :---:     |
| - 👊 Iron           | 0                      | 0         | **0**     |
| - 👁️ Mirrors        | 0                      | 0         | **0**     |
| - ❤️ Hearts         | 0                      | 0         | **0**     |
| - 🎭 Veils          | 0                      | 0         | **0**     |
| 🔍 **AFFILIATIONS** | **Base**               | **Perks** | **Total** |
| - 🔍 Academe        | 0                      | 0         | **0**     |
| - 🍷 Bohemia        | 0                      | 0         | **0**     |
| - 👑 Establishment  | 0                      | 0         | **0**     |
| - 🎩 Villainy       | 0                      | 0         | **0**     |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** Unassigned (No Ambition Selected) — *Current Focus: Awaiting Next Milestone*

📋 **Executive Officer's Counsel (Mr. Bligh — Concept of Maneuver):**
> Rapid turnaround completed at Lustrum, Captain. I logged our arrival on 20 January 1905 (`-1` barrel of fuel burned en route), cleared our 2 Crates of Unseasoned Hours at the exchange for `+160` Sovereigns, and bunkered 2 fresh Barrels of Fuel (`-40` Sovereigns, bringing our wallet to `620` Sovereigns). We are now back underway in the open sky bound for Port Avon (Full Resupply 🟢) with 5 barrels of fuel (`🟢`) and 3 crates of supplies (`⚠️` at minimum reserve).

### 🧭 Active Trajectory:
⚓ Lustrum ➔ 🟢 **Port Avon**

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 8 / 12

| Trade Good Name | Physical Hold (`hold_qty`) | Hub Bank (`bank_qty`) | Unit Cost (`MAC`) | Status / Earmark | Destination Port |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **🔥 Barrel of Fuel** | 5 | 0 | 20.00 | 🟢 | — |
| **📦 Crate of Supplies** | 3 | 0 | 40.00 | ⚠️ | — |

---

## 🛞 BRIDGE ROSTER

| Station                   | Active Officer                          | Skill Perks                  | Affiliation Perks                  |
| :---                      | :---                                    | :---                         | :---                               |
| ⚓ **First Officer**      | 🔘 Vacant                               | —                            | —                                  |
| 🛞 **Quartermaster**      | 🔘 Vacant                               | —                            | —                                  |
| 🏮 **Signaller**          | 🔘 Vacant                               | —                            | —                                  |
| ⚙️ **Chief Engineer**     | 🔘 Vacant                               | —                            | —                                  |
| 🐶 **Mascot**             | 🔘 Vacant                               | —                            | —                                  |

  ---

*Respectfully submitted,*  

### 🪶 **_Mr. Bligh_**

*Executive Officer, Zephyr*

⚜️ ─── ✦ 🧭 ۞ ⚓ ✦ ─── ⚜️

```

## Test Case 15: Economic Core — Moving Average Unit Cost (MAC) & Full Hold Saturation

**Feature Tags:** `[economy, inventory, datetime]`

### Objective

Tests the Moving Average Unit Cost formula (`Rule 3.1.3.1`): holding `2` crates of `munitions` at `60.00` MAC and purchasing `4` additional crates at `30.00` each recalculates `average_unit_cost` to $\frac{(2 \times 60.00) + (4 \times 30.00)}{2 + 4} = 40.00$. Verifies atomic sovereign deduction ($1000 - 120 - 40 = 840$), full physical hold saturation (`12 / 12` slots: `3` fuel + `3` supplies + `6` munitions), and calendar evaluation (`30 April 1905` = Day 119) on departure from London to Brabazon Workworld.

### Input Prompt

> Update state. We are docked at London on 1905-04-30. We currently hold 2 crates of Munitions with an average cost of 60 Sovereigns each. The Ministries are offering surplus munitions at a discount: we just purchased 4 additional crates of Munitions for 30 Sovereigns each. We also picked up 2 barrels of Fuel at 20 each, and now we are casting off lines for Brabazon Workworld.

### Initial State Seed

*(Baseline defaults from `State_Scalars.csv` and `data_package.json` apply to all omitted tables and scalar keys.)*

#### `State_Scalars` Overrides:

| `property_key` | `property_value` | 
| ----- | ----- | 
| `sovereigns` | `1000` | 
| `current_epoch` | `119` | 
| `current_crew` | `8` | 
| `terror` | `15` | 
| `current_location_key` | `london` | 
| `last_location_visited_key` | `london` | 
| `navigation_state` | `docked` | 

#### `State_Inventory`:

| `good_key` | `hold_qty` | `bank_qty` | `average_unit_cost` | 
| ----- | ----- | ----- | ----- | 
| `fuel` | `1` | `0` | `20.00` | 
| `supplies` | `3` | `0` | `40.00` | 
| `munitions` | `2` | `0` | `60.00` | 

#### `State_Navigation_History`:

| `leg_index` | `location_key` | `arrived_epoch` | 
| ----- | ----- | ----- | 
| `1` | `london` | `119` | 

#### `State_Navigation_Itinerary`:

| `sequence_order` | `location_key` | 
| ----- | ----- | 
| *(Empty — 0 rows)* |  | 

### Expected Verification

#### State Transition:

`docked` ➔ `departing` ➔ `enroute`

#### Targeted State Verification:

| Target Address (`Table[PK].Column`) | Expected Value | Verification Note | 
| ----- | ----- | ----- | 
| `State_Scalars.current_epoch` | `119` | `30 April 1905` = $31 + 28 + 31 + 29 = \text{Day } 119$ | 
| `State_Scalars.sovereigns` | `840` | `1000 - (4 * 30) - (2 * 20) = 840` | 
| `State_Inventory[fuel].hold_qty` | `3` | `1 + 2 = 3` barrels (`⚠️` at minimum reserve) | 
| `State_Inventory[fuel].average_unit_cost` | `20.00` | $\frac{(1 \times 20) + (2 \times 20)}{3} = 20.00$ | 
| `State_Inventory[munitions].hold_qty` | `6` | `2 + 4 = 6` crates in hold | 
| `State_Inventory[munitions].average_unit_cost` | `40.00` | $\frac{(2 \times 60) + (4 \times 30)}{6} = 40.00$ (`Rule 3.1.3.1`) | 
| `State_Navigation_Itinerary[1].location_key` | `brabazon_workworld` | Active destination waypoint | 
| `State_Scalars.navigation_state` | `enroute` | Exited `departing` into open sky | 

#### Report Text:

```
# 🚂 CAPTAIN'S LOG 🚀

## 📅 30 April 1905 (Day 119) · ⚓ London

**🗺️ Region:** Albion | **👤 Captain:** Sinclair | **🪙 Wallet:** 840 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS
| System          | Status                                   |
| :---            | :---                                     |
| **Crew:**       | 🟢 8 / 10                                |
| **Hull:**       | 🟢 30 / 30                               |
| **Terror:**     | 🟢 15 / 100                              |
| **Nightmares:** | 🟢 0 / 4                                 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS           | Base                   | Perks     | Total     |
| :---                | :---:                  | :---:     | :---:     |
| - 👊 Iron           | 0                      | 0         | **0**     |
| - 👁️ Mirrors        | 0                      | 0         | **0**     |
| - ❤️ Hearts         | 0                      | 0         | **0**     |
| - 🎭 Veils          | 0                      | 0         | **0**     |
| 🔍 **AFFILIATIONS** | **Base**               | **Perks** | **Total** |
| - 🔍 Academe        | 0                      | 0         | **0**     |
| - 🍷 Bohemia        | 0                      | 0         | **0**     |
| - 👑 Establishment  | 0                      | 0         | **0**     |
| - 🎩 Villainy       | 0                      | 0         | **0**     |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** Unassigned (No Ambition Selected) — *Current Focus: Awaiting Next Milestone*

📋 **Executive Officer's Counsel (Mr. Bligh — Concept of Maneuver):**
> Mr. Bligh at the ledger. We have taken aboard 4 surplus Crates of Munitions at 30 Sovereigns apiece (`-120` Sovereigns), bringing our total stock to 6 crates and diluting our Moving Average Unit Cost from `60.00` down to `40.00` Sovereigns. We also bunkered 2 Barrels of Fuel (`-40` Sovereigns), restoring our fuel and supply reserves to the 3-unit minimum threshold (`⚠️`). Note that our hold is now packed to its absolute ceiling at `12 / 12` slots, leaving zero free room for mid-sky salvage until we offload cargo at Brabazon Workworld (Full Resupply 🟢).

### 🧭 Active Trajectory:
⚓ London ➔ 🟢 **Brabazon Workworld**

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 12 / 12

| Trade Good Name | Physical Hold (`hold_qty`) | Hub Bank (`bank_qty`) | Unit Cost (`MAC`) | Status / Earmark | Destination Port |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **🔥 Barrel of Fuel** | 3 | 0 | 20.00 | ⚠️ | — |
| **📦 Crate of Supplies** | 3 | 0 | 40.00 | ⚠️ | — |
| **Crate of Munitions** | 6 | 0 | 40.00 | Unassigned Cargo | — |

---

## 🛞 BRIDGE ROSTER

| Station                   | Active Officer                          | Skill Perks                  | Affiliation Perks                  |
| :---                      | :---                                    | :---                         | :---                               |
| ⚓ **First Officer**      | 🔘 Vacant                               | —                            | —                                  |
| 🛞 **Quartermaster**      | 🔘 Vacant                               | —                            | —                                  |
| 🏮 **Signaller**          | 🔘 Vacant                               | —                            | —                                  |
| ⚙️ **Chief Engineer**     | 🔘 Vacant                               | —                            | —                                  |
| 🐶 **Mascot**             | 🔘 Vacant                               | —                            | —                                  |

  ---

*Respectfully submitted,*  

### 🪶 **_Mr. Bligh_**

*Executive Officer, Zephyr*

⚜️ ─── ✦ 🧭 ۞ ⚓ ✦ ─── ⚜️

```

## Test Case 16: Inter-Region Transit Relay Trajectory & Toll Option Evaluation

**Feature Tags:** `[navigation, datetime]`

### Objective

Tests inter-region trajectory planning and `Ref_TransitTolls.csv` advisory lookup (`Rule 2.2.3.1` & `4.1.5.2`). Verifies that plotting a 2-stop route from `new_winchester` through `albion_transit_relay` (`🟡` Partial Resupply — exports `fuel` only) to `london` (`🟢` Full Resupply) confirms `State_Scalars.albion_transit_permit == TRUE`, details the playable crossing options in `Ref_TransitTolls.csv` (`Option 1 First Class`: `1` `ministry_stamped_permit`, `2` days, `-15` terror; `Option 2 Second Class`: `2` `unseasoned_hours`, `2` days, `-5` terror; `Option 3 Third Class`: `200` `sovereigns`, `2` days, `+5` terror), and does **not** prematurely deduct relay tolls when departing `new_winchester` (`15 June 1905` = Day 165).

### Input Prompt

> Update state. We are docked at New Winchester on 1905-06-15. We hold the necessary Albion Transit Permit stamped by the Ministry. Plot an inter-region course out through the Albion Transit Relay and straight on to London. Review our gate clearance and let me know our toll options before we set out.

### Initial State Seed

*(Baseline defaults from `State_Scalars.csv` and `data_package.json` apply to all omitted tables and scalar keys.)*

#### `State_Scalars` Overrides:

| `property_key` | `property_value` | 
| ----- | ----- | 
| `sovereigns` | `1200` | 
| `current_epoch` | `165` | 
| `current_crew` | `9` | 
| `terror` | `10` | 
| `skill_iron` | `10` | 
| `skill_mirrors` | `5` | 
| `skill_hearts` | `5` | 
| `skill_veils` | `5` | 
| `affiliation_establishment` | `1` | 
| `albion_transit_permit` | `TRUE` | 
| `possession_ministry_stamped_permit` | `1` | 
| `current_location_key` | `new_winchester` | 
| `last_location_visited_key` | `new_winchester` | 
| `navigation_state` | `docked` | 

#### `State_Inventory`:

| `good_key` | `hold_qty` | `bank_qty` | `average_unit_cost` | 
| ----- | ----- | ----- | ----- | 
| `fuel` | `4` | `0` | `20.00` | 
| `supplies` | `4` | `0` | `40.00` | 
| `unseasoned_hours` | `2` | `0` | `80.00` | 

#### `State_Navigation_History`:

| `leg_index` | `location_key` | `arrived_epoch` | 
| ----- | ----- | ----- | 
| `1` | `new_winchester` | `160` | 

#### `State_Navigation_Itinerary`:

| `sequence_order` | `location_key` | 
| ----- | ----- | 
| *(Empty — 0 rows)* |  | 

### Expected Verification

#### State Transition:

`docked` ➔ `departing` ➔ `enroute`

#### Targeted State Verification:

| Target Address (`Table[PK].Column`) | Expected Value | Verification Note | 
| ----- | ----- | ----- | 
| `State_Scalars.current_epoch` | `165` | `15 June 1905` = $31 + 28 + 31 + 30 + 31 + 14 = \text{Day } 165$ | 
| `State_Scalars.albion_transit_permit` | `TRUE` | Required regional permit verified | 
| `State_Scalars.sovereigns` | `1200` | Unchanged — relay toll not deducted until departing the relay (`Rule 2.2.3.3`) | 
| `State_Scalars.possession_ministry_stamped_permit` | `1` | Unchanged prior to relay gate engagement | 
| `State_Inventory[unseasoned_hours].hold_qty` | `2` | Unchanged prior to relay gate engagement | 
| `State_Navigation_Itinerary[1].location_key` | `albion_transit_relay` | Contiguous 1-indexed Stop 1 | 
| `State_Navigation_Itinerary[2].location_key` | `london` | Contiguous 1-indexed Stop 2 | 
| `State_Scalars.navigation_state` | `enroute` | Exited `departing` into open sky | 

#### Report Text:

```
# 🚂 CAPTAIN'S LOG 🚀

## 📅 15 June 1905 (Day 165) · ⚓ New Winchester

**🗺️ Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 1200 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS
| System          | Status                                   |
| :---            | :---                                     |
| **Crew:**       | 🟢 9 / 10                                |
| **Hull:**       | 🟢 30 / 30                               |
| **Terror:**     | 🟢 10 / 100                              |
| **Nightmares:** | 🟢 0 / 4                                 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS           | Base                   | Perks     | Total     |
| :---                | :---:                  | :---:     | :---:     |
| - 👊 Iron           | 10                     | 0         | **10**    |
| - 👁️ Mirrors        | 5                      | 0         | **5**     |
| - ❤️ Hearts         | 5                      | 0         | **5**     |
| - 🎭 Veils          | 5                      | 0         | **5**     |
| 🔍 **AFFILIATIONS** | **Base**               | **Perks** | **Total** |
| - 🔍 Academe        | 0                      | 0         | **0**     |
| - 🍷 Bohemia        | 0                      | 0         | **0**     |
| - 👑 Establishment  | 1                      | 0         | **1**     |
| - 🎩 Villainy       | 0                      | 0         | **0**     |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** Unassigned (No Ambition Selected) — *Current Focus: Awaiting Next Milestone*

📋 **Executive Officer's Counsel (Mr. Bligh — Concept of Maneuver):**
> Inter-region trajectory plotted from New Winchester to the Albion Transit Relay (Partial Resupply 🟡 — exports Fuel only) and onward to London (Full Resupply 🟢). Our **Albion Transit Permit** is in order. Upon reaching the relay gate, we have three lawful passage options currently funded in our manifest: **Option 1 (First Class)** using our 1 Ministry Stamped Permit (`2` days elapsed, `-15` Terror), **Option 2 (Second Class)** using our 2 Crates of Unseasoned Hours (`2` days elapsed, `-5` Terror), or **Option 3 (Third Class)** for 200 Sovereigns (`2` days elapsed, `+5` Terror). No relay toll is deducted until we engage the relay's sequencer-wheels.

### 🧭 Active Trajectory:
⚓ New Winchester ➔ 🟡 **Albion Transit Relay** ➔ 🟢 London

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 10 / 12

| Trade Good Name | Physical Hold (`hold_qty`) | Hub Bank (`bank_qty`) | Unit Cost (`MAC`) | Status / Earmark | Destination Port |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **🔥 Barrel of Fuel** | 4 | 0 | 20.00 | 🟢 | — |
| **📦 Crate of Supplies** | 4 | 0 | 40.00 | 🟢 | — |
| **Crate of Unseasoned Hours** | 2 | 0 | 80.00 | Unassigned Cargo | — |

---

## 🛞 BRIDGE ROSTER

| Station                   | Active Officer                          | Skill Perks                  | Affiliation Perks                  |
| :---                      | :---                                    | :---                         | :---                               |
| ⚓ **First Officer**      | 🔘 Vacant                               | —                            | —                                  |
| 🛞 **Quartermaster**      | 🔘 Vacant                               | —                            | —                                  |
| 🏮 **Signaller**          | 🔘 Vacant                               | —                            | —                                  |
| ⚙️ **Chief Engineer**     | 🔘 Vacant                               | —                            | —                                  |
| 🐶 **Mascot**             | 🔘 Vacant                               | —                            | —                                  |

  ---

*Respectfully submitted,*  

### 🪶 **_Mr. Bligh_**

*Executive Officer, Zephyr*

⚜️ ─── ✦ 🧭 ۞ ⚓ ✦ ─── ⚜️

```

## Test Case 17: Navigation Itinerary Pop, Contiguous Re-Indexing & Append-Only History

**Feature Tags:** `[fsm, navigation, ui-gates, datetime]`

### Objective

Verifies the kinetic arrival transition `enroute` ➔ `arriving` ➔ `docked` at `lustrum` (`1905-03-05` = $31 + 28 + 4 = \text{Day } 63$). Confirms that `lustrum` (`sequence_order == 1`) is popped from `State_Navigation_Itinerary` while the remaining forward stops (`titania`, `new_winchester`) are atomically re-indexed to `sequence_order = 1, 2` (`Rule 2.2.1.1` & `2.3.3.1`). Verifies that `State_Navigation_History` (Class C Append-Only, `Rule 1.1.2.1` & `2.3.3.2`) appends `leg_index = 4` (`lustrum`, `arrived_epoch = 63`) while permanently retaining legs `1..3`. Confirms `logbook.md` suppression on arrival.

### Input Prompt

> Update state. We just dropped mooring lines and arrived at Lustrum on 1905-03-05. Fuel burn on this leg was 2. What's the lay of the land here, First Mate?

### Initial State Seed

*(Baseline defaults from `State_Scalars.csv` and `data_package.json` apply to all omitted tables and scalar keys.)*

#### `State_Scalars` Overrides:

| `property_key` | `property_value` | 
| ----- | ----- | 
| `sovereigns` | `1100` | 
| `current_epoch` | `61` | 
| `current_crew` | `9` | 
| `terror` | `15` | 
| `skill_iron` | `10` | 
| `skill_mirrors` | `5` | 
| `skill_hearts` | `5` | 
| `skill_veils` | `5` | 
| `current_location_key` | `""` | 
| `last_location_visited_key` | `port_avon` | 
| `navigation_state` | `enroute` | 

#### `State_Inventory`:

| `good_key` | `hold_qty` | `bank_qty` | `average_unit_cost` | 
| ----- | ----- | ----- | ----- | 
| `fuel` | `5` | `0` | `20.00` | 
| `supplies` | `4` | `0` | `40.00` | 

#### `State_Navigation_History`:

| `leg_index` | `location_key` | `arrived_epoch` | 
| ----- | ----- | ----- | 
| `1` | `new_winchester` | `45` | 
| `2` | `port_prosper` | `52` | 
| `3` | `port_avon` | `58` | 

#### `State_Navigation_Itinerary`:

| `sequence_order` | `location_key` | 
| ----- | ----- | 
| `1` | `lustrum` | 
| `2` | `titania` | 
| `3` | `new_winchester` | 

### Expected Verification

#### State Transition:

`enroute` ➔ `arriving` ➔ `docked`

#### Targeted State Verification:

| Target Address (`Table[PK].Column`) | Expected Value | Verification Note | 
| ----- | ----- | ----- | 
| `State_Scalars.current_epoch` | `63` | `5 March 1905` = $31 + 28 + 4 = \text{Day } 63$ | 
| `State_Scalars.fuel_used_last_leg` | `2` | Recorded leg burn | 
| `State_Scalars.navigation_state` | `docked` | Completed arrival transition | 
| `State_Scalars.current_location_key` | `lustrum` | Active docked port | 
| `State_Inventory[fuel].hold_qty` | `3` | `5 - 2 = 3` barrels remaining (`⚠️`) | 
| `State_Navigation_History[1].location_key` | `new_winchester` | Retained permanently (Class C Append-Only) | 
| `State_Navigation_History[4].location_key` | `lustrum` | Appended leg `4` | 
| `State_Navigation_History[4].arrived_epoch` | `63` | Stamped with arrival Day 63 | 
| `State_Navigation_Itinerary[1].location_key` | `titania` | Re-indexed from `2` $\to$ `1` (`Rule 2.3.3.1`) | 
| `State_Navigation_Itinerary[2].location_key` | `new_winchester` | Re-indexed from `3` $\to$ `2` (`Rule 2.3.3.1`) | 
| `State_Navigation_Itinerary.row_count` | `2` | Only 2 forward stops remain | 

#### Report Text:

*(Full Markdown `logbook.md` is strictly suppressed during `arriving` and `docked` turns per Rule `4.4.1.2`.)*

> **Mr. Bligh's Bridge Micro-Briefing:**
> "Mooring lines secured at the icy quays of Lustrum on 5 March 1905 (Day 63), Captain. Two barrels of fuel have been deducted from the hold manifest for the transit burn, leaving 3 barrels of fuel (`⚠️` at minimum reserve) and 4 crates of supplies (`🟢`).
>
> High in the freezing peaks of the Mother of Mountains, prospectors and miners quarry raw, unseasoned hours from the rockface. Station services here include **Crew Recruitment** (`9 / 10` aboard), and local merchants export **Barrels of Fuel**, **Crates of Supplies**, and **Crates of Unseasoned Hours** (note: there is no drydock shipyard at Lustrum). Our bazaar bargain window here is open for a fresh market scan whenever you inspect the exchange. Next on our sky-chart lie **Titania** (Stop 1) and **New Winchester** (Stop 2)."

## Test Case 18: Two-Table Bazaar Discovery & Bargain Stock Logging

**Feature Tags:** `[startup-recovery, economy, ui-gates]`

### Objective

Verifies the Two-Table Bazaar Cycle (`Rule 3.2.1`) upon docking at a commercial station (`new_winchester`) on `9 January 1905` (Day 8) and reporting fresh bazaar bargains (`5` crates of `munitions` at `60` Sovereigns each). Confirms that `State_Discovered_Locations[new_winchester].bazaar_reset_epoch` is set to `38` (`current_epoch + 30`), a corresponding bargain row is inserted into `State_Bazaar_Stock` (`expiration_epoch = 38`), and `logbook.md` is suppressed while `docked`.

### Input Prompt

> Update state. We've docked in New Winchester on 9 Jan 1905. The bazaar market refreshes in 30 days and currently lists 5 crates of munitions at 60 Sovereigns each.

### Initial State Seed

*(Baseline defaults from `State_Scalars.csv` and `data_package.json` apply to all omitted tables and scalar keys.)*

#### `State_Scalars` Overrides:

| `property_key` | `property_value` | 
| ----- | ----- | 
| `sovereigns` | `1000` | 
| `current_epoch` | `5` | 
| `current_crew` | `8` | 
| `current_location_key` | `""` | 
| `last_location_visited_key` | `port_avon` | 
| `navigation_state` | `enroute` | 

#### `State_Inventory`:

| `good_key` | `hold_qty` | `bank_qty` | `average_unit_cost` | 
| ----- | ----- | ----- | ----- | 
| `fuel` | `3` | `0` | `20.00` | 
| `supplies` | `3` | `0` | `40.00` | 

#### `State_Navigation_Itinerary`:

| `sequence_order` | `location_key` | 
| ----- | ----- | 
| `1` | `new_winchester` | 

#### `State_Discovered_Locations`:

| `location_key` | `clock_position` | `bazaar_reset_epoch` | 
| ----- | ----- | ----- | 
| *(Empty — 0 rows)* |  |  | 

### Expected Verification

#### State Transition:

`enroute` ➔ `arriving` ➔ `docked`

#### Targeted State Verification:

| Target Address (`Table[PK].Column`) | Expected Value | Verification Note | 
| ----- | ----- | ----- | 
| `State_Scalars.current_epoch` | `8` | `9 January 1905` = Day 8 | 
| `State_Scalars.navigation_state` | `docked` | Completed arrival transition | 
| `State_Scalars.current_location_key` | `new_winchester` | Active docked port | 
| `State_Discovered_Locations[new_winchester].clock_position` | `""` | Center hub has no clock bearing (`null` = `""`) | 
| `State_Discovered_Locations[new_winchester].bazaar_reset_epoch` | `38` | `8 + 30 = 38` (`Rule 3.2.1.2`) | 
| `State_Bazaar_Stock[new_winchester, munitions].qty_available` | `5` | 5 crates available | 
| `State_Bazaar_Stock[new_winchester, munitions].cost` | `60` | 60 Sovereigns each | 
| `State_Bazaar_Stock[new_winchester, munitions].expiration_epoch` | `38` | `8 + 30 = 38` (`Rule 3.2.1.2`) | 

#### Report Text:

*(Full Markdown `logbook.md` is strictly suppressed during `arriving` and `docked` turns per Rule `4.4.1.2`.)*

> **Mr. Bligh's Bridge Micro-Briefing:**
> "Moored safely at the bustling central hub of New Winchester on 9 January 1905 (Day 8), Captain. Did we burn a barrel of fuel on the approach leg so I can square the hold tally?
>
> Here at the heart of the Windward Company's power in The Reach, full hub facilities are at our disposal: the **Central Hub Bank**, **Shipyard**, **Crew Recruitment**, **Smuggling** channels, and **Port Reports** offices, along with standard **Fuel** and **Supplies** exports. I have logged the bazaar's active bargain window (good through 8 February 1905 / Day 38): **5 Crates of Munitions at 60 Sovereigns apiece**."

## Test Case 19: Non-Commercial Node Discovery & Expired Bazaar Garbage Collection

**Feature Tags:** `[startup-recovery, navigation, ui-gates]`

### Objective

Verifies non-commercial node discovery (`Rule 2.2.1.1`) and Class D `State_Bazaar_Stock` Swept-Expired Garbage Collection (`Rule 1.1.3.3`) upon arriving at `albion_transit_relay` (`clock_position = 4`) on `1 February 1905` (Day 31). Confirms that `State_Discovered_Locations[albion_transit_relay]` records `clock_position = 4` and `bazaar_reset_epoch = ""` (`null`), any stale bargain row in `State_Bazaar_Stock` where `expiration_epoch <= 31` is deleted immediately, and `logbook.md` is suppressed while `docked`.

### Input Prompt

> Update state. We just arrived at the Albion Transit Relay at clock position 4 on 1st February, 1905. Bring us in and tie off to the docks.

### Initial State Seed

*(Baseline defaults from `State_Scalars.csv` and `data_package.json` apply to all omitted tables and scalar keys.)*

#### `State_Scalars` Overrides:

| `property_key` | `property_value` | 
| ----- | ----- | 
| `sovereigns` | `1000` | 
| `current_epoch` | `25` | 
| `current_crew` | `8` | 
| `current_location_key` | `""` | 
| `last_location_visited_key` | `new_winchester` | 
| `navigation_state` | `enroute` | 

#### `State_Inventory`:

| `good_key` | `hold_qty` | `bank_qty` | `average_unit_cost` | 
| ----- | ----- | ----- | ----- | 
| `fuel` | `3` | `0` | `20.00` | 
| `supplies` | `3` | `0` | `40.00` | 

#### `State_Bazaar_Stock`:

| `location_key` | `good_key` | `qty_available` | `cost` | `expiration_epoch` | 
| ----- | ----- | ----- | ----- | ----- | 
| `port_avon` | `bronzed_wood_fake_check` — *use canonical:* `bronzewood` | `2` | `130` | `30` | 

*(Note: Seeded row in `State_Bazaar_Stock` is `["port_avon", "bronzewood", 2, 130, 30]`, which expires at Epoch 30.)*

#### `State_Navigation_Itinerary`:

| `sequence_order` | `location_key` | 
| ----- | ----- | 
| `1` | `albion_transit_relay` | 

#### `State_Discovered_Locations`:

| `location_key` | `clock_position` | `bazaar_reset_epoch` | 
| ----- | ----- | ----- | 
| `new_winchester` | `""` | `""` | 

### Expected Verification

#### State Transition:

`enroute` ➔ `arriving` ➔ `docked`

#### Targeted State Verification:

| Target Address (`Table[PK].Column`) | Expected Value | Verification Note | 
| ----- | ----- | ----- | 
| `State_Scalars.current_epoch` | `31` | `1 February 1905` = Day 31 | 
| `State_Scalars.navigation_state` | `docked` | Completed arrival transition | 
| `State_Scalars.current_location_key` | `albion_transit_relay` | Active docked relay | 
| `State_Discovered_Locations[albion_transit_relay].clock_position` | `4` | Charted at 4 o'clock bearing (`Rule 2.2.1.1`) | 
| `State_Discovered_Locations[albion_transit_relay].bazaar_reset_epoch` | `""` | Non-commercial relay has no bazaar reset epoch (`null` = `""`) | 
| `State_Bazaar_Stock[port_avon, bronzewood]` | `<Deleted>` | Swept and deleted since `expiration_epoch (30) <= current_epoch (31)` (`Rule 1.1.3.3`) | 
| `State_Navigation_Itinerary.row_count` | `0` | Completed waypoint popped from itinerary | 

#### Report Text:

*(Full Markdown `logbook.md` is strictly suppressed during `arriving` and `docked` turns per Rule `4.4.1.2`.)*

> **Mr. Bligh's Bridge Micro-Briefing:**
> "Lines secured at the **Albion Transit Relay** on 1 February 1905 (Day 31), Captain. I have charted the relay on our sky-map at the **4 o'clock** bearing and swept expired market notices from our ledger. How many barrels of fuel did we burn on the approach leg?
>
> Heavily patrolled by dreadnoughts, this colossal mechanical aperture hurls locomotives across the void to the heart of the Empire. As a military transit relay, there is no bazaar exchange here, and station stores export **Barrels of Fuel** only (Partial Resupply 🟡 — no Supplies). Whenever you are ready to plot a jump to Albion or head back toward the Reach, give the word."

## Test Case 20: Itinerary Stop Action Filtering, Priority Badges & Off-Itinerary Suppression

**Feature Tags:** `[narrative, navigation, ui-gates]`

### Objective

Verifies that when departing a port (`new_winchester` on `1905-03-01` = Day 59), the `### ➡️ STOP 1: Port Avon` block in `logbook.md` (`Rule 4.4.3.3`) includes only actions targeting `port_avon` (`ACT-3001` with `‼️` high-priority badge and `ACT-3002` with `🔻` low-priority badge), while excluding unpinned off-itinerary action `ACT-3003` (targeting `titania`, `is_pinned = FALSE`) from the stop block and suppressing `### 📌 PINNED OBJECTIVES (OFF-ITINERARY)`. Also verifies that `📦 LOGISTICS` still accurately reflects the physical cargo earmark for `ACT-3003` on the `bronzewood` row.

### Input Prompt

> Update state. We are docked at New Winchester on 1905-03-01. Our active itinerary is set for Port Avon. Review our pending logs, apply our standard priority markers, and cast off lines.

### Initial State Seed

*(Baseline defaults from `State_Scalars.csv` and `data_package.json` apply to all omitted tables and scalar keys.)*

#### `State_Scalars` Overrides:

| `property_key` | `property_value` | 
| ----- | ----- | 
| `sovereigns` | `1000` | 
| `current_epoch` | `59` | 
| `current_crew` | `8` | 
| `current_location_key` | `new_winchester` | 
| `last_location_visited_key` | `new_winchester` | 
| `navigation_state` | `docked` | 

#### `State_Inventory`:

| `good_key` | `hold_qty` | `bank_qty` | `average_unit_cost` | 
| ----- | ----- | ----- | ----- | 
| `fuel` | `3` | `0` | `20.00` | 
| `supplies` | `3` | `0` | `40.00` | 
| `approved_literature` | `2` | `0` | `100.00` | 
| `bronzewood` | `2` | `0` | `175.00` | 

#### `State_Action`:

| `action_id` | `parent_action_id` | `title` | `action_type` | `action_status` | `target_location_key` | `target_entity_key` | `quantity_required` | `quantity_delivered` | `priority` | `is_pinned` | `created_epoch` | `updated_epoch` | `deadline_epoch` | `notes` | 
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | 
| `ACT-3001` | `""` | `Avon Reading Materials` | `prospect` | `ready` | `port_avon` | `approved_literature` | `2` | `0` | `high` | `FALSE` | `50` | `50` | `""` | `Deliver Approved Literature to Port Avon.` | 
| `ACT-3002` | `""` | `Inspect the docks at Port Avon` | `todo` | `active` | `port_avon` | `""` | `0` | `0` | `low` | `FALSE` | `55` | `55` | `""` | `Check cargo handling efficiency.` | 
| `ACT-3003` | `""` | `Irrelevant Titania Haul` | `prospect` | `ready` | `titania` | `bronzewood` | `2` | `0` | `high` | `FALSE` | `52` | `52` | `""` | `Cargo destined elsewhere.` | 

#### `State_Navigation_History`:

| `leg_index` | `location_key` | `arrived_epoch` | 
| ----- | ----- | ----- | 
| `1` | `new_winchester` | `50` | 

#### `State_Navigation_Itinerary`:

| `sequence_order` | `location_key` | 
| ----- | ----- | 
| `1` | `port_avon` | 

### Expected Verification

#### State Transition:

`docked` ➔ `departing` ➔ `enroute`

#### Targeted State Verification:

| Target Address (`Table[PK].Column`) | Expected Value | Verification Note | 
| ----- | ----- | ----- | 
| `State_Scalars.current_epoch` | `59` | `1 March 1905` = $31 + 28 = \text{Day } 59$ | 
| `State_Scalars.navigation_state` | `enroute` | Exited `departing` into open sky | 
| `State_Scalars.current_location_key` | `""` | Cleared upon entering `enroute` | 
| `State_Scalars.last_location_visited_key` | `new_winchester` | Origin port recorded | 
| `State_Navigation_Itinerary[1].location_key` | `port_avon` | Stop 1 on active trajectory | 
| `State_Action[ACT-3001].action_status` | `ready` | Rendered under `STOP 1: Port Avon` with `‼️` prefix | 
| `State_Action[ACT-3002].action_status` | `active` | Rendered under `STOP 1: Port Avon` with `🔻` prefix | 
| `State_Action[ACT-3003].is_pinned` | `FALSE` | Excluded from Stop 1 and `PINNED OBJECTIVES` suppressed (`Rule 4.4.3.3`) | 

#### Report Text:

```
# 🚂 CAPTAIN'S LOG 🚀

## 📅 1 March 1905 (Day 59) · ⚓ New Winchester

**🗺️ Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 1000 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS
| System          | Status                                   |
| :---            | :---                                     |
| **Crew:**       | 🟢 8 / 10                                |
| **Hull:**       | 🟢 30 / 30                               |
| **Terror:**     | 🟢 0 / 100                               |
| **Nightmares:** | 🟢 0 / 4                                 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS           | Base                   | Perks     | Total     |
| :---                | :---:                  | :---:     | :---:     |
| - 👊 Iron           | 0                      | 0         | **0**     |
| - 👁️ Mirrors        | 0                      | 0         | **0**     |
| - ❤️ Hearts         | 0                      | 0         | **0**     |
| - 🎭 Veils          | 0                      | 0         | **0**     |
| 🔍 **AFFILIATIONS** | **Base**               | **Perks** | **Total** |
| - 🔍 Academe        | 0                      | 0         | **0**     |
| - 🍷 Bohemia        | 0                      | 0         | **0**     |
| - 👑 Establishment  | 0                      | 0         | **0**     |
| - 🎩 Villainy       | 0                      | 0         | **0**     |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** Unassigned (No Ambition Selected) — *Current Focus: Awaiting Next Milestone*

📋 **Executive Officer's Counsel (Mr. Bligh — Concept of Maneuver):**
> Mooring lines cast off from New Winchester for Port Avon (Full Resupply 🟢), Captain. At Port Avon, our high-priority prospect *Avon Reading Materials* (`ACT-3001`, 2 Batches of Approved Literature) is loaded in the hold and ready for immediate turn-in (`‼️`), alongside our low-priority dock inspection reminder (`ACT-3002`, `🔻`). Note that we are also carrying 2 Loads of Bronzewood earmarked for Titania (`ACT-3003`), which is currently off our plotted itinerary. Both Fuel (`3`) and Supplies (`3`) sit at minimum safe reserve (`⚠️`).

### 🧭 Active Trajectory:
⚓ New Winchester ➔ 🟢 **Port Avon**

### ➡️ STOP 1: Port Avon
* ‼️ 🔑 **PROSPECT:** Avon Reading Materials (`ACT-3001`) — Deliver 2 Batch of Approved Literature (ready)
* 🔻 📌 **TODO:** Inspect the docks at Port Avon (`ACT-3002`) — Check cargo handling efficiency.

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 10 / 12

| Trade Good Name | Physical Hold (`hold_qty`) | Hub Bank (`bank_qty`) | Unit Cost (`MAC`) | Status / Earmark | Destination Port |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **🔥 Barrel of Fuel** | 3 | 0 | 20.00 | ⚠️ | — |
| **📦 Crate of Supplies** | 3 | 0 | 40.00 | ⚠️ | — |
| **Batch of Approved Literature** | 2 | 0 | 100.00 | Earmarked for `ACT-3001`: Avon Reading Materials (2/2) | Port Avon |
| **Load of Bronzewood** | 2 | 0 | 175.00 | Earmarked for `ACT-3003`: Irrelevant Titania Haul (2/2) | Titania |

---

## 🛞 BRIDGE ROSTER

| Station                   | Active Officer                          | Skill Perks                  | Affiliation Perks                  |
| :---                      | :---                                    | :---                         | :---                               |
| ⚓ **First Officer**      | 🔘 Vacant                               | —                            | —                                  |
| 🛞 **Quartermaster**      | 🔘 Vacant                               | —                            | —                                  |
| 🏮 **Signaller**          | 🔘 Vacant                               | —                            | —                                  |
| ⚙️ **Chief Engineer**     | 🔘 Vacant                               | —                            | —                                  |
| 🐶 **Mascot**             | 🔘 Vacant                               | —                            | —                                  |

  ---

*Respectfully submitted,*  

### 🪶 **_Mr. Bligh_**

*Executive Officer, Zephyr*

⚜️ ─── ✦ 🧭 ۞ ⚓ ✦ ─── ⚜️

```