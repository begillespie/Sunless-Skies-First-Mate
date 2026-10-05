# SUNLESS SKIES FIRST MATE TEST CASES

<!--
Sunless Skies First Mate Engine Test Suite
Tests version: 0.5.0

Rules version: 0.6.1
Logbook version: 0.5.1
Save schema version: 0.5.1
Static data version: 0.4.1
-->

## MASTER TEST PACKAGE INDEX
| Sequence | Package Identifier | Functional Domain | Included Tests | Scope & Invariants Under Test |
| --- | --- | --- | --- | --- |
| 1 | **`PKG-IO`** | Core I/O & Validation | **TC1, TC4** | Cold-boot state initialization, baseline day 0 epoch, default locomotive parameters, and foreign key/location schema guardrail intercepts. |
| 2 | **`PKG-STATE`** | Kinetic State & Navigation | **TC2, TC5, TC6, TC14, TC16, TC17, TC18, TC19** | Kinetic loop cycling (`np`/`ne`/`na`), month-boundary temporal conversions, rolling history 3-stop clamps, crew/hull warning thresholds, and sparse bazaar serialization. |
| 3 | **`PKG-ECON`** | Routing & Economy | **TC3, TC7, TC8, TC15** | Central hub bank transfers, non-leap year calendar anomalies, multi-leg itinerary sequencing ($N+1$), angular coordinate checks ($\Delta\theta$), resupply isolation alerts, and Moving Average Cost ($MAC$) recomputations. |
| 4 | **`PKG-NARRATIVE`** | Actions & Officers | **TC9, TC10, TC11, TC12, TC13, TC20** | Weightless category 2/3 item isolation, prospect sourcing mutations (`active` ➔ `ready`), multi-item quest shopping lists, partial cargo handoffs, dynamic officer perk resolutions, and secondments. |

---

## MASTER TEST SUITE INDEX
| Test # | Package | Title | Primary Features Under Test |
| --- | --- | --- | --- |
| **TC1** | `PKG-IO` | **Session Initialization (Blank Slate Verification)** | Engine cold-boot without prior JSON; assignment of First Mate identity ("Mr. Bligh"); Day 0 baseline epoch handling; initial sovereign/fuel/supply parameters; default hold rules; initial departure logbook and autosave rendering.|
| **TC2** | `PKG-STATE` | **Port Arrival & Month-Boundary Bargain Discovery Tracking** | Kinetic FSM transition (`ne` ➔ `na` ➔ `np`); transit burn accounting; date conversion crossing month boundary (Jan 31 to Feb 12); bazaar bargain discovery and reset epoch logging; strict UI suppression during port calls.|
| **TC3** | `PKG-ECON` | **Inventory Math, Banking Logistics & Non-Leap Temporal Calculation** | Central hub bank transfers (`[0]` $\leftrightarrow$ `[1]`); standardized 365-day High Wilderness calendar invariant across non-leap leap-year anomalies (Feb 28 to Mar 1 1908 = +1 day); hold capacity re-evaluation; departure logbook rendering.|
| **TC4** | `PKG-IO` | **State Integrity Breach Emergency Intercept (Directive 2.2.4)** | Safety guardrail triggers; foreign key validation failure against unwhitelisted commodity keys (`quantum_æther_crystal`) and invalid locations (`missing_port_x`); execution halt and verbatim emergency recovery alert output.|
| **TC5** | `PKG-STATE` | **Crew Status Color Mapping - Yellow Tier Warning** | Numeric threshold mapping for crew ($50\% \le \text{Crew} < 70\% \rightarrow$ Yellow Tier) and hull integrity ($30\% \le \text{Hull} < 60\% \rightarrow$ Yellow Tier); year-boundary calendar calculation (Dec 31 1905 to Jan 15 1906); zero-quantity item suppression.|
| **TC6** | ``PKG-STATE`` | **Critical Low Crew Threshold & Consumable Depletion** | High-fatigue tone shifts when crew drops below 50% (Red Tier); consumable hold warnings (fuel $\le 1$ = ⚠️, supplies $= 0$ = 🚨); high-priority unpinned bridge note tracking (`todo`); departure manifest generation.|
| **TC7** | `PKG-ECON` | **Route Planner - Multi-Stop Sequential Itinerary & Task Linking** | Multi-leg route planning; sequential leg indexing ($N+1$ continuity); spatial task filtering under NEXT STOP for pending mercantile prospects and bridge notes; mid-year non-leap calendar conversion.|
| **TC8** | `PKG-ECON` | **Route Planner - Resupply Isolation Alert & Intermediate Port Recommendation** | Pre-departure consumable deficit guard; angular coordinate evaluation ($\Delta\theta$); automated intermediate port detour recommendations (Titania insertion); professional caution bridge counsel.|
| **TC9** | `PKG-NARRATIVE` | **Cargo Isolation & Weightless Possessions Tracking** | Physical hold isolation for Category 2 progression tokens (`possessions.villainy`) and Category 3 narrative items (`apl.items_manifest.ni`); polymorphic quest instantiation (`fetch` pattern).|
| **TC10** | `PKG-NARRATIVE` | **Prospect Sourcing Phase to Sourced Readiness Mutation** | Commodity purchase accounting; atomic progression of mercantile prospect lifecycle from `status: "active"` to `status: "rdy"` upon sourcing complete cargo; dynamic NEXT STOP spatial matching.|
| **TC11** | `PKG-NARRATIVE` | **Partial Delivery of a Quest Shopping List Pattern** | Multi-item quest manifest handling (`ql` pattern); hold inventory decrements alongside incrementing `quantity_delivered`; retention of `status: "active"` pending outstanding requirements; zero-inventory suppression.|
| **TC12** | `PKG-NARRATIVE` | **Partial Delivery of an Underway Prospect** | Port destination delivery interactions; partial contract handoff; decrements to physical cargo while retaining `status: "rdy"`; hold utilization updates; forced logbook rendering via explicit Captain command.|
| **TC13** | `PKG-NARRATIVE` | **Dynamic Stat Resolution & Companion Upgrades** | Runtime dynamic perk evaluation across officer composite keys (`ons`); prevention of calculated perk serialization in JSON; officer secondment lifecycle and maturity tracking; multi-year calendar calculation.|
| **TC14** | `PKG-STATE` | **Multi-State Compound Turn Pipeline** | Atomic resolution of a multi-phase turn (`ne` ➔ `na` ➔ `np` ➔ `nd` ➔ `ne`); transit fuel burns, market sales, bazaar restocking, and departure execution in a single turn; rolling history tracking.|
| **TC15** | `PKG-ECON` | **Economic Core & Moving Average Cost (MAC) Recalculation** | Atomic Moving Average Cost ($MAC$) re-computation when acquiring standard commodities at discounted market rates; floating capital tracking; physical hold capacity saturation checks ($12/12$ slots).|
| **TC16** | `PKG-STATE` | **Inter-Region Transit Relay Trajectory & Toll Evaluation** | Inter-region navigation gating; transit permit validation (`possessions.ptp`); toll option assessment across first- and second-class options without premature fee deductions prior to gate engagement.|
| **TC17** | `PKG-STATE` | **Navigation Itinerary Lifecycle, Rolling History Pruning & Port Arrival** | Kinetic arrival processing (`itinerary[0]` resolution); sequential leg transfer to `rh`; strict rolling cap invariant enforcement (clamping history to the 3 most recent stops and discarding oldest entry); port arrival dialogue.|
| **TC18** | `PKG-STATE` | **Commercial Station Serialization (With Bazaar)** | Discovered location tracking with sparse bazaar serialization. |
| **TC19** | `PKG-STATE` | **Non-Commercial Node Serialization (Without Bazaar)** | Discoverd location without baazaar. Test sparse bazaar serialization. |
| **TC20** | `PKG-NARRATIVE` | **Actions & UI Filtering** | Next Stop action spatial filtering against active itineraries, suppression of un-matched destinations, and visual priority indicator rendering (`‼️` / `🔻`). |
---

## Test Case 1: Session Initialization (Blank Slate Verification)

### Objective
Verifies that when no prior JSON state is provided, the system boots cleanly, assigns the First Mate persona ("Mr. Bligh"), sets Day 0 (1 January 1905), handles initial sovereign parameters, initializes default locomotive and non-zero inventory attributes (suppressing zero-quantity commodities and possessions), and renders the departure logbook.

### Input Prompt
> Start fresh. Captain Sinclair here, taking command of a brand new Spatchcock-Class Scout on this fine New Year's Day, 1905-01-01. Set our starting Sovereigns to 1000. We are departing New Winchester.

### Expected Verification:

#### State Transition:
`uninitialized` ➔ `np` ➔ `nd`

#### Targeted State Verification:
```json
{
  "sfn": "Mr. Bligh",
  "sds.cpt.cnm": "Sinclair",
  "sds.sep": 0,
  "sds.sso": 1000,
  "sds.clc.mcd": "Spatchcock-Class Scout",
  "sds.clc.chl": 30,
  "sds.clc.cmh": 30,
  "sds.gui.gfu": [ 3, 0, 20.0 ],
  "sds.gui.gsu": [ 3, 0, 40.0 ],
  "sds.nv.ns": "nd",
  "sds.nv.cl": "lnw"
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
{"ssf":"sunless-skies-first-mate","ssv":"0.5.0","sfn":"Mr. Bligh","sds":{"sso":1000,"sep":0,"cpt":{"cnm":"Sinclair","csk":{"ir":0,"mi":0,"he":0,"ve":0},"caf":{"ac":0,"bo":0,"es":0,"vi":0}},"clc":{"cmd":"Spatchcock-Class Scout","cnm":"","chl":30,"cmh":30,"cfl":0,"chc":12,"chs":0,"chr":{"frm":3,"srm":3,"dbs":2}},"ccr":{"ccu":8,"cmx":10,"ctr":0,"cng":0},"oom":{},"gui":{"gfu":[3,0,20.0],"gsu":[3,0,40.0]},"pps":{},"aaa":[],"nv":{"cl":"lnw","ns":"nd","lue":0,"rh":[],"it":[]},"dl":{"lnw":{"cd":null,"bz":{"re":null,"ab":[]}}}}}
```

