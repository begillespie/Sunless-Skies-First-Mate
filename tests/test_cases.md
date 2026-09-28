# SUNLESS SKIES FIRST MATE TEST CASES

## MASTER TEST PACKAGE INDEX
| Sequence | Package Identifier | Functional Domain | Included Tests | Scope & Invariants Under Test |
| --- | --- | --- | --- | --- |
| 1 | **`PKG-CORE`** | Core Boot & Validation | **TC1, TC4** | Cold-boot state initialization, baseline day 0 epoch, default locomotive parameters, and foreign key/location schema guardrail intercepts.|
| 2 | **`PKG-NAV-TRANSIT`** | Kinetic State & Waypoints | **TC2, TC14, TC16, TC17** | Kinetic loop cycling (`docked`/`enroute`/`arriving`), 6-phase compound turns, relay toll validation, rolling history 3-stop clamp, and arrival UI suppression.|
| 3 | **`PKG-NAV-ROUTING`** | Navigation & Planning | **TC7, TC8** | Multi-leg itinerary generation ($N+1$), spatial task matching under NEXT STOP, angular coordinate checking ($\Delta\theta$), and resupply deficit warnings.|
| 4 | **`PKG-ECON-INVENTORY`** | Inventory & Banking | **TC3, TC9, TC15** | Bank deposits/withdrawals, weightless category 2/3 item isolation, hold capacity limits, moving average cost ($MAC$), and non-leap calendar handling.|
| 5 | **`PKG-ACTION-LIFECYCLE`** | Actions & Prospects | **TC10, TC11, TC12** | Prospect progression (`active` ➔ `ready`), partial cargo delivery decrements, multi-item quest shopping lists, and logbook override triggers.|
| 6 | **`PKG-CREW-OFFICERS`** | Locomotive & Officers | **TC5, TC6, TC13** | Crew/hull warning color thresholds, low-crew narrative tone shifts, consumable alerts (⚠️/🚨), dynamic officer perk calculations, and secondments.|

---

## MASTER TEST SUITE INDEX
| Test # | Package | Title | Primary Features Under Test |
| --- | --- | --- | --- |
| **TC1** | `PKG-CORE` | **Session Initialization (Blank Slate Verification)** | Engine cold-boot without prior JSON; assignment of First Mate identity ("Mr. Bligh"); Day 0 baseline epoch handling; initial sovereign/fuel/supply parameters; default hold rules; initial departure logbook and autosave rendering.|
| **TC2** | `PKG-NAV-TRANSIT` | **Port Arrival & Month-Boundary Bargain Discovery Tracking** | Kinetic FSM transition (`enroute` ➔ `arriving` ➔ `docked`); transit burn accounting; date conversion crossing month boundary (Jan 31 to Feb 12); bazaar bargain discovery and reset epoch logging; strict UI suppression during port calls.|
| **TC3** | `PKG-ECON-INVENTORY` | **Inventory Math, Banking Logistics & Non-Leap Temporal Calculation** | Central hub bank transfers (`qty_in_hold` $\leftrightarrow$ `qty_in_bank`); standardized 365-day High Wilderness calendar invariant across non-leap leap-year anomalies (Feb 28 to Mar 1 1908 = +1 day); hold capacity re-evaluation; departure logbook rendering.|
| **TC4** | `PKG-CORE` | **State Integrity Breach Emergency Intercept (Directive 2.2.4)** | Safety guardrail triggers; foreign key validation failure against unwhitelisted commodity keys (`quantum_æther_crystal`) and invalid locations (`missing_port_x`); execution halt and verbatim emergency recovery alert output.|
| **TC5** | `PKG-CREW-OFFICERS` | **Crew Status Color Mapping - Yellow Tier Warning** | Numeric threshold mapping for crew ($50\% \le \text{Crew} < 70\% \rightarrow$ Yellow Tier) and hull integrity ($30\% \le \text{Hull} < 60\% \rightarrow$ Yellow Tier); year-boundary calendar calculation (Dec 31 1905 to Jan 15 1906); zero-quantity item suppression.|
| **TC6** | `PKG-CREW-OFFICERS` | **Critical Low Crew Threshold & Consumable Depletion** | High-fatigue tone shifts when crew drops below 50% (Red Tier); consumable hold warnings (fuel $\le 1$ = ⚠️, supplies $= 0$ = 🚨); high-priority unpinned bridge note tracking (`todo`); departure manifest generation.|
| **TC7** | `PKG-NAV-ROUTING` | **Route Planner - Multi-Stop Sequential Itinerary & Task Linking** | Multi-leg route planning; sequential leg indexing ($N+1$ continuity); spatial task filtering under NEXT STOP for pending mercantile prospects and bridge notes; mid-year non-leap calendar conversion.|
| **TC8** | `PKG-NAV-ROUTING` | **Route Planner - Resupply Isolation Alert & Intermediate Port Recommendation** | Pre-departure consumable deficit guard; angular coordinate evaluation ($\Delta\theta$); automated intermediate port detour recommendations (Titania insertion); professional caution bridge counsel.|
| **TC9** | `PKG-ECON-INVENTORY` | **Cargo Isolation & Weightless Possessions Tracking** | Physical hold isolation for Category 2 progression tokens (`possessions.villainy`) and Category 3 narrative items (`payload.items_manifest.narrative_items`); polymorphic quest instantiation (`fetch` pattern).|
| **TC10** | `PKG-ACTION-LIFECYCLE` | **Prospect Sourcing Phase to Sourced Readiness Mutation** | Commodity purchase accounting; atomic progression of mercantile prospect lifecycle from `status: "active"` to `status: "ready"` upon sourcing complete cargo; dynamic NEXT STOP spatial matching.|
| **TC11** | `PKG-ACTION-LIFECYCLE` | **Partial Delivery of a Quest Shopping List Pattern** | Multi-item quest manifest handling (`shopping_list` pattern); hold inventory decrements alongside incrementing `quantity_delivered`; retention of `status: "active"` pending outstanding requirements; zero-inventory suppression.|
| **TC12** | `PKG-ACTION-LIFECYCLE` | **Partial Delivery of an Underway Prospect** | Port destination delivery interactions; partial contract handoff; decrements to physical cargo while retaining `status: "ready"`; hold utilization updates; forced logbook rendering via explicit Captain command.|
| **TC13** | `PKG-CREW-OFFICERS` | **Dynamic Stat Resolution & Companion Upgrades** | Runtime dynamic perk evaluation across officer composite keys (`navigator.stalwart`); prevention of calculated perk serialization in JSON; officer secondment lifecycle and maturity tracking; multi-year calendar calculation.|
| **TC14** | `PKG-NAV-TRANSIT` | **Multi-State Compound Turn Pipeline** | Atomic resolution of a multi-phase turn (`enroute` ➔ `arriving` ➔ `docked` ➔ `departing` ➔ `enroute`); transit fuel burns, market sales, bazaar restocking, and departure execution in a single turn; rolling history tracking.|
| **TC15** | `PKG-ECON-INVENTORY` | **Economic Core & Moving Average Cost (MAC) Recalculation** | Atomic Moving Average Cost ($MAC$) re-computation when acquiring standard commodities at discounted market rates; floating capital tracking; physical hold capacity saturation checks ($12/12$ slots).|
| **TC16** | `PKG-NAV-TRANSIT` | **Inter-Region Transit Relay Trajectory & Toll Evaluation** | Inter-region navigation gating; transit permit validation (`possessions.transit_permits`); toll option assessment across first- and second-class options without premature fee deductions prior to gate engagement.|
| **TC17** | `PKG-NAV-TRANSIT` | **Navigation Itinerary Lifecycle, Rolling History Pruning & Port Arrival** | Kinetic arrival processing (`itinerary[0]` resolution); sequential leg transfer to `recent_history`; strict rolling cap invariant enforcement (clamping history to the 3 most recent stops and discarding oldest entry); port arrival dialogue.|

---

## Test Case 1: Session Initialization (Blank Slate Verification)

### Objective
Verifies that when no prior JSON state is provided, the system boots cleanly, assigns the First Mate persona ("Mr. Bligh"), sets Day 0 (1 January 1905), handles initial sovereign parameters, initializes default locomotive and non-zero inventory attributes (suppressing zero-quantity commodities and possessions), and renders the departure logbook.

### Input Prompt
> Start fresh. Captain Sinclair here, taking command of a brand new Spatchcock-Class Scout on this fine New Year's Day, 1905-01-01. Set our starting Sovereigns to 1000. We are departing New Winchester.

#### JSON State Verification:
- `first_mate_name`
- `dynamic_save_state.captain.name`
- `dynamic_save_state.current_day_epoch`
- `dynamic_save_state.sovereigns`
- `dynamic_save_state.locomotive.model`
- `dynamic_save_state.locomotive.hull`
- `dynamic_save_state.locomotive.max_hull`
- `dynamic_save_state.unified_inventory_registry.fuel.qty_in_hold`
- `dynamic_save_state.unified_inventory_registry.fuel.qty_in_bank`
- `dynamic_save_state.unified_inventory_registry.supplies.qty_in_hold`
- `dynamic_save_state.unified_inventory_registry.supplies.qty_in_bank`
- `dynamic_save_state.navigation.state`
- `dynamic_save_state.navigation.current_location`

### Expected Verification:

#### State Transition:
`uninitialized` ➔ `docked` ➔ `departing`

#### Flat JSON State Extraction:
```json
{
  "first_mate_name": "Mr. Bligh",
  "dynamic_save_state.captain.name": "Sinclair",
  "dynamic_save_state.current_day_epoch": 0,
  "dynamic_save_state.sovereigns": 1000,
  "dynamic_save_state.locomotive.model": "Spatchcock-Class Scout",
  "dynamic_save_state.locomotive.hull": 30,
  "dynamic_save_state.locomotive.max_hull": 30,
  "dynamic_save_state.unified_inventory_registry.fuel.qty_in_hold": 3,
  "dynamic_save_state.unified_inventory_registry.fuel.qty_in_bank": 0,
  "dynamic_save_state.unified_inventory_registry.supplies.qty_in_hold": 3,
  "dynamic_save_state.unified_inventory_registry.supplies.qty_in_bank": 0,
  "dynamic_save_state.navigation.state": "departing",
  "dynamic_save_state.navigation.current_location": "new_winchester"
}

```

#### Report Text:

```markdown
# 🚂 CAPTAIN'S LOG 🚀

## 📅 1 January 1905 (Day 0) · ⚓ New Winchester

**🗺️ Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 1000 Sovereigns

**🚂 Current Engine:** Spatchcock-Class Scout ()


---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS

| System | Status |
| --- | --- |
| **Crew:** | 🟢 8 / 10 |
| **Hull:** | 🟢 30 / 30 |
| **Terror:** | 🟢 0 / 100 |
| **Nightmares:** | 🟢 0 / 4 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS | Base | Perks | Total |
| --- | --- | --- | --- |
| - 👊 Iron | 0 | 0 | **0** |
| - 👁️ Mirrors | 0 | 0 | **0** |
| - ❤️ Hearts | 0 | 0 | **0** |
| - 🎭 Veils | 0 | 0 | **0** |
| 🔍 **AFFILIATIONS** | **Base** | **Perks** | **Total** |
| - 🔍 Academe | 0 | 0 | **0** |
| - 🍷 Bohemia | 0 | 0 | **0** |
| - 👑 Establishment | 0 | 0 | **0** |
| - 🎩 Villainy | 0 | 0 | **0** |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** [ unknown ] (Tier [ unknown ]) — *Next Milestone: [ unknown ]*

📋 **First Officer's Counsel:**

> Mr. Bligh here, Captain. Fresh boilers, clean ledger, and a thousand Sovereigns in the strongbox. We've cast off from New Winchester with standard reserves in the hold. Let's see what the High Wilderness has in store for us.

### 🧭 Active Trajectory:

New Winchester ➔ 🟢 **[ unknown ]**

### ➡️ NEXT STOP: [ unknown ]

### 👤 ACTIVE PASSENGERS & BRIDGE TRANSIT

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 6 / 12

| Trade Good Name | Physical Hold | Hub Bank Stock | Active Sourcing Progress / Status | Destination Port |
| --- | --- | --- | --- | --- |
| **🔥 Fuel** | 3 | 0 | 🟢 | — |
| **📦 Supplies** | 3 | 0 | 🟢 | — |

---

## 🛞 BRIDGE ROSTER

| Station | Active Officer | Skill Perks | Affiliation Perks |
| --- | --- | --- | --- |
| ⚓ **First Officer** | 🔘 Vacant | — | — |
| 🛞 **Quartermaster** | 🔘 Vacant | — | — |
| 🏮 **Signaller** | 🔘 Vacant | — | — |
| ⚙️ **Chief Engineer** | 🔘 Vacant | — | — |
| 🐶 **Mascot** | 🔘 Vacant | — | — |

### ⏳ SECONDMENT OUTLOOK

```
---

#### 🔒 INTERNAL STATE AUTOSAVE

```json
{"save_format":"sunless-skies-first-mate","schema_version":"0.4.0","rules_version":"0.4.0","static_data_version":"0.4.0","first_mate_name":"Mr. Bligh","dynamic_save_state":{"sovereigns":1000,"current_day_epoch":0,"captain":{"name":"Sinclair","skills":{"iron":0,"mirrors":0,"hearts":0,"veils":0},"affiliations":{"academe":0,"bohemia":0,"establishment":0,"villainy":0}},"locomotive":{"model":"Spatchcock-Class Scout","name":"","hull":30,"max_hull":30,"fuel_used_last_leg":0,"hold_capacity":12,"hidden_slots":0,"hold_rules":{"fuel_reserve_minimum":3,"supplies_reserve_minimum":3,"discovery_buffer_slots":2}},"crew":{"current":8,"max":10,"terror":0,"nightmares":0},"officer_manifest":{"on_duty":{"first_officer":null,"quartermaster":null,"signaller":null,"chief_engineer":null,"mascot":null},"unassigned":{"first_officer":[],"quartermaster":[],"signaller":[],"chief_engineer":[],"mascot":[]},"seconded":{"first_officer":[],"quartermaster":[],"signaller":[],"chief_engineer":[],"mascot":[]},"departed":{"first_officer":[],"quartermaster":[],"signaller":[],"chief_engineer":[],"mascot":[]}},"unified_inventory_registry":{"fuel":{"qty_in_hold":3,"qty_in_bank":0,"average_unit_cost":20.0},"supplies":{"qty_in_hold":3,"qty_in_bank":0,"average_unit_cost":40.0}},"possessions":{"academe":{},"bohemia":{},"establishment":{},"villainy":{},"transit_permits":[]},"active_action_stream":[],"completed_action_log":[],"navigation":{"current_location":"new_winchester","state":"departing","last_updated_epoch":0,"recent_history":[],"itinerary":[]},"discovered_locations":{"new_winchester":{"clock_direction":null,"captains_notes":[],"bazaar":{"reset_epoch":null,"available_bargains":[]}}}}}
```

---

## Test Case 2: Port Arrival & Month-Boundary Bargain Discovery Tracking

### Objective

Verifies kinetic state transition from `enroute` ➔ `arriving` ➔ `docked`, temporal conversion crossing a month boundary (`1905-01-31` = Day 30; reset `1905-02-12` = Day 42), canonical market key matching, suppression of zero-quantity items, and strict visual UI suppression during docked arrivals.

### Input Prompt

> Update state. We docked at Lustrum on 1905-01-31. Fuel used on this leg was 2. While checking the local market, we spotted a bargain: 3 crates of Unseasoned Hours selling for 40 Sovereigns each. The market broker says this deal expires on 1905-02-12.

```json
{
  "save_format": "sunless-skies-first-mate",
  "schema_version": "0.4.0",
  "rules_version": "0.4.0",
  "static_data_version": "0.4.0",
  "first_mate_name": "Mr. Bligh",
  "dynamic_save_state": {
    "sovereigns": 1000,
    "current_day_epoch": 26,
    "captain": {
      "name": "Sinclair",
      "skills": {"iron": 0,"mirrors": 0,"hearts": 0,"veils": 0},
      "affiliations": {"academe": 0,"bohemia": 0,"establishment": 0,"villainy": 0}
    },
    "locomotive": {
      "model": "Spatchcock-Class Scout","name": "Zephyr",
      "hull": 30,"max_hull": 30,
      "fuel_used_last_leg": 0,"hold_capacity": 12,"hidden_slots": 0,
      "hold_rules":{"fuel_reserve_minimum": 3,"supplies_reserve_minimum": 3,"discovery_buffer_slots": 2}
    },
    "crew": {"current": 8,"max": 10,"terror": 0,"nightmares": 0},
    "officer_manifest": {},
    "unified_inventory_registry": {
      "fuel": {"qty_in_hold": 5,"qty_in_bank": 0,"average_unit_cost": 20.00},
      "supplies": {"qty_in_hold": 4,"qty_in_bank": 0,"average_unit_cost": 40.00}
    },
    "possessions": {},
    "active_action_stream": [],
    "completed_action_log": [],
    "navigation": {
      "current_location": null,
      "state": "enroute",
      "last_updated_epoch": 26,
      "recent_history": [{"leg": 1, "location": "new_winchester", "arrived_epoch": 0}],
      "itinerary": [{"leg": 2, "location": "lustrum"}]
    },
    "discovered_locations": {}
  }
}

```

#### JSON State Verification:

* `dynamic_save_state.current_day_epoch`
* `dynamic_save_state.locomotive.fuel_used_last_leg`
* `dynamic_save_state.unified_inventory_registry.fuel.qty_in_hold`
* `dynamic_save_state.navigation.state`
* `dynamic_save_state.navigation.current_location`
* `dynamic_save_state.discovered_locations.lustrum.bazaar.reset_epoch`
* `dynamic_save_state.discovered_locations.lustrum.bazaar.available_bargains[0].good_key`
* `dynamic_save_state.discovered_locations.lustrum.bazaar.available_bargains[0].quantity_available`
* `dynamic_save_state.discovered_locations.lustrum.bazaar.available_bargains[0].cost_per_unit`

### Expected Verification:

#### State Transition:

`enroute` ➔ `arriving` ➔ `docked`

#### Flat JSON State Extraction:

