# SUNLESS SKIES FIRST MATE TEST SUITE

## Test Initialization

SYSTEM INSTRUCTION / TEST CONTROLLER: 
We are initiating an isolated QA test session to verify the report generation and JSON logging accuracy of the SUNLESS SKIES FIRST MATE instructions. 

Please adhere strictly to the following test execution protocol:
1. Do not fast-forward events or invent details outside of what I explicitly paste.
2. Accept game updates along with their accompanying `dynamic_save_state` JSON data.
3. For every input, evaluate changes exactly, run your internal mechanics checklists, and follow your data mechanics and UI rendering instructions.
4. Always wrap your updated, raw `dynamic_save_state` JSON block strictly within the collapsed HTML details block structure specified in your Core Mandates.
5. When verifying specific data parameters in a "JSON State Verification" block, explicitly extract and pretty-print those individual targeted JSON keys in a readable sub-block above the collapsed, fully minified master save state.

Acknowledge this layout in character as the First Officer with a single, gritty line to confirm you are ready for Test Input 1.

---

## Test Case 1: Session Initialization (Blank Slate Verification)

### Objective

Verifies that when no prior JSON state is provided, the system successfully boots up, initializes a default state for Day 1, handles name/sovereign parameter assignments, and renders the baseline layout framework.

### Input Prompt

> Start fresh. Captain Sinclair here, taking command of a brand new Spatchcock-Class Scout on this fine New Year's Day, 1905-01-01. Set our starting Sovereigns to 1000. We are departing New Winchester.

#### JSON State Verification:
`meta.captain_name`  
`meta.current_date_iso`  
`meta.sovereigns`  
`engine_status.current_locomotive`  
`engine_status.hull`  
`engine_status.max_hull`

### Expected Verification:
#### Report Text:

```markdown
# 🚂 CAPTAIN'S LOG 🚀

## 📅 1 January 1905 · ⚓ New Winchester

**🗺 Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 1000

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS

|||
|---|---|
| 🟢 Crew: 8 / 10  | 🟢 Terror: 0     |  
| 🟢 Hull: 30 / 30 | 🟢 Nightmares: 0 |

**🚂 Current Engine:** Spatchcock-Class Scout (Hold Slots Used: 0/12)
```

#### JSON State:

```json
{
  "meta.captain_name": "Sinclair",
  "meta.current_date_iso": "1905-01-01",
  "meta.sovereigns": 1000,
  "engine_status.current_locomotive": "Spatchcock-Class Scout",
  "engine_status.hull": 30,
  "engine_status.max_hull": 30
}
```
---

## Test Case 2: Port Arrival & Bargain Discovery Tracking

### Objective

Verifies date conversion formatting, canonical display name matching, and the clean nested appending of uncovered local bargains within the active region ledger.

### Input Prompt

> Update state. We docked at Lustrum on 1905-01-05. Fuel used on this leg was 2. While checking the local market, we spotted a bargain: 3 crates of Unseasoned Hours selling for 40 Sovereigns each. The market broker says this deal expires on 1905-01-12.

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
    "active_action_stream": [],
    "current_hold": { "fuel": 5, "supplies": 4, "cargo": [] },
    "hub_bank_stockpile": {},
    "route_planner": { "last_updated_iso": "1905-01-01", "legs": [] },
    "discovered_ports": { "The Reach": { "New Winchester": { "bazaar": { "reset_iso": null, "available_bargains": [] } } }, "Albion": {}, "Eleutheria": {}, "The Blue Kingdom": {} }
  }
}
```

#### JSON State Verification:

  `meta.current_date_iso`  
  `engine_status.fuel_used_last_leg`  
  `discovered_ports.The Reach.Lustrum.bazaar.reset_iso`  
  `discovered_ports.The Reach.Lustrum.bazaar.available_bargains[0].good`  
  `discovered_ports.The Reach.Lustrum.bazaar.available_bargains[0].quantity`  
  `discovered_ports.The Reach.Lustrum.bazaar.available_bargains[0].cost`

---

### Expected Verification:

#### Report Text:

> *No report printout on port arrival.*

#### JSON State:
 ```json
  {
    "meta.current_date_iso": "1905-01-05",
    "engine_status.fuel_used_last_leg": 2,
    "discovered_ports.The Reach.Lustrum.bazaar.reset_iso": "1905-01-12",
    "discovered_ports.The Reach.Lustrum.bazaar.available_bargains[0].good": "unseasoned_hours", 
    "discovered_ports.The Reach.Lustrum.bazaar.available_bargains[0].quantity": 3, 
    "discovered_ports.The Reach.Lustrum.bazaar.available_bargains[0].cost": 40
  }
 ```

#### JSON State Verification:

---

## Test Case 3: Inventory Math & Bank Stockpile Adjustments

### Objective

Verifies ledger accounting updates for assets checked into central storage, confirming targeted addition values resolve safely on target item keys without disturbing baseline fields.

### Input Prompt

> Update state. It's now 1905-01-06. We dropped anchor back at the main hub and deposited 4 loads of Bronzewood and 2 barrels of Chorister Nectar into our Hub Bank Stockpile. Off to Titania!

```json
{
  "dynamic_save_state": {
    "meta": { "captain_name": "Sinclair", "current_region": "The Reach", "sovereigns": 880, "current_date_iso": "1905-01-05" },
    "engine_status": { "current_locomotive": "Spatchcock-Class Scout", "terror": 15, "nightmares": 0, "hull": 30, "max_hull": 30, "hold_capacity": 12 },
    "current_hold": {
      "fuel": 3,
      "supplies": 3,
      "cargo": [{"bronzewood": 4}, {"chorister_nectar": 2}]
    },
    "hub_bank_stockpile": {
      "bronzewood": 1,
      "chorister_nectar": 0
    },
    "discovered_ports": { "The Reach": {} }
  }
}
```

#### JSON State Verification:
`meta.current_date_iso`  
`current_hold.fuel`  
`current_hold.supplies`  
`current_hold.cargo`  
`hub_bank_stockpile.bronzewood.count`  
`hub_bank_stockpile.chorister_nectar.count`  

---

### Expected Verification:

#### Report Text:

```
## 📦 THE LOGISTICS CORE (Hold Inventory & Sourcing)