---

## Test Case 2: Port Arrival & Month-Boundary Bargain Discovery Tracking

### Objective

Verifies kinetic state transition from `ne` ➔ `na` ➔ `np`, temporal conversion crossing a month boundary (`1905-01-31` = Day 30; reset `1905-02-12` = Day 42), canonical market key matching, suppression of zero-quantity items, and strict visual UI suppression during docked arrivals.

### Input Prompt

> Update state. We docked at Lustrum on 1905-01-31. Fuel used on this leg was 2. While checking the local market, we spotted a bargain: 3 crates of Unseasoned Hours selling for 40 Sovereigns each. The market broker says this deal expires on 1905-02-12.

```json
{
  "ssf": "sunless-skies-first-mate",
  "ssv": "0.5.0",
  "sfn": "Mr. Bligh",
  "sds": {
    "sso": 1000,
    "sep": 26,
    "cpt": {
      "cnm":"Sinclair",
      "csk": {"ir": 0,"mi": 0,"he": 0,"ve": 0},
      "caf": {"ac": 0,"bo": 0,"es": 0,"vi": 0}
    },
    "clc": {
      "cmd": "Spatchcock-Class Scout","cnm": "Zephyr",
      "chl": 30,"cmh": 30,
      "cfl": 0,"chc": 12,"chs": 0,
      "chr":{"frm": 3,"srm": 3,"dbs": 2}
    },
    "ccr": {"ccu": 8,"cmx": 10,"ctr": 0,"cng": 0},
    "oom": {},
    "gui": {
      "gfu": [5,0,20.00],
      "gsu": [4,0,40.00]
    },
    "pps": {},
    "aaa": [],
    "nv": {
      "cl": null,
      "ns": "ne",
      "lue": 26,
      "rh": [1,"lnw",0],
      "it": [2,"llu"]
    },
    "dl": {}
  }
}

```

### Expected Verification:

#### State Transition:

`ne` ➔ `na` ➔ `np`

#### Targeted State Verification:

```json
{
  "sds.sep": 30,
  "sds.clc.cfl": 2,
  "sds.gui.gfu[0]": 3,
  "sds.nv.ns": "np",
  "sds.nv.cl": "llu",
  "sds.dl.llu.bz.re": 42,
  "sds.dl.llu.bz.ab[0]": [ "guh", 3, 40 ]
}
```

#### Report Text:

(Full Markdown logbooks and JSON autosave blocks are strictly suppressed during `na` and `np` turns.)

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
  "ssf": "sunless-skies-first-mate",
  "ssv": "0.5.0",
  "sfn": "Mr. Bligh",
  "sds": {
    "sso": 880,
    "sep": 1153,
    "cpt": {
      "cnm":"Sinclair",
      "csk": {"ir": 10,"mi": 3,"he": 6,"ve": 3},
      "caf": {"ac": 0,"bo": 0,"es": 0,"vi": 0}
    },
    "clc": {
      "cmd": "Spatchcock-Class Scout","cnm": "Zephyr",
      "chl": 30,"cmh": 30,
      "cfl": 0,"chc": 12,"chs": 0,
      "chr": {"frm": 3,"srm": 3,"dbs": 2}
    },
    "ccr": {"ccu": 8,"cmx": 10,"ctr": 0,"cng": 0},
    "oom": {
      "ood": {"fo": "onf"}
    },
    "gui": {
      "gfu": [3,0,20.00],
      "gsu": [3,0,40.00],
      "gbw": [4,1,175.00],
      "gcn": [2,0,120.00]
    },
    "pps": {},
    "aaa": [],
    "nv": {
      "cl": "lnw",
      "ns": "np",
      "lue": 1153,
      "rh": [4,"lpr",1150],
      "it": []
    },
    "dl": {}
  }
}
```

### Expected Verification:

#### State Transition:

`np` ➔ `nd` (Multi-state compound turn: bank transfer executed while docked, then departing plotted for Titania)

#### Targeted State Verification:

```json
{
  "sds.sep": 1154,
  "gfu": [ 3, 0, 20.0 ],
  "gsu": [ 3, 0, 40.0 ],
  "gbw": [ 0, 5, 175.0 ],
  "gcn": [ 0, 2, 120.0 ],
  "sds.nv.ns": "nd"
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
{"ssf":"sunless-skies-first-mate","ssv":"0.5.0","sfn":"Mr. Bligh","sds":{"sso":880,"sep":1154,"cpt":{"cnm":"Sinclair","csk":{"ir":10,"mi":3,"he":6,"ve":3},"caf":{"ac":0,"bo":0,"es":0,"vi":0}},"clc":{"cmd":"Spatchcock-Class Scout","cnm":"Zephyr","chl":30,"cmh":30,"cfl":0,"chc":12,"chs":0,"chr":{"frm":3,"srm":3,"dbs":2}},"ccr":{"ccu":8,"cmx":10,"ctr":0,"cng":0},"oom":{"ood":{"fo":"onf","qm":null,"sc":null,"ce":null,"ma":null},"oun":{"fo":[],"qm":[],"sc":[],"ce":[],"ma":[]},"osc":{"fo":[],"qm":[],"sc":[],"ce":[],"ma":[]},"odp":{"fo":[],"qm":[],"sc":[],"ce":[],"ma":[]}},"gui":{"gfu":[3,0,20.0],"gsu":[3,0,40.0],"gbw":[0,5,175.0],"gcn":[0,2,120.0]},"pps":{"ac":{},"bo":{},"es":{},"vi":{},"ptp":[]},"aaa":[],"nv":{"cl":"lnw","ns":"nd","lue":1154,"rh":[4,"lpr",1150],"it":[5,"lti"]},"dl":{}}}
```

---

## Test Case 4: State Integrity Breach Emergency Intercept (Directive 2.2.4)

### Objective

Probes compliance with safety guardrails by forcing an intentional relational integrity break (illegal commodity key `quantum_æther_crystal` and unwhitelisted location `missing_port_x`), confirming that the engine halts state mutation and outputs the mandatory verbatim alert.

### Input Prompt

> Captain's log: 1905-01-10. Processing a logistics pass over our active trade agreements. Let me know what our current route optimization options look like.

```json
{
  "ssf": "sunless-skies-first-mate",
  "ssv": "0.5.0",
  "sfn": "Mr. Bligh",
  "sds": {
    "sso": 880,
    "sep": 9,
    "cpt": {
      "cnm":"Sinclair",
      "csk": {"ir": 0,"mi": 0,"he": 0,"ve": 0},
      "caf": {"ac": 0,"bo": 0,"es": 0,"vi": 0}
    },
    "clc": {
      "cmd": "Spatchcock-Class Scout","cnm": "Zephyr",
      "chl": 30,"cmh": 30,
      "cfl": 0,"chc": 12,"chs": 0,
      "chr": {"frm": 3,"srm": 3,"dbs": 2}
    },
    "ccr": {"ccu": 8,"cmx": 10,"ctr": 15,"cng": 0},
    "oom": {},
    "gui": {
      "gfu": [3,0,20.00],
      "gsu": [3,0,40.00],
      "gbw": [1,0,175.00],
      "quantum_æther_crystal": [1,0,100.00]
    },
    "pps": {},
    "aaa": [
      {
        "aid": "ACT-1016",
        "atp": "tod",
        "ast": "act",
        "aol": "missing_port_x",
        "att": "Deliver supplies to custom outpost",
        "ant": "Error payload item: Unwhitelisted location key.",
        "apr": "md",
        "apn": false,
        "ace": 2,
        "aue": 2,
        "ade": null,
        "apl": ["missing_port_x"]
      }
    ],
    "nv": {
      "cl": "lnw",
      "ns": "np",
      "lue": 9,
      "rh": [],
      "it": []
    },
    "dl": {}
  }
}

```

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
  "ssf": "sunless-skies-first-mate",
  "ssv": "0.5.0",
  "sfn": "Mr. Bligh",
  "sds": {
    "sso": 880,
    "sep": 364,
    "cpt": {
      "cnm":"Sinclair",
      "csk": {"ir": 0,"mi": 0,"he": 0,"ve": 0},
      "caf": {"ac": 0,"bo": 0,"es": 0,"vi": 0}
    },
    "clc": {
      "cmd": "Spatchcock-Class Scout",
      "cnm": "Zephyr",
      "chl": 30,
      "cmh": 30,
      "cfl": 0,
      "chc": 12,
      "chs": 0,
      "chr": {"frm": 3,"srm": 3,"dbs": 2}
    },
    "ccr": {"ccu": 8,"cmx": 10,"ctr": 20,"cng": 0},
    "oom": {},
    "gui": {
      "gfu": [3,0,20.00],
      "gsu": [3,0,40.00]
    },
    "pps": {},
    "aaa": [],
    "nv": {
      "cl": "lpo",
      "ns": "np",
      "lue": 364,
      "rh": [1,"lnw",350],
      "it": []
    },
    "dl": {}
  }
}

```

### Expected Verification:

#### State Transition:

`np` ➔ `nd`

#### Targeted State Verification:

```json
{
  "sds.sep": 379,
  "sds.crew.current": 6,
  "sds.clc.chl": 17,
  "sds.nv.ns": "nd",
  "sds.nv.it[0]": [ 2, "lnw" ]
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
{"ssf":"sunless-skies-first-mate","ssv":"0.5.0","sfn":"Mr. Bligh","sds":{"sso":880,"sep":379,"cpt":{"cnm":"Sinclair","csk":{"ir":0,"mi":0,"he":0,"ve":0},"caf":{"ac":0,"bo":0,"es":0,"vi":0}},"clc":{"cmd":"Spatchcock-Class Scout","cnm":"Zephyr","chl":17,"cmh":30,"cfl":0,"chc":12,"chs":0,"chr":{"frm":3,"srm":3,"dbs":2}},"ccr":{"ccu":6,"cmx":10,"ctr":20,"cng":0},"oom":{},"gui":{"gfu":[3,0,20.0],"gsu":[3,0,40.0]},"pps":{},"aaa":[],"nv":{"cl":"lpo","ns":"nd","lue":379,"rh":[1,"lnw",350],"it":[2,"lnw"]},"dl":{}}}
```

## Test Case 6: Critical Low Crew Threshold & Consumable Depletion

### Objective

Verifies behavioral tone shifts when crew drops below 50%, triggering fatigue and sluggish engine complaints, checks hold warning icons for depleted consumables (Fuel at 1 = ⚠️, Supplies at 0 = 🚨), tests pinning/unpinned high-priority note handling, and tests calendar date conversion at year-start boundary (`1906-01-20` = Day 384).

### Input Prompt

> Update state. 1906-01-20. Sickness swept through the lower bunks while out on the high sky. We've dropped 3 more hands off at the local care station in Hybras. Crew strength is down to 3 out of 10. Make a high-priority note to hire on crew at the circus. Clear docks for Polmear & Plenty's with haste.

```json
{
  "ssf": "sunless-skies-first-mate",
  "ssv": "0.5.0",
  "sfn": "Mr. Bligh",
  "sds": {
    "sso": 880,
    "sep": 379,
    "cpt": {
      "cnm":"Sinclair",
      "csk": {"ir": 0,"mi": 0,"he": 0,"ve": 0},
      "caf": {"ac": 0,"bo": 0,"es": 0,"vi": 0}
    },
    "clc": {
      "cmd": "Spatchcock-Class Scout",
      "cnm": "Zephyr",
      "chl": 17,
      "cmh": 30,
      "cfl": 0,
      "chc": 12,
      "chs": 0,
      "chr": {"frm": 3,"srm": 3,"dbs": 2}
    },
    "ccr": {"ccu": 6,"cmx": 10,"ctr": 35,"cng": 0},
    "oom": {},
    "gui": {
      "gfu": [1,0,20.00],
      "gsu": [0,0,40.00]
    },
    "pps": { },
    "aaa": [],
    "nv": {
      "cl": "lhy",
      "ns": "np",
      "lue": 379,
      "rh": [2,"lpo",379],
      "it": []
    },
    "dl": {}
  }
}

```

### Expected Verification:

#### State Transition:

`np` ➔ `nd`

#### Targeted State Verification:

```json
{
  "sds.sep": 384,
  "sds.crew.current": 3,
  "sds.gui.gsu": [ 0, 0, 40.0 ],
  "sds.aaa[0].aid": "ACT-1001",
  "sds.aaa[0].apr": "hi",
  "sds.aaa[0].apl": [ "lpp" ],
  "sds.nv.ns": "nd"
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
{"ssf":"sunless-skies-first-mate","ssv":"0.5.0","sfn":"Mr. Bligh","sds":{"sso":880,"sep":384,"cpt":{"cnm":"Sinclair","csk":{"ir":0,"mi":0,"he":0,"ve":0},"caf":{"ac":0,"bo":0,"es":0,"vi":0}},"clc":{"cmd":"Spatchcock-Class Scout","cnm":"Zephyr","chl":17,"cmh":30,"cfl":0,"chc":12,"chs":0,"chr":{"frm":3,"srm":3,"dbs":2}},"ccr":{"ccu":3,"cmx":10,"ctr":35,"cng":0},"oom":{},"gui":{"gfu":[1,0,20.0],"gsu":[0,0,40.0]},"pps":{},"aaa":[{"aid":"ACT-1001","atp":"tod","ast":"act","aol":"lhy","att":"Hire crew at the circus","ant":"Hire replacement crew from the circus","apr":"hi","apn":false,"ace":384,"aue":384,"ade":null,"apl":["lpp"]}],"nv":{"cl":"lhy","ns":"nd","lue":384,"rh":[2,"lpo",379],"it":[[3,"lpp"]]},"dl":{}}}
```

## Test Case 7: Route Planner - Multi-Stop Sequential Itinerary & Task Linking

### Objective

Verifies multi-stop itinerary construction, sequential leg renumbering, spatial target filtering for NEXT STOP linking, and mid-year calendar conversion across leap-year anomaly (`1908-04-11` = Day 1195, evaluating 1905, 1906, 1907 as $3 \times 365 = 1095$ plus Jan 31 + Feb 28 + Mar 31 + 10 days of April).

### Input Prompt

> Update state. Plot a route from New Winchester to Titania, and then onward to Lustrum, and set sail. Let's see what business we have pending at those locations, First Mate.

```json
{
  "ssf": "sunless-skies-first-mate",
  "ssv": "0.5.0",
  "sfn": "Mr. Bligh",
  "sds": {
    "sso": 1450,
    "sep": 1195,
    "cpt": {
      "cnm":"Sinclair",
      "csk": {"ir": 0,"mi": 0,"he": 0,"ve": 0},
      "caf": {"ac": 0,"bo": 0,"es": 0,"vi": 0}
    },
    "clc": {
      "cmd": "Spatchcock-Class Scout",
      "cnm": "Zephyr",
      "chl": 30,
      "cmh": 30,
      "cfl": 0,
      "chc": 12,
      "chs": 0,
      "chr": {"frm": 3,"srm": 3,"dbs": 2}
    },
    "ccr": {"ccu": 9,"cmx": 10,"ctr": 15,"cng": 0},
    "oom": {},
    "gui": {
      "gfu": [3,0,20.00],
      "gsu": [3,0,40.00],
      "gbw": [2,0,175.00]
    },
    "pps": { },
    "aaa": [
      {
        "aid": "ACT-1001",
        "atp": "amb",
        "ast": "act",
        "aol": "lnw",
        "att": "Ambition: Wealth",
        "ant": "",
        "apr": "md",
        "apn": false,
        "ace": 6,
        "aue": 6,
        "ade": null,
        "apl": ["aw",1,"Purchase the Governor's Manor",5000,[]]
      },
      {
        "aid": "ACT-1012",
        "atp": "prs",
        "ast": "act",
        "aol": "lnw",
        "att": "Nectar for the Fairies",
        "ant": "",
        "apr": "md",
        "apn": false,
        "ace": 79,
        "aue": 79,
        "ade": null,
        "apl": ["gcn",1,0,0,"lti"]
      },
      {
        "aid": "ACT-1013",
        "atp": "prs",
        "ast": "rdy",
        "aol": "lnw",
        "att": "Bronzewood Shipments",
        "ant": "",
        "apr": "md",
        "apn": false,
        "ace": 82,
        "aue": 82,
        "ade": null,
        "apl": ["gbw",3,3,1,"llu"]
      },
      {
        "aid": "ACT-1016",
        "atp": "tod",
        "ast": "act",
        "aol": "lnw",
        "att": "Helping the Horticulturalist",
        "ant": "Deliver structural schematics to the Horticulturalist",
        "apr": "md",
        "apn": false,
        "ace": 90,
        "aue": 90,
        "ade": null,
        "apl": ["lti"]
      }
    ],
    "nv": {
      "cl": "lnw",
      "ns": "np",
      "lue": 1195,
      "rh": [1,"lnw",1180],
      "it": []
    },
    "dl": {}
  }
}

```

### Expected Verification:

#### State Transition:

`np` ➔ `nd`

#### Targeted State Verification:

```json
{
  "sds.nv.ns": "nd",
  "sds.nv.it[0]": [ 2, "lti" ],
  "sds.nv.it[1]": [ 3, "llu" ]
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
{"ssf":"sunless-skies-first-mate","ssv":"0.5.0","sfn":"Mr. Bligh","sds":{"sso":1450,"sep":1195,"cpt":{"cnm":"Sinclair","csk":{"ir":0,"mi":0,"he":0,"ve":0},"caf":{"ac":0,"bo":0,"es":0,"vi":0}},"clc": {"cmd":"Spatchcock-Class Scout","cnm":"Zephyr","chl":30,"cmh":30,"cfl":0,"chc":12,"chs":0,"chr":{"frm":3,"srm":3,"dbs":2}},"ccr":{"ccu":9,"cmx":10,"ctr":15,"cng":0},"oom":{},"gui":{"gfu":[3,0,20.0],"gsu":[3,0,40.0],"gbw":[2,0,175.0]},"pps": {"ac": {},"bo": {},"es": {},"vi": {},"ptp": []},"aaa": [{"aid":"ACT-1001","atp":"amb","ast":"act","aol":"lnw","att":"Ambition: Wealth","ant":"","apr":"md","apn":false,"ace":6,"aue":6,"ade":null,"apl":["aw",1,"Purchase the Governor's Manor",5000,{"gd":[],"pk":[],"ni":[]}]},{"aid":"ACT-1012","atp":"prs","ast":"act","aol":"lnw","att":"Nectar for the Fairies","ant":"","apr":"md","apn":false,"ace":79,"aue":79,"ade":null,"apl":["gcn",1,0,0,"lti"]},{"aid":"ACT-1013","atp":"prs","ast":"rdy","aol":"lnw","att":"Bronzewood Shipments","ant":"","apr":"md","apn":false,"ace":82,"aue":82,"ade":null,"apl":["gbw",3,3,1,"llu"]},{"aid":"ACT-1016","atp":"tod","ast":"act","aol":"lnw","att":"Helping the Horticulturalist","ant":"Deliver structural schematics to the Horticulturalist","apr":"md","apn":false,"ace":90,"aue":90,"ade":null,"apl":["lti"]}],"nv":{"cl":"lnw","ns":"nd","lue":1195,"rh":[[1,"lnw",1180]],"it":[[2,"lti"], [3,"llu"]]},"dl": {}}}
```

## Test Case 8: Route Planner - Resupply Isolation Alert & Intermediate Port Recommendation

### Objective

Verifies that the Route Planner detects critical consumable deficits prior to a long haul, evaluates clock coordinates to propose an intermediate port insertion (Titania at clock 2), delivers a professional caution tone without low-hull panic, and parses non-leap February dates (`1905-02-18` = Day 48).

### Input Prompt

> Update state. Lay a direct course from New Winchester straight out to Port Prosper, First Mate. We have a long haul ahead, let's get moving.

```json
{
  "ssf": "sunless-skies-first-mate",
  "ssv": "0.5.0",
  "sfn": "Mr. Bligh",
  "sds": {
    "sso": 620,
    "sep": 48,
    "cpt": {
      "cnm":"Sinclair",
      "csk": {"ir": 0,"mi": 0,"he": 0,"ve": 0},
      "caf": {"ac": 0,"bo": 0,"es": 0,"vi": 0}
    },
    "clc": {
      "cmd": "Spatchcock-Class Scout",
      "cnm": "Zephyr",
      "chl": 25,
      "cmh": 30,
      "cfl": 0,
      "chc": 12,
      "chs": 0,
      "chr": {"frm": 3,"srm": 3,"dbs": 2}
    },
    "ccr": {"ccu": 10,"cmx": 10,"ctr": 40,"cng": 1},
    "oom": {},
    "gui": {
      "gfu": [1,0,20.00],
      "gsu": [1,0,40.00]
    },
    "pps": {},
    "aaa": [],
    "nv": {
      "cl": "lnw",
      "ns": "np",
      "lue": 48,
      "rh": [1,"lnw",48],
      "it": []
    },
    "dl": {
      "lnw": {
        "cd": null,
        "captains_notes": [],
        "bz": {"re": null, "ab": []}
      },
      "lti": {
        "cd": 2,
        "captains_notes": [],
        "bz": {"re": null, "ab": []}
      },
      "lpr": {
        "cd": 6,
        "captains_notes": [],
        "bz": {"re": null, "ab": []}
      }
    }
  }
}
```

### Expected Verification:

#### State Transition:

`np` ➔ `nd`

#### Targeted State Verification:

```json
{
  "sds.sep": 48,
  "sds.gui.gfu": [ 1, 0, 20.0 ],
  "sds.gui.gsu": [ 1, 0, 40.0 ],
  "sds.nv.ns": "nd",
  "sds.nv.it[0]": [ 2, "lpr" ]
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
{"ssf":"sunless-skies-first-mate","ssv":"0.5.0","sfn":"Mr. Bligh","sds":{"sso":620,"sep":48,"cpt":{"cnm":"Sinclair","csk":{"ir":0,"mi":0,"he":0,"ve":0},"caf":{"ac":0,"bo":0,"es":0,"vi":0}},"clc":{"cmd":"Spatchcock-Class Scout","cnm":"Zephyr","chl":25,"cmh":30,"cfl":0,"chc":12,"chs":0,"chr":{"frm":3,"srm":3,"dbs":2}},"ccr":{"ccu":10,"cmx":10,"ctr":40,"cng":1},"oom":{},"gui":{"gfu":[1,0,20.0],"gsu":[1,0,40.0]},"pps":{},"aaa":[],"nv":{"cl":"lnw","ns":"nd","lue":48,"rh":[1,"lnw",48],"it":[2,"lpr"]},"dl":{"lnw":{"cd":null,"bz":{"re":null,"ab":[]}},"lti":{"cd":2,"bz":{"re":null,"ab":[]}},"lpr":{"cd":6,"bz":{"re":null,"ab":[]}}}}}
```


## Test Case 9: Cargo Isolation & Weightless Possessions Tracking

### Objective
Verifies that spatial possessions (Category 2: 16 immutable progression tokens) and narrative quest items (Category 3: polymorphic items manifest) do not draw physical hold space against `locomotive.chc`. Confirms that a polymorphic quest object is cleanly constructed within `sds.aaa`, checks that non-zero possessions populate their respective affiliation domain while zero-quantity commodities and possessions are strictly suppressed from the JSON payload, and tests mid-month High Wilderness calendar calculation (`1905-01-15` = Day 14).

### Input Prompt
> Update state. Captain's log: 1905-01-15. We acquired two Tales of Terror out in the dark on that last run. We took on a quest from The Sequestered Scholar to deliver a Primordial Star Shard to Port Avon. Log this as "The Last Consignment." Let's make sure our logistics files are updated before we cast off lines for Port Avon.

```json
{
  "ssf": "sunless-skies-first-mate",
  "ssv": "0.5.0",
  "sfn": "Mr. Bligh",
  "sds": {
    "sso": 800,
    "sep": 14,
    "cpt": {
      "cnm":"Sinclair",
      "csk": {"ir": 0, "mi": 0, "he": 0, "ve": 0},
      "caf": {"ac": 0, "bo": 0, "es": 0, "vi": 0}
    },
    "clc": {
      "cmd": "Spatchcock-Class Scout",
      "cnm": "Zephyr",
      "chl": 30,
      "cmh": 30,
      "cfl": 2,
      "chc": 12,
      "chs": 0,
      "chr": {"frm": 3, "srm": 3, "dbs": 2}
    },
    "ccr": {"ccu": 8, "cmx": 10, "ctr": 0, "cng": 0},
    "oom": {},
    "gui": {
      "gfu": [4, 0, 20.00],
      "gsu": [4, 0, 40.00],
      "gal": [2, 0, 100.00]
    },
    "pps": {},
    "aaa": [],
    "nv": {
      "cl": "lnw",
      "ns": "np",
      "lue": 14,
      "rh": [1,"lnw",0],
      "it": []
    },
    "dl": {}
  }
}

```

### Expected Verification:

#### State Transition:

`np` ➔ `nd`

#### Targeted State Verification:

```json
{
  "sds.pps.vi.ptt": 2,
  "sds.aaa[0].aid": "ACT-1001",
  "sds.aaa[0].type": "qst",
  "sds.aaa[0].apl[3][0].ni[0]": [ "Primordial Star Shard", 1, 0 ],
  "sds.nv.ns": "nd",
  "sds.nv.it[0]": [ 2, "lpo" ]
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
{"ssf":"sunless-skies-first-mate","ssv":"0.5.0","sfn":"Mr. Bligh","sds":{"sso":800,"sep":14,"cpt":{"cnm":"Sinclair","csk":{"ir":0,"mi":0,"he":0,"ve":0},"caf":{"ac":0,"bo":0,"es":0,"vi":0}},"clc": {"cmd":"Spatchcock-Class Scout","cnm":"Zephyr","chl":30,"cmh":30,"cfl":2,"chc":12,"chs":0,"chr":{"frm":3,"srm":3,"dbs":2}},"ccr":{"ccu":8,"cmx":10,"ctr":0,"cng":0},"oom": {},"gui":{"gfu":[4,0,20.0],"gsu":[4,0,40.0],"gal":[2,0,100.0]},"pps":{"ac":{},"bo":{},"es":{},"vi":{"ptt":2},"ptp":[]},"aaa":[{"aid":"ACT-1001","atp":"qst","ast":"act","aol":"lnw","att":"The LastConsignment","ant":"Deliver a Primordial Star Shard to Port Avon forThe Sequestered Scholar","apr":"md","apn":false,"ace":14,"aue":14"ade":null,"apl":[1,"qf",[["lpo","Deliver a Primordial Star Shard"]],{"gd":[],"pk":[],"ni":[["Primordial Star Shard",1,0]]}]}],"nv": {"cl":"lnw","ns":"nd","lue":14,"rh":[[1,"lnw",0]],"it":[[2"lpo"]]},"dl":{}}}
```

---

## Test Case 10: Prospect Sourcing Phase to Sourced Readiness Mutation

### Objective

Verifies that sourcing the final required units of a standard trade good atomically increments `gui` hold quantities, updates `quantity_sourced`, transitions the prospect lifecycle from `status: "active"` to `status: "rdy"`, evaluates spatial target matching to surface the contract under NEXT STOP, suppresses zero-quantity commodities/possessions, and parses mid-February High Wilderness dates (`1905-02-18` = Day 48).

### Input Prompt

> Update state. I've finished loading the remaining 2 crates of Munitions here at New Winchester, completely filling our contract order. Plotting course to set sail for Port Prosper.

```json
{
  "ssf": "sunless-skies-first-mate",
  "ssv": "0.5.0",
  "sfn": "Mr. Bligh",
  "sds": {
    "sso": 1000,
    "sep": 48,
    "cpt": {
      "cnm":"Sinclair",
      "csk": {"ir": 0, "mi": 0, "he": 0, "ve": 0},
      "caf": {"ac": 0, "bo": 0, "es": 0, "vi": 0}
    },
    "clc": {
      "cmd": "Spatchcock-Class Scout",
      "cnm": "Zephyr",
      "chl": 30,
      "cmh": 30,
      "cfl": 0,
      "chc": 12,
      "chs": 0,
      "chr": {"frm": 3, "srm": 3, "dbs": 2}
    },
    "ccr": {"ccu": 10, "cmx": 10, "ctr": 12, "cng": 0},
    "oom": {},
    "gui": {
      "gfu": [3, 0, 20.00],
      "gsu": [3, 0, 40.00],
      "gmu": [2, 0, 60.00]
    },
    "pps": {},
    "aaa": [
      {
        "aid": "ACT-1001",
        "atp": "prs",
        "ast": "act",
        "aol": "lnw",
        "att": "Fortress Resupply",
        "ant": "Urgent munitions shipment for the garrison.",
        "apr": "md",
        "apn": false,
        "ace": 48,
        "aue": 48,
        "ade": null,
        "apl": ["gmu",4,2,0,"lpr"]
      }
    ],
    "nv": {
      "cl": "lnw",
      "ns": "np",
      "lue": 48,
      "rh": [1,"lnw",48],
      "it": []
    },
    "dl": {}
  }
}
```

### Expected Verification:

#### State Transition:

`np` ➔ `nd`

#### Targeted State Verification:

```json
{
  "sds.gui.munitions.[0]": 4,
  "sds.aaa[0].ast": "rdy",
  "sds.aaa[0].apl": [ "gmu", 4, 4, 0, "lpr" ],
  "sds.nv.ns": "nd",
  "sds.nv.it[0]]": [ 2, "lpr" ]
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
{"ssf":"sunless-skies-first-mate","ssv":"0.5.0","sfn":"Mr. Bligh","sds":{"sso":1000,"sep":48,"cpt":{"cnm":"Sinclair","csk":{"ir":0,"mi":0,"he":0,"ve":0},"caf":{"ac":0,"bo":0,"es":0,"vi":0}},"clc":{"cmd":"Spatchcock-Class Scout","cnm":"Zephyr","chl":30,"cmh":30,"cfl":0,"chc":12,"chs":0,"chr":{"frm":3,"srm":3,"dbs":2}},"ccr":{"ccu":10,"cmx":10,"ctr":12,"cng":0},"oom":{},"gui":{"gfu":[3,0,20.0],"gsu":[3,0,40.0],"gmu":[4,0,60.0]},"pps":{},"aaa":[{"aid":"ACT-1001","atp":"prs","ast":"rdy","aol":"lnw","att":"Fortress Resupply","ant":"Urgent munitions shipment for the garrison.","apr":"md","apn":false,"ace":48,"aue":48,"ade":null,"apl":["gmu",4,4,0,"lpr"]}],"nv":{"cl":"lnw","ns":"nd","lue":48,"rh":[1,"lnw",48],"it":[2,"lpr"]},"dl":{}}}
```

---

## Test Case 11: Partial Delivery of a Quest Shopping List Pattern

### Objective

Verifies that partial delivery of items toward a quest "shopping list" pattern correctly decrements the physical hold inventory, increments `quantity_delivered` within `items_manifest.goods`, maintains `status: "active"` until the entire manifest is satisfied, retains active destinations, and completely suppresses zero-quantity commodities (`gcn`) and empty possession blocks from the JSON payload.

### Input Prompt

> Update state. Just arrived at Titania and went straight to the Chief Botanist. I handed over the single bottle of Chorister Nectar he requested, but I don't have the Verdant Seeds yet. Setting off lines toward New Winchester to search for the seeds.

```json
{
  "ssf": "sunless-skies-first-mate",
  "ssv": "0.5.0",
  "sfn": "Mr. Bligh",
  "sds": {
    "sso": 1000,
    "sep": 48,
    "cpt": {
      "cnm":"Sinclair",
      "csk": {"ir": 0, "mi": 0, "he": 0, "ve": 0},
      "caf": {"ac": 0, "bo": 0, "es": 0, "vi": 0}
    },
    "clc": {
      "cmd": "Spatchcock-Class Scout",
      "cnm": "Zephyr",
      "chl": 30,
      "cmh": 30,
      "cfl": 0,
      "chc": 12,
      "chs": 0,
      "chr": {"frm": 3, "srm": 3, "dbs": 2}
    },
    "ccr": {"ccu": 10, "cmx": 10, "ctr": 12, "cng": 0},
    "oom": {},
    "gui": {
      "gfu": [3, 0, 20.00],
      "gsu": [3, 0, 40.00],
      "gcn": [1, 0, 120.00]
    },
    "pps": {},
    "aaa": [
      {
        "aid": "ACT-2002",
        "atp": "qst",
        "ast": "act",
        "aol": "lti",
        "att": "The Glass Greenhouse",
        "ant": "Gather elements for the biome update.",
        "apr": "md",
        "apn": false,
        "ace": 45,
        "aue": 45,
        "ade": null,
        "apl": [
          1,
          "qs",
          [["lti", "Deliver Chorister Nectar and Verdant Seeds"]],
          {
            "gd": [
              ["gcn",1,0],
              ["gvs",2,0]
            ],
            "pk": [],
            "ni": []
          }
        ]
      }
    ],
    "nv": {
      "cl": "lti",
      "ns": "np",
      "lue": 48,
      "rh": [1,"lti",48],
      "it": []
    },
    "dl": {}
  }
}

```

### Expected Verification:

#### State Transition:

`np` ➔ `nd`

#### Targeted State Verification:

```json
{
  "sds.gui.gcn": null,
  "sds.aaa[0].ast": "active",
  "sds.aaa[0].apl[3].gd[0]": [ "gcn", 1, 1 ], 
  "sds.aaa[0].apl[3].gd[1]": [ "gvs", 2, 0 ],
  "sds.nv.ns": "nd",
  "sds.nv.it[0]": [ 2, "lnw" ]
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
{"ssf":"sunless-skies-first-mate","ssv":"0.5.0","sfn":"Mr. Bligh","sds":{"sso":1000,"sep":48,"cpt":{"cnm":"Sinclair","csk":{"ir":0,"mi":0,"he":0,"ve":0},"caf":{"ac":0,"bo":0,"es":0,"vi":0}},"clc":{"cmd":"Spatchcock-Class Scout","cnm":"Zephyr","chl":30,"cmh":30,"cfl":0,"chc":12,"chs":0,"chr":{"frm":3,"srm":3,"dbs":2}},"ccr":{"ccu":10,"cmx":10,"ctr":12,"cng":0},"oom":{},"gui":{"gfu":[3,0,20.0],"gsu":[3,0,40.0]},"pps":{},
"aaa":[{"aid":"ACT-2002","atp":"qst","ast":"act","aol":"lti","att":"The Glass Greenhouse","ant":"Gather elements for the biome update.","apr":"md","apn":false,"ace":45,"aue":48,"ade":null,"apl":[1,"ql",[["lti","Deliver Chorister Nectar and Verdant Seeds"]],{"gd": [["gcn",1,1],["gvs",2,0]],"pps":[],"ni":[]}]}],"nv":{"cl":"lti","ns":"nd","lue":48,"rh":[1,"lti",48],"it":[2,"lnw"]},"dl":{}}}
```

---

## Test Case 12: Partial Delivery of an Underway Prospect

### Objective

Verifies that when docked at the destination location of an active mercantile prospect, delivering partial units increments `quantity_delivered`, decrements physical hold inventory, maintains `status: "rdy"` (since `quantity_delivered < quantity_required`), leaves the action active in the stream, correctly reflects hold utilization in the departure logbook, suppresses unheld commodities/empty possessions, and checks calendar advance (`1905-02-19` = Day 49).

### Input Prompt

> Update state. Just docked at Port Prosper. I went to the garrison quartermaster and delivered 2 of our 4 loaded crates of Munitions. We are holding onto the other 2 crates for now while I check the local markets. Show me the logbook.

```json
{
  "ssf": "sunless-skies-first-mate",
  "ssv": "0.5.0",
  "sfn": "Mr. Bligh",
  "sds": {
    "sso": 1000,
    "sep": 49,
    "cpt": {
      "cnm":"Sinclair",
      "csk": {"ir": 0, "mi": 0, "he": 0, "ve": 0},
      "caf": {"ac": 0, "bo": 0, "es": 0, "vi": 0}
    },
    "clc": {
      "cmd": "Spatchcock-Class Scout",
      "cnm": "Zephyr",
      "chl": 30,
      "cmh": 30,
      "cfl": 0,
      "chc": 12,
      "chs": 0,
      "chr": {"frm": 3, "srm": 3, "dbs": 2}
    },
    "ccr": {"ccu": 10, "cmx": 10, "ctr": 10, "cng": 0},
    "oom": {},
    "gui": {
      "gfu": [3, 0, 20.00],
      "gsu": [3, 0, 40.00],
      "gmu": [4, 0, 60.00]
    },
    "pps": {},
    "aaa": [
      {
        "aid": "ACT-1001",
        "atp": "prs",
        "ast": "rdy",
        "aol": "lnw",
        "att": "Fortress Resupply",
        "ant": "Urgent munitions shipment for the garrison.",
        "apr": "md",
        "apn": false,
        "ace": 48,
        "aue": 48,
        "ade": null,
        "apl": [
          ["gmu",4,4,0,"lpr"]
        ]
      }
    ],
    "nv": {
      "cl": "lpr",
      "ns": "np",
      "lue": 49,
      "rh": [1,"lpr",49],
      "it": []
    },
    "dl": {}
  }
}
```

### Expected Verification:

#### State Transition:

`np` ➔ `nd` (Prompt explicitly commands: "Show me the logbook", forcing departure logbook generation)

#### Targeted State Verification:

```json
{
  "sds.gui.munitions.[0]": 2,
  "sds.aaa[0].ast": "rdy",
  "sds.aaa[0].apl": [ "gmu", 4, 4, 2, "lpr" ],
  "sds.nv.ns": "nd"
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
{"ssf":"sunless-skies-first-mate","ssv":"0.5.0","sfn":"Mr. Bligh","sds":{"sso":1000,"sep":49,"cpt":{"cnm":"Sinclair","csk":{"ir":0,"mi":0,"he":0,"ve":0},"caf":{"ac":0,"bo":0,"es":0,"vi":0}},"clc":{"cmd":"Spatchcock-Class Scout","cnm":"Zephyr","chl":30,"cmh":30,"cfl":0,"chc":12,"chs":0,"chr":{"frm":3,"srm":3,"dbs":2}},"ccr":{"ccu":10,"cmx":10,"ctr":10,"cng":0},"oom":{},"gui":{"gfu":[3,0,20.0],"gsu":[3,0,40.0],"gmu":[2,0,60.0]},"pps":{},"aaa":[{"aid":"ACT-1001","atp":"prs","ast":"rdy","aol":"lnw","att":"Fortress Resupply","ant":"Urgent munitions shipment for the garrison.","apr":"md","apn":false,"ace":48,"aue":49,"ade":null,"apl":["gmu",4,4,2,"lpr"]}],"nv":{"cl":"lpr","ns":"nd","lue":49,"rh":[1,"lpr",49],"it":[]},"dl":{}}}
```

---

## Test Case 13: Dynamic Stat Resolution & Companion Upgrades

### Objective
Verifies dynamic officer perk resolution, ensuring runtime evaluation reads composite keys (e.g., `"ons"`) and that perks are not written to JSON. Validates non-leap High Wilderness calendar calculations crossing into the subsequent year (`1906-02-22` = \(365 + 31 + 21 = \text{Day } 417\)), confirms zero-quantity commodities/possessions remain suppressed in JSON, and checks layout mapping for officer secondments under NEXT STOP.

### Input Prompt
> Update state. London - 22 February 1906. Our First Officer has promoted to "The Stalwart Navigator." Ready the crew and cast lines off for Avid Horizon.

```json
{
  "ssf": "sunless-skies-first-mate",
  "ssv": "0.5.0",
  "sfn": "Mr. Bligh",
  "sds": {
    "sso": 1000,
    "sep": 417,
    "cpt": {
      "cnm":"Sinclair",
      "csk": {"ir": 10, "mi": 18, "he": 25, "ve": 7},
      "caf": {"ac": 0, "bo": 0, "es": 0, "vi": 0}
    },
    "clc": {
      "cmd": "Spatchcock-Class Scout",
      "cnm": "Zephyr",
      "chl": 30,
      "cmh": 30,
      "cfl": 0,
      "chc": 12,
      "chs": 0,
      "chr": {"frm": 3, "srm": 3, "dbs": 2}
    },
    "ccr": {"ccu": 10, "cmx": 10, "ctr": 12, "cng": 0},
    "oom": {
      "ood": {
        "fo": "onf",
        "qm": "oai",
        "ma": "dog"
      },
      "oun": {"fo": ["opi", "ocl"]},
      "osc": {"sc": ["olr"]}
    },
    "gui": {
      "gfu": [3, 0, 20.00],
      "gsu": [3, 0, 40.00]
    },
    "pps": {},
    "aaa": [
      {
        "aid": "ACT-1011",
        "atp": "sec",
        "ast": "act",
        "aol": "home_bureau",
        "att": "Secondment: Repentant Devil",
        "ant": "Generates prospects near the Avid Horizon.",
        "apr": "md",
        "apn": false,
        "ace": 366,
        "aue": 366,
        "ade": 400,
        "apl": [
          ["olr",34,"Generates prospects at Avid Horizon","Collect in person"]
        ]
      }
    ],
    "nv": {
      "cl": "llo",
      "ns": "np",
      "lue": 417,
      "rh": [1,"llo",417],
      "it": []
    },
    "dl": {}
  }
}
```

### Expected Verification:

#### State Transition:

`np` ➔ `nd`

#### Targeted State Verification:

```json
{
  "sds.sep": 417,
  "sds.oom.ood.fo": "ons",
  "sds.nv.ns": "nd",
  "sds.nv.it[0][1]": [ 2, "lah" ]
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

* **Repentant Devil** (signaller) ➔ Deployed at: home_bureau
* *Maturity Condition:* 🟢 **Ready**
* *Pending Interaction Reward:* Generates prospects at Avid Horizon
```

---

#### 🔒 INTERNAL STATE AUTOSAVE

```json
{"ssf":"sunless-skies-first-mate","ssv":"0.5.0","sfn":"Mr. Bligh","sds":{"sso":1000,"sep":417,"cpt":{"cnm":"Sinclair","csk":{"ir":10,"mi":18,"he":25,"ve":7},"caf":{"ac":0,"bo":0,"es":0,"vi":0}},"clc":{"cmd":"Spatchcock-Class Scout","cnm":"Zephyr","chl":30,"cmh":30,"cfl":0,"chc":12,"chs":0,"chr":{"frm":3,"srm":3,"dbs":2}},"ccr":{"ccu":10,"cmx":10,"ctr":12,"cng":0},"oom":{"ood":{"fo":"ons","qm":"oai","ma":"dog"},"oun":{"fo":["opi","ocl"]},"osc":{"sc":["olr"]}},"gui":{"gfu":[3,0,20.0],"gsu":[3,0,40.0]},"pps":{},"aaa":[{"aid":"ACT-1011","atp":"sec","ast":"rdy","aol":"home_bureau","att":"Secondment: Repentant Devil","ant":"Generates prospects near the Avid Horizon.","apr":"hi","apn":false,"ace":366,"aue":366,"ade":400,"apl":[["olr",34,"Generates prospects at Avid Horizon","Collect in person"]]}],"nv":{"cl":"llo","ns":"nd","lue":417,"rh":[1,"llo",417],"it":[[2,"lah"]]},"dl":{}}}
```

---

## Test Case 14: Multi-State Compound Turn Pipeline

### Objective

Tests the multi-state kinetic turn pipeline. Ingests transit burn and arrival at Lustrum (`ne` ➔ `na`), executes commerce and hold adjustments while docked (`na` ➔ `np`), performs rolling hold/fuel checks, and transitions out to open skies (`np` ➔ `nd` ➔ `ne`). Verifies `rh` captures arrival epoch while forward itinerary renumbers cleanly, evaluates the terminal state as `ne`, emits the departure logbook and autosave block, suppresses zero-quantity goods/possessions, and validates date advance (`1905-01-20` = Day 19).

### Input Prompt

> Update state. Arrived at Lustrum on 1905-01-20 with 1 fuel spent. While docked, we sold our 2 crates of Unseasoned Hours for 160 Sovereigns total, bought 2 Barrels of Fuel at standard cost (20 each), and immediately cast off lines for Port Avon.

```json
{
  "ssf": "sunless-skies-first-mate",
  "ssv": "0.5.0",
  "sfn": "Mr. Bligh",
  "sds": {
    "sso": 500,
    "sep": 16,
    "cpt": {
      "cnm":"Sinclair",
      "csk": {"ir": 0, "mi": 0, "he": 0, "ve": 0},
      "caf": {"ac": 0, "bo": 0, "es": 0, "vi": 0}
    },
    "clc": {
      "cmd": "Spatchcock-Class Scout",
      "cnm": "Zephyr",
      "chl": 30,
      "cmh": 30,
      "cfl": 0,
      "chc": 12,
      "chs": 0,
      "chr": {"frm": 3, "srm": 3, "dbs": 2}
    },
    "ccr": {"ccu": 8, "cmx": 10, "ctr": 10, "cng": 0},
    "oom": {},
    "gui": {
      "gfu": [4, 0, 20.00],
      "gsu": [3, 0, 40.00],
      "guh": [2, 0, 40.00]
    },
    "pps": {},
    "aaa": [],
    "nv": {
      "cl": null,
      "ns": "ne",
      "lue": 16,
      "rh": [[1,"lpr",7],[2,"lnw",10],[3,"lcr",16]],
      "it": [4,"llu"]
    },
    "dl": {}
  }
}
```

### Expected Verification:

#### State Transition:

`ne` ➔ `na` ➔ `np` ➔ `nd` ➔ `ne` (Multi-state compound turn pipeline executed atomically)

#### Targeted State Verification:

```json
{
  "sds.sep": 19,
  "sds.sso": 620,
  "sds.clc.cfl": 1,
  "sds.gui.gfu[0]": 5,
  "sds.gui.guh": null,
  "sds.nv.ns": "ne",
  "sds.nv.cl": null,
  "sds.nv.rh[0]": [ 2, "lnw", 10 ],
  "sds.nv.rh[1]": [ 3, "lcr", 16 ],
  "sds.nv.rh[2]": [ 4, "llu", 19 ],
  "sds.nv.it[0]": [ 5, "lpo" ]
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
{"ssf":"sunless-skies-first-mate","ssv":"0.5.0","sfn":"Mr. Bligh","sds":{"sso":620,"sep":19,"cpt":{"cnm":"Sinclair","csk":{"ir":0,"mi":0,"he":0,"ve":0},"caf":{"ac":0,"bo":0,"es":0,"vi":0}},"clc":{"cmd":"Spatchcock-Class Scout","cnm":"Zephyr","chl":30,"cmh":30,"cfl":1,"chc":12,"chs":0,"chr":{"frm":3,"srm":3,"dbs":2}},"ccr":{"ccu":8,"cmx":10,"ctr":10,"cng":0},"oom":{},"gui":{"gfu":[5,0,20.0],"gsu":[3,0,40.0]},"pps":{},"aaa":[],"nv":{"cl":null,"ns":"ne","lue":19,"rh":[[2,"lnw",10],[3,"lcr",16],[4,"llu",19]],"it":[5,"lpo"]},"dl":{}}}
```

---

## Test Case 15: Economic Core & Moving Average Cost (MAC) Recalculation

### Objective

Tests the Moving Average Cost (MAC) formula. Verifies atomic sovereign deduction, hold slot tracking, physical free slot validation, suppression of unheld inventory items, and calendar evaluation crossing a 30-day month boundary.

### Input Prompt

> Update state. We are docked at London on 1905-04-30. We currently hold 2 crates of Munitions with an average cost of 60 Sovereigns each. The Ministries are offering surplus munitions at a discount: we just purchased 4 additional crates of Munitions for 30 Sovereigns each. We also picked up 2 barrels of Fuel at 20 each, and now we are casting off lines for Brabazon Workworld.

```json
{
  "ssf": "sunless-skies-first-mate",
  "ssv": "0.5.0",
  "sfn": "Mr. Bligh",
  "sds": {
    "sso": 1000,
    "sep": 119,
    "cpt": {
      "cnm":"Sinclair",
      "csk": {"ir": 0, "mi": 0, "he": 0, "ve": 0},
      "caf": {"ac": 0, "bo": 0, "es": 0, "vi": 0}
    },
    "clc": {
      "cmd": "Spatchcock-Class Scout",
      "cnm": "Zephyr",
      "chl": 30,
      "cmh": 30,
      "cfl": 0,
      "chc": 12,
      "chs": 0,
      "chr": {"frm": 3, "srm": 3, "dbs": 2}
    },
    "ccr": {"ccu": 8, "cmx": 10, "ctr": 15, "cng": 0},
    "oom": {},
    "gui": {
      "gfu": [1, 0, 20.00],
      "gsu": [3, 0, 40.00],
      "gmu": [2, 0, 60.00]
    },
    "pps": {},
    "aaa": [],
    "nv": {
      "cl": "llo",
      "ns": "np",
      "lue": 119,
      "rh": [1,"llo",119],
      "it": []
    },
    "dl": {}
  }
}

```

### Expected Verification:

#### State Transition:

`np` ➔ `nd`

#### Mathematical Pipeline Calculation:

* **Munitions MAC:** Existing $(2 \times 60.00 = 120.00)$ plus New $(4 \times 30.00 = 120.00) \rightarrow \frac{240.00}{6} = 40.00$
* **Sovereign Deductions:** $1000 - (4 \times 30) - (2 \times 20) = 1000 - 120 - 40 = 840$ Sovereigns
* **Hold Slots Used:** $3 \text{ Fuel} + 3 \text{ Supplies} + 6 \text{ Munitions} = 12 / 12$ slots ($Free = 0$)

#### Targeted State Verification:

```json
{
  "sds.sso": 840,
  "sds.gui.gmu[0]": [ 6, 0, 40.0 ],
  "sds.gui.gfu[0]": [ 3, 0, 20.0 ],
  "sds.nv.ns": "nd",
  "sds.nv.it[0][1]": [ 2, "lbw" ]
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
{"ssf":"sunless-skies-first-mate","ssv":"0.5.0","sfn":"Mr. Bligh","sds":{"sso":840,"sep":119,"cpt":{"cnm":"Sinclair","csk":{"ir":0,"mi":0,"he":0,"ve":0},"caf":{"ac":0,"bo":0,"es":0,"vi":0}},"clc":{"cmd":"Spatchcock-Class Scout","cnm":"Zephyr","chl":30,"cmh":30,"cfl":0,"chc":12,"chs":0,"chr":{"frm":3,"srm":3,"dbs":2}},"ccr":{"ccu":8,"cmx":10,"ctr":15,"cng":0},"oom":{},"gui":{"gfu":[3,0,20.0],"gsu":[3,0,40.0],"gmu":[6,0,40.0]},"pps":{},"aaa":[],"nv":{"cl":"llo","ns":"nd","lue":119,"rh":[1,"llo",119],"it":[2,"lbw"]},"dl":{}}}
```

---

## Test Case 16: Inter-Region Transit Relay Trajectory & Toll Evaluation

### Objective

Tests inter-region relay gating rules. Verifies that plotting course through a transit relay (`lt2`) to an external destination in Albion (`london`) verifies the required transit permit (`albion` permit key in `possessions.ptp`), audits payable toll options, alerts the Captain of required crossing costs without prematurely deducting assets while docked, suppresses zero-quantity items, and parses standardized High Wilderness calendar dates (`1905-06-15` = $31 + 28 + 31 + 30 + 31 + 14 = \text{Day } 165$).

### Input Prompt

> Update state. We are docked at New Winchester on 1905-06-15. We hold the necessary Albion Transit Permit stamped by the Ministry. Plot an inter-region course out through the Albion Transit Relay and straight on to London. Review our gate clearance and let me know our toll options before we set out.

```json
{
  "ssf": "sunless-skies-first-mate",
  "ssv": "0.5.0",
  "sfn": "Mr. Bligh",
  "sds": {
    "sso": 1200,
    "sep": 165,
    "cpt": {
      "cnm":"Sinclair",
      "csk": {"ir": 10, "mi": 5, "he": 5, "ve": 5},
      "caf": {"ac": 0, "bo": 0, "es": 1, "vi": 0}
    },
    "clc": {
      "cmd": "Spatchcock-Class Scout",
      "cnm": "Zephyr",
      "chl": 30,
      "cmh": 30,
      "cfl": 0,
      "chc": 12,
      "chs": 0,
      "chr": {"frm": 3, "srm": 3, "dbs": 2}
    },
    "ccr": {"ccu": 9, "cmx": 10, "ctr": 10, "cng": 0},
    "oom": {},
    "gui": {
      "gfu": [4, 0, 20.00],
      "gsu": [4, 0, 40.00],
      "guh": [2, 0, 80.00]
    },
    "pps": {
      "es": {"pmp": 1},
      "ptp": ["ta"]
    },
    "aaa": [],
    "nv": {
      "cl": "lnw",
      "ns": "np",
      "lue": 165,
      "rh": [1,"lnw",160],
      "it": []
    },
    "dl": {}
  }
}

```

### Expected Verification:

#### State Transition:

`np` ➔ `nd`

#### Targeted State Verification:

```json
{
  "sds.sep": 165,
  "sds.pps.ptp[0]": [ "ta" ],
  "sds.nv.ns": "nd",
  "sds.nv.it[0]": [ 2, "lt2" ],
  "sds.nv.it[1]": [ 3, "llo" ]
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
{"ssf":"sunless-skies-first-mate","ssv":"0.5.0","sfn":"Mr. Bligh","sds":{"sso":1200,"sep":165,"cpt":{"cnm":"Sinclair","csk":{"ir":10,"mi":5,"he":5,"ve":5},"caf":{"ac":0,"bo":0,"es":1,"vi":0}},"clc":{"cmd":"Spatchcock-Class Scout","cnm":"Zephyr","chl":30,"cmh":30,"cfl":0,"chc":12,"chs":0,"chr":{"frm":3,"srm":3,"dbs":2}},"ccr":{"ccu":9,"cmx":10,"ctr":10,"cng":0},"oom":{},"gui":{"gfu":[4,0,20.0],"gsu":[4,0,40.0],"guh":[2,0,80.0]},"pps":{"es":{"pmp":1},"ptp":["ta"]},"aaa":[],"nv":{"cl":"lnw","ns":"nd","lue":165,"rh":[1,"lnw",160],"it":[[2,"lt2"],[3,"llo"]]},"dl":{}}}
```

## Test Case 17: Navigation Itinerary Lifecycle, Rolling History Pruning & Port Arrival

### Objective
Verifies the kinetic transition from `ne` ➔ `na` ➔ `np` for a planned waypoint (`itinerary[0][1] == cl`). Confirms that the completed leg is popped from `navigation.itinerary`, stamped with `arrived_epoch: sep`, and appended to `navigation.rh`. Probes the rolling history cap invariant: since `navigation.rh` begins with 3 prior locations, appending the 4th completed leg must drop the oldest historical entry (`rh[0]`) to maintain a strict rolling clamp of 3 completed stops. Checks that remaining forward itinerary legs are retained, verifies strict suppression of Markdown logbooks and autosave JSON blocks during arrival/docked turns, suppresses zero-quantity commodities/possessions, and tests non-leap year boundary date calculations (`1905-03-05` = \(31 + 28 + 4 = \text{Day } 63\)).

### Input Prompt
> Update state. We just dropped mooring lines and arrived at Lustrum on 1905-03-05. Fuel burn on this leg was 2. What's the lay of the land here, First Mate?

```json
{
  "ssf": "sunless-skies-first-mate",
  "ssv": "0.5.0",
  "sfn": "Mr. Bligh",
  "sds": {
    "sso": 1100,
    "sep": 61,
    "cpt": {
      "cnm":"Sinclair",
      "csk": {"ir": 10, "mi": 5, "he": 5, "ve": 5},
      "caf": {"ac": 0, "bo": 0, "es": 0, "vi": 0}
    },
    "clc": {
      "cmd": "Spatchcock-Class Scout",
      "cnm": "Zephyr",
      "chl": 30,
      "cmh": 30,
      "cfl": 0,
      "chc": 12,
      "chs": 0,
      "chr": {"frm": 3, "srm": 3, "dbs": 2}
    },
    "ccr": {"ccu": 9, "cmx": 10, "ctr": 15, "cng": 0},
    "oom": {},
    "gui": {
      "gfu": [5, 0, 20.00],
      "gsu": [4, 0, 40.00]
    },
    "pps": {},
    "aaa": [],
    "nv": {
      "cl": null,
      "ns": "ne",
      "lue": 61,
      "rh": [
        [1,"lnw",45],
        [2,"lpr",52],
        [3,"lpo",58]
      ],
      "it": [
        [4,"llu"],
        [5,"lti"],
        [6,"lnw"]
      ]
    },
    "dl": {}
  }
}
```

### Expected Verification:

#### State Transition:

`ne` ➔ `na` ➔ `np`

#### Targeted State Verification:

```json
{
  "sds.sep": 63,
  "sds.clc.cfl": 2,
  "sds.gui.gfu[0]": 3,
  "sds.nv.ns": "np",
  "sds.nv.cl": "llu",
  "sds.nv.rh[0]": [ 2, "lpr", 52 ],
  "sds.nv.rh[1]": [ 3, "lpo", 58 ],
  "sds.nv.rh[2]": [ 4, "llu", 63 ],
  "sds.nv.it[0]": [ 5, "lti" ],
  "sds.nv.it[1]": [ 6, "lnw" ]
}

```

#### Report Text:

(Full Markdown logbooks and JSON autosave blocks are strictly suppressed during `na` and `np` turns.)

> **Mr. Bligh reports:**
> "Lines secured at the icy quays of Lustrum on 5 March 1905. Two barrels of fuel deducted for the transit burn, leaving 3 in the hold alongside our 4 crates of supplies.
> Lustrum is freezing and bleak, huddled beneath the shadow of the Mother of Mountains where prospectors quarry frozen time straight from the rockface. Station facilities are operational: fuel bunkering, provisions, and crew recruitment are open, though there's no drydock shipyard here. Ahead on our charted course lie Titania and our eventual return to New Winchester. The ledger and transit logs are updated; awaiting your command before we step into the cold or conduct trade at the exchange."

---

## Test Case 18: Commercial Station Serialization (With Bazaar)

### Objective

Verifies that when charting a commercial station (such as New Winchester), the engine serializes the `cd` and the complete `bazaar` block with its reset epoch and active bargains.

### Input Prompt

> Update state. We've docked in New Winchester on 9 Jan 1905. The bazaar market refreshes in 30 days and currently lists 5 crates of munitions at 60 Sovereigns each.

```json
{
  "ssf": "sunless-skies-first-mate",
  "ssv": "0.5.0",
  "sfn": "Mr. Bligh",
  "sds": {
    "sso": 1000,
    "sep": 5,
    "cpt": {
      "cnm":"Sinclair",
      "csk": {"ir": 0, "mi": 0, "he": 0, "ve": 0},
      "caf": {"ac": 0, "bo": 0, "es": 0, "vi": 0}
    },
    "clc": {
      "cmd": "Spatchcock-Class Scout",
      "cnm": "Zephyr",
      "chl": 30,
      "cmh": 30,
      "cfl": 0,
      "chc": 12,
      "chs": 0,
      "chr": {"frm": 3, "srm": 3, "dbs": 2}
    },
    "ccr": {"ccu": 8, "cmx": 10, "ctr": 0, "cng": 0},
    "oom": {},
    "gui": {
      "gfu": [3, 0, 20.00],
      "gsu": [3, 0, 40.00]
    },
    "pps": {},
    "aaa": [],
    "nv": {
      "cl": "lnw",
      "ns": "arriving",
      "lue": 0,
      "rh": [],
      "it": []
    },
    "dl": {}
  }
}
```

### Expected Verification:

#### State Transition:

`na` ➔ `np`

#### Report Text:

(Full Markdown logbooks and JSON autosave blocks are strictly suppressed during  `np` turns.)

#### Targeted State Verification:

```json
{
"sds.dl.lnw.cd": null,
"sds.dl.lnw.bz.re": 38,
"sds.dl.lnw.bz.ab[0]": [ "gmu", 5, 60 ]
}
```

#### 🔒 INTERNAL STATE AUTOSAVE

```json
{"ssf":"sunless-skies-first-mate","ssv":"0.5.0","sfn":"Mr. Bligh","sds":{"sso":1000,"sep":8,"cpt":{"cnm":"Sinclair","csk":{"ir":0,"mi":0,"he":0,"ve":0},"caf": {"ac":0,"bo":0,"es":0,"vi":0}},"clc":{"cmd":"Spatchcock-Class Scout","cnm": "Zephyr","chl":30,"cmh":30,"cfl":0,"chc":12,"chs":0,"chr":{"frm":3,"srm":3, "dbs":2}},"ccr":{"ccu":8,"cmx":10,"ctr":0,"cng":0},"oom":{},"gui":{"gfu":[3,0,20.00],"gsu":[3,0,40.00]},"pps":{},"aaa":[],"nv":{"cl":"lnw","ns":"np","lue":0,"rh":[],"it":[]},"dl":{"lnw":{"cd":null,"bz":{"re":38,"ab":[["gmu",5,60]]}}}}}
```
---

## Test Case 19: Non-Commercial Node Serialization (Without Bazaar)

### Objective

Verifies the ultra-sparse rule for non-commercial nodes (such as a transit relay like `lt2` or a platform/spectacle) where the `"bz"` key is completely omitted to conserve telegraphic tokens, leaving strictly the clock position.

### Input Prompt

> Update state. We just arrived at The Albion Transit Relay at clock position 4 on 1st February, 1905. Bring us in and tie off to the docks.

```json
{
  "ssf": "sunless-skies-first-mate",
  "ssv": "0.5.0",
  "sfn": "Mr. Bligh",
  "sds": {
    "sso": 1000,
    "sep": 25,
    "cpt": {
      "cnm":"Sinclair",
      "csk": {"ir": 0, "mi": 0, "he": 0, "ve": 0},
      "caf": {"ac": 0, "bo": 0, "es": 0, "vi": 0}
    },
    "clc": {
      "cmd": "Spatchcock-Class Scout",
      "cnm": "Zephyr",
      "chl": 30,
      "cmh": 30,
      "cfl": 0,
      "chc": 12,
      "chs": 0,
      "chr": {"frm": 3, "srm": 3, "dbs": 2}
    },
    "ccr": {"ccu": 8, "cmx": 10, "ctr": 0, "cng": 0},
    "oom": {},
    "gui": {
      "gfu": [3, 0, 20.00],
      "gsu": [3, 0, 40.00]
    },
    "pps": {},
    "aaa": [],
    "nv": {
      "cl": null,
      "ns": "ne",
      "lue": 0,
      "rh": [],
      "it": []
    },
    "dl": {
      "lt2": {
        "cd": 4
      }
    }
  }
}
```

### Expected Verification:

```json
{
  "sds.dl.lt2.cd": 4,
  "sds.dl.lt2.bazaar": null
}
```

#### State Transition:

`ne` ➔ `na` ➔ `np`

#### Report Text:

(Full Markdown logbooks and JSON autosave blocks are strictly suppressed during  `np` turns.)

#### 🔒 INTERNAL STATE AUTOSAVE

```json
{"ssf":"sunless-skies-first-mate","ssv":"0.5.0","sfn":"Mr. Bligh","sds":{"sso":1000,"sep":25,"cpt":{"cnm":"Sinclair","csk":{"ir":0,"mi":0,"he":0,"ve":0},"caf":{"ac":0,"bo":0,"es":0,"vi":0}},"clc":{"cmd": "Spatchcock-Class Scout","cnm":"Zephyr","chl":30,"cmh":30,"cfl":0,"chc":12,"chs":0,"chr": {"frm":3,"srm":3,"dbs":2}},"ccr":{"ccu":8,"cmx":10,"ctr":0,"cng":0},"oom":{},"gui":{"gfu":[3,0,20.00],"gsu":[3,0,40.00]},"pps":{},"aaa":[],"nv":{"cl":"lt2","ns":"np","lue":31,"rh":[],"it":[]},"dl":{"lt2":{"cd":4}}}}
```

---

## Test Case 20: Next Stop Action Filtering & Priority Indicator Verification

### Objective

Verifies that when departing a port, the **NEXT STOP** section under **OPERATIONS & TRANSIT** strictly filters actions to include only those whose target location matches the active itinerary (or are explicitly pinned). Furthermore, it validates that high-priority (`🟥`) and low-priority (`🟩`) visual indicators are correctly prepended to the filtered action list items.

### Test Input Prompt

> Update state. We are docked at New Winchester on 1905-03-01. Our active itinerary is set for Port Avon. Review our pending logs, apply our standard priority markers, and cast off lines.

```json
{
  "ssf": "sunless-skies-first-mate",
  "ssv": "0.5.0",
  "sfn": "Mr. Bligh",
  "sds": {
    "sso": 1000,
    "sep": 60,
    "cpt": {
      "cnm": "Sinclair",
      "csk": {"ir": 0, "mi": 0, "he": 0, "ve": 0},
      "caf": {"ac": 0, "bo": 0, "es": 0, "vi": 0}
    },
    "clc": {
      "cmd": "Spatchcock-Class Scout",
      "cnm": "Zephyr",
      "chl": 30,
      "cmh": 30,
      "cfl": 0,
      "chc": 12,
      "chs": 0,
      "chr": {"frm": 3, "srm": 3, "dbs": 2}
    },
    "ccr": {"ccu": 8, "cmx": 10, "ctr": 0, "cng": 0},
    "oom": {},
    "gui": {
      "gfu": [3, 0, 20.00],
      "gsu": [3, 0, 40.00]
    },
    "pps": {},
    "aaa": [
      {
        "aid": "ACT-3001",
        "atp": "prs",
        "ast": "rdy",
        "aol": "lnw",
        "att": "Avon Reading Materials",
        "ant": "Deliver Approved Literature to Port Avon.",
        "apr": "hi",
        "apn": false,
        "ace": 50,
        "aue": 50,
        "ade": null,
        "apl": ["gal", 2, 2, 0, "lpo"]
      },
      {
        "aid": "ACT-3002",
        "atp": "tod",
        "ast": "act",
        "aol": "lnw",
        "att": "Inspect the docks at Port Avon",
        "ant": "Check cargo handling efficiency.",
        "apr": "lo",
        "apn": false,
        "ace": 55,
        "aue": 55,
        "ade": null,
        "apl": ["lpo"]
      },
      {
        "aid": "ACT-3003",
        "atp": "prs",
        "ast": "rdy",
        "aol": "lnw",
        "att": "Irrelevant Titania Haul",
        "ant": "Cargo destined elsewhere.",
        "apr": "hi",
        "apn": false,
        "ace": 52,
        "aue": 52,
        "ade": null,
        "apl": ["gbw", 2, 2, 0, "lti"]
      }
    ],
    "nv": {
      "cl": "lnw",
      "ns": "np",
      "lue": 60,
      "rh": [1, "lnw", 50],
      "it": [[2, "lpo"]]
    },
    "dl": {}
  }
}

```

---

### Expected Verification

#### State Transition:

`np` ➔ `nd`

#### Report Text:

Upon successful execution, the generated Markdown logbook must display the following structured block under **NEXT STOP**, ensuring `ACT-3003` (destined for Titania `lti`) is filtered out, while `ACT-3001` and `ACT-3002` (destined for Port Avon `lpo`) appear with their respective priority indicators (`🟥` and `🟩`):

```markdown
### ➡️ NEXT STOP: Port Avon
* ‼️ 🔑 **READY FOR DELIVERY:** Avon Reading Materials — Deliver 2 Approved Literature to Port Avon to complete contract
* 🔻 📌 **BRIDGE NOTE:** Inspect the docks at Port Avon — Check cargo handling efficiency. — Priority: LOW
```

#### 🔒 INTERNAL STATE AUTOSAVE

```json
{"ssf":"sunless-skies-first-mate","ssv":"0.5.0","sfn":"Mr. Bligh","sds":{"sso":1000,"sep":58,"cpt":{"cnm":"Sinclair","csk":{"ir":0,"mi":0,"he":0,"ve":0},"caf":{"ac":0,"bo":0,"es":0,"vi":0}},"clc":{"cmd":"Spatchcock-Class Scout","cnm":"Zephyr","chl":30,"cmh":30,"cfl":0,"chc":12,"chs":0,"chr":{"frm":3,"srm":3,"dbs":2}},"ccr":{"ccu":8,"cmx":10,"ctr":0,"cng":0},"oom":{},"gui":{"gfu":[3,0,20.0],"gsu":[3,0,40.0],"gal":[2,2,0]},"pps":{},"aaa":[{"aid":"ACT-3001","atp":"prs","ast":"rdy","aol":"lnw","att":"Avon Reading Materials","ant": null,"apr":"hi","apn":false,"ace":50,"aue":58,"ade":null,"apl":["gal",2,2,2,"lpo"]},{"aid":"ACT-3002","atp":"tod","ast":"act","aol":"lnw","att":"Inspect the docks at Port Avon","ant":"Check cargo handling efficiency.","apr":"lo","apn":false,"ace":55,"aue":58,"ade":null,"apl":["lpo"]},{"aid":"ACT-3003","atp":"prs","ast":"rdy","aol":"lnw","att":"Irrelevant Titania Haul","ant":"Cargo destined elsewhere.","apr":"hi","apn":false,"ace":52,"aue":58,"ade":null,"apl":["gbw",2,2,0,"lti"]}],"nv":{"cl":null,"ns":"nd","lue":58,"rh":[1,"lnw",50],"it":[[2,"lpo"]]},"dl":{}}}
```