```json
{
  "dynamic_save_state.current_day_epoch": 30,
  "dynamic_save_state.locomotive.fuel_used_last_leg": 2,
  "dynamic_save_state.unified_inventory_registry.fuel.qty_in_hold": 3,
  "dynamic_save_state.navigation.state": "docked",
  "dynamic_save_state.navigation.current_location": "lustrum",
  "dynamic_save_state.discovered_locations.lustrum.bazaar.reset_epoch": 42,
  "dynamic_save_state.discovered_locations.lustrum.bazaar.available_bargains[0].good_key": "unseasoned_hours",
  "dynamic_save_state.discovered_locations.lustrum.bazaar.available_bargains[0].quantity_available": 3,
  "dynamic_save_state.discovered_locations.lustrum.bazaar.available_bargains[0].cost_per_unit": 40
}

```

#### Report Text:

(Per Section 3.2.5 and Section 8.1.2, full Markdown logbooks and JSON autosave blocks are strictly suppressed during `arriving` and `docked` turns.)

> **Mr. Bligh reports:**
> "Lines secured at the freezing docks of Lustrum on this last day of January, 1905. Engines cooled and 2 barrels of fuel accounted for in the burn.
> Lustrum's miners are chipping frozen moments straight out of the Mother of Mountains. Down at the exchange, I've noted a prime bargain on the boards: 3 crates of Unseasoned Hours going for 40 Sovereigns apiece, good until the 12th of February. Standard bunkering and supplies are open, and fresh hands are lingering in the taverns if we need to fill the bunks. Awaiting your trade orders before we talk departure."

---

## Test Case 3: Inventory Math, Banking Logistics & Non-Leap Temporal Calculation

### Objective

Verifies ledger accounting updates for assets moved to central hub storage, suppressing zero-quantity hold/bank items and possessions, while testing standardized High Wilderness calendar handling across a leap-year anomaly (`1908-02-28` = Day 1153 $\rightarrow$ `1908-03-01` = Day 1154, verifying February is locked invariant at 28 days with 0 leap days).

### Input Prompt

> Update state. It's now 1908-03-01. We dropped anchor back at the main hub and deposited 4 loads of Bronzewood and 2 barrels of Chorister Nectar into our Hub Bank Stockpile. Off to Titania!

```json
{
  "save_format": "sunless-skies-first-mate",
  "schema_version": "0.4.0",
  "rules_version": "0.4.0",
  "static_data_version": "0.4.0",
  "first_mate_name": "Mr. Bligh",
  "dynamic_save_state": {
    "sovereigns": 880,
    "current_day_epoch": 1153,
    "captain": {
      "name": "Sinclair",
      "skills": {"iron": 10,"mirrors": 3,"hearts": 6,"veils": 3},
      "affiliations": {"academe": 0,"bohemia": 0,"establishment": 0,"villainy": 0}
    },
    "locomotive": {
      "model": "Spatchcock-Class Scout","name": "Zephyr",
      "hull": 30,"max_hull": 30,
      "fuel_used_last_leg": 0,"hold_capacity": 12,"hidden_slots": 0,
      "hold_rules": {"fuel_reserve_minimum": 3,"supplies_reserve_minimum": 3,"discovery_buffer_slots": 2}
    },
    "crew": {"current": 8,"max": 10,"terror": 0,"nightmares": 0},
    "officer_manifest": {
      "on_duty": {"first_officer": "navigator.fortunate"}
    },
    "unified_inventory_registry": {
      "fuel": {"qty_in_hold": 3,"qty_in_bank": 0,"average_unit_cost": 20.00},
      "supplies": {"qty_in_hold": 3,"qty_in_bank": 0,"average_unit_cost": 40.00},
      "bronzewood": {"qty_in_hold": 4,"qty_in_bank": 1,"average_unit_cost": 175.00},
      "chorister_nectar": {"qty_in_hold": 2,"qty_in_bank": 0,"average_unit_cost": 120.00}
    },
    "possessions": {},
    "active_action_stream": [],
    "completed_action_log": [],
    "navigation": {
      "current_location": "new_winchester",
      "state": "docked",
      "last_updated_epoch": 1153,
      "recent_history": [{"leg": 4, "location": "port_prosper", "arrived_epoch": 1150}],
      "itinerary": []
    },
    "discovered_locations": {}
  }
}
```

#### JSON State Verification:

* `dynamic_save_state.current_day_epoch`
* `dynamic_save_state.unified_inventory_registry.fuel.qty_in_hold`
* `dynamic_save_state.unified_inventory_registry.supplies.qty_in_hold`
* `dynamic_save_state.unified_inventory_registry.bronzewood.qty_in_hold`
* `dynamic_save_state.unified_inventory_registry.bronzewood.qty_in_bank`
* `dynamic_save_state.unified_inventory_registry.chorister_nectar.qty_in_hold`
* `dynamic_save_state.unified_inventory_registry.chorister_nectar.qty_in_bank`
* `dynamic_save_state.navigation.state`


### Expected Verification:

#### State Transition:

`docked` ➔ `departing` (Multi-state compound turn: bank transfer executed while docked, then departing plotted for Titania)

#### Flat JSON State Extraction:

```json
{
  "dynamic_save_state.current_day_epoch": 1154,
  "dynamic_save_state.unified_inventory_registry.fuel.qty_in_hold": 3,
  "dynamic_save_state.unified_inventory_registry.supplies.qty_in_hold": 3,
  "dynamic_save_state.unified_inventory_registry.bronzewood.qty_in_hold": 0,
  "dynamic_save_state.unified_inventory_registry.bronzewood.qty_in_bank": 5,
  "dynamic_save_state.unified_inventory_registry.chorister_nectar.qty_in_hold": 0,
  "dynamic_save_state.unified_inventory_registry.chorister_nectar.qty_in_bank": 2,
  "dynamic_save_state.navigation.state": "departing"
}

```

#### Report Text:

```markdown
# 🚂 CAPTAIN'S LOG 🚀

## 📅 1 March 1908 (Day 1154) · ⚓ New Winchester

**🗺️ Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 880 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock-Class Scout)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS

| System | Status |
| --- | --- |
| **Crew:** | 🟢 8 / 10 |
| **Hull:** | 🟢 30 / 30 |
| **Terror:** | 🟢 0 / 100 |
| **Nightmares:** | 🟢 0 / 4 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS | Base | Perks | Total |
| --- | --- | --- | --- |
| - 👊 Iron | 10 | +6 | **16** |
| - 👁️ Mirrors | 3 | 0 | **3** |
| - ❤️ Hearts | 6 | 0 | **6** |
| - 🎭 Veils | 3 | +2 | **5** |
| 🔍 **AFFILIATIONS** | **Base** | **Perks** | **Total** |
| - 🔍 Academe | 0 | 0 | **0** |
| - 🍷 Bohemia | 0 | 0 | **0** |
| - 👑 Establishment | 0 | +1 | **1** |
| - 🎩 Villainy | 0 | 0 | **0** |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** [ unknown ] (Tier [ unknown ]) — *Next Milestone: [ unknown ]*

📋 **First Officer's Counsel:**

> Mr. Bligh logging operations. We've transferred 4 Bronzewood and 2 Chorister Nectar to the Company vaults here at New Winchester, clearing 6 hold spaces for the run. Course plotted for Titania; fuel and supply reserves sit comfortably at minimum safe buffer.

### 🧭 Active Trajectory:

New Winchester ➔ 🟢 **Titania**

### ➡️ NEXT STOP: Titania

### 👤 ACTIVE PASSENGERS & BRIDGE TRANSIT

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 6 / 12

| Trade Good Name | Physical Hold | Hub Bank Stock | Active Sourcing Progress / Status | Destination Port |
| --- | --- | --- | --- | --- |
| **🔥 Fuel** | 3 | 0 | 🟢 | — |
| **📦 Supplies** | 3 | 0 | 🟢 | — |
| **Bronzewood** | 0 | 5 | — | — |
| **Chorister Nectar** | 0 | 2 | — | — |

---

## 🛞 BRIDGE ROSTER

| Station | Active Officer | Skill Perks | Affiliation Perks |
| --- | --- | --- | --- |
| ⚓ **First Officer** | Fortunate Navigator | +6 Iron / +2 Veils | +1 Establishment |
| 🛞 **Quartermaster** | 🔘 Vacant | — | — |
| 🏮 **Signaller** | 🔘 Vacant | — | — |
| ⚙️ **Chief Engineer** | 🔘 Vacant | — | — |
| 🐶 **Mascot** | 🔘 Vacant | — | — |

### ⏳ SECONDMENT OUTLOOK
```

---

#### 🔒 INTERNAL STATE AUTOSAVE

```json
{"save_format":"sunless-skies-first-mate","schema_version":"0.4.0","rules_version":"0.4.0","static_data_version":"0.4.0","first_mate_name":"Mr. Bligh","dynamic_save_state":{"sovereigns":880,"current_day_epoch":1154,"captain":{"name":"Sinclair","skills":{"iron":10,"mirrors":3,"hearts":6,"veils":3},"affiliations":{"academe":0,"bohemia":0,"establishment":0,"villainy":0}},"locomotive":{"model":"Spatchcock-Class Scout","name":"Zephyr","hull":30,"max_hull":30,"fuel_used_last_leg":0,"hold_capacity":12,"hidden_slots":0,"hold_rules":{"fuel_reserve_minimum":3,"supplies_reserve_minimum":3,"discovery_buffer_slots":2}},"crew":{"current":8,"max":10,"terror":0,"nightmares":0},"officer_manifest":{"on_duty":{"first_officer":"navigator.fortunate","quartermaster":null,"signaller":null,"chief_engineer":null,"mascot":null},"unassigned":{"first_officer":[],"quartermaster":[],"signaller":[],"chief_engineer":[],"mascot":[]},"seconded":{"first_officer":[],"quartermaster":[],"signaller":[],"chief_engineer":[],"mascot":[]},"departed":{"first_officer":[],"quartermaster":[],"signaller":[],"chief_engineer":[],"mascot":[]}},"unified_inventory_registry":{"fuel":{"qty_in_hold":3,"qty_in_bank":0,"average_unit_cost":20.0},"supplies":{"qty_in_hold":3,"qty_in_bank":0,"average_unit_cost":40.0},"bronzewood":{"qty_in_hold":0,"qty_in_bank":5,"average_unit_cost":175.0},"chorister_nectar":{"qty_in_hold":0,"qty_in_bank":2,"average_unit_cost":120.0}},"possessions":{"academe":{},"bohemia":{},"establishment":{},"villainy":{},"transit_permits":[]},"active_action_stream":[],"completed_action_log":[],"navigation":{"current_location":"new_winchester","state":"departing","last_updated_epoch":1154,"recent_history":[{"leg":4,"location":"port_prosper","arrived_epoch":1150}],"itinerary":[{"leg":5,"location":"titania"}]},"discovered_locations":{}}}
```

---

## Test Case 4: State Integrity Breach Emergency Intercept (Directive 2.2.4)

### Objective

Probes compliance with Section 2.2 safety guardrails by forcing an intentional relational integrity break (illegal commodity key `quantum_æther_crystal` and unwhitelisted location `missing_port_x`), confirming that the engine halts state mutation and outputs the mandatory verbatim alert.

### Input Prompt

> Captain's log: 1905-01-10. Processing a logistics pass over our active trade agreements. Let me know what our current route optimization options look like.

```json
{
  "save_format": "sunless-skies-first-mate",
  "schema_version": "0.4.0",
  "rules_version": "0.4.0",
  "static_data_version": "0.4.0",
  "first_mate_name": "Mr. Bligh",
  "dynamic_save_state": {
    "sovereigns": 880,
    "current_day_epoch": 9,
    "captain": {
      "name": "Sinclair",
      "skills": {"iron": 0,"mirrors": 0,"hearts": 0,"veils": 0},
      "affiliations": {"academe": 0,"bohemia": 0,"establishment": 0,"villainy": 0}
    },
    "locomotive": {
      "model": "Spatchcock-Class Scout","name": "Zephyr",
      "hull": 30,"max_hull": 30,
      "fuel_used_last_leg": 0,"hold_capacity": 12,"hidden_slots": 0,
      "hold_rules": {"fuel_reserve_minimum": 3,"supplies_reserve_minimum": 3,"discovery_buffer_slots": 2}
    },
    "crew": {"current": 8,"max": 10,"terror": 15,"nightmares": 0},
    "officer_manifest": {},
    "unified_inventory_registry": {
      "fuel": {"qty_in_hold": 3,"qty_in_bank": 0,"average_unit_cost": 20.00},
      "supplies": {"qty_in_hold": 3,"qty_in_bank": 0,"average_unit_cost": 40.00},
      "bronzewood": {"qty_in_hold": 1,"qty_in_bank": 0,"average_unit_cost": 175.00},
      "quantum_æther_crystal": {"qty_in_hold": 1,"qty_in_bank": 0,"average_unit_cost": 100.00}
    },
    "possessions": {},
    "active_action_stream": [
      {
        "action_id": "ACT-1016",
        "type": "todo",
        "status": "active",
        "origin_location": "missing_port_x",
        "title": "Deliver supplies to custom outpost",
        "notes": "Error payload item: Unwhitelisted location key.",
        "priority": "routine",
        "is_pinned": false,
        "created_epoch": 2,
        "updated_epoch": 2,
        "deadline_epoch": null,
        "payload": {
          "target_location": "missing_port_x"
        }
      }
    ],
    "completed_action_log": [],
    "navigation": {
      "current_location": "new_winchester",
      "state": "docked",
      "last_updated_epoch": 9,
      "recent_history": [],
      "itinerary": []
    },
    "discovered_locations": {}
  }
}

```

#### JSON State Verification:

`[ No updates are applied. Processing must freeze immediately without returning standard tracker logs or shifting saved nodes until valid structural recovery data is input by the user. ]`

### Expected Verification:

#### State Transition:

`aborted` (No valid transition permitted)

#### Output Text:

> ⚠️ EXECUTIVE OFFICER'S ALERT - STATE INTEGRITY FAILURE. Captain, I've lost my grip on the logbook. My records have gone dark - likely a break in the telegraph line between sessions. To restore full operational status, please paste your most recent Internal Game State JSON block into the chat. You'll find it collapsed at the bottom of your last log entry under 'Internal Game State JSON'. If no prior log exist, say 'Start fresh' and I'll initialize a clean slate.

## Test Case 5: Crew Status Color Mapping - Yellow Tier Warning

### Objective
Verifies the application of the structural color math threshold where crew count drops into the caution zone, checks that zero-quantity commodities and possessions are suppressed from the JSON payload, evaluates hull percentage thresholds, and tests non-leap year boundary crossing from 31 December 1905 to 15 January 1906.

### Input Prompt
> Update state. Bad news. An uncharted celestial anomaly scorched our hull crossing to Port Avon on 1906-01-15. We lost 2 crew members to the stars and took a pounding. Set our hull to 17 and our crew to 6. We must immediately depart for New Winchester to hire on new crew.

```json
{
  "save_format": "sunless-skies-first-mate",
  "schema_version": "0.4.0",
  "rules_version": "0.4.0",
  "static_data_version": "0.4.0",
  "first_mate_name": "Mr. Bligh",
  "dynamic_save_state": {
    "sovereigns": 880,
    "current_day_epoch": 364,
    "captain": {
      "name": "Sinclair",
      "skills": {"iron": 0,"mirrors": 0,"hearts": 0,"veils": 0},
      "affiliations": {"academe": 0,"bohemia": 0,"establishment": 0,"villainy": 0}
    },
    "locomotive": {
      "model": "Spatchcock-Class Scout",
      "name": "Zephyr",
      "hull": 30,
      "max_hull": 30,
      "fuel_used_last_leg": 0,
      "hold_capacity": 12,
      "hidden_slots": 0,
      "hold_rules": {"fuel_reserve_minimum": 3,"supplies_reserve_minimum": 3,"discovery_buffer_slots": 2}
    },
    "crew": {"current": 8,"max": 10,"terror": 20,"nightmares": 0},
    "officer_manifest": {},
    "unified_inventory_registry": {
      "fuel": {"qty_in_hold": 3,"qty_in_bank": 0,"average_unit_cost": 20.00},
      "supplies": {"qty_in_hold": 3,"qty_in_bank": 0,"average_unit_cost": 40.00}
    },
    "possessions": {},
    "active_action_stream": [],
    "completed_action_log": [],
    "navigation": {
      "current_location": "port_avon",
      "state": "docked",
      "last_updated_epoch": 364,
      "recent_history": [{"leg": 1, "location": "new_winchester", "arrived_epoch": 350}],
      "itinerary": []
    },
    "discovered_locations": {}
  }
}

```

#### JSON State Verification:
* `dynamic_save_state.current_day_epoch`
* `dynamic_save_state.crew.current`
* `dynamic_save_state.locomotive.hull`
* `dynamic_save_state.navigation.state`
* `dynamic_save_state.navigation.itinerary[0].location`

### Expected Verification:

#### State Transition:

`docked` ➔ `departing`

#### Flat JSON State Extraction:

```json
{
  "dynamic_save_state.current_day_epoch": 379,
  "dynamic_save_state.crew.current": 6,
  "dynamic_save_state.locomotive.hull": 17,
  "dynamic_save_state.navigation.state": "departing",
  "dynamic_save_state.navigation.itinerary[0].location": "new_winchester"
}

```

#### Report Text:

```markdown
# 🚂 CAPTAIN'S LOG 🚀

## 📅 15 January 1906 (Day 379) · ⚓ Port Avon

**🗺️ Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 880 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock-Class Scout)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS

| System | Status |
| --- | --- |
| **Crew:** | 🟡 6 / 10 |
| **Hull:** | 🟡 17 / 30 |
| **Terror:** | 🟢 20 / 100 |
| **Nightmares:** | 🟢 0 / 4 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS | Base | Perks | Total |
| --- | --- | --- | --- |
| - 👊 Iron | 0 | 0 | **0** |
| - 👁️ Mirrors | 0 | 0 | **0** |
| - ❤️ Hearts | 0 | 0 | **0** |
| - 🎭 Veils | 0 | 0 | **0** |
| 🔍 **AFFILIATIONS** | **Base** | **Perks** | **Total** |
| - 🔍 Academe | 0 | 0 | **0** |
| - 🍷 Bohemia | 0 | 0 | **0** |
| - 👑 Establishment | 0 | 0 | **0** |
| - 🎩 Villainy | 0 | 0 | **0** |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** [ unknown ] (Tier [ unknown ]) — *Next Milestone: [ unknown ]*

📋 **First Officer's Counsel:**

> Mr. Bligh at the bridge. We've cast off lines from Port Avon with scorched plates and two empty bunks. Hull's down to 17 and crew down to 6—watches are stretched thin and the engine room is rattling. Steady course back to New Winchester to drydock and hire on replacements.

### 🧭 Active Trajectory:

Port Avon ➔ 🟢 **New Winchester**

### ➡️ NEXT STOP: New Winchester

### 👤 ACTIVE PASSENGERS & BRIDGE TRANSIT

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 6 / 12

| Trade Good Name | Physical Hold | Hub Bank Stock | Active Sourcing Progress / Status | Destination Port |
| --- | --- | --- | --- | --- |
| **🔥 Fuel** | 3 | 0 | 🟢 | — |
| **📦 Supplies** | 3 | 0 | 🟢 | — |

---

## 🛞 BRIDGE ROSTER

| Station | Active Officer | Skill Perks | Affiliation Perks |
| --- | --- | --- | --- |
| ⚓ **First Officer** | 🔘 Vacant | — | — |
| 🛞 **Quartermaster** | 🔘 Vacant | — | — |
| 🏮 **Signaller** | 🔘 Vacant | — | — |
| ⚙️ **Chief Engineer** | 🔘 Vacant | — | — |
| 🐶 **Mascot** | 🔘 Vacant | — | — |

### ⏳ SECONDMENT OUTLOOK
```

#### 🔒 INTERNAL STATE AUTOSAVE

```json
{"save_format":"sunless-skies-first-mate","schema_version":"0.4.0","rules_version":"0.4.0","static_data_version":"0.4.0","first_mate_name":"Mr. Bligh","dynamic_save_state":{"sovereigns":880,"current_day_epoch":379,"captain":{"name":"Sinclair","skills":{"iron":0,"mirrors":0,"hearts":0,"veils":0},"affiliations":{"academe":0,"bohemia":0,"establishment":0,"villainy":0}},"locomotive":{"model":"Spatchcock-Class Scout","name":"Zephyr","hull":17,"max_hull":30,"fuel_used_last_leg":0,"hold_capacity":12,"hidden_slots":0,"hold_rules":{"fuel_reserve_minimum":3,"supplies_reserve_minimum":3,"discovery_buffer_slots":2}},"crew":{"current":6,"max":10,"terror":20,"nightmares":0},"officer_manifest":{},"unified_inventory_registry":{"fuel":{"qty_in_hold":3,"qty_in_bank":0,"average_unit_cost":20.0},"supplies":{"qty_in_hold":3,"qty_in_bank":0,"average_unit_cost":40.0}},"possessions":{},"active_action_stream":[],"completed_action_log":[],"navigation":{"current_location":"port_avon","state":"departing","last_updated_epoch":379,"recent_history":[{"leg":1,"location":"new_winchester","arrived_epoch":350}],"itinerary":[{"leg":2,"location":"new_winchester"}]},"discovered_locations":{}}}
```

## Test Case 6: Critical Low Crew Threshold & Consumable Depletion

### Objective

Verifies behavioral tone shifts when crew drops below 50%, triggering fatigue and sluggish engine complaints, checks hold warning icons for depleted consumables (Fuel at 1 = ⚠️, Supplies at 0 = 🚨), tests pinning/unpinned high-priority note handling, and tests calendar date conversion at year-start boundary (`1906-01-20` = Day 384).

### Input Prompt

> Update state. 1906-01-20. Sickness swept through the lower bunks while out on the high sky. We've dropped 3 more hands off at the local care station in Hybras. Crew strength is down to 3 out of 10. Make a high-priority note to hire on crew at the circus. Clear docks for Polmear & Plenty's with haste.

```json
{
  "save_format": "sunless-skies-first-mate",
  "schema_version": "0.4.0",
  "rules_version": "0.4.0",
  "static_data_version": "0.4.0",
  "first_mate_name": "Mr. Bligh",
  "dynamic_save_state": {
    "sovereigns": 880,
    "current_day_epoch": 379,
    "captain": {
      "name": "Sinclair",
      "skills": {"iron": 0,"mirrors": 0,"hearts": 0,"veils": 0},
      "affiliations": {"academe": 0,"bohemia": 0,"establishment": 0,"villainy": 0}
    },
    "locomotive": {
      "model": "Spatchcock-Class Scout",
      "name": "Zephyr",
      "hull": 17,
      "max_hull": 30,
      "fuel_used_last_leg": 0,
      "hold_capacity": 12,
      "hidden_slots": 0,
      "hold_rules": {"fuel_reserve_minimum": 3,"supplies_reserve_minimum": 3,"discovery_buffer_slots": 2}
    },
    "crew": {"current": 6,"max": 10,"terror": 35,"nightmares": 0},
    "officer_manifest": {},
    "unified_inventory_registry": {
      "fuel": {"qty_in_hold": 1,"qty_in_bank": 0,"average_unit_cost": 20.00},
      "supplies": {"qty_in_hold": 0,"qty_in_bank": 0,"average_unit_cost": 40.00}
    },
    "possessions": { },
    "active_action_stream": [],
    "completed_action_log": [],
    "navigation": {
      "current_location": "hybras",
      "state": "docked",
      "last_updated_epoch": 379,
      "recent_history": [{"leg": 2, "location": "port_avon", "arrived_epoch": 379}],
      "itinerary": []
    },
    "discovered_locations": {}
  }
}

```

#### JSON State Verification:

* `dynamic_save_state.current_day_epoch`
* `dynamic_save_state.crew.current`
* `dynamic_save_state.unified_inventory_registry.supplies.qty_in_hold`
* `dynamic_save_state.active_action_stream[0].action_id`
* `dynamic_save_state.active_action_stream[0].priority`
* `dynamic_save_state.active_action_stream[0].payload.target_location`
* `dynamic_save_state.navigation.state`


### Expected Verification:

#### State Transition:

`docked` ➔ `departing`

#### Flat JSON State Extraction:

```json
{
  "dynamic_save_state.current_day_epoch": 384,
  "dynamic_save_state.crew.current": 3,
  "dynamic_save_state.unified_inventory_registry.supplies.qty_in_hold": 0,
  "dynamic_save_state.active_action_stream[0].action_id": "ACT-1001",
  "dynamic_save_state.active_action_stream[0].priority": "high",
  "dynamic_save_state.active_action_stream[0].payload.target_location": "polmear_and_plentys_inconceivable_circus",
  "dynamic_save_state.navigation.state": "departing"
}

```

#### Report Text:

```markdown
# 🚂 CAPTAIN'S LOG 🚀

## 📅 20 January 1906 (Day 384) · ⚓ Hybras

**🗺️ Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 880 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock-Class Scout)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS

| System | Status |
| --- | --- |
| **Crew:** | 🔴 3 / 10 |
| **Hull:** | 🟡 17 / 30 |
| **Terror:** | 🟢 35 / 100 |
| **Nightmares:** | 🟢 0 / 4 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS | Base | Perks | Total |
| --- | --- | --- | --- |
| - 👊 Iron | 0 | 0 | **0** |
| - 👁️ Mirrors | 0 | 0 | **0** |
| - ❤️ Hearts | 0 | 0 | **0** |
| - 🎭 Veils | 0 | 0 | **0** |
| 🔍 **AFFILIATIONS** | **Base** | **Perks** | **Total** |
| - 🔍 Academe | 0 | 0 | **0** |
| - 🍷 Bohemia | 0 | 0 | **0** |
| - 👑 Establishment | 0 | 0 | **0** |
| - 🎩 Villainy | 0 | 0 | **0** |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** [ unknown ] (Tier [ unknown ]) — *Next Milestone: [ unknown ]*

📋 **First Officer's Counsel:**

> Mr. Bligh speaking—and God help us, Captain. We're hauling out of Hybras with a dead skeleton crew. Three living souls left to fire boilers, steer the helm, and mind the pressure valves. The men are exhausted, the engines respond like molasses, and our galley is stark empty with zero crates of supplies. If we don't hire on hands at the Circus immediately, we'll be drifting as ghosts.

### 🧭 Active Trajectory:

Hybras ➔ 🟢 **Polmear & Plenty's Inconceivable Circus**

### ➡️ NEXT STOP: Polmear & Plenty's Inconceivable Circus

* 📌 **BRIDGE NOTE:** Hire replacement crew from the circus — Priority: HIGH

### 👤 ACTIVE PASSENGERS & BRIDGE TRANSIT

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 1 / 12

| Trade Good Name | Physical Hold | Hub Bank Stock | Active Sourcing Progress / Status | Destination Port |
| --- | --- | --- | --- | --- |
| **🔥 Fuel** | 1 | 0 | ⚠️ | — |
| **📦 Supplies** | 0 | 0 | 🚨 | — |

---

## 🛞 BRIDGE ROSTER

| Station | Active Officer | Skill Perks | Affiliation Perks |
| --- | --- | --- | --- |
| ⚓ **First Officer** | 🔘 Vacant | — | — |
| 🛞 **Quartermaster** | 🔘 Vacant | — | — |
| 🏮 **Signaller** | 🔘 Vacant | — | — |
| ⚙️ **Chief Engineer** | 🔘 Vacant | — | — |
| 🐶 **Mascot** | 🔘 Vacant | — | — |

### ⏳ SECONDMENT OUTLOOK

---
```
#### 🔒 INTERNAL STATE AUTOSAVE

```json
{"save_format":"sunless-skies-first-mate","schema_version":"0.4.0","rules_version":"0.4.0","static_data_version":"0.4.0","first_mate_name":"Mr. Bligh","dynamic_save_state":{"sovereigns":880,"current_day_epoch":384,"captain":{"name":"Sinclair","skills":{"iron":0,"mirrors":0,"hearts":0,"veils":0},"affiliations":{"academe":0,"bohemia":0,"establishment":0,"villainy":0}},"locomotive":{"model":"Spatchcock-Class Scout","name":"Zephyr","hull":17,"max_hull":30,"fuel_used_last_leg":0,"hold_capacity":12,"hidden_slots":0,"hold_rules":{"fuel_reserve_minimum":3,"supplies_reserve_minimum":3,"discovery_buffer_slots":2}},"crew":{"current":3,"max":10,"terror":35,"nightmares":0},"officer_manifest":{},"unified_inventory_registry":{"fuel":{"qty_in_hold":1,"qty_in_bank":0,"average_unit_cost":20.0},"supplies":{"qty_in_hold":0,"qty_in_bank":0,"average_unit_cost":40.0}},"possessions":{},"active_action_stream":[{"action_id":"ACT-1001","type":"todo","status":"active","origin_location":"hybras","title":"Hire crew at the circus","notes":"Hire replacement crew from the circus","priority":"high","is_pinned":false,"created_epoch":384,"updated_epoch":384,"deadline_epoch":null,"payload":{"target_location":"polmear_and_plentys_inconceivable_circus"}}],"completed_action_log":[],"navigation":{"current_location":"hybras","state":"departing","last_updated_epoch":384,"recent_history":[{"leg":2,"location":"port_avon","arrived_epoch":379}],"itinerary":[{"leg":3,"location":"polmear_and_plentys_inconceivable_circus"}]},"discovered_locations":{}}}
```

## Test Case 7: Route Planner - Multi-Stop Sequential Itinerary & Task Linking

### Objective

Verifies multi-stop itinerary construction, sequential leg renumbering (§ 5.3), spatial target filtering for NEXT STOP linking (§ 4.2), and mid-year calendar conversion across leap-year anomaly (`1908-04-11` = Day 1195, evaluating 1905, 1906, 1907 as $3 \times 365 = 1095$ plus Jan 31 + Feb 28 + Mar 31 + 10 days of April).

### Input Prompt

> Update state. Plot a route from New Winchester to Titania, and then onward to Lustrum, and set sail. Let's see what business we have pending at those locations, First Mate.

```json
{
  "save_format": "sunless-skies-first-mate",
  "schema_version": "0.4.0",
  "rules_version": "0.4.0",
  "static_data_version": "0.4.0",
  "first_mate_name": "Mr. Bligh",
  "dynamic_save_state": {
    "sovereigns": 1450,
    "current_day_epoch": 1195,
    "captain": {
      "name": "Sinclair",
      "skills": {"iron": 0,"mirrors": 0,"hearts": 0,"veils": 0},
      "affiliations": {"academe": 0,"bohemia": 0,"establishment": 0,"villainy": 0}
    },
    "locomotive": {
      "model": "Spatchcock-Class Scout",
      "name": "Zephyr",
      "hull": 30,
      "max_hull": 30,
      "fuel_used_last_leg": 0,
      "hold_capacity": 12,
      "hidden_slots": 0,
      "hold_rules": {"fuel_reserve_minimum": 3,"supplies_reserve_minimum": 3,"discovery_buffer_slots": 2}
    },
    "crew": {"current": 9,"max": 10,"terror": 15,"nightmares": 0},
    "officer_manifest": {},
    "unified_inventory_registry": {
      "fuel": {"qty_in_hold": 3,"qty_in_bank": 0,"average_unit_cost": 20.00},
      "supplies": {"qty_in_hold": 3,"qty_in_bank": 0,"average_unit_cost": 40.00},
      "bronzewood": {"qty_in_hold": 2,"qty_in_bank": 0,"average_unit_cost": 175.00}
    },
    "possessions": { },
    "active_action_stream": [
      {
        "action_id": "ACT-1001",
        "type": "ambition",
        "status": "active",
        "origin_location": "new_winchester",
        "title": "Ambition: Wealth",
        "notes": "",
        "priority": "routine",
        "is_pinned": false,
        "created_epoch": 6,
        "updated_epoch": 6,
        "deadline_epoch": null,
        "payload": {
          "ambition_type": "Wealth",
          "current_tier": 1,
          "milestone_description": "Purchase the Governor's Manor",
          "sovereigns_required_for_next_tier": 5000,
          "items_manifest": {
            "goods": [],
            "possessions": [],
            "narrative_items": []
          }
        }
      },
      {
        "action_id": "ACT-1012",
        "type": "prospect",
        "status": "active",
        "origin_location": "new_winchester",
        "title": "Nectar for the Fairies",
        "notes": "",
        "priority": "routine",
        "is_pinned": false,
        "created_epoch": 79,
        "updated_epoch": 79,
        "deadline_epoch": null,
        "payload": {
          "good_key": "chorister_nectar",
          "quantity_required": 1,
          "quantity_sourced": 0,
          "quantity_delivered": 0,
          "destination_location": "titania"
        }
      },
      {
        "action_id": "ACT-1013",
        "type": "prospect",
        "status": "ready",
        "origin_location": "new_winchester",
        "title": "Bronzewood Shipments",
        "notes": "",
        "priority": "routine",
        "is_pinned": false,
        "created_epoch": 82,
        "updated_epoch": 82,
        "deadline_epoch": null,
        "payload": {
          "good_key": "bronzewood",
          "quantity_required": 3,
          "quantity_sourced": 3,
          "quantity_delivered": 1,
          "destination_location": "lustrum"
        }
      },
      {
        "action_id": "ACT-1016",
        "type": "todo",
        "status": "active",
        "origin_location": "new_winchester",
        "title": "Helping the Horticulturalist",
        "notes": "Deliver structural schematics to the Horticulturalist",
        "priority": "routine",
        "is_pinned": false,
        "created_epoch": 90,
        "updated_epoch": 90,
        "deadline_epoch": null,
        "payload": {
          "target_location": "titania"
        }
      }
    ],
    "completed_action_log": [],
    "navigation": {
      "current_location": "new_winchester",
      "state": "docked",
      "last_updated_epoch": 1195,
      "recent_history": [{"leg": 1, "location": "new_winchester", "arrived_epoch": 1180}],
      "itinerary": []
    },
    "discovered_locations": {}
  }
}

```

#### JSON State Verification:

* `dynamic_save_state.navigation.state`
* `dynamic_save_state.navigation.itinerary[0].leg`
* `dynamic_save_state.navigation.itinerary[0].location`
* `dynamic_save_state.navigation.itinerary[1].leg`
* `dynamic_save_state.navigation.itinerary[1].location`

### Expected Verification:

#### State Transition:

`docked` ➔ `departing`

#### Flat JSON State Extraction:

```json
{
  "dynamic_save_state.navigation.state": "departing",
  "dynamic_save_state.navigation.itinerary[0].leg": 2,
  "dynamic_save_state.navigation.itinerary[0].location": "titania",
  "dynamic_save_state.navigation.itinerary[1].leg": 3,
  "dynamic_save_state.navigation.itinerary[1].location": "lustrum"
}

```

#### Report Text:

```markdown
# 🚂 CAPTAIN'S LOG 🚀

## 📅 11 April 1908 (Day 1195) · ⚓ New Winchester

**🗺️ Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 1450 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock-Class Scout)

---

#### ⚙️ VESSEL SYSTEMS & RECOVERY STATUS

| System | Status |
| --- | --- |
| **Crew:** | 🟢 9 / 10 |
| **Hull:** | 🟢 30 / 30 |
| **Terror:** | 🟢 15 / 100 |
| **Nightmares:** | 🟢 0 / 4 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS | Base | Perks | Total |
| --- | --- | --- | --- |
| - 👊 Iron | 0 | 0 | **0** |
| - 👁️ Mirrors | 0 | 0 | **0** |
| - ❤️ Hearts | 0 | 0 | **0** |
| - 🎭 Veils | 0 | 0 | **0** |
| 🔍 **AFFILIATIONS** | **Base** | **Perks** | **Total** |
| - 🔍 Academe | 0 | 0 | **0** |
| - 🍷 Bohemia | 0 | 0 | **0** |
| - 👑 Establishment | 0 | 0 | **0** |
| - 🎩 Villainy | 0 | 0 | **0** |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** Wealth (Tier 1) — *Next Milestone: Purchase the Governor's Manor*

📋 **First Officer's Counsel:**

> Route laid, Captain. Mooring lines cast off from New Winchester for a two-stage sweep: first out to Titania, then swinging along the perimeter to Lustrum. At Titania, we've bridge business with the Horticulturalist, but keep in mind that fairy nectar prospect remains completely unsourced. Bronzewood for Lustrum is loaded and ready for delivery once we close the loop.

### 🧭 Active Trajectory:

New Winchester ➔ 🟢 **Titania** ➔ 🟡 Lustrum

### ➡️ NEXT STOP: Titania

* 📌 **BRIDGE NOTE:** Helping the Horticulturalist — Deliver structural schematics to the Horticulturalist — Priority: ROUTINE

### 👤 ACTIVE PASSENGERS & BRIDGE TRANSIT

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 8 / 12

| Trade Good Name | Physical Hold | Hub Bank Stock | Active Sourcing Progress / Status | Destination Port |
| --- | --- | --- | --- | --- |
| **🔥 Fuel** | 3 | 0 | 🟢 | — |
| **📦 Supplies** | 3 | 0 | 🟢 | — |
| **Bronzewood** | 2 | 0 | 3 / 3 Loaded (ACT-1013) | Lustrum |

---

## 🛞 BRIDGE ROSTER

| Station | Active Officer | Skill Perks | Affiliation Perks |
| --- | --- | --- | --- |
| ⚓ **First Officer** | 🔘 Vacant | — | — |
| 🛞 **Quartermaster** | 🔘 Vacant | — | — |
| 🏮 **Signaller** | 🔘 Vacant | — | — |
| ⚙️ **Chief Engineer** | 🔘 Vacant | — | — |
| 🐶 **Mascot** | 🔘 Vacant | — | — |

### ⏳ SECONDMENT OUTLOOK
```
---