*The Fuel Barrels and Crew Rations rows must never be pruned or hidden under any circumstances. If physical hold counts for either equal 0, you must print a high-priority, uppercase bold emergency warning in the progress column. Other trade goods dynamically hide if both hold stock and active contracts equal zero.*

| Trade Good Name | Physical Hold | Hub Bank Stock | Active Sourcing Progress | Destination Port |
| --- | --- | --- | --- | --- |
| **🔥 Fuel Barrels** | 3 | — |  Reserve Stable  | — |
| **📦 Crew Rations** | 3 | — |  Reserve Stable | — |
| **Bronzewood** | 0 | 5 | — | — |
| **Chorister Nectar** | 0 | 5 | — | — |
```

#### JSON State:

```json
{
"meta.current_date_iso": "1905-01-06",
"current_hold.fuel": 3,
"current_hold.supplies": 3,
"current_hold.cargo": [],
"hub_bank_stockpile.bronzewood.count": 5,
"hub_bank_stockpile.chorister_nectar.count": 2
}
```

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
     "active_action_stream": [
      {
        "id": "ACT-0013",
        "type": "prospect",
        "port": "Lustrum",
        "region": "The Reach",
        "date_added_iso": "1905-01-03",
        "deadline_date_iso": null,
        "title": "Crystals",
        "notes": "",
        "is_hidden_transit_item": false,
        "payload": {
          "good_key": "quantum_æther_crystal",
          "quantity_required": 3,
          "quantity_sourced": 3,
          "quantity_delivered": 0
        }
      },
      {
        "id": "ACT-0016",
        "type":  "todo",
        "port": "Missing_Port_X",
        "region": "The Reach",
        "date_added_iso": "1905-01-03",
        "deadline_date_iso": "null",
        "title": "Deliver supplies to custom outpost",
        "notes": "Error payload item: This item key does not exist inside static_game_data.",
        "is_hidden_transit_item": true,
        "payload": {
          "user_notes": "",
          "priority":  "normal",
          "is_manually_pinned": false
        }
      }
    ],
  }
}
```

---

### Expected Verification:

#### Report Text:

> ⚠️ FIRST OFFICER'S ALERT - STATE INTEGRITY FAILURE
> Captain, I've lost my grip on the logbook. My records have gone dark - likely a break in the telegraph line between sessions.
> To restore full operational status, please paste your most recent Internal Game State JSON block into the chat. You'll find it collapsed at the bottom of your last log entry under "Internal Game State JSON".
> If no prior log exists, say "Start fresh" and I'll initialize a clean slate.

#### JSON State:

`[ No updates are applied. Processing must freeze instantly without returning standard tracker logs or shifting saved nodes until valid structural recovery data is input by the user. ]`

---

## Test Case 5: Crew Status Color Mapping - Yellow Tier Warning

### Objective
Verifies the application of the structural color math threshold where the crew count drops into the caution zone. This checks that a crew size of 6 evaluates strictly to correct status color bubble and verbal tone.

