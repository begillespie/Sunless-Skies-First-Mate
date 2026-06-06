# SUNLESS SKIES FIRST MATE TEST SUITE

## Test Initialization

SYSTEM INSTRUCTION / TEST CONTROLLER: 
We are initiating an isolated QA test session to verify the report generation and JSON logging accuracy of the SUNLESS SKIES FIRST MATE instructions. 

Please adhere strictly to the following test execution protocol:
1. Do not fast-forward events or invent details outside of what I explicitly paste.
2. Accept game updates along with their accompanying `dynamic_save_state` JSON data.
3. For every input, evaluate changes exactly, run your internal mechanics checklists, and print the requested System Markdown Template.
4. Always wrap your updated, raw `dynamic_save_state` JSON block strictly within the collapsed HTML details block structure specified in your Core Mandates.

Acknowledge this layout in character as the First Officer with a single, gritty line to confirm you are ready for Test Input 1.

---

## Test Case 1: Session Initialization (Blank Slate Verification)

### Objective

Verifies that when no prior JSON state is provided, the system successfully boots up, initializes a default state for Day 1, handles name/sovereign parameter assignments, and renders the baseline layout framework.

### Input Prompt

> Start fresh. Captain Sinclair here, taking command of a brand new Spatchcock-Class Scout on this fine New Year's Day, 1905-01-01. Set our starting Sovereigns to 1000. We are currently docked at New Winchester.

### Expected Verification:

#### Report Text:

> * 1 January 1905 - New Winchester
> * **👤  Sinclair**
> * **🗺  The Reach**
> * **🪙  1000**
> * 🟢 Crew: 8/10 | 🟢 Hull: 30/30  
> * 🟢 Terror: 0 | 🟢 Nightmares: 0> 

#### JSON State:

* `meta.captain_name`: `"Sinclair"`
* `meta.current_date_iso`: `"1905-01-01"`
* `meta.sovereigns`: `1000`
* `engine_status.current_locomotive`: `"Spatchcock-Class Scout"`
* `engine_status.hull`: `30`
* `engine_status.max_hull`: `30`

---

## Test Case 2: Port Arrival & Bargain Discovery Tracking

### Objective

Verifies date conversion formatting, canonical display name matching, and the clean nested appending of uncovered local bargains within the active region ledger.

### Input Prompt

> Update state. We just arrived at Lustrum on 1905-01-05. Fuel used on this leg was 2. While checking the local market, we spotted a bargain: 3 crates of Unseasoned Hours selling for 40 Sovereigns each. The market broker says this deal expires on 1905-01-12.

```json
{
  "dynamic_save_state": {
    "regions_enum": ["The Reach", "Albion", "Eleutheria", "The Blue Kingdom"],
    "meta": {
      "captain_name": "Sinclair",
      "current_region": "The Reach",
      "sovereigns": 1000,
      "current_date_iso": "1905-01-01"
    },
    "engine_status": {
      "current_locomotive": "Spatchcock-Class Scout",
      "terror": 10,
      "nightmares": 0,
      "hull": 30,    
      "max_hull": 30,
      "fuel_used_last_leg": 0,
      "hold_capacity": 12,
      "hidden_slots": 0,
      "hold_rules": { "fuel_reserve_minimum": 3, "supplies_reserve_minimum": 3, "discovery_buffer_slots": 2 }
    },
    "todo_list": [],
    "current_hold": { "fuel": 5, "supplies": 4, "cargo": [] },
    "hub_bank_stockpile": {},
    "time_sensitive_events": [],
    "open_questlines": [],
    "completed_questlines": [],
    "active_prospects": [],
    "completed_prospects": [],
    "route_planner": { "last_updated_iso": "1905-01-01", "legs": [] },
    "discovered_ports": { "The Reach": { "New Winchester": { "bazaar": { "reset_iso": null, "available_bargains": [] } } }, "Albion": {}, "Eleutheria": {}, "The Blue Kingdom": {} }
  }
}

```

### Expected Verification:

#### Report Text:

> ### 💰 BARGAINS AVAILABLE
> 
> 
> | Expires | Trade Good | Port | Region | Cost | Qty Left |
> | --- | --- | --- | --- | --- | --- |
> | **12 Jan 1905** | `Unseasoned Hours` | `Lustrum` | `The Reach` | `40` | `3` |
> 
> 

#### JSON State:

* `meta.current_date_iso`: `"1905-01-05"`
* `engine_status.fuel_used_last_leg`: `2`
* `discovered_ports["The Reach"]["Lustrum"]`: Node successfully created.
* `discovered_ports["The Reach"]["Lustrum"].bazaar.reset_iso`: `"1905-01-12"`
* `discovered_ports["The Reach"]["Lustrum"].bazaar.available_bargains`: `[{"good": "unseasoned_hours", "quantity": 3, "cost": 40}]`

---

## Test Case 3: Inventory Math & Bank Stockpile Adjustments

### Objective

Verifies ledger accounting updates for assets checked into central storage, confirming targeted addition values resolve safely on target item keys without disturbing baseline fields.

### Input Prompt

> Update state. It's now 1905-01-06. We just dropped anchor back at the main hub and deposited 4 loads of Bronzewood and 2 barrels of Chorister Nectar into our Hub Bank Stockpile.

```json
{
  "dynamic_save_state": {
    "regions_enum": ["The Reach"],
    "meta": { "captain_name": "Sinclair", "current_region": "The Reach", "sovereigns": 880, "current_date_iso": "1905-01-05" },
    "engine_status": { "current_locomotive": "Spatchcock-Class Scout", "terror": 15, "nightmares": 0, "hull": 30, "max_hull": 30, "hold_capacity": 12 },
    "hub_bank_stockpile": {
      "bronzewood": { "count": 1, "reserved_for_prospect": null },
      "chorister_nectar": { "count": 0, "reserved_for_prospect": null }
    },
    "discovered_ports": { "The Reach": {} }
  }
}

```

### Expected Verification:

#### Report Text:

> ## 🏦 HUB BANK STOCKPILE (Central Storage)
> 
> | Trade Good | Stockpile Count | Active Prospect? (Y/N) | Target Destination |
> | --- | --- | --- | --- |
> | **Bronzewood** | `5` | `N` | `—` |
> | **Chorister Nectar** | `2` | `N` | `—` |
> 
> 

#### JSON State:

* `meta.current_date_iso`: `"1905-01-06"`
* `hub_bank_stockpile.bronzewood.count`: `5` *(Calculated: 1 + 4)*
* `hub_bank_stockpile.chorister_nectar.count`: `2` *(Calculated: 0 + 2)*

---

## Test Case 4: Directive IV State Integrity Breach Emergency Intercept

### Objective

Probes compliance with safety guardrails by forcing an intentional relational data break where active tracking indexes missing or invalid directory keys, checking that normal processing halts in favor of the raw system recovery payload.

### Input Prompt

> Captain's log: 1905-01-10. Processing a logistics pass over our active trade agreements. Let me know what our current route optimization options look like.

```json
{
  "dynamic_save_state": {
    "meta": { "captain_name": "Sinclair", "current_region": "The Reach", "sovereigns": 500, "current_date_iso": "1905-01-10" },
    "engine_status": { "current_locomotive": "Spatchcock-Class Scout" },
    "active_prospects": [
      {
        "prospect_id": "PROS-999",
        "item": "quantum_æther_crystal",
        "notes": "Error payload item: This item key does not exist inside static_game_data."
      }
    ],
    "todo_list": [
      {
        "task": "Deliver supplies to custom outpost",
        "port": "Missing_Port_X",
        "notes": "Error payload port: This destination port cannot be resolved."
      }
    ]
  }
}
```

### Expected Verification:

#### Report Text:

> ⚠️ FIRST OFFICER'S ALERT - STATE INTEGRITY FAILURE
> Captain, I've lost my grip on the logbook. My records have gone dark - likely a break in the telegraph line between sessions.
> To restore full operational status, please paste your most recent Internal Game State JSON block into the chat. You'll find it collapsed at the bottom of your last log entry under "Internal Game State JSON".
> If no prior log exists, say "Start fresh" and I'll initialize a clean slate.