#### 🔒 INTERNAL STATE AUTOSAVE

```json
{"save_format":"sunless-skies-first-mate","schema_version":"0.4.0","rules_version":"0.4.0","static_data_version":"0.4.0","first_mate_name":"Mr. Bligh","dynamic_save_state":{"sovereigns":1450,"current_day_epoch":1195,"captain":{"name":"Sinclair","skills":{"iron":0,"mirrors":0,"hearts":0,"veils":0},"affiliations":{"academe":0,"bohemia":0,"establishment":0,"villainy":0}},"locomotive":{"model":"Spatchcock-Class Scout","name":"Zephyr","hull":30,"max_hull":30,"fuel_used_last_leg":0,"hold_capacity":12,"hidden_slots":0,"hold_rules":{"fuel_reserve_minimum":3,"supplies_reserve_minimum":3,"discovery_buffer_slots":2}},"crew":{"current":9,"max":10,"terror":15,"nightmares":0},"officer_manifest":{},"unified_inventory_registry":{"fuel":{"qty_in_hold":3,"qty_in_bank":0,"average_unit_cost":20.0},"supplies":{"qty_in_hold":3,"qty_in_bank":0,"average_unit_cost":40.0},"bronzewood":{"qty_in_hold":2,"qty_in_bank":0,"average_unit_cost":175.0}},"possessions":{},"active_action_stream":[{"action_id":"ACT-1001","type":"ambition","status":"active","origin_location":"new_winchester","title":"Ambition: Wealth","notes":"","priority":"routine","is_pinned":false,"created_epoch":6,"updated_epoch":6,"deadline_epoch":null,"payload":{"ambition_type":"Wealth","current_tier":1,"milestone_description":"Purchase the Governor's Manor","sovereigns_required_for_next_tier":5000,"items_manifest":{"goods":[],"possessions":[],"narrative_items":[]}}},{"action_id":"ACT-1012","type":"prospect","status":"active","origin_location":"new_winchester","title":"Nectar for the Fairies","notes":"","priority":"routine","is_pinned":false,"created_epoch":79,"updated_epoch":79,"deadline_epoch":null,"payload":{"good_key":"chorister_nectar","quantity_required":1,"quantity_sourced":0,"quantity_delivered":0,"destination_location":"titania"}},{"action_id":"ACT-1013","type":"prospect","status":"ready","origin_location":"new_winchester","title":"Bronzewood Shipments","notes":"","priority":"routine","is_pinned":false,"created_epoch":82,"updated_epoch":82,"deadline_epoch":null,"payload":{"good_key":"bronzewood","quantity_required":3,"quantity_sourced":3,"quantity_delivered":1,"destination_location":"lustrum"}},{"action_id":"ACT-1016","type":"todo","status":"active","origin_location":"new_winchester","title":"Helping the Horticulturalist","notes":"Deliver structural schematics to the Horticulturalist","priority":"routine","is_pinned":false,"created_epoch":90,"updated_epoch":90,"deadline_epoch":null,"payload":{"target_location":"titania"}}],"completed_action_log":[],"navigation":{"current_location":"new_winchester","state":"departing","last_updated_epoch":1195,"recent_history":[{"leg":1,"location":"new_winchester","arrived_epoch":1180}],"itinerary":[{"leg":2,"location":"titania"},{"leg":3,"location":"lustrum"}]},"discovered_locations":{}}}
```

## Test Case 8: Route Planner - Resupply Isolation Alert & Intermediate Port Recommendation

### Objective

Verifies that the Route Planner detects critical consumable deficits prior to a long haul (§ 3.4.2 Guard 2, § 5.2.3 Resupply Isolation Alert), evaluates clock coordinates to propose an intermediate port insertion (Titania at clock 2), delivers a professional caution tone without low-hull panic (§ 1.1.2), and parses non-leap February dates (`1905-02-18` = Day 48).

### Input Prompt

> Update state. Lay a direct course from New Winchester straight out to Port Prosper, First Mate. We have a long haul ahead, let's get moving.

```json
{
  "save_format": "sunless-skies-first-mate",
  "schema_version": "0.4.0",
  "rules_version": "0.4.0",
  "static_data_version": "0.4.0",
  "first_mate_name": "Mr. Bligh",
  "dynamic_save_state": {
    "sovereigns": 620,
    "current_day_epoch": 48,
    "captain": {
      "name": "Sinclair",
      "skills": {"iron": 0,"mirrors": 0,"hearts": 0,"veils": 0},
      "affiliations": {"academe": 0,"bohemia": 0,"establishment": 0,"villainy": 0}
    },
    "locomotive": {
      "model": "Spatchcock-Class Scout",
      "name": "Zephyr",
      "hull": 25,
      "max_hull": 30,
      "fuel_used_last_leg": 0,
      "hold_capacity": 12,
      "hidden_slots": 0,
      "hold_rules": {"fuel_reserve_minimum": 3,"supplies_reserve_minimum": 3,"discovery_buffer_slots": 2}
    },
    "crew": {"current": 10,"max": 10,"terror": 40,"nightmares": 1},
    "officer_manifest": {},
    "unified_inventory_registry": {
      "fuel": {"qty_in_hold": 1,"qty_in_bank": 0,"average_unit_cost": 20.00},
      "supplies": {"qty_in_hold": 1,"qty_in_bank": 0,"average_unit_cost": 40.00}
    },
    "possessions": {},
    "active_action_stream": [],
    "completed_action_log": [],
    "navigation": {
      "current_location": "new_winchester",
      "state": "docked",
      "last_updated_epoch": 48,
      "recent_history": [{"leg": 1, "location": "new_winchester", "arrived_epoch": 48}],
      "itinerary": []
    },
    "discovered_locations": {
      "new_winchester": {
        "clock_direction": null,
        "captains_notes": [],
        "bazaar": {"reset_epoch": null, "available_bargains": []}
      },
      "titania": {
        "clock_direction": 2,
        "captains_notes": [],
        "bazaar": {"reset_epoch": null, "available_bargains": []}
      },
      "port_prosper": {
        "clock_direction": 6,
        "captains_notes": [],
        "bazaar": {"reset_epoch": null, "available_bargains": []}
      }
    }
  }
}
```

#### JSON State Verification:

* `dynamic_save_state.current_day_epoch`
* `dynamic_save_state.unified_inventory_registry.fuel.qty_in_hold`
* `dynamic_save_state.unified_inventory_registry.supplies.qty_in_hold`
* `dynamic_save_state.navigation.state`
* `dynamic_save_state.navigation.itinerary[0].location`

### Expected Verification:

#### State Transition:

`docked` ➔ `departing`

#### Flat JSON State Extraction:

```json
{
  "dynamic_save_state.current_day_epoch": 48,
  "dynamic_save_state.unified_inventory_registry.fuel.qty_in_hold": 1,
  "dynamic_save_state.unified_inventory_registry.supplies.qty_in_hold": 1,
  "dynamic_save_state.navigation.state": "departing",
  "dynamic_save_state.navigation.itinerary[0].location": "port_prosper"
}
```

#### Report Text:

```markdown
# 🚂 CAPTAIN'S LOG 🚀

## 📅 18 February 1905 (Day 48) · ⚓ New Winchester

**🗺️ Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 620 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock-Class Scout)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS

| System | Status |
| --- | --- |
| **Crew:** | 🟢 10 / 10 |
| **Hull:** | 🟢 25 / 30 |
| **Terror:** | 🟢 40 / 100 |
| **Nightmares:** | 🟢 1 / 4 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS | Base | Perks | Total |
| --- | --- | --- | --- |
| - 👊 Iron | 0 | 0 | **0** |
| - 👁️ Mirrors | 0 | 0 | **0** |
| - ❤️ Hearts | 0 | 0 | **0** |
| - 🎭 Veils | 0 | 0 | **0** |
| 🔍 **AFFILIATIONS** | **Base** | **Perks** | **Total** |
| - 🔍 Academe | 0 | 0 | **0** |
| - 🍷 Bohemia | 0 | 0 | **0** |
| - 👑 Establishment | 0 | 0 | **0** |
| - 🎩 Villainy | 0 | 0 | **0** |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** [ unknown ] (Tier [ unknown ]) — *Next Milestone: [ unknown ]*

📋 **First Officer's Counsel:**

> Mr. Bligh raising a serious operational concern, Captain. Casting off directly for Port Prosper with a single barrel of fuel and one crate of supplies is courting disaster. Prosper sits way out on the outer ring at the 6 o'clock mark. Our reserves are beneath safe thresholds. I strongly counsel an immediate diversion via Titania at the 2 o'clock ring to bunker fuel and provisions before we push across the wild expanse.

### 🧭 Active Trajectory:

New Winchester ➔ 🟢 **Port Prosper**

### ➡️ NEXT STOP: Port Prosper

### 👤 ACTIVE PASSENGERS & BRIDGE TRANSIT

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 2 / 12

| Trade Good Name | Physical Hold | Hub Bank Stock | Active Sourcing Progress / Status | Destination Port |
| --- | --- | --- | --- | --- |
| **🔥 Fuel** | 1 | 0 | ⚠️ | — |
| **📦 Supplies** | 1 | 0 | ⚠️ | — |

---

## 🛞 BRIDGE ROSTER

| Station | Active Officer | Skill Perks | Affiliation Perks |
| --- | --- | --- | --- |
| ⚓ **First Officer** | 🔘 Vacant | — | — |
| 🛞 **Quartermaster** | 🔘 Vacant | — | — |
| 🏮 **Signaller** | 🔘 Vacant | — | — |
| ⚙️ **Chief Engineer** | 🔘 Vacant | — | — |
| 🐶 **Mascot** | 🔘 Vacant | — | — |

### ⏳ SECONDMENT OUTLOOK
```

---

#### 🔒 INTERNAL STATE AUTOSAVE

```json
{"save_format":"sunless-skies-first-mate","schema_version":"0.4.0","rules_version":"0.4.0","static_data_version":"0.4.0","first_mate_name":"Mr. Bligh","dynamic_save_state":{"sovereigns":620,"current_day_epoch":48,"captain":{"name":"Sinclair","skills":{"iron":0,"mirrors":0,"hearts":0,"veils":0},"affiliations":{"academe":0,"bohemia":0,"establishment":0,"villainy":0}},"locomotive":{"model":"Spatchcock-Class Scout","name":"Zephyr","hull":25,"max_hull":30,"fuel_used_last_leg":0,"hold_capacity":12,"hidden_slots":0,"hold_rules":{"fuel_reserve_minimum":3,"supplies_reserve_minimum":3,"discovery_buffer_slots":2}},"crew":{"current":10,"max":10,"terror":40,"nightmares":1},"officer_manifest":{},"unified_inventory_registry":{"fuel":{"qty_in_hold":1,"qty_in_bank":0,"average_unit_cost":20.0},"supplies":{"qty_in_hold":1,"qty_in_bank":0,"average_unit_cost":40.0}},"possessions":{},"active_action_stream":[],"completed_action_log":[],"navigation":{"current_location":"new_winchester","state":"departing","last_updated_epoch":48,"recent_history":[{"leg":1,"location":"new_winchester","arrived_epoch":48}],"itinerary":[{"leg":2,"location":"port_prosper"}]},"discovered_locations":{"new_winchester":{"clock_direction":null,"captains_notes":[],"bazaar":{"reset_epoch":null,"available_bargains":[]}},"titania":{"clock_direction":2,"captains_notes":[],"bazaar":{"reset_epoch":null,"available_bargains":[]}},"port_prosper":{"clock_direction":6,"captains_notes":[],"bazaar":{"reset_epoch":null,"available_bargains":[]}}}}}
```


## Test Case 9: Cargo Isolation & Weightless Possessions Tracking

### Objective
Verifies that spatial possessions (Category 2: 16 immutable progression tokens) and narrative quest items (Category 3: polymorphic items manifest) do not draw physical hold space against `locomotive.hold_capacity` (§ 6.3.2, § 6.3.3). Confirms that a polymorphic quest object is cleanly constructed within `dynamic_save_state.active_action_stream` (§ 4.3.2), checks that non-zero possessions populate their respective affiliation domain while zero-quantity commodities and possessions are strictly suppressed from the JSON payload, and tests mid-month High Wilderness calendar calculation (`1905-01-15` = Day 14).

### Input Prompt
> Update state. Captain's log: 1905-01-15. We acquired two Tales of Terror out in the dark on that last run. We took on a quest from The Sequestered Scholar to deliver a Primordial Star Shard to Port Avon. Log this as "The Last Consignment." Let's make sure our logistics files are updated before we cast off lines for Port Avon.

```json
{
  "save_format": "sunless-skies-first-mate",
  "schema_version": "0.4.0",
  "rules_version": "0.4.0",
  "static_data_version": "0.4.0",
  "first_mate_name": "Mr. Bligh",
  "dynamic_save_state": {
    "sovereigns": 800,
    "current_day_epoch": 14,
    "captain": {
      "name": "Sinclair",
      "skills": {"iron": 0, "mirrors": 0, "hearts": 0, "veils": 0},
      "affiliations": {"academe": 0, "bohemia": 0, "establishment": 0, "villainy": 0}
    },
    "locomotive": {
      "model": "Spatchcock-Class Scout",
      "name": "Zephyr",
      "hull": 30,
      "max_hull": 30,
      "fuel_used_last_leg": 2,
      "hold_capacity": 12,
      "hidden_slots": 0,
      "hold_rules": {"fuel_reserve_minimum": 3, "supplies_reserve_minimum": 3, "discovery_buffer_slots": 2}
    },
    "crew": {"current": 8, "max": 10, "terror": 0, "nightmares": 0},
    "officer_manifest": {},
    "unified_inventory_registry": {
      "fuel": {"qty_in_hold": 4, "qty_in_bank": 0, "average_unit_cost": 20.00},
      "supplies": {"qty_in_hold": 4, "qty_in_bank": 0, "average_unit_cost": 40.00},
      "approved_literature": {"qty_in_hold": 2, "qty_in_bank": 0, "average_unit_cost": 100.00}
    },
    "possessions": {},
    "active_action_stream": [],
    "completed_action_log": [],
    "navigation": {
      "current_location": "new_winchester",
      "state": "docked",
      "last_updated_epoch": 14,
      "recent_history": [{"leg": 1, "location": "new_winchester", "arrived_epoch": 0}],
      "itinerary": []
    },
    "discovered_locations": {}
  }
}

```

### JSON State Verification:

* `dynamic_save_state.possessions.villainy.tale_of_terror`
* `dynamic_save_state.active_action_stream[0].action_id`
* `dynamic_save_state.active_action_stream[0].type`
* `dynamic_save_state.active_action_stream[0].payload.items_manifest.narrative_items[0].narrative_item_name`
* `dynamic_save_state.active_action_stream[0].payload.items_manifest.narrative_items[0].quantity_required`
* `dynamic_save_state.active_action_stream[0].payload.active_destinations[0].location`
* `dynamic_save_state.navigation.state`
* `dynamic_save_state.navigation.itinerary[0].location`


### Expected Verification:

#### State Transition:

`docked` ➔ `departing`

#### Flat JSON State Extraction:

```json
{
  "dynamic_save_state.possessions.villainy.tale_of_terror": 2,
  "dynamic_save_state.active_action_stream[0].action_id": "ACT-1001",
  "dynamic_save_state.active_action_stream[0].type": "quest",
  "dynamic_save_state.active_action_stream[0].payload.items_manifest.narrative_items[0].narrative_item_name": "Primordial Star Shard",
  "dynamic_save_state.active_action_stream[0].payload.items_manifest.narrative_items[0].quantity_required": 1,
  "dynamic_save_state.active_action_stream[0].payload.active_destinations[0].location": "port_avon",
  "dynamic_save_state.navigation.state": "departing",
  "dynamic_save_state.navigation.itinerary[0].location": "port_avon"
}

```

#### Report Text:

```markdown
# 🚂 CAPTAIN'S LOG 🚀

## 📅 15 January 1905 (Day 14) · ⚓ New Winchester

**🗺️ Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 800 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock-Class Scout)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS

| System | Status |
| --- | --- |
| **Crew:** | 🟢 8 / 10 |
| **Hull:** | 🟢 30 / 30 |
| **Terror:** | 🟢 0 / 100 |
| **Nightmares:** | 🟢 0 / 4 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS | Base | Perks | Total |
| --- | --- | --- | --- |
| - 👊 Iron | 0 | 0 | **0** |
| - 👁️ Mirrors | 0 | 0 | **0** |
| - ❤️ Hearts | 0 | 0 | **0** |
| - 🎭 Veils | 0 | 0 | **0** |
| 🔍 **AFFILIATIONS** | **Base** | **Perks** | **Total** |
| - 🔍 Academe | 0 | 0 | **0** |
| - 🍷 Bohemia | 0 | 0 | **0** |
| - 👑 Establishment | 0 | 0 | **0** |
| - 🎩 Villainy | 0 | 0 | **0** |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** [ unknown ] (Tier [ unknown ]) — *Next Milestone: [ unknown ]*

📋 **First Officer's Counsel:**

> Mr. Bligh at the logbook. The Sequestered Scholar's commission is entered as 'The Last Consignment', bound for Port Avon with that Primordial Star Shard stowed safely in the charts cabinet. It takes up no physical hold tonnage, nor do the two Tales of Terror tucked into our records. Hold utilization sits at 10 of 12 with full boilers and larders. Clear skies out to Port Avon.

### 🧭 Active Trajectory:

New Winchester ➔ 🟢 **Port Avon**

### ➡️ NEXT STOP: Port Avon

* 📖 **QUEST PLOTLINE:** The Last Consignment — Step 1: Deliver a Primordial Star Shard to Port Avon for The Sequestered Scholar

### 👤 ACTIVE PASSENGERS & BRIDGE TRANSIT

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 10 / 12

| Trade Good Name | Physical Hold | Hub Bank Stock | Active Sourcing Progress / Status | Destination Port |
| --- | --- | --- | --- | --- |
| **🔥 Fuel** | 4 | 0 | 🟢 | — |
| **📦 Supplies** | 4 | 0 | 🟢 | — |
| **Approved Literature** | 2 | 0 | — | — |

---

## 🛞 BRIDGE ROSTER

| Station | Active Officer | Skill Perks | Affiliation Perks |
| --- | --- | --- | --- |
| ⚓ **First Officer** | 🔘 Vacant | — | — |
| 🛞 **Quartermaster** | 🔘 Vacant | — | — |
| 🏮 **Signaller** | 🔘 Vacant | — | — |
| ⚙️ **Chief Engineer** | 🔘 Vacant | — | — |
| 🐶 **Mascot** | 🔘 Vacant | — | — |

### ⏳ SECONDMENT OUTLOOK
```

---

#### 🔒 INTERNAL STATE AUTOSAVE

```json
{"save_format":"sunless-skies-first-mate","schema_version":"0.4.0","rules_version":"0.4.0","static_data_version":"0.4.0","first_mate_name":"Mr. Bligh","dynamic_save_state":{"sovereigns":800,"current_day_epoch":14,"captain":{"name":"Sinclair","skills":{"iron":0,"mirrors":0,"hearts":0,"veils":0},"affiliations":{"academe":0,"bohemia":0,"establishment":0,"villainy":0}},"locomotive":{"model":"Spatchcock-Class Scout","name":"Zephyr","hull":30,"max_hull":30,"fuel_used_last_leg":2,"hold_capacity":12,"hidden_slots":0,"hold_rules":{"fuel_reserve_minimum":3,"supplies_reserve_minimum":3,"discovery_buffer_slots":2}},"crew":{"current":8,"max":10,"terror":0,"nightmares":0},"officer_manifest":{},"unified_inventory_registry":{"fuel":{"qty_in_hold":4,"qty_in_bank":0,"average_unit_cost":20.0},"supplies":{"qty_in_hold":4,"qty_in_bank":0,"average_unit_cost":40.0},"approved_literature":{"qty_in_hold":2,"qty_in_bank":0,"average_unit_cost":100.0}},"possessions":{"villainy":{"tale_of_terror":2},},"active_action_stream":[{"action_id":"ACT-1001","type":"quest","status":"active","origin_location":"new_winchester","title":"The Last Consignment","notes":"Deliver a Primordial Star Shard to Port Avon for The Sequestered Scholar","priority":"routine","is_pinned":false,"created_epoch":14,"updated_epoch":14,"deadline_epoch":null,"payload":{"npc_or_faction":"The Sequestered Scholar","current_step_number":1,"quest_pattern":"fetch","active_destinations":[{"location":"port_avon","objective":"Deliver a Primordial Star Shard"}],"items_manifest":{"goods":[],"possessions":[],"narrative_items":[{"narrative_item_name":"Primordial Star Shard","quantity_required":1,"quantity_delivered":0}]}}}],"completed_action_log":[],"navigation":{"current_location":"new_winchester","state":"departing","last_updated_epoch":14,"recent_history":[{"leg":1,"location":"new_winchester","arrived_epoch":0}],"itinerary":[{"leg":2,"location":"port_avon"}]},"discovered_locations":{}}}
```

---

## Test Case 10: Prospect Sourcing Phase to Sourced Readiness Mutation

### Objective

Verifies that sourcing the final required units of a standard trade good atomically increments `unified_inventory_registry` hold quantities, updates `quantity_sourced`, transitions the prospect lifecycle from `status: "active"` to `status: "ready"` (§ 4.2.2, § 4.3.1), evaluates spatial target matching to surface the contract under NEXT STOP (§ 4.2.1, § 8.2.1), suppresses zero-quantity commodities/possessions, and parses mid-February High Wilderness dates (`1905-02-18` = Day 48).

### Input Prompt

> Update state. I've finished loading the remaining 2 crates of Munitions here at New Winchester, completely filling our contract order. Plotting course to set sail for Port Prosper.

```json
{
  "save_format": "sunless-skies-first-mate",
  "schema_version": "0.4.0",
  "rules_version": "0.4.0",
  "static_data_version": "0.4.0",
  "first_mate_name": "Mr. Bligh",
  "dynamic_save_state": {
    "sovereigns": 1000,
    "current_day_epoch": 48,
    "captain": {
      "name": "Sinclair",
      "skills": {"iron": 0, "mirrors": 0, "hearts": 0, "veils": 0},
      "affiliations": {"academe": 0, "bohemia": 0, "establishment": 0, "villainy": 0}
    },
    "locomotive": {
      "model": "Spatchcock-Class Scout",
      "name": "Zephyr",
      "hull": 30,
      "max_hull": 30,
      "fuel_used_last_leg": 0,
      "hold_capacity": 12,
      "hidden_slots": 0,
      "hold_rules": {"fuel_reserve_minimum": 3, "supplies_reserve_minimum": 3, "discovery_buffer_slots": 2}
    },
    "crew": {"current": 10, "max": 10, "terror": 12, "nightmares": 0},
    "officer_manifest": {
      "on_duty": {},
    "unified_inventory_registry": {
      "fuel": {"qty_in_hold": 3, "qty_in_bank": 0, "average_unit_cost": 20.00},
      "supplies": {"qty_in_hold": 3, "qty_in_bank": 0, "average_unit_cost": 40.00},
      "munitions": {"qty_in_hold": 2, "qty_in_bank": 0, "average_unit_cost": 60.00}
    },
    "possessions": {},
    "active_action_stream": [
      {
        "action_id": "ACT-1001",
        "type": "prospect",
        "status": "active",
        "origin_location": "new_winchester",
        "title": "Fortress Resupply",
        "notes": "Urgent munitions shipment for the garrison.",
        "priority": "routine",
        "is_pinned": false,
        "created_epoch": 48,
        "updated_epoch": 48,
        "deadline_epoch": null,
        "payload": {
          "good_key": "munitions",
          "quantity_required": 4,
          "quantity_sourced": 2,
          "quantity_delivered": 0,
          "destination_location": "port_prosper"
        }
      }
    ],
    "completed_action_log": [],
    "navigation": {
      "current_location": "new_winchester",
      "state": "docked",
      "last_updated_epoch": 48,
      "recent_history": [{"leg": 1, "location": "new_winchester", "arrived_epoch": 48}],
      "itinerary": []
    },
    "discovered_locations": {}
  }
}
```

### JSON State Verification:

* `dynamic_save_state.unified_inventory_registry.munitions.qty_in_hold`
* `dynamic_save_state.active_action_stream[0].status`
* `dynamic_save_state.active_action_stream[0].payload.quantity_sourced`
* `dynamic_save_state.active_action_stream[0].payload.destination_location`
* `dynamic_save_state.navigation.state`
* `dynamic_save_state.navigation.itinerary[0].location`

### Expected Verification:

#### State Transition:

`docked` ➔ `departing`

#### Flat JSON State Extraction:

```json
{
  "dynamic_save_state.unified_inventory_registry.munitions.qty_in_hold": 4,
  "dynamic_save_state.active_action_stream[0].status": "ready",
  "dynamic_save_state.active_action_stream[0].payload.quantity_sourced": 4,
  "dynamic_save_state.active_action_stream[0].payload.destination_location": "port_prosper",
  "dynamic_save_state.navigation.state": "departing",
  "dynamic_save_state.navigation.itinerary[0].location": "port_prosper"
}

```

#### Report Text:

```markdown
# 🚂 CAPTAIN'S LOG 🚀

## 📅 18 February 1905 (Day 48) · ⚓ New Winchester

**🗺️ Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 1000 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock-Class Scout)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS

| System | Status |
| --- | --- |
| **Crew:** | 🟢 10 / 10 |
| **Hull:** | 🟢 30 / 30 |
| **Terror:** | 🟢 12 / 100 |
| **Nightmares:** | 🟢 0 / 4 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS | Base | Perks | Total |
| --- | --- | --- | --- |
| - 👊 Iron | 0 | 0 | **0** |
| - 👁️ Mirrors | 0 | 0 | **0** |
| - ❤️ Hearts | 0 | 0 | **0** |
| - 🎭 Veils | 0 | 0 | **0** |
| 🔍 **AFFILIATIONS** | **Base** | **Perks** | **Total** |
| - 🔍 Academe | 0 | 0 | **0** |
| - 🍷 Bohemia | 0 | 0 | **0** |
| - 👑 Establishment | 0 | 0 | **0** |
| - 🎩 Villainy | 0 | 0 | **0** |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** [ unknown ] (Tier [ unknown ]) — *Next Milestone: [ unknown ]*

📋 **First Officer's Counsel:**

> Mr. Bligh here. Final 2 crates of Munitions are strapped down in the forward hold, bringing the order for Port Prosper to full manifest. Total hold space used is 10 of 12. Course laid straight out to the company garrison at Port Prosper; boilers are up and lines are clear.

### 🧭 Active Trajectory:

New Winchester ➔ 🟢 **Port Prosper**

### ➡️ NEXT STOP: Port Prosper

* 🔑 **READY FOR DELIVERY:** Fortress Resupply — Deliver 4 Crate of Munitions to Port Prosper to complete contract

### 👤 ACTIVE PASSENGERS & BRIDGE TRANSIT

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 10 / 12

| Trade Good Name | Physical Hold | Hub Bank Stock | Active Sourcing Progress / Status | Destination Port |
| --- | --- | --- | --- | --- |
| **🔥 Fuel** | 3 | 0 | 🟢 | — |
| **📦 Supplies** | 3 | 0 | 🟢 | — |
| **Crate of Munitions** | 4 | 0 | 4 / 4 Loaded (ACT-1001) | Port Prosper |

---

## 🛞 BRIDGE ROSTER

| Station | Active Officer | Skill Perks | Affiliation Perks |
| --- | --- | --- | --- |
| ⚓ **First Officer** | 🔘 Vacant | — | — |
| 🛞 **Quartermaster** | 🔘 Vacant | — | — |
| 🏮 **Signaller** | 🔘 Vacant | — | — |
| ⚙️ **Chief Engineer** | 🔘 Vacant | — | — |
| 🐶 **Mascot** | 🔘 Vacant | — | — |

### ⏳ SECONDMENT OUTLOOK
```

---

#### 🔒 INTERNAL STATE AUTOSAVE

```json
{"save_format":"sunless-skies-first-mate","schema_version":"0.4.0","rules_version":"0.4.0","static_data_version":"0.4.0","first_mate_name":"Mr. Bligh","dynamic_save_state":{"sovereigns":1000,"current_day_epoch":48,"captain":{"name":"Sinclair","skills":{"iron":0,"mirrors":0,"hearts":0,"veils":0},"affiliations":{"academe":0,"bohemia":0,"establishment":0,"villainy":0}},"locomotive":{"model":"Spatchcock-Class Scout","name":"Zephyr","hull":30,"max_hull":30,"fuel_used_last_leg":0,"hold_capacity":12,"hidden_slots":0,"hold_rules":{"fuel_reserve_minimum":3,"supplies_reserve_minimum":3,"discovery_buffer_slots":2}},"crew":{"current":10,"max":10,"terror":12,"nightmares":0},"officer_manifest":{},"unified_inventory_registry":{"fuel":{"qty_in_hold":3,"qty_in_bank":0,"average_unit_cost":20.0},"supplies":{"qty_in_hold":3,"qty_in_bank":0,"average_unit_cost":40.0},"munitions":{"qty_in_hold":4,"qty_in_bank":0,"average_unit_cost":60.0}},"possessions":{},"active_action_stream":[{"action_id":"ACT-1001","type":"prospect","status":"ready","origin_location":"new_winchester","title":"Fortress Resupply","notes":"Urgent munitions shipment for the garrison.","priority":"routine","is_pinned":false,"created_epoch":48,"updated_epoch":48,"deadline_epoch":null,"payload":{"good_key":"munitions","quantity_required":4,"quantity_sourced":4,"quantity_delivered":0,"destination_location":"port_prosper"}}],"completed_action_log":[],"navigation":{"current_location":"new_winchester","state":"departing","last_updated_epoch":48,"recent_history":[{"leg":1,"location":"new_winchester","arrived_epoch":48}],"itinerary":[{"leg":2,"location":"port_prosper"}]},"discovered_locations":{}}}
```

---

## Test Case 11: Partial Delivery of a Quest Shopping List Pattern

### Objective

Verifies that partial delivery of items toward a quest "shopping list" pattern (§ 4.3.2) correctly decrements the physical hold inventory, increments `quantity_delivered` within `items_manifest.goods`, maintains `status: "active"` until the entire manifest is satisfied, retains active destinations, and completely suppresses zero-quantity commodities (`chorister_nectar`) and empty possession blocks from the JSON payload.

### Input Prompt

> Update state. Just arrived at Titania and went straight to the Chief Botanist. I handed over the single bottle of Chorister Nectar he requested, but I don't have the Verdant Seeds yet. Setting off lines toward New Winchester to search for the seeds.

```json
{
  "save_format": "sunless-skies-first-mate",
  "schema_version": "0.4.0",
  "rules_version": "0.4.0",
  "static_data_version": "0.4.0",
  "first_mate_name": "Mr. Bligh",
  "dynamic_save_state": {
    "sovereigns": 1000,
    "current_day_epoch": 48,
    "captain": {
      "name": "Sinclair",
      "skills": {"iron": 0, "mirrors": 0, "hearts": 0, "veils": 0},
      "affiliations": {"academe": 0, "bohemia": 0, "establishment": 0, "villainy": 0}
    },
    "locomotive": {
      "model": "Spatchcock-Class Scout",
      "name": "Zephyr",
      "hull": 30,
      "max_hull": 30,
      "fuel_used_last_leg": 0,
      "hold_capacity": 12,
      "hidden_slots": 0,
      "hold_rules": {"fuel_reserve_minimum": 3, "supplies_reserve_minimum": 3, "discovery_buffer_slots": 2}
    },
    "crew": {"current": 10, "max": 10, "terror": 12, "nightmares": 0},
    "officer_manifest": {},
    "unified_inventory_registry": {
      "fuel": {"qty_in_hold": 3, "qty_in_bank": 0, "average_unit_cost": 20.00},
      "supplies": {"qty_in_hold": 3, "qty_in_bank": 0, "average_unit_cost": 40.00},
      "chorister_nectar": {"qty_in_hold": 1, "qty_in_bank": 0, "average_unit_cost": 120.00}
    },
    "possessions": {},
    "active_action_stream": [
      {
        "action_id": "ACT-2002",
        "type": "quest",
        "status": "active",
        "origin_location": "titania",
        "title": "The Glass Greenhouse",
        "notes": "Gather elements for the biome update.",
        "priority": "routine",
        "is_pinned": false,
        "created_epoch": 45,
        "updated_epoch": 45,
        "deadline_epoch": null,
        "payload": {
          "npc_or_faction": "Chief Botanist",
          "current_step_number": 1,
          "quest_pattern": "shopping_list",
          "active_destinations": [
            {"location": "titania", "objective": "Deliver Chorister Nectar and Verdant Seeds"}
          ],
          "items_manifest": {
            "goods": [
              {"good_key": "chorister_nectar", "quantity_required": 1, "quantity_delivered": 0},
              {"good_key": "verdant_seeds", "quantity_required": 2, "quantity_delivered": 0}
            ],
            "possessions": [],
            "narrative_items": []
          }
        }
      }
    ],
    "completed_action_log": [],
    "navigation": {
      "current_location": "titania",
      "state": "docked",
      "last_updated_epoch": 48,
      "recent_history": [{"leg": 1, "location": "titania", "arrived_epoch": 48}],
      "itinerary": []
    },
    "discovered_locations": {}
  }
}

```

### JSON State Verification:

* `dynamic_save_state.unified_inventory_registry.chorister_nectar`
* `dynamic_save_state.active_action_stream[0].status`
* `dynamic_save_state.active_action_stream[0].payload.items_manifest.goods[0].good_key`
* `dynamic_save_state.active_action_stream[0].payload.items_manifest.goods[0].quantity_delivered`
* `dynamic_save_state.active_action_stream[0].payload.items_manifest.goods[1].good_key`
* `dynamic_save_state.active_action_stream[0].payload.items_manifest.goods[1].quantity_delivered`
* `dynamic_save_state.navigation.state`
* `dynamic_save_state.navigation.itinerary[0].location`

### Expected Verification:

#### State Transition:

`docked` ➔ `departing`

#### Flat JSON State Extraction:

```json
{
  "dynamic_save_state.unified_inventory_registry.chorister_nectar": null,
  "dynamic_save_state.active_action_stream[0].status": "active",
  "dynamic_save_state.active_action_stream[0].payload.items_manifest.goods[0].good_key": "chorister_nectar",
  "dynamic_save_state.active_action_stream[0].payload.items_manifest.goods[0].quantity_delivered": 1,
  "dynamic_save_state.active_action_stream[0].payload.items_manifest.goods[1].good_key": "verdant_seeds",
  "dynamic_save_state.active_action_stream[0].payload.items_manifest.goods[1].quantity_delivered": 0,
  "dynamic_save_state.navigation.state": "departing",
  "dynamic_save_state.navigation.itinerary[0].location": "new_winchester"
}
```

#### Report Text:

```markdown
# 🚂 CAPTAIN'S LOG 🚀

## 📅 18 February 1905 (Day 48) · ⚓ Titania

**🗺️ Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 1000 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock-Class Scout)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS

| System | Status |
| --- | --- |
| **Crew:** | 🟢 10 / 10 |
| **Hull:** | 🟢 30 / 30 |
| **Terror:** | 🟢 12 / 100 |
| **Nightmares:** | 🟢 0 / 4 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS | Base | Perks | Total |
| --- | --- | --- | --- |
| - 👊 Iron | 0 | 0 | **0** |
| - 👁️ Mirrors | 0 | 0 | **0** |
| - ❤️ Hearts | 0 | 0 | **0** |
| - 🎭 Veils | 0 | 0 | **0** |
| 🔍 **AFFILIATIONS** | **Base** | **Perks** | **Total** |
| - 🔍 Academe | 0 | 0 | **0** |
| - 🍷 Bohemia | 0 | 0 | **0** |
| - 👑 Establishment | 0 | 0 | **0** |
| - 🎩 Villainy | 0 | 0 | **0** |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** [ unknown ] (Tier [ unknown ]) — *Next Milestone: [ unknown ]*

📋 **First Officer's Counsel:**

> Mr. Bligh logging cargo handoff. We delivered the single crate of Chorister Nectar to the Chief Botanist here at Titania, satisfying the first half of the Glass Greenhouse requisition. We still owe him 2 sacks of Verdant Seeds before this plotline clears. Casting off lines for New Winchester to source the remaining goods.

### 🧭 Active Trajectory:

Titania ➔ 🟢 **New Winchester**

### ➡️ NEXT STOP: New Winchester

### 👤 ACTIVE PASSENGERS & BRIDGE TRANSIT

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 6 / 12

| Trade Good Name | Physical Hold | Hub Bank Stock | Active Sourcing Progress / Status | Destination Port |
| --- | --- | --- | --- | --- |
| **🔥 Fuel** | 3 | 0 | 🟢 | — |
| **📦 Supplies** | 3 | 0 | 🟢 | — |

---

## 🛞 BRIDGE ROSTER

| Station | Active Officer | Skill Perks | Affiliation Perks |
| --- | --- | --- | --- |
| ⚓ **First Officer** | 🔘 Vacant | — | — |
| 🛞 **Quartermaster** | 🔘 Vacant | — | — |
| 🏮 **Signaller** | 🔘 Vacant | — | — |
| ⚙️ **Chief Engineer** | 🔘 Vacant | — | — |
| 🐶 **Mascot** | 🔘 Vacant | — | — |

### ⏳ SECONDMENT OUTLOOK
```

---

#### 🔒 INTERNAL STATE AUTOSAVE

```json
{"save_format":"sunless-skies-first-mate","schema_version":"0.4.0","rules_version":"0.4.0","static_data_version":"0.4.0","first_mate_name":"Mr. Bligh","dynamic_save_state":{"sovereigns":1000,"current_day_epoch":48,"captain":{"name":"Sinclair","skills":{"iron":0,"mirrors":0,"hearts":0,"veils":0},"affiliations":{"academe":0,"bohemia":0,"establishment":0,"villainy":0}},"locomotive":{"model":"Spatchcock-Class Scout","name":"Zephyr","hull":30,"max_hull":30,"fuel_used_last_leg":0,"hold_capacity":12,"hidden_slots":0,"hold_rules":{"fuel_reserve_minimum":3,"supplies_reserve_minimum":3,"discovery_buffer_slots":2}},"crew":{"current":10,"max":10,"terror":12,"nightmares":0},"officer_manifest":{},"unified_inventory_registry":{"fuel":{"qty_in_hold":3,"qty_in_bank":0,"average_unit_cost":20.0},"supplies":{"qty_in_hold":3,"qty_in_bank":0,"average_unit_cost":40.0}},"possessions":{},"active_action_stream":[{"action_id":"ACT-2002","type":"quest","status":"active","origin_location":"titania","title":"The Glass Greenhouse","notes":"Gather elements for the biome update.","priority":"routine","is_pinned":false,"created_epoch":45,"updated_epoch":48,"deadline_epoch":null,"payload":{"npc_or_faction":"Chief Botanist","current_step_number":1,"quest_pattern":"shopping_list","active_destinations":[{"location":"titania","objective":"Deliver Chorister Nectar and Verdant Seeds"}],"items_manifest":{"goods":[{"good_key":"chorister_nectar","quantity_required":1,"quantity_delivered":1},{"good_key":"verdant_seeds","quantity_required":2,"quantity_delivered":0}],"possessions":[],"narrative_items":[]}}}],"completed_action_log":[],"navigation":{"current_location":"titania","state":"departing","last_updated_epoch":48,"recent_history":[{"leg":1,"location":"titania","arrived_epoch":48}],"itinerary":[{"leg":2,"location":"new_winchester"}]},"discovered_locations":{}}}
```

---

## Test Case 12: Partial Delivery of an Underway Prospect

### Objective

Verifies that when docked at the destination location of an active mercantile prospect, delivering partial units increments `quantity_delivered`, decrements physical hold inventory, maintains `status: "ready"` (since `quantity_delivered < quantity_required`), leaves the action active in the stream (§ 4.2.2, § 4.3.1), correctly reflects hold utilization in the departure logbook, suppresses unheld commodities/empty possessions, and checks calendar advance (`1905-02-19` = Day 49).

### Input Prompt

> Update state. Just docked at Port Prosper. I went to the garrison quartermaster and delivered 2 of our 4 loaded crates of Munitions. We are holding onto the other 2 crates for now while I check the local markets. Show me the logbook.

```json
{
  "save_format": "sunless-skies-first-mate",
  "schema_version": "0.4.0",
  "rules_version": "0.4.0",
  "static_data_version": "0.4.0",
  "first_mate_name": "Mr. Bligh",
  "dynamic_save_state": {
    "sovereigns": 1000,
    "current_day_epoch": 49,
    "captain": {
      "name": "Sinclair",
      "skills": {"iron": 0, "mirrors": 0, "hearts": 0, "veils": 0},
      "affiliations": {"academe": 0, "bohemia": 0, "establishment": 0, "villainy": 0}
    },
    "locomotive": {
      "model": "Spatchcock-Class Scout",
      "name": "Zephyr",
      "hull": 30,
      "max_hull": 30,
      "fuel_used_last_leg": 0,
      "hold_capacity": 12,
      "hidden_slots": 0,
      "hold_rules": {"fuel_reserve_minimum": 3, "supplies_reserve_minimum": 3, "discovery_buffer_slots": 2}
    },
    "crew": {"current": 10, "max": 10, "terror": 10, "nightmares": 0},
    "officer_manifest": {
      "on_duty": {},
    "unified_inventory_registry": {
      "fuel": {"qty_in_hold": 3, "qty_in_bank": 0, "average_unit_cost": 20.00},
      "supplies": {"qty_in_hold": 3, "qty_in_bank": 0, "average_unit_cost": 40.00},
      "munitions": {"qty_in_hold": 4, "qty_in_bank": 0, "average_unit_cost": 60.00}
    },
    "possessions": {},
    "active_action_stream": [
      {
        "action_id": "ACT-1001",
        "type": "prospect",
        "status": "ready",
        "origin_location": "new_winchester",
        "title": "Fortress Resupply",
        "notes": "Urgent munitions shipment for the garrison.",
        "priority": "routine",
        "is_pinned": false,
        "created_epoch": 48,
        "updated_epoch": 48,
        "deadline_epoch": null,
        "payload": {
          "good_key": "munitions",
          "quantity_required": 4,
          "quantity_sourced": 4,
          "quantity_delivered": 0,
          "destination_location": "port_prosper"
        }
      }
    ],
    "completed_action_log": [],
    "navigation": {
      "current_location": "port_prosper",
      "state": "docked",
      "last_updated_epoch": 49,
      "recent_history": [{"leg": 1, "location": "port_prosper", "arrived_epoch": 49}],
      "itinerary": []
    },
    "discovered_locations": {}
  }
}
```

### JSON State Verification:

* `dynamic_save_state.unified_inventory_registry.munitions.qty_in_hold`
* `dynamic_save_state.active_action_stream[0].status`
* `dynamic_save_state.active_action_stream[0].payload.quantity_delivered`
* `dynamic_save_state.active_action_stream[0].payload.quantity_required`
* `dynamic_save_state.navigation.state`

### Expected Verification:

#### State Transition:

`docked` ➔ `departing` (Prompt explicitly commands: "Show me the logbook", forcing departure logbook generation per § 8.1.1)

#### Flat JSON State Extraction:

```json
{
  "dynamic_save_state.unified_inventory_registry.munitions.qty_in_hold": 2,
  "dynamic_save_state.active_action_stream[0].status": "ready",
  "dynamic_save_state.active_action_stream[0].payload.quantity_delivered": 2,
  "dynamic_save_state.active_action_stream[0].payload.quantity_required": 4,
  "dynamic_save_state.navigation.state": "departing"
}
```

#### Report Text:

```markdown
# 🚂 CAPTAIN'S LOG 🚀

## 📅 19 February 1905 (Day 49) · ⚓ Port Prosper

**🗺️ Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 1000 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock-Class Scout)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS

| System | Status |
| --- | --- |
| **Crew:** | 🟢 10 / 10 |
| **Hull:** | 🟢 30 / 30 |
| **Terror:** | 🟢 10 / 100 |
| **Nightmares:** | 🟢 0 / 4 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS | Base | Perks | Total |
| --- | --- | --- | --- |
| - 👊 Iron | 0 | 0 | **0** |
| - 👁️ Mirrors | 0 | 0 | **0** |
| - ❤️ Hearts | 0 | 0 | **0** |
| - 🎭 Veils | 0 | 0 | **0** |
| 🔍 **AFFILIATIONS** | **Base** | **Perks** | **Total** |
| - 🔍 Academe | 0 | 0 | **0** |
| - 🍷 Bohemia | 0 | 0 | **0** |
| - 👑 Establishment | 0 | 0 | **0** |
| - 🎩 Villainy | 0 | 0 | **0** |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** [ unknown ] (Tier [ unknown ]) — *Next Milestone: [ unknown ]*

📋 **First Officer's Counsel:**

> Mr. Bligh logging inventory. 2 of the 4 crates of Munitions have been transferred to the garrison storehouse here at Port Prosper. The contract remains active with 2 crates retained in our physical hold. Hold utilization sits at 8 of 12. Logbook printed per your command, Captain.

### 🧭 Active Trajectory:

Port Prosper ➔ 🟢 **[ unknown ]**

### ➡️ NEXT STOP: [ unknown ]

### 👤 ACTIVE PASSENGERS & BRIDGE TRANSIT

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 8 / 12

| Trade Good Name | Physical Hold | Hub Bank Stock | Active Sourcing Progress / Status | Destination Port |
| --- | --- | --- | --- | --- |
| **🔥 Fuel** | 3 | 0 | 🟢 | — |
| **📦 Supplies** | 3 | 0 | 🟢 | — |
| **Crate of Munitions** | 2 | 0 | 2 / 4 Loaded (ACT-1001) | Port Prosper |

---

## 🛞 BRIDGE ROSTER

| Station | Active Officer | Skill Perks | Affiliation Perks |
| --- | --- | --- | --- |
| ⚓ **First Officer** | 🔘 Vacant | — | — |
| 🛞 **Quartermaster** | 🔘 Vacant | — | — |
| 🏮 **Signaller** | 🔘 Vacant | — | — |
| ⚙️ **Chief Engineer** | 🔘 Vacant | — | — |
| 🐶 **Mascot** | 🔘 Vacant | — | — |

### ⏳ SECONDMENT OUTLOOK
```

---

#### 🔒 INTERNAL STATE AUTOSAVE

```json
{"save_format":"sunless-skies-first-mate","schema_version":"0.4.0","rules_version":"0.4.0","static_data_version":"0.4.0","first_mate_name":"Mr. Bligh","dynamic_save_state":{"sovereigns":1000,"current_day_epoch":49,"captain":{"name":"Sinclair","skills":{"iron":0,"mirrors":0,"hearts":0,"veils":0},"affiliations":{"academe":0,"bohemia":0,"establishment":0,"villainy":0}},"locomotive":{"model":"Spatchcock-Class Scout","name":"Zephyr","hull":30,"max_hull":30,"fuel_used_last_leg":0,"hold_capacity":12,"hidden_slots":0,"hold_rules":{"fuel_reserve_minimum":3,"supplies_reserve_minimum":3,"discovery_buffer_slots":2}},"crew":{"current":10,"max":10,"terror":10,"nightmares":0},"officer_manifest":{},"unified_inventory_registry":{"fuel":{"qty_in_hold":3,"qty_in_bank":0,"average_unit_cost":20.0},"supplies":{"qty_in_hold":3,"qty_in_bank":0,"average_unit_cost":40.0},"munitions":{"qty_in_hold":2,"qty_in_bank":0,"average_unit_cost":60.0}},"possessions":{},"active_action_stream":[{"action_id":"ACT-1001","type":"prospect","status":"ready","origin_location":"new_winchester","title":"Fortress Resupply","notes":"Urgent munitions shipment for the garrison.","priority":"routine","is_pinned":false,"created_epoch":48,"updated_epoch":49,"deadline_epoch":null,"payload":{"good_key":"munitions","quantity_required":4,"quantity_sourced":4,"quantity_delivered":2,"destination_location":"port_prosper"}}],"completed_action_log":[],"navigation":{"current_location":"port_prosper","state":"departing","last_updated_epoch":49,"recent_history":[{"leg":1,"location":"port_prosper","arrived_epoch":49}],"itinerary":[]},"discovered_locations":{}}}
```

---

## Test Case 13: Dynamic Stat Resolution & Companion Upgrades

### Objective
Verifies dynamic officer perk resolution (§ 7.3.1), ensuring runtime evaluation reads composite keys (e.g., `"navigator.stalwart"`) and that perks are not written to JSON (§ 8.3.1). Validates non-leap High Wilderness calendar calculations crossing into the subsequent year (`1906-02-22` = \(365 + 31 + 21 = \text{Day } 417\)), confirms zero-quantity commodities/possessions remain suppressed in JSON, and checks layout mapping for officer secondments under NEXT STOP (§ 4.2.4, § 8.2.1).

### Input Prompt
> Update state. London - 22 February 1906. Our First Officer has promoted to "The Stalwart Navigator." Ready the crew and cast lines off for Avid Horizon.

```json
{
  "save_format": "sunless-skies-first-mate",
  "schema_version": "0.4.0",
  "rules_version": "0.4.0",
  "static_data_version": "0.4.0",
  "first_mate_name": "Mr. Bligh",
  "dynamic_save_state": {
    "sovereigns": 1000,
    "current_day_epoch": 417,
    "captain": {
      "name": "Sinclair",
      "skills": {"iron": 10, "mirrors": 18, "hearts": 25, "veils": 7},
      "affiliations": {"academe": 0, "bohemia": 0, "establishment": 0, "villainy": 0}
    },
    "locomotive": {
      "model": "Spatchcock-Class Scout",
      "name": "Zephyr",
      "hull": 30,
      "max_hull": 30,
      "fuel_used_last_leg": 0,
      "hold_capacity": 12,
      "hidden_slots": 0,
      "hold_rules": {"fuel_reserve_minimum": 3, "supplies_reserve_minimum": 3, "discovery_buffer_slots": 2}
    },
    "crew": {"current": 10, "max": 10, "terror": 12, "nightmares": 0},
    "officer_manifest": {
      "on_duty": {
        "first_officer": "navigator.fortunate",
        "quartermaster": "aunt.inconvenient",
        "mascot": "dog"
      },
      "unassigned": {"first_officer": ["princess.incognito", "conductor.clay"]},
      "seconded": {"signaller": ["devil.repentant"]}
    },
    "unified_inventory_registry": {
      "fuel": {"qty_in_hold": 3, "qty_in_bank": 0, "average_unit_cost": 20.00},
      "supplies": {"qty_in_hold": 3, "qty_in_bank": 0, "average_unit_cost": 40.00}
    },
    "possessions": {},
    "active_action_stream": [
      {
        "action_id": "ACT-1011",
        "type": "officer_secondment",
        "status": "active",
        "origin_location": "home_office",
        "title": "Secondment: Repentant Devil",
        "notes": "Generates prospects near the Avid Horizon.",
        "priority": "routine",
        "is_pinned": false,
        "created_epoch": 366,
        "updated_epoch": 366,
        "deadline_epoch": 400,
        "payload": {
          "officer_id_key": "devil.repentant",
          "duration_days": 34,
          "contribution_effect": "Generates prospects at Avid Horizon",
          "return_condition": "Collect in person"
        }
      }
    ],
    "completed_action_log": [],
    "navigation": {
      "current_location": "london",
      "state": "docked",
      "last_updated_epoch": 417,
      "recent_history": [{"leg": 1, "location": "london", "arrived_epoch": 417}],
      "itinerary": []
    },
    "discovered_locations": {}
  }
}
```

### JSON State Verification:

* `dynamic_save_state.current_day_epoch`
* `dynamic_save_state.officer_manifest.on_duty.first_officer`
* `dynamic_save_state.navigation.state`
* `dynamic_save_state.navigation.itinerary[0].location`

### Expected Verification:

#### State Transition:

`docked` ➔ `departing`

#### Flat JSON State Extraction:

```json
{
  "dynamic_save_state.current_day_epoch": 417,
  "dynamic_save_state.officer_manifest.on_duty.first_officer": "navigator.stalwart",
  "dynamic_save_state.navigation.state": "departing",
  "dynamic_save_state.navigation.itinerary[0].location": "avid_horizon"
}
```

#### Report Text:

```markdown
# 🚂 CAPTAIN'S LOG 🚀

## 📅 22 February 1906 (Day 417) · ⚓ London

**🗺️ Region:** Albion | **👤 Captain:** Sinclair | **🪙 Wallet:** 1000 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock-Class Scout)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS

| System | Status |
| --- | --- |
| **Crew:** | 🟢 10 / 10 |
| **Hull:** | 🟢 30 / 30 |
| **Terror:** | 🟢 12 / 100 |
| **Nightmares:** | 🟢 0 / 4 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS | Base | Perks | Total |
| --- | --- | --- | --- |
| - 👊 Iron | 10 | +17 | **27** |
| - 👁️ Mirrors | 18 | +2 | **20** |
| - ❤️ Hearts | 25 | 0 | **25** |
| - 🎭 Veils | 7 | 0 | **7** |
| 🔍 **AFFILIATIONS** | **Base** | **Perks** | **Total** |
| - 🔍 Academe | 0 | 0 | **0** |
| - 🍷 Bohemia | 0 | +1 | **1** |
| - 👑 Establishment | 0 | +2 | **2** |
| - 🎩 Villainy | 0 | 0 | **0** |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** [ unknown ] (Tier [ unknown ]) — *Next Milestone: [ unknown ]*

📋 **First Officer's Counsel:**

> Mr. Bligh at the bridge log. The Navigator has stepped into his new rank as Stalwart Navigator—our gunnery and bridge discipline are markedly sharper for it (+10 Iron, +1 Bohemia). Lines cast off from London into the cold mist of Albion, steaming toward the Avid Horizon spectacle via Home Office coordinates.

### 🧭 Active Trajectory:

London ➔ 🟢 **The Avid Horizon**

### ➡️ NEXT STOP: The Avid Horizon

### 👤 ACTIVE PASSENGERS & BRIDGE TRANSIT

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 6 / 12

| Trade Good Name | Physical Hold | Hub Bank Stock | Active Sourcing Progress / Status | Destination Port |
| --- | --- | --- | --- | --- |
| **🔥 Fuel** | 3 | 0 | 🟢 | — |
| **📦 Supplies** | 3 | 0 | 🟢 | — |

---

## 🛞 BRIDGE ROSTER

| Station | Active Officer | Skill Perks | Affiliation Perks |
| --- | --- | --- | --- |
| ⚓ **First Officer** | Stalwart Navigator | +10 Iron | +1 Bohemia / +1 Establishment |
| 🛞 **Quartermaster** | Inconvenient Aunt | +6 Iron / +2 Mirrors | +1 Establishment |
| 🏮 **Signaller** | 🔘 Vacant | — | — |
| ⚙️ **Chief Engineer** | 🔘 Vacant | — | — |
| 🐶 **Mascot** | Inadvisably Big Dog | +1 Iron | — |

### ⏳ SECONDMENT OUTLOOK

* **Repentant Devil** (signaller) ➔ Deployed at: home_office
* *Maturity Condition:* 🟢 **Ready**
* *Pending Interaction Reward:* Generates prospects at Avid Horizon
```

---

#### 🔒 INTERNAL STATE AUTOSAVE

```json
{"save_format":"sunless-skies-first-mate","schema_version":"0.4.0","rules_version":"0.4.0","static_data_version":"0.4.0","first_mate_name":"Mr. Bligh","dynamic_save_state":{"sovereigns":1000,"current_day_epoch":417,"captain":{"name":"Sinclair","skills":{"iron":10,"mirrors":18,"hearts":25,"veils":7},"affiliations":{"academe":0,"bohemia":0,"establishment":0,"villainy":0}},"locomotive":{"model":"Spatchcock-Class Scout","name":"Zephyr","hull":30,"max_hull":30,"fuel_used_last_leg":0,"hold_capacity":12,"hidden_slots":0,"hold_rules":{"fuel_reserve_minimum":3,"supplies_reserve_minimum":3,"discovery_buffer_slots":2}},"crew":{"current":10,"max":10,"terror":12,"nightmares":0},"officer_manifest":{"on_duty":{"first_officer":"navigator.stalwart","quartermaster":"aunt.inconvenient","mascot":"dog"},"unassigned":{"first_officer":["princess.incognito","conductor.clay"]},"seconded":{"signaller":["devil.repentant"]}},"unified_inventory_registry":{"fuel":{"qty_in_hold":3,"qty_in_bank":0,"average_unit_cost":20.0},"supplies":{"qty_in_hold":3,"qty_in_bank":0,"average_unit_cost":40.0}},"possessions":{},"active_action_stream":[{"action_id":"ACT-1011","type":"officer_secondment","status":"ready","origin_location":"home_office","title":"Secondment: Repentant Devil","notes":"Generates prospects near the Avid Horizon.","priority":"high","is_pinned":false,"created_epoch":366,"updated_epoch":366,"deadline_epoch":400,"payload":{"officer_id_key":"devil.repentant","duration_days":34,"contribution_effect":"Generates prospects at Avid Horizon","return_condition":"Collect in person"}}],"completed_action_log":[],"navigation":{"current_location":"london","state":"departing","last_updated_epoch":417,"recent_history":[{"leg":1,"location":"london","arrived_epoch":417}],"itinerary":[{"leg":2,"location":"avid_horizon"}]},"discovered_locations":{}}}
```

---

## Test Case 14: Multi-State Compound Turn Pipeline

### Objective

Tests the multi-state kinetic turn pipeline (§ 3.1.2). Ingests transit burn and arrival at Lustrum (`enroute` ➔ `arriving`), executes commerce and hold adjustments while docked (`arriving` ➔ `docked`), performs rolling hold/fuel checks, and transitions out to open skies (`docked` ➔ `departing` ➔ `enroute`). Verifies `recent_history` captures arrival epoch while forward itinerary renumbers cleanly (§ 5.3), evaluates the terminal state as `enroute` (§ 3.1.2 Step 6), emits the departure logbook and autosave block, suppresses zero-quantity goods/possessions, and validates date advance (`1905-01-20` = Day 19).

### Input Prompt

> Update state. Arrived at Lustrum on 1905-01-20 with 1 fuel spent. While docked, we sold our 2 crates of Unseasoned Hours for 160 Sovereigns total, bought 2 Barrels of Fuel at standard cost (20 each), and immediately cast off lines for Port Avon.

```json
{
  "save_format": "sunless-skies-first-mate",
  "schema_version": "0.4.0",
  "rules_version": "0.4.0",
  "static_data_version": "0.4.0",
  "first_mate_name": "Mr. Bligh",
  "dynamic_save_state": {
    "sovereigns": 500,
    "current_day_epoch": 16,
    "captain": {
      "name": "Sinclair",
      "skills": {"iron": 0, "mirrors": 0, "hearts": 0, "veils": 0},
      "affiliations": {"academe": 0, "bohemia": 0, "establishment": 0, "villainy": 0}
    },
    "locomotive": {
      "model": "Spatchcock-Class Scout",
      "name": "Zephyr",
      "hull": 30,
      "max_hull": 30,
      "fuel_used_last_leg": 0,
      "hold_capacity": 12,
      "hidden_slots": 0,
      "hold_rules": {"fuel_reserve_minimum": 3, "supplies_reserve_minimum": 3, "discovery_buffer_slots": 2}
    },
    "crew": {"current": 8, "max": 10, "terror": 10, "nightmares": 0},
    "officer_manifest": {}
    "unified_inventory_registry": {
      "fuel": {"qty_in_hold": 4, "qty_in_bank": 0, "average_unit_cost": 20.00},
      "supplies": {"qty_in_hold": 3, "qty_in_bank": 0, "average_unit_cost": 40.00},
      "unseasoned_hours": {"qty_in_hold": 2, "qty_in_bank": 0, "average_unit_cost": 40.00}
    },
    "possessions": {},
    "active_action_stream": [],
    "completed_action_log": [],
    "navigation": {
      "current_location": null,
      "state": "enroute",
      "last_updated_epoch": 16,
      "recent_history": [{"leg": 1, "location": "port_prosper", "arrived_epoch": 7},{"leg": 2, "location": "new_winchester", "arrived_epoch": 10},{"leg": 3, "location": "carillon", "arrived_epoch": 16}],
      "itinerary": [{"leg": 4, "location": "lustrum"}]
    },
    "discovered_locations": {}
  }
}
```

### JSON State Verification:

* `dynamic_save_state.current_day_epoch`
* `dynamic_save_state.sovereigns`
* `dynamic_save_state.locomotive.fuel_used_last_leg`
* `dynamic_save_state.unified_inventory_registry.fuel.qty_in_hold`
* `dynamic_save_state.unified_inventory_registry.unseasoned_hours`
* `dynamic_save_state.navigation.state`
* `dynamic_save_state.navigation.current_location`
* `dynamic_save_state.navigation.recent_history[0].location`
* `dynamic_save_state.navigation.recent_history[0].arrived_epoch`
* `dynamic_save_state.navigation.recent_history[1].location`
* `dynamic_save_state.navigation.recent_history[1].arrived_epoch`
* `dynamic_save_state.navigation.itinerary[0].location`

### Expected Verification:

#### State Transition:

`enroute` ➔ `arriving` ➔ `docked` ➔ `departing` ➔ `enroute` (Multi-state compound turn pipeline executed atomically)

#### Flat JSON State Extraction:

```json
{
  "dynamic_save_state.current_day_epoch": 19,
  "dynamic_save_state.sovereigns": 620,
  "dynamic_save_state.locomotive.fuel_used_last_leg": 1,
  "dynamic_save_state.unified_inventory_registry.fuel.qty_in_hold": 5,
  "dynamic_save_state.unified_inventory_registry.unseasoned_hours": null,
  "dynamic_save_state.navigation.state": "enroute",
  "dynamic_save_state.navigation.current_location": null,
  "dynamic_save_state.navigation.recent_history[1].location": "carillon",
  "dynamic_save_state.navigation.recent_history[1].arrived_epoch": 16,
  "dynamic_save_state.navigation.recent_history[2].location": "lustrum",
  "dynamic_save_state.navigation.recent_history[2].arrived_epoch": 19,
  "dynamic_save_state.navigation.itinerary[0].location": "port_avon"
}
```

#### Report Text:

```markdown
# 🚂 CAPTAIN'S LOG 🚀

## 📅 20 January 1905 (Day 19) · ⚓ Lustrum

**🗺️ Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 620 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock-Class Scout)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS

| System | Status |
| --- | --- |
| **Crew:** | 🟢 8 / 10 |
| **Hull:** | 🟢 30 / 30 |
| **Terror:** | 🟢 10 / 100 |
| **Nightmares:** | 🟢 0 / 4 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS | Base | Perks | Total |
| --- | --- | --- | --- |
| - 👊 Iron | 0 | 0 | **0** |
| - 👁️ Mirrors | 0 | 0 | **0** |
| - ❤️ Hearts | 0 | 0 | **0** |
| - 🎭 Veils | 0 | 0 | **0** |
| 🔍 **AFFILIATIONS** | **Base** | **Perks** | **Total** |
| - 🔍 Academe | 0 | 0 | **0** |
| - 🍷 Bohemia | 0 | 0 | **0** |
| - 👑 Establishment | 0 | 0 | **0** |
| - 🎩 Villainy | 0 | 0 | **0** |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** [ unknown ] (Tier [ unknown ]) — *Next Milestone: [ unknown ]*

📋 **First Officer's Counsel:**

> Mr. Bligh reporting underway operations. Quick turnaround at Lustrum: transit burn of 1 fuel ingested, 2 crates of Unseasoned Hours sold into the market for +160 Sovereigns, and bunkered 2 barrels of fuel (-40 Sovereigns). Mooring slipped immediately; we are underway in open sky for Port Avon with 5 fuel and 3 supplies.

### 🧭 Active Trajectory:

Lustrum ➔ 🟢 **Port Avon**

### ➡️ NEXT STOP: Port Avon

### 👤 ACTIVE PASSENGERS & BRIDGE TRANSIT

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 8 / 12

| Trade Good Name | Physical Hold | Hub Bank Stock | Active Sourcing Progress / Status | Destination Port |
| --- | --- | --- | --- | --- |
| **🔥 Fuel** | 5 | 0 | 🟢 | — |
| **📦 Supplies** | 3 | 0 | 🟢 | — |

---

## 🛞 BRIDGE ROSTER

| Station | Active Officer | Skill Perks | Affiliation Perks |
| --- | --- | --- | --- |
| ⚓ **First Officer** | 🔘 Vacant | — | — |
| 🛞 **Quartermaster** | 🔘 Vacant | — | — |
| 🏮 **Signaller** | 🔘 Vacant | — | — |
| ⚙️ **Chief Engineer** | 🔘 Vacant | — | — |
| 🐶 **Mascot** | 🔘 Vacant | — | — |

### ⏳ SECONDMENT OUTLOOK
```

---

#### 🔒 INTERNAL STATE AUTOSAVE

```json
{"save_format":"sunless-skies-first-mate","schema_version":"0.4.0","rules_version":"0.4.0","static_data_version":"0.4.0","first_mate_name":"Mr. Bligh","dynamic_save_state":{"sovereigns":620,"current_day_epoch":19,"captain":{"name":"Sinclair","skills":{"iron":0,"mirrors":0,"hearts":0,"veils":0},"affiliations":{"academe":0,"bohemia":0,"establishment":0,"villainy":0}},"locomotive":{"model":"Spatchcock-Class Scout","name":"Zephyr","hull":30,"max_hull":30,"fuel_used_last_leg":1,"hold_capacity":12,"hidden_slots":0,"hold_rules":{"fuel_reserve_minimum":3,"supplies_reserve_minimum":3,"discovery_buffer_slots":2}},"crew":{"current":8,"max":10,"terror":10,"nightmares":0},"officer_manifest":{},"unified_inventory_registry":{"fuel":{"qty_in_hold":5,"qty_in_bank":0,"average_unit_cost":20.0},"supplies":{"qty_in_hold":3,"qty_in_bank":0,"average_unit_cost":40.0}},"possessions":{},"active_action_stream":[],"completed_action_log":[],"navigation":{"current_location":null,"state":"enroute","last_updated_epoch":19,"recent_history":[{"leg":1,"location":"new_winchester","arrived_epoch":10},{"leg": 2, "location": "new_winchester", "arrived_epoch": 10},{"leg": 3, "location": "carillon", "arrived_epoch": 16,"leg":4,"location":"lustrum","arrived_epoch":19}],"itinerary":[{"leg":5,"location":"port_avon"}]},"discovered_locations":{}}}
```

---

## Test Case 15: Economic Core & Moving Average Cost (MAC) Recalculation

### Objective

Tests the Moving Average Cost (MAC) formula. Verifies atomic sovereign deduction, hold slot tracking, physical free slot validation (§ 7.2.1), suppression of unheld inventory items, and calendar evaluation crossing a 30-day month boundary.

### Input Prompt

> Update state. We are docked at London on 1905-04-30. We currently hold 2 crates of Munitions with an average cost of 60 Sovereigns each. The Ministries are offering surplus munitions at a discount: we just purchased 4 additional crates of Munitions for 30 Sovereigns each. We also picked up 2 barrels of Fuel at 20 each, and now we are casting off lines for Brabazon Workworld.

```json
{
  "save_format": "sunless-skies-first-mate",
  "schema_version": "0.4.0",
  "rules_version": "0.4.0",
  "static_data_version": "0.4.0",
  "first_mate_name": "Mr. Bligh",
  "dynamic_save_state": {
    "sovereigns": 1000,
    "current_day_epoch": 119,
    "captain": {
      "name": "Sinclair",
      "skills": {"iron": 0, "mirrors": 0, "hearts": 0, "veils": 0},
      "affiliations": {"academe": 0, "bohemia": 0, "establishment": 0, "villainy": 0}
    },
    "locomotive": {
      "model": "Spatchcock-Class Scout",
      "name": "Zephyr",
      "hull": 30,
      "max_hull": 30,
      "fuel_used_last_leg": 0,
      "hold_capacity": 12,
      "hidden_slots": 0,
      "hold_rules": {"fuel_reserve_minimum": 3, "supplies_reserve_minimum": 3, "discovery_buffer_slots": 2}
    },
    "crew": {"current": 8, "max": 10, "terror": 15, "nightmares": 0},
    "officer_manifest": {},
    "unified_inventory_registry": {
      "fuel": {"qty_in_hold": 1, "qty_in_bank": 0, "average_unit_cost": 20.00},
      "supplies": {"qty_in_hold": 3, "qty_in_bank": 0, "average_unit_cost": 40.00},
      "munitions": {"qty_in_hold": 2, "qty_in_bank": 0, "average_unit_cost": 60.00}
    },
    "possessions": {},
    "active_action_stream": [],
    "completed_action_log": [],
    "navigation": {
      "current_location": "london",
      "state": "docked",
      "last_updated_epoch": 119,
      "recent_history": [{"leg": 1, "location": "london", "arrived_epoch": 119}],
      "itinerary": []
    },
    "discovered_locations": {}
  }
}

```

### JSON State Verification:

* `dynamic_save_state.sovereigns`
* `dynamic_save_state.unified_inventory_registry.munitions.qty_in_hold`
* `dynamic_save_state.unified_inventory_registry.munitions.average_unit_cost`
* `dynamic_save_state.unified_inventory_registry.fuel.qty_in_hold`
* `dynamic_save_state.navigation.state`
* `dynamic_save_state.navigation.itinerary[0].location`


### Expected Verification:

#### State Transition:

`docked` ➔ `departing`

#### Mathematical Pipeline Calculation:

* **Munitions MAC:** Existing $(2 \times 60.00 = 120.00)$ plus New $(4 \times 30.00 = 120.00) \rightarrow \frac{240.00}{6} = 40.00$
* **Sovereign Deductions:** $1000 - (4 \times 30) - (2 \times 20) = 1000 - 120 - 40 = 840$ Sovereigns
* **Hold Slots Used:** $3 \text{ Fuel} + 3 \text{ Supplies} + 6 \text{ Munitions} = 12 / 12$ slots ($Free = 0$)

#### Flat JSON State Extraction:

```json
{
  "dynamic_save_state.sovereigns": 840,
  "dynamic_save_state.unified_inventory_registry.munitions.qty_in_hold": 6,
  "dynamic_save_state.unified_inventory_registry.munitions.average_unit_cost": 40.0,
  "dynamic_save_state.unified_inventory_registry.fuel.qty_in_hold": 3,
  "dynamic_save_state.navigation.state": "departing",
  "dynamic_save_state.navigation.itinerary[0].location": "brabazon_workworld"
}
```

#### Report Text:

```markdown
# 🚂 CAPTAIN'S LOG 🚀

## 📅 30 April 1905 (Day 119) · ⚓ London

**🗺️ Region:** Albion | **👤 Captain:** Sinclair | **🪙 Wallet:** 840 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock-Class Scout)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS

| System | Status |
| --- | --- |
| **Crew:** | 🟢 8 / 10 |
| **Hull:** | 🟢 30 / 30 |
| **Terror:** | 🟢 15 / 100 |
| **Nightmares:** | 🟢 0 / 4 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS | Base | Perks | Total |
| --- | --- | --- | --- |
| - 👊 Iron | 0 | 0 | **0** |
| - 👁️ Mirrors | 0 | 0 | **0** |
| - ❤️ Hearts | 0 | 0 | **0** |
| - 🎭 Veils | 0 | 0 | **0** |
| 🔍 **AFFILIATIONS** | **Base** | **Perks** | **Total** |
| - 🔍 Academe | 0 | 0 | **0** |
| - 🍷 Bohemia | 0 | 0 | **0** |
| - 👑 Establishment | 0 | 0 | **0** |
| - 🎩 Villainy | 0 | 0 | **0** |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** [ unknown ] (Tier [ unknown ]) — *Next Milestone: [ unknown ]*

📋 **First Officer's Counsel:**

> Mr. Bligh at the ledger. We acquired 4 surplus crates of Munitions at 30 Sovereigns apiece, bringing our total hold stock to 6 crates with a recalculated moving average cost of 40.00 Sovereigns each. Bunkered 2 barrels of fuel to meet minimum safety reserves. Hold is packed to absolute maximum capacity at 12 of 12 slots; discovery buffer is zeroed out. Clearing the Thames mooring collar for Brabazon Workworld.

### 🧭 Active Trajectory:

London ➔ 🟢 **The Brabazon Workworld**

### ➡️ NEXT STOP: The Brabazon Workworld

### 👤 ACTIVE PASSENGERS & BRIDGE TRANSIT

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 12 / 12

| Trade Good Name | Physical Hold | Hub Bank Stock | Active Sourcing Progress / Status | Destination Port |
| --- | --- | --- | --- | --- |
| **🔥 Fuel** | 3 | 0 | 🟢 | — |
| **📦 Supplies** | 3 | 0 | 🟢 | — |
| **Crate of Munitions** | 6 | 0 | — | — |

---

## 🛞 BRIDGE ROSTER

| Station | Active Officer | Skill Perks | Affiliation Perks |
| --- | --- | --- | --- |
| ⚓ **First Officer** | 🔘 Vacant | — | — |
| 🛞 **Quartermaster** | 🔘 Vacant | — | — |
| 🏮 **Signaller** | 🔘 Vacant | — | — |
| ⚙️ **Chief Engineer** | 🔘 Vacant | — | — |
| 🐶 **Mascot** | 🔘 Vacant | — | — |

### ⏳ SECONDMENT OUTLOOK

---
```

#### 🔒 INTERNAL STATE AUTOSAVE

```json
{"save_format":"sunless-skies-first-mate","schema_version":"0.4.0","rules_version":"0.4.0","static_data_version":"0.4.0","first_mate_name":"Mr. Bligh","dynamic_save_state":{"sovereigns":840,"current_day_epoch":119,"captain":{"name":"Sinclair","skills":{"iron":0,"mirrors":0,"hearts":0,"veils":0},"affiliations":{"academe":0,"bohemia":0,"establishment":0,"villainy":0}},"locomotive":{"model":"Spatchcock-Class Scout","name":"Zephyr","hull":30,"max_hull":30,"fuel_used_last_leg":0,"hold_capacity":12,"hidden_slots":0,"hold_rules":{"fuel_reserve_minimum":3,"supplies_reserve_minimum":3,"discovery_buffer_slots":2}},"crew":{"current":8,"max":10,"terror":15,"nightmares":0},"officer_manifest":{},"unified_inventory_registry":{"fuel":{"qty_in_hold":3,"qty_in_bank":0,"average_unit_cost":20.0},"supplies":{"qty_in_hold":3,"qty_in_bank":0,"average_unit_cost":40.0},"munitions":{"qty_in_hold":6,"qty_in_bank":0,"average_unit_cost":40.0}},"possessions":{},"active_action_stream":[],"completed_action_log":[],"navigation":{"current_location":"london","state":"departing","last_updated_epoch":119,"recent_history":[{"leg":1,"location":"london","arrived_epoch":119}],"itinerary":[{"leg":2,"location":"brabazon_workworld"}]},"discovered_locations":{}}}
```

---

## Test Case 16: Inter-Region Transit Relay Trajectory & Toll Evaluation

### Objective

Tests inter-region relay gating rules (§ 3.4.2 Guard 4 Case B). Verifies that plotting course through a transit relay (`reach_albion_relay`) to an external destination in Albion (`london`) verifies the required transit permit (`albion` permit key in `possessions.transit_permits`), audits payable toll options, alerts the Captain of required crossing costs without prematurely deducting assets while docked, suppresses zero-quantity items, and parses standardized High Wilderness calendar dates (`1905-06-15` = $31 + 28 + 31 + 30 + 31 + 14 = \text{Day } 165$).

### Input Prompt

> Update state. We are docked at New Winchester on 1905-06-15. We hold the necessary Albion Transit Permit stamped by the Ministry. Plot an inter-region course out through the Albion Transit Relay and straight on to London. Review our gate clearance and let me know our toll options before we set out.

```json
{
  "save_format": "sunless-skies-first-mate",
  "schema_version": "0.4.0",
  "rules_version": "0.4.0",
  "static_data_version": "0.4.0",
  "first_mate_name": "Mr. Bligh",
  "dynamic_save_state": {
    "sovereigns": 1200,
    "current_day_epoch": 165,
    "captain": {
      "name": "Sinclair",
      "skills": {"iron": 10, "mirrors": 5, "hearts": 5, "veils": 5},
      "affiliations": {"academe": 0, "bohemia": 0, "establishment": 1, "villainy": 0}
    },
    "locomotive": {
      "model": "Spatchcock-Class Scout",
      "name": "Zephyr",
      "hull": 30,
      "max_hull": 30,
      "fuel_used_last_leg": 0,
      "hold_capacity": 12,
      "hidden_slots": 0,
      "hold_rules": {"fuel_reserve_minimum": 3, "supplies_reserve_minimum": 3, "discovery_buffer_slots": 2}
    },
    "crew": {"current": 9, "max": 10, "terror": 10, "nightmares": 0},
    "officer_manifest": {},
    "unified_inventory_registry": {
      "fuel": {"qty_in_hold": 4, "qty_in_bank": 0, "average_unit_cost": 20.00},
      "supplies": {"qty_in_hold": 4, "qty_in_bank": 0, "average_unit_cost": 40.00},
      "unseasoned_hours": {"qty_in_hold": 2, "qty_in_bank": 0, "average_unit_cost": 80.00}
    },
    "possessions": {
      "establishment": {"ministry_stamped_permit": 1},
      "transit_permits": ["albion"]
    },
    "active_action_stream": [],
    "completed_action_log": [],
    "navigation": {
      "current_location": "new_winchester",
      "state": "docked",
      "last_updated_epoch": 165,
      "recent_history": [{"leg": 1, "location": "new_winchester", "arrived_epoch": 160}],
      "itinerary": []
    },
    "discovered_locations": {}
  }
}

```

### JSON State Verification:

* `dynamic_save_state.current_day_epoch`
* `dynamic_save_state.possessions.transit_permits[0]`
* `dynamic_save_state.navigation.state`
* `dynamic_save_state.navigation.itinerary[0].location`
* `dynamic_save_state.navigation.itinerary[1].location`

### Expected Verification:

#### State Transition:

`docked` ➔ `departing`

#### Flat JSON State Extraction:

```json
{
  "dynamic_save_state.current_day_epoch": 165,
  "dynamic_save_state.possessions.transit_permits[0]": "albion",
  "dynamic_save_state.navigation.state": "departing",
  "dynamic_save_state.navigation.itinerary[0].location": "reach_albion_relay",
  "dynamic_save_state.navigation.itinerary[1].location": "london"
}
```

#### Report Text:

```markdown
# 🚂 CAPTAIN'S LOG 🚀

## 📅 15 June 1905 (Day 165) · ⚓ New Winchester

**🗺️ Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 1200 Sovereigns

**🚂 Current Engine:** Zephyr (Spatchcock-Class Scout)

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS

| System | Status |
| --- | --- |
| **Crew:** | 🟢 9 / 10 |
| **Hull:** | 🟢 30 / 30 |
| **Terror:** | 🟢 10 / 100 |
| **Nightmares:** | 🟢 0 / 4 |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS | Base | Perks | Total |
| --- | --- | --- | --- |
| - 👊 Iron | 10 | 0 | **10** |
| - 👁️ Mirrors | 5 | 0 | **5** |
| - ❤️ Hearts | 5 | 0 | **5** |
| - 🎭 Veils | 5 | 0 | **5** |
| 🔍 **AFFILIATIONS** | **Base** | **Perks** | **Total** |
| - 🔍 Academe | 0 | 0 | **0** |
| - 🍷 Bohemia | 0 | 0 | **0** |
| - 👑 Establishment | 1 | 0 | **1** |
| - 🎩 Villainy | 0 | 0 | **0** |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** [ unknown ] (Tier [ unknown ]) — *Next Milestone: [ unknown ]*

📋 **First Officer's Counsel:**

> Mr. Bligh at the charts. Course laid through the Avid Horizon Relay to London in Albion. Permit verification passed: the Admiralty's Albion Transit Permit is present in our papers. Regarding the relay toll at the gate: we qualify for First Class transit using our 1 Ministry-Stamped Permit (2 days elapsed, -15 Terror), or Second Class using our 2 Unseasoned Hours (2 days elapsed, -5 Terror). No toll deducted until the sequencer-wheels engage. Boilers up for the relay run.

### 🧭 Active Trajectory:

New Winchester ➔ 🟢 **The Albion Transit Relay** ➔ 🟡 London

### ➡️ NEXT STOP: The Albion Transit Relay

### 👤 ACTIVE PASSENGERS & BRIDGE TRANSIT

---

## 📦 LOGISTICS

**📦 Hold Utilization:** 10 / 12

| Trade Good Name | Physical Hold | Hub Bank Stock | Active Sourcing Progress / Status | Destination Port |
| --- | --- | --- | --- | --- |
| **🔥 Fuel** | 4 | 0 | 🟢 | — |
| **📦 Supplies** | 4 | 0 | 🟢 | — |
| **Unseasoned Hours** | 2 | 0 | — | — |

---

## 🛞 BRIDGE ROSTER

| Station | Active Officer | Skill Perks | Affiliation Perks |
| --- | --- | --- | --- |
| ⚓ **First Officer** | 🔘 Vacant | — | — |
| 🛞 **Quartermaster** | 🔘 Vacant | — | — |
| 🏮 **Signaller** | 🔘 Vacant | — | — |
| ⚙️ **Chief Engineer** | 🔘 Vacant | — | — |
| 🐶 **Mascot** | 🔘 Vacant | — | — |

### ⏳ SECONDMENT OUTLOOK
```

---

#### 🔒 INTERNAL STATE AUTOSAVE

```json
{"save_format":"sunless-skies-first-mate","schema_version":"0.4.0","rules_version":"0.4.0","static_data_version":"0.4.0","first_mate_name":"Mr. Bligh","dynamic_save_state":{"sovereigns":1200,"current_day_epoch":165,"captain":{"name":"Sinclair","skills":{"iron":10,"mirrors":5,"hearts":5,"veils":5},"affiliations":{"academe":0,"bohemia":0,"establishment":1,"villainy":0}},"locomotive":{"model":"Spatchcock-Class Scout","name":"Zephyr","hull":30,"max_hull":30,"fuel_used_last_leg":0,"hold_capacity":12,"hidden_slots":0,"hold_rules":{"fuel_reserve_minimum":3,"supplies_reserve_minimum":3,"discovery_buffer_slots":2}},"crew":{"current":9,"max":10,"terror":10,"nightmares":0},"officer_manifest":{},"unified_inventory_registry":{"fuel":{"qty_in_hold":4,"qty_in_bank":0,"average_unit_cost":20.0},"supplies":{"qty_in_hold":4,"qty_in_bank":0,"average_unit_cost":40.0},"unseasoned_hours":{"qty_in_hold":2,"qty_in_bank":0,"average_unit_cost":80.0}},"possessions":{"establishment":{"ministry_stamped_permit":1},"transit_permits":["albion"]},"active_action_stream":[],"completed_action_log":[],"navigation":{"current_location":"new_winchester","state":"departing","last_updated_epoch":165,"recent_history":[{"leg":1,"location":"new_winchester","arrived_epoch":160}],"itinerary":[{"leg":2,"location":"reach_albion_relay"},{"leg":3,"location":"london"}]},"discovered_locations":{}}}
```

## Test Case 17: Navigation Itinerary Lifecycle, Rolling History Pruning & Port Arrival

### Objective
Verifies the kinetic transition from `enroute` ➔ `arriving` ➔ `docked` (§ 3.2) for a planned waypoint (`itinerary[0].location == current_location`). Confirms that the completed leg is popped from `navigation.itinerary`, stamped with `arrived_epoch: current_day_epoch`, and appended to `navigation.recent_history` (§ 3.2.3). Probes the rolling history cap invariant (§ 3.2.3, § 5.3): since `navigation.recent_history` begins with 3 prior locations, appending the 4th completed leg must drop the oldest historical entry (`recent_history[0]`) to maintain a strict rolling clamp of 3 completed stops. Checks that remaining forward itinerary legs are retained, verifies strict suppression of Markdown logbooks and autosave JSON blocks during arrival/docked turns (§ 3.2.5, § 8.1.2), suppresses zero-quantity commodities/possessions, and tests non-leap year boundary date calculations (`1905-03-05` = \(31 + 28 + 4 = \text{Day } 63\)).

### Input Prompt
> Update state. We just dropped mooring lines and arrived at Lustrum on 1905-03-05. Fuel burn on this leg was 2. What's the lay of the land here, First Mate?

```json
{
  "save_format": "sunless-skies-first-mate",
  "schema_version": "0.4.0",
  "rules_version": "0.4.0",
  "static_data_version": "0.4.0",
  "first_mate_name": "Mr. Bligh",
  "dynamic_save_state": {
    "sovereigns": 1100,
    "current_day_epoch": 61,
    "captain": {
      "name": "Sinclair",
      "skills": {"iron": 10, "mirrors": 5, "hearts": 5, "veils": 5},
      "affiliations": {"academe": 0, "bohemia": 0, "establishment": 0, "villainy": 0}
    },
    "locomotive": {
      "model": "Spatchcock-Class Scout",
      "name": "Zephyr",
      "hull": 30,
      "max_hull": 30,
      "fuel_used_last_leg": 0,
      "hold_capacity": 12,
      "hidden_slots": 0,
      "hold_rules": {"fuel_reserve_minimum": 3, "supplies_reserve_minimum": 3, "discovery_buffer_slots": 2}
    },
    "crew": {"current": 9, "max": 10, "terror": 15, "nightmares": 0},
    "officer_manifest": {},
    "unified_inventory_registry": {
      "fuel": {"qty_in_hold": 5, "qty_in_bank": 0, "average_unit_cost": 20.00},
      "supplies": {"qty_in_hold": 4, "qty_in_bank": 0, "average_unit_cost": 40.00}
    },
    "possessions": {},
    "active_action_stream": [],
    "completed_action_log": [],
    "navigation": {
      "current_location": null,
      "state": "enroute",
      "last_updated_epoch": 61,
      "recent_history": [
        {"leg": 1, "location": "new_winchester", "arrived_epoch": 45},
        {"leg": 2, "location": "port_prosper", "arrived_epoch": 52},
        {"leg": 3, "location": "port_avon", "arrived_epoch": 58}
      ],
      "itinerary": [
        {"leg": 4, "location": "lustrum"},
        {"leg": 5, "location": "titania"},
        {"leg": 6, "location": "new_winchester"}
      ]
    },
    "discovered_locations": {}
  }
}
```

### JSON State Verification:

* `dynamic_save_state.current_day_epoch`
* `dynamic_save_state.locomotive.fuel_used_last_leg`
* `dynamic_save_state.unified_inventory_registry.fuel.qty_in_hold`
* `dynamic_save_state.navigation.state`
* `dynamic_save_state.navigation.current_location`
* `dynamic_save_state.navigation.recent_history[0].location`
* `dynamic_save_state.navigation.recent_history[1].location`
* `dynamic_save_state.navigation.recent_history[2].location`
* `dynamic_save_state.navigation.recent_history[2].arrived_epoch`
* `dynamic_save_state.navigation.itinerary[0].location`
* `dynamic_save_state.navigation.itinerary[0].leg`
* `dynamic_save_state.navigation.itinerary[1].location`
* `dynamic_save_state.navigation.itinerary[1].leg`

### Expected Verification:

#### State Transition:

`enroute` ➔ `arriving` ➔ `docked`

#### Flat JSON State Extraction:

```json
{
  "dynamic_save_state.current_day_epoch": 63,
  "dynamic_save_state.locomotive.fuel_used_last_leg": 2,
  "dynamic_save_state.unified_inventory_registry.fuel.qty_in_hold": 3,
  "dynamic_save_state.navigation.state": "docked",
  "dynamic_save_state.navigation.current_location": "lustrum",
  "dynamic_save_state.navigation.recent_history[0].location": "port_prosper",
  "dynamic_save_state.navigation.recent_history[1].location": "port_avon",
  "dynamic_save_state.navigation.recent_history[2].location": "lustrum",
  "dynamic_save_state.navigation.recent_history[2].arrived_epoch": 63,
  "dynamic_save_state.navigation.itinerary[0].location": "titania",
  "dynamic_save_state.navigation.itinerary[0].leg": 5,
  "dynamic_save_state.navigation.itinerary[1].location": "new_winchester",
  "dynamic_save_state.navigation.itinerary[1].leg": 6
}

```

#### Report Text:

(Per Section 3.2.5 and Section 8.1.2, full Markdown logbooks and JSON autosave blocks are strictly suppressed during `arriving` and `docked` turns.)

> **Mr. Bligh reports:**
> "Lines secured at the icy quays of Lustrum on 5 March 1905. Two barrels of fuel deducted for the transit burn, leaving 3 in the hold alongside our 4 crates of supplies.
> Lustrum is freezing and bleak, huddled beneath the shadow of the Mother of Mountains where prospectors quarry frozen time straight from the rockface. Station facilities are operational: fuel bunkering, provisions, and crew recruitment are open, though there's no drydock shipyard here. Ahead on our charted course lie Titania and our eventual return to New Winchester. The ledger and transit logs are updated; awaiting your command before we step into the cold or conduct trade at the exchange."
