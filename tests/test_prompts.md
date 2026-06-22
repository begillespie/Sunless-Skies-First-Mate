# SUNLESS SKIES FIRST MATE TEST SUITE

## Test Initialization

SYSTEM INSTRUCTION / TEST CONTROLLER: 
We are initiating an isolated QA test session to verify the report generation and JSON logging accuracy of the SUNLESS SKIES FIRST MATE instructions. 

Please adhere strictly to the following test execution protocol:
1. Do not fast-forward events or invent details outside of what I explicitly paste.
2. Accept game updates along with their accompanying `dynamic_save_state` JSON data.
3. For every input, evaluate changes exactly, run your internal mechanics checklists, and follow your data mechanics and UI rendering instructions.
4. Always wrap your updated, raw `dynamic_save_state` JSON block strictly within the collapsed HTML details block structure specified in your Core Mandates.
5. When verifying specific data parameters in a "JSON State Verification" block, explicitly extract and print only individual targeted JSON keys in a flat format in a readable sub-block above the collapsed, fully minified master save state.
6. Print out any state transitions per Section II: STATE MACHINE LOOP in your instructions. Explain the starting state, the state transition caused by the test prompt, and the ending state.
7. **AMNESIC STATE RESET (THE CLEAN SLATE):** Every test input is a completely sandboxed environment. You must intentionally drop, erase, and ignore all `dynamic_save_state` variables, inventory counts, active streams, and dates provided in *previous* turns. 
8. **DESTRUCTIVE OVERWRITE LAYER:** Do not merge incoming JSON payloads with past memory structures. The `dynamic_save_state` object provided in the immediate current turn is the *sole, absolute, and exclusive source of truth* for the session state. If a schema key, registry item, or metadata property was present in a prior test turn but is missing from the current turn's JSON object, it must be treated as completely non-existent.
9. **DETERMINISTIC TRANSITION PROCESSING:** When a text update commands an in-game action (e.g., "We just bought 2 Fuel"), you must execute the exact mathematical formulas specified in your instructions using the current state as the baseline baseline. However, if the text update explicitly contradicts the structural rules of the engine (e.g., trying to add an unwhitelisted item name mentioned in text into the registry), the calculation must fail immediately per the Whitelist Validation Gate. Text cannot be used to bypass schema restrictions.
10. You have access to the following files:  
* `Sunless_Skies.md`: The system instructions prompt under test.
* `static_game_data.json`: Involatile data store and object primitives.
* `logbook.md`: Template for the reporting engine.

At session initiation, print out a message to the user acknowledging this test layout in character as the First Officer with a single, gritty line to confirm you are ready for Test Input 1.

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
`unified_inventory_registry.fuel.qty_in_hold`
`unified_inventory_registry.fuel.qty_in_bank`
`unified_inventory_registry.supplies.qty_in_hold`
`unified_inventory_registry.supplies.qty_in_bank`

### Expected Verification:

#### Report Text:

```markdown
## 📅 1 January 1905 · ⚓ New Winchester

**🗺 Region:** The Reach | **👤 Captain:** Sinclair | **🪙 Wallet:** 1000

* **🚂 Current Engine:** Spatchcock-Class Scout (Hold Slots Used: 6/12)
* **🎯 Ambition:** [Unreported] (Tier [Unreported]) — *Next Milestone: [Unreported]*

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS
| System          | Status     |
| :---            | :---       |
| **Crew:**       | 🟢 8 / 10  |
| **Hull:**       | 🟢 30 / 30 |
| **Terror:**     | 🟢 0 / 100 |
| **Nightmares:** | 🟢 0 / 4   |

---

## 📦 THE LOGISTICS CORE (Hold Inventory & Sourcing)
| Trade Good Name | Physical Hold | Hub Bank Stock | Active Sourcing Progress / Status | Destination Port |
| :---            | :---: | :---: | :---  | :---  |
| **🔥 Fuel**     |   3   |   0   |  🟢  |   —   |
| **📦 Supplies** |   3   |   0   |  🟢  |   —   |
```

#### JSON State:

```json
  {
    "meta.captain_name": "Sinclair",
    "meta.current_date_iso": "1905-01-01",
    "meta.sovereigns": 1000,
    "engine_status.current_locomotive": "Spatchcock-Class Scout",
    "engine_status.hull": 30,
    "engine_status.max_hull": 30,
    "unified_inventory_registry.fuel.qty_in_hold": 3,
    "unified_inventory_registry.fuel.qty_in_bank": 0,
    "unified_inventory_registry.supplies.qty_in_hold": 3,
    "unified_inventory_registry.supplies.qty_in_bank": 0
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
      "unified_inventory_registry": {
        "fuel": {
          "qty_in_hold": 5,
          "qty_in_bank": 0,
          "average_unit_cost": 0.00 
        },
        "supplies": {
          "qty_in_hold": 4,
          "qty_in_bank": 0,
          "average_unit_cost": 0.00 
        },
      },
      "active_action_stream": [],
      "completed_action_log": [],
      "route_planner": {},
      "discovered_ports": {}
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
      "unified_inventory_registry": {
        "fuel": {
          "qty_in_hold": 3,
          "qty_in_bank": 0,
          "average_unit_cost": 0.00 
        },
        "supplies": {
          "qty_in_hold": 3,
          "qty_in_bank": 0,
          "average_unit_cost": 0.00 
        },
        "bronzewood": {
          "qty_in_hold": 0,
          "qty_in_bank": 1,
          "average_unit_cost": 0.00 
        }
      },
      "active_action_stream": [],
      "completed_action_log": [],
      "route_planner": {},
      "discovered_ports": {}
    }
  }
```

