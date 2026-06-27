## Test Case #: Test Title

### Objective
[ State objective ]

### Input Prompt
> Update state. [ Input prompt text ]

```json
{
    "dynamic_save_state": {
        "meta": {
            "captain_name": "Sinclair",
            "current_region": "The Reach",
            "sovereigns": 1000,
            "current_date_iso": "1905-02-18"
        },
        "crew_stats": {},
        "officer_manifest": {},
        "engine_status": {
            "current_locomotive": "Spatchcock-Class Scout",
            "terror": 12,
            "nightmares": 0,
            "hull": 30,
            "max_hull": 30,
            "crew": 10,
            "max_crew": 10,
            "hold_capacity": 12
        },
        "unified_inventory_registry": {
            "fuel": {
                "qty_in_hold": 3,
                "qty_in_bank": 0,
                "average_unit_cost": 20.00 
            },
                "supplies": {
                "qty_in_hold": 3,
                "qty_in_bank": 0,
                "average_unit_cost": 40.00 
            },
        },
        "possessions":{},
        "active_action_stream": [],
        "completed_action_log": [],
        "route_planner": {},
        "discovered_ports": {}
    }
}
```

#### JSON State Verification:

[ List the keys to print out for verification ]
`path.to.example.key`

### Expected Verification:

#### JSON State: 
```json
{
  "__NOTE":"list verification keys here in a flat json object (dot notation, not nested)"
}
```

#### Report Text: 

> [ Relevant report output ]

---