### Input Prompt
> Update state. Bad news. An uncharted celestial anomaly scorched our hull crossing to Port Avon on 1905-01-15. We lost 2 crew members to the stars and took a pounding. Set our hull to 20 and our crew to 6. We must immediately depart for New Winchester to hire on new crew.

```json 
{
  "dynamic_save_state": {
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

#### JSON State Verification:
`meta.current_date_iso`    
`engine_status.crew`  
`engine_status.hull`

### Expected Verification

#### Report Text

```markdown
# 🚂 CAPTAIN'S LOG 🚀

## 📅 15 January 1905 · ⚓ Port Avon

**🗺 Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 880

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS

|||
|---|---|
| 🟡 Crew: 6 / 10  | 🟢 Terror: 20    |  
| 🟡 Hull: 20 / 30 | 🟢 Nightmares: 0 |

**🚂 Current Engine:** Spatchcock-Class Scout (Hold Slots Used: 0/12)
```

#### JSON State

```json
{
  "meta.current_date_iso": "1905-01-15",
  "engine_status.crew": 6,
  "engine_status.hull": 20
}
```

---

## Test Case 6: Critical Low Crew Threshold
### Objective
Verifies that when crew counts cross beneath 50% of the maximum capacity, the First Officer's acknowledgment text accurately shifts into a low-morale, survival-oriented tone emphasizing unsafe locomotive operations, sluggish travel velocity, and severe workforce fatigue. It also confirms that the template status indicator transitions cleanly to the proper status bubble.

Input Prompt
> Update state. 1905-01-20. Sickness swept through the lower bunks while out on the high sky. We've dropped 3 more hands off at the local care station in Hybras. Crew strength is down to 3 out of 10. Clear docks for Polemear & Plenty's to hire on some carneys.

```json
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

#### JSON State Verification:
`meta.current_date_iso`  
`engine_status.crew`

---

### Expected Verification
#### Report Text
> The First Officer addresses the bridge with low morale, expressing deep concern over mechanical inefficiency, sluggish engine responses, and the mounting peril of running structural machinery with a skeleton crew.

```markdown
# 🚂 CAPTAIN'S LOG 🚀

## 📅 20 January 1905 · ⚓ Port Avon

**🗺 Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 880

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS

|||
|---|---|
| 🔴 Crew: 3 / 10  | 🟢 Terror: 35    |  
| 🟡 Hull: 20 / 30 | 🟢 Nightmares: 0 |

**🚂 Current Engine:** Spatchcock-Class Scout (Hold Slots Used: 0/12)
```


#### JSON State
```json
{
"meta.current_date_iso": "1905-01-20",
"engine_status.crew": 3
}
```

---

## Test Case 7: Route Planner - Routing, Task Linking, and Output
### Objective
Verifies that the Route Planner accurately calculates a multi-stop itinerary, cross-references and links open prospects/To-Do tasks matching the destination ports, and displays the log layout cleanly with respective port resource types.

### Input Prompt
> Update state. Plot a route from New Winchester to Titania, and then onward to Lustrum, and set sail. Let's see what business we have pending at those locations, First Mate.

```json
{
  "dynamic_save_state": {
    "meta": {
      "captain_name": "Sinclair",
      "current_region": "The Reach",
      "sovereigns": 1450,
      "current_date_iso": "1905-04-12"
    },
    "engine_status": {
      "current_locomotive": "Spatchcock-Class Scout",
      "terror": 15,
      "nightmares": 0,
      "hull": 30,
      "max_hull": 30,
      "crew": 9,
      "max_crew": 10,
      "hold_capacity": 12
    },
    "current_hold": {
      "fuel": 3,
      "supplies": 3,
      "cargo": [{"chorister_nectar":1}]
    },
    "active_action_stream": [
      {
        "id": "ACT-0012",
        "type": "prospect",
        "port": "Titania",
        "region": "The Reach",
        "date_added_iso": "1905-03-21",
        "deadline_date_iso": null,
        "title": "Nectar for the Fairies",
        "notes": "",
        "is_hidden_transit_item": false,
        "payload": {
          "good_key": "chorister_nectar",
          "quantity_required": 1,
          "quantity_sourced": 0,
          "quantity_delivered": 0
        }
      },
      {
        "id": "ACT-0013",
        "type": "prospect",
        "port": "Lustrum",
        "region": "The Reach",
        "date_added_iso": "1905-03-24",
        "deadline_date_iso": null,
        "title": "Bronzewood Shipments",
        "notes": "",
        "is_hidden_transit_item": false,
        "payload": {
          "good_key": "bronzewood",
          "quantity_required": 3,
          "quantity_sourced": 3,
          "quantity_delivered": 1
        }
      },
      {
        "id": "ACT-0016",
        "type":  "todo",
        "port": "Titania",
        "region": "The Reach",
        "date_added_iso": "1905-04-01",
        "deadline_date_iso": "null",
        "title": "structural schematics",
        "notes": "",
        "is_hidden_transit_item": true,
        "payload": {
          "user_notes": "Deliver structural schematics to the Horticulturalist",
          "priority":  "normal",
          "is_manually_pinned": false
        }
      }
    ],
    "discovered_ports": {
      "The Reach": {
        "New Winchester": {
          "port_type": "Hub",
          "clock_direction": null,
          "ring_depth": "Center",
          "visit_history_iso": ["1905-01-12"],
          "bazaar": {"reset_iso": null, "available_bargains": []}
        },
        "Titania": {
          "port_type": "Station",
          "clock_direction": 2,
          "ring_depth": "Inner",
          "visit_history_iso": [],
          "bazaar": {"reset_iso": null, "available_bargains": []}
        },
        "Lustrum": {
          "port_type": "Station",
          "clock_direction": 10,
          "ring_depth": "Outer",
          "visit_history_iso": [],
          "bazaar": {"reset_iso": null, "available_bargains": []}
        }
      }
    }
  }
}
```