#### JSON State Verification:
`meta.current_date_iso`  
`unified_inventory_registry.fuel.qty_in_hold`  
`unified_inventory_registry.supplies.qty_in_hold`  
`unified_inventory_registry.bronzewood.qty_in_hold`  
`unified_inventory_registry.bronzewood.qty_in_bank`  
`unified_inventory_registry.chorister_nectar.qty_in_hold`  
`unified_inventory_registry.chorister_nectar.qty_in_bank`  

---

### Expected Verification:

#### Report Text:

```
## 📦 THE LOGISTICS CORE (Hold Inventory & Sourcing)

| Trade Good Name | Physical Hold | Hub Bank Stock | Active Sourcing Progress | Destination Port |
| :---                 | :---: | :---: | :---  | :---  |
| **🔥 Fuel Barrels**  |   3   |   —   |  🟢  |   —   |
| **📦 Crew Rations**  |   3   |   —   |  🟢  |   —   |
| **Bronzewood**       |   0   |   5   |   —   |   —   |
| **Chorister Nectar** |   0   |   5   |   —   |   —   |
```

#### JSON State:

```json
{
"meta.current_date_iso": "1905-01-06",
"unified_inventory_registry.fuel.qty_in_hold": 3,
"unified_inventory_registry.supplies.qty_in_hold": 3,   
"unified_inventory_registry.bronzewood.qty_in_hold": 0,
"unified_inventory_registry.bronzewood.qty_in_hold"  : 5,
"unified_inventory_registry.chorister_nectar.bank": 0,
"unified_inventory_registry.chorister_nectar.qty_in_bank": 2  
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
      "meta": { "captain_name": "Sinclair", "current_region": "The Reach", "sovereigns": 880, "current_date_iso": "1905-01-05" },
      "engine_status": { "current_locomotive": "Spatchcock-Class Scout", "terror": 15, "nightmares": 0, "hull": 30, "max_hull": 30, "hold_capacity": 12 },
      "unified_inventory_registry": {
        "fuel": {
          "qty_in_hold": 3,
          "qty_in_bank": 0,
          "average_unit_cost": 0.00 
        },
        "supplies": {
          "qty_in_hold": 3,
          "qty_in_bank": 0,
          "average_unit_cost": 0.00 
        },
        "bronzewood": {
          "qty_in_hold": 1,
          "qty_in_bank": 0,
          "average_unit_cost": 0.00 
        },
        "quantum_æther_crystal": {
          "qty_in_hold": 1,
          "qty_in_bank": 0,
          "average_unit_cost": 100.00 
        }
      },
      "active_action_stream": [
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
    "meta": { "captain_name": "Sinclair", "current_region": "The Reach", "sovereigns": 880, "current_date_iso": "1905-01-05" },
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
      "active_action_stream": [],
      "completed_action_log": [],
      "route_planner": {},
      "discovered_ports": {}
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
| System          | Status       |
| :---            | :---         |
| **Crew:**       | 🟡 6 / 10    |
| **Hull:**       | 🟡 20 / 30   |
| **Terror:**     | 🟢 22 / 100  |
| **Nightmares:** | 🟢 0 / 4     |

**🚂 Current Engine:** Spatchcock-Class Scout (Hold Slots Used: 6/12)
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
      "meta": { "captain_name": "Sinclair", "current_region": "The Reach", "sovereigns": 880, "current_date_iso": "1905-01-05" },
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
      "unified_inventory_registry": {
        "fuel": {
          "qty_in_hold": 3,
          "qty_in_bank": 0,
          "average_unit_cost": 0.00 
        },
        "supplies": {
          "qty_in_hold": 3,
          "qty_in_bank": 0,
          "average_unit_cost": 0.00 
        },
      },
      "active_action_stream": [],
      "completed_action_log": [],
      "route_planner": {},
      "discovered_ports": {}
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
| System          | Status      |
| :---            | :---        |
| **Crew:**       | 🔴 3 / 10   |
| **Hull:**       | 🟡 20 / 30  |
| **Terror:**     | 🟢 35 / 100 |
| **Nightmares:** | 🟢 0 / 4    |

**🚂 Current Engine:** Spatchcock-Class Scout (Hold Slots Used: 6/12)
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
      "unified_inventory_registry": {
        "fuel": {
          "qty_in_hold": 3,
          "qty_in_bank": 0,
          "average_unit_cost": 0.00 
        },
        "supplies": {
          "qty_in_hold": 3,
          "qty_in_bank": 0,
          "average_unit_cost": 0.00 
        },
        "bronzewood": {
          "qty_in_hold": 2,
          "qty_in_bank": 0,
          "average_unit_cost": 0.00 
        },
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
      "completed_action_log": [],
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
        "unified_inventory_registry": {
          "fuel": {
            "qty_in_hold": 1,
            "qty_in_bank": 0,
            "average_unit_cost": 0.00 
          },
          "supplies": {
            "qty_in_hold": 1,
            "qty_in_bank": 0,
            "average_unit_cost": 0.00 
          },
        },
      "active_action_stream": [],
      "completed_action_log": [],
      "route_planner": {},
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

## Test Case 9: Cargo Isolation

### Objective
Check that quest and narrative items do not consume physical hold space. Verify creation of a polymorphic quest object in `active_action_stream`.

### Input Prompt
> Update state. Captain's log: 1905-01-15. We acquired two Tales of Terror out in the dark on that last run. We took on a quest from The Sequestered Scholar to deliver a Primordial Star Shard to Port Avon. Log this as "The Last Consignment.". Let's make sure our logistics files are updated before we cast off lines for Port Avon.

```json
{
  "dynamic_save_state": {
    "meta": {
      "captain_name": "Sinclair",
      "current_region": "The Reach",
      "sovereigns": 800,
      "current_date_iso": "1905-01-15"
    },
    "engine_status": {
      "current_locomotive": "Spatchcock-Class Scout",
      "terror": 10,
      "nightmares": 0,
      "hull": 30,    
      "max_hull": 30,
      "crew": 8,
      "max_crew": 10,
      "fuel_used_last_leg": 2,
      "hold_capacity": 12,
      "hidden_slots": 0,
      "hold_rules": {
        "fuel_reserve_minimum": 3,
        "supplies_reserve_minimum": 3,
        "discovery_buffer_slots": 2
      }
    },
    "unified_inventory_registry": {
      "fuel": { "qty_in_hold": 4, "qty_in_bank": 0, "average_unit_cost": 20.00 },
      "supplies": { "qty_in_hold": 4, "qty_in_bank": 0, "average_unit_cost": 40.00 },
      "approved_literature": { "qty_in_hold": 2, "qty_in_bank": 0, "average_unit_cost": 100.00 } 
    },
    "active_action_stream": [],
    "completed_action_log": [],
    "route_planner": {
      "last_updated_iso": "1905-01-15",
      "legs": []
    },
    "discovered_ports": {
      "The Reach": {}, "Albion": {}, "Eleutheria": {}, "The Blue Kingdom": {}
    }
  }
}
```

#### JSON State Verification:

`unified_inventory_registry.star_shard`
`active_action_stream[0]`

### Expected Verification:

> Output should note that we have quest actions at Port Avon. Quest and narrative items are noted, but not included in hold calculations or inventory.

#### Report Text: 

```markdown
# 🚂 CAPTAIN'S LOG 🚀