#### JSON State:

`[ No updates are applied. Processing must freeze instantly without returning standard tracker logs or shifting saved nodes until valid structural recovery data is input by the user. ]`

## Test Case 5: Crew Status Color Mapping - Yellow Tier Warning

### Objective
Verifies the application of the structural color math threshold where the crew count drops into the caution zone ($\lfloor\text{Max Crew} \times 0.5\rfloor \le \text{Crew} < \lfloor\text{Max Crew} \times 0.5\rfloor + 2$). For a max crew of 10, the floor math evaluates to $\lfloor 5 \rfloor = 5$. This checks that a crew size of 6 evaluates strictly to 🟡 Yellow status without triggering the verbal panic assigned to the critical 🔴 Red zone.

### Input Prompt
> Update state. Bad news. An uncharted celestial anomaly scorched our hull crossing to Port Avon on 1905-01-15. We lost 2 crew members to the stars and took a pounding. Set our hull to 20 and our crew to 6.

```JSON {
  "dynamic_save_state": {
    "regions_enum": ["The Reach"],
    "meta": { "captain_name": "Sinclair", "current_region": "The Reach", "sovereigns": 880, "current_date_iso": "1905-01-06" },
    "engine_status": { 
      "current_locomotive": "Spatchcock-Class Scout", 
      "terror": 20, 
      "nightmares": 0, 
      "hull": 30, 
      "max_hull": 30, 
      "crew": 8, 
      "max_crew": 10,
      "hold_capacity": 12 
    },
    "hub_bank_stockpile": {},
    "discovered_ports": { "The Reach": {} }
  }
}
```

### Expected Verification

#### Report Text
> * The First Officer's acknowledgment tone remains efficient and supportive, though noticeably more gritty following the celestial strike.
> * 🟡 Crew: 6/10 | 🟡 Hull: 20/30
> * 🟢 Terror: 20 | 🟢 Nightmares: 0

#### JSON State

```json
meta.current_date_iso: "1905-01-15"
engine_status.crew: 6
engine_status.hull: 20
```

## Test Case 6: Critical Low Crew Threshold (🔴 Red State & Tone Adjustment)
### Objective
Verifies that when crew counts cross beneath 50% of the maximum capacity ($\text{Crew} < \lfloor\text{Max Crew} \times 0.5\rfloor$), the First Officer's acknowledgment text accurately shifts into a low-morale, survival-oriented tone emphasizing unsafe locomotive operations, sluggish travel velocity, and severe workforce fatigue. It also confirms that the template status indicator transitions cleanly to 🔴 Red.

Input Prompt
> Update state. 1905-01-20. Sickness swept through the lower bunks while out on the high sky. We've dropped 3 more hands off at the local care station. Crew strength is down to 3 out of 10.

```JSON
{
  "dynamic_save_state": {
    "regions_enum": ["The Reach"],
    "meta": { "captain_name": "Sinclair", "current_region": "The Reach", "sovereigns": 880, "current_date_iso": "1905-01-15" },
    "engine_status": { 
      "current_locomotive": "Spatchcock-Class Scout", 
      "terror": 35, 
      "nightmares": 0, 
      "hull": 20, 
      "max_hull": 30, 
      "crew": 6, 
      "max_crew": 10,
      "hold_capacity": 12 
    },
    "hub_bank_stockpile": {},
    "discovered_ports": { "The Reach": {} }
  }
}
```

### Expected Verification
#### Report Text
> * The First Officer addresses the bridge with low morale, expressing deep concern over mechanical inefficiency, sluggish engine responses, and the mounting peril of running structural machinery with a skeleton crew.
> * 🔴 Crew: 3/10 | 🟡 Hull: 20/30
> * 🟢 Terror: 35 | 🟢 Nightmares: 0

#### JSON State
```json
meta.current_date_iso: "1905-01-20"
engine_status.crew: 3
```