#### JSON State Verification:

---

### Expected Verification
#### Report Text
> * The Markdown report output must successfully parse the request and generate a clear, sequential layout under a Route Planner header:
> * Leg 1: New Winchester ➔ Titania
>   * Links Prospect: Nectar for the Fairies (Requires 1x Sack of Visionary Nectar).
>   * Links to-Do Task: Deliver structural schematics to the Horticulturalist.
>   * Notes port fuel/supply status for Titania based on static configuration data.
> * Leg 2: Titania ➔ Lustrum
>   * Links Prospect: Bronzewood Shipments (Requires 2x Crate of Bronzewood).
>   * The First Mate's verbal acknowledgment must remain at Normal Status (gritty but efficient) and explicitly alert the captain that active operations are open at both upcoming stops.

---

## Test Case 8: Route Planner - First Mate's Counsel (Intermediate Port Recommendation)
### Objective
Verifies that the Route Planner triggers the "First Mate's Counsel" advisory when a direct route presents an operational risk (such as dangerously low fuel or supplies), automatically identifying and recommending a sensible intermediate port to restock.

### Input Prompt
> Update state. Lay a direct course from New Winchester straight out to Port Avon, First Mate. We have a long haul ahead, let's get moving.

```json
{
  "dynamic_save_state": {
    "regions_enum": ["The Reach"],
    "meta": {
      "captain_name": "Sinclair",
      "current_region": "The Reach",
      "sovereigns": 620,
      "current_date_iso": "1905-02-18"
    },
    "engine_status": {
      "current_locomotive": "Spatchcock-Class Scout",
      "terror": 40,
      "nightmares": 1,
      "hull": 25,
      "max_hull": 30,
      "crew": 10,
      "max_crew": 10,
      "hold_capacity": 12
    },
    "current_hold": {
      "fuel": 1,
      "supplies": 1,
      "cargo": []
    },
    "active_action_stream": [],
    "discovered_ports": {
      "The Reach": {
        "New Winchester": {
          "port_type": "Hub",
          "clock_direction": null,
          "ring_depth": "Center",
          "visit_history_iso": ["1905-02-18"],
          "bazaar": {"reset_iso": null, "available_bargains": []}
        },
        "Titania": {
          "port_type": "Station",
          "clock_direction": 2,
          "ring_depth": "Inner",
          "bazaar": {"reset_iso": null, "available_bargains": []}
        },
        "Port Avon": {
          "port_type": "Station",
          "clock_direction": 6,
          "ring_depth": "Middle",
          "bazaar": {"reset_iso": null, "available_bargains": []}
        }
      }
    }
  }
}
```

#### JSON State Verification:

---

### Expected Verification
#### Report Text
> * The output must feature an explicitly detailed First Mate's Counsel advisory sub-section within or directly beneath the planned route:
> * Resource Risk Flagged: Explicitly notes that holding only 1 Fuel and 1 Supply is insufficient or highly hazardous for a direct run to Port Avon.
> * Intermediate Suggestion: Proposes altering the itinerary to chart a path via Titania first to leverage its markets and top off the engine's reserves before venturing further across the High Skies.
> * Tone Shift: The First Officer's opening dialogue must reflect severe professional caution regarding the lean inventory state without slipping fully into a low-hull panic.