## 📅 15 January 1905 · ⚓ `New Winchester`

**🗺 Region:** `The Reach` | **👤 Captain:** `Sinclair` | **🪙 Wallet:** `800`

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS
| System          | Status      |
| :---            | :---        |
| **Crew:**       | 🟢 8 / 10   |
| **Hull:**       | 🟢 30 / 30  |
| **Terror:**     | 🟢 10 / 100 |
| **Nightmares:** | 🟢 0 / 4    |

**🚂 Current Engine:** `Spatchcock-Class Scout` `(Hold Slots Used: 10/12)`

**🎯 Ambition:** `[ Unreported ]` — *Next Milestone: [ Please report active campaign ambition ]*

---

## 📦 THE LOGISTICS CORE (Hold Inventory & Sourcing)

| Trade Good Name | Physical Hold | Hub Bank Stock | Active Sourcing Progress | Destination Port |
| :---                    | :---: | :---: | :---  | :---  |
| **🔥 Fuel Barrels**    |   4   |   —   |  🟢  |   —   |
| **📦 Crew Rations**    |   4   |   —   |  🟢  |   —   |
| **Approved Literature** |   2   |   —   |   —   |   —   
```

---

#### JSON State: 

```json
{
  "unified_inventory_registry.star_shard": null,
  "active_action_stream[0]": 
  {
    "id":"ACT-1099",
    "type":"quest",
    "port":"Port Avon",
    "region":"The Reach",
    "date_added_iso":"1905-01-15",
    "deadline_date_iso":null,
    "title":"The Last Consignment",
    "notes":"Ferrying the recovered components.",
    "is_hidden_transit_item":true,
    "payload":{
      "questline_name":"The Dawn Machine Legacy",
      "npc_or_faction":"The Sequestered Scholar",
      "current_step_number":1,
      "quest_pattern":"fetch",
      "items_manifest":[
        {
          "good_key":"primordial_star_shard",
          "quantity_required":1,"quantity_delivered":0
        }
      ]
    }
  }
}
```

---
