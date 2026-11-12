<!--
Sunless Skies First Mate Logbook Template
Version 1.0.1
Data Package Compatibility: 1.1.2
-->

# 🚂 CAPTAIN'S LOG 🚀

## 📅 [DATE] (Day [current_epoch]) · ⚓ [last_location_visited_key.display_name]

**🗺️ Region:** [last_location_visited_key.region.display_label] | **👤 Captain:** [captain_name] | **🪙 Wallet:** [sovereigns] Sovereigns

**🚂 Current Engine:** [vessel_name] ([model])

---

## ⚙️ VESSEL SYSTEMS & RECOVERY STATUS
| System          | Status                                   |
| :---            | :---                                     |
| **Crew:**       | [🟢/🟡/🔴] [current_crew] / [max_crew]  |
| **Hull:**       | [🟢/🟡/🔴] [current_hull] / [max_hull]  |
| **Terror:**     | [🟢/🟡/🔴] [terror] / 100               |
| **Nightmares:** | [🟢/🟡/🔴] [nightmares] / 4             |

## 🔮 VESSEL APTITUDE & STAT BALANCES

| 📐 SKILLS           | Base                   | Perks     | Total     |
| :---                | :---:                  | :---:     | :---:     |
| - 👊 Iron           | [ skill_iron ]         | [ +Perk ] | **[ T ]** |
| - 👁️ Mirrors        | [ skill_mirrors ]      | [ +Perk ] | **[ T ]** |
| - ❤️ Hearts         | [ skill_hearts ]       | [ +Perk ] | **[ T ]** |
| - 🎭 Veils          | [ skill_veils ]        | [ +Perk ] | **[ T ]** |
| 🔍 **AFFILIATIONS** | **Base**               | **Perks** | **Total** |
| - 🔍 Academe        | [ affiliation_academe ]| [ +Perk ] | **[ T ]** |
| - 🍷 Bohemia        | [ affiliation_bohemia ]| [ +Perk ] | **[ T ]** |
| - 👑 Establishment  | [ affiliation_establishment ] | [ +Perk ] | **[ T ]** |
| - 🎩 Villainy       | [ affiliation_villainy ]| [ +Perk ] | **[ T ]** |

---

## 🗺️ OPERATIONS & TRANSIT

**🎯 Ambition:** [Ambition Root Wrapper `title`] ([Ambition Root Wrapper `notes`]) — *Current Focus: [Active Ambition Subtask `title`]*

📋 **Executive Officer's Counsel ([first_mate_name] — Concept of Maneuver):**
> [Tactical Concept of Maneuver: routing rationale, fuel/supply burn projections across upcoming legs, resupply bottlenecks, bazaar arbitrage or contract expirations, and staleness reminders for open actions.]

### 🧭 Active Trajectory:
<!--
Resupply Badges per waypoint (evaluated via Ref_Location_Goods for that location_key, or its parent waypoint_location_key):
🟢 = Full Resupply (exports BOTH `fuel` and `supplies`)
🟡 = Partial Resupply (exports EITHER `fuel` OR `supplies`)
🔴 = No Resupply (exports NEITHER `fuel` NOR `supplies`)
-->
⚓ [last_location_visited_key.display_name] ➔ [🟢/🟡/🔴] **[itinerary[1].display_name]** ➔ [🟢/🟡/🔴] [itinerary[2].display_name] ➔ [🟢/🟡/🔴] [itinerary[n].display_name]

<!--
ITINERARY STOP BLOCKS:
Replicate the `### ➡️ STOP [sequence_order]: [PORT_DISPLAY_NAME]` block below for each waypoint in `State_Navigation_Itinerary` (in sequence_order 1..n) that has active/ready/blocked actions.
- Only include bullet types that have an active/ready/blocked record at that stop.
- Priority Indicator prefix: `‼️ ` for `high`, omit for `routine`, `🔻 ` for `low`.
- Include `🎯 AMBITION:` ONLY if an active/ready/blocked Ambition child subtask (`ACT-XXXX.YY`) resolves at this stop.
- Include `💼 SECONDMENT READY:` ONLY if a seconded officer at this stop has `action_status == 'ready'` (or unlocks upon arrival at this stop: `current_epoch + sequence_order >= deadline_epoch`).
-->
### ➡️ STOP [sequence_order]: [itinerary_location.display_name]
* `[Priority]`🎯 **AMBITION:** [Subtask `title`] (`[action_id]`) — [Subtask `notes` / Quota: `quantity_delivered`/`quantity_required` `target_entity_key`]
* `[Priority]`🔑 **PROSPECT:** [Prospect `title`] (`[action_id]`) — Deliver [quantity_required - quantity_delivered] [target_entity_key.display_name] ([`action_status`])
* `[Priority]`📖 **QUEST:** [Root Wrapper `title`] — Step [.YY]: [Subtask `title`] (`[action_id]`) — [Subtask `notes`]
* `[Priority]`👤 **OFFICER STORY:** [target_entity_key.lexical_name] (`[action_id]`) — [Subtask/Action `title`] — [Subtask/Action `notes`]
* `[Priority]`💼 **SECONDMENT READY:** Reclaim **[target_entity_key.lexical_name]** (`[action_id]`) — Outcome: [Action `notes`]
* `[Priority]`📌 **TODO:** [Action `title`] (`[action_id]`) — [Action `notes`]

<!--
OPTIONAL PINNED OFF-ROUTE BLOCK:
Render ONLY if there are actions with `is_pinned == TRUE` whose `target_location_key` is NOT on the current `State_Navigation_Itinerary`. Suppress otherwise.
-->
### 📌 PINNED OBJECTIVES (OFF-ITINERARY)
* `[Priority]`**[action_type]**: [Action `title`] (`[action_id]`) at **[target_location_key.display_name]** — [Action `notes`]

<!--
ACTIVE PASSENGERS:
Render continuously while any `action_type == 'passenger'` has `action_status == 'active'`. Suppress if no passengers are aboard.
-->
### 👤 ACTIVE PASSENGERS & BERTH TRANSIT
* **[Action `title`] (`[action_id]`)** ➔ Bound for: **[target_location_key.display_name]** ([target_location_key.region.display_label]) — Notes: *[notes]* — Timeline: [created_epoch Date] ➔ [deadline_epoch Date / Open Timeline]

---

## 📦 LOGISTICS

<!--
Render `| **🗝️ Hidden Hold Utilization:** [CONTRABAND_HIDDEN] / [hidden_slots]` ONLY when `State_Scalars.hidden_slots > 0`. Suppress when `hidden_slots == 0`.
-->
**📦 Hold Utilization:** [STANDARD_HOLD_USED] / [hold_capacity] | **🗝️ Hidden Hold Utilization:** [CONTRABAND_HIDDEN] / [hidden_slots]

| Trade Good Name | Physical Hold (`hold_qty`) | Hub Bank (`bank_qty`) | Unit Cost (`MAC`) | Status / Earmark | Destination Port |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **🔥 Barrel of Fuel** | [hold_qty] | [bank_qty] | [average_unit_cost] | [🟢/⚠️/🚨 Reserve Status] | — |
| **📦 Crate of Supplies** | [hold_qty] | [bank_qty] | [average_unit_cost] | [🟢/⚠️/🚨 Reserve Status] | — |
| **[good_key.display_name]** | [hold_qty] | [bank_qty] | [average_unit_cost] | [Earmarked for `[action_id]`: [Action `title`] ([allocated_hold_qty]/[rem_req]) (join multiple with `; `) / `Unassigned Cargo`] | [target_location_key.display_name (join multiple with `; `) / —] |

---

## 🛞 BRIDGE ROSTER

| Station                   | Active Officer                          | Skill Perks                  | Affiliation Perks                  |
| :---                      | :---                                    | :---                         | :---                               |
| ⚓ **First Officer**      | [ lexical_name / 🔘 Vacant ]            | [ +X Skill / -Y Skill / — ]  | [ +Z Affiliation / — ]             |
| 🛞 **Quartermaster**      | [ lexical_name / 🔘 Vacant ]            | [ +X Skill / -Y Skill / — ]  | [ +Z Affiliation / — ]             |
| 🏮 **Signaller**          | [ lexical_name / 🔘 Vacant ]            | [ +X Skill / -Y Skill / — ]  | [ +Z Affiliation / — ]             |
| ⚙️ **Chief Engineer**     | [ lexical_name / 🔘 Vacant ]            | [ +X Skill / -Y Skill / — ]  | [ +Z Affiliation / — ]             |
| 🐶 **Mascot**             | [ lexical_name / 🔘 Vacant ]            | [ +X Skill / -Y Skill / — ]  | [ +Z Affiliation / — ]             |

<!--
SECONDMENT OUTLOOK:
Join `State_Officers` (`officer_status == 'seconded'`) with active `State_Action` (`action_type == 'secondment'`).
Suppress this entire `### ⏳ SECONDMENT OUTLOOK` sub-section if no officers currently have `officer_status == 'seconded'`.
-->
### ⏳ SECONDMENT OUTLOOK
* **[target_entity_key.lexical_name]** ([position_slot.display_label]) ➔ Ashore at **[target_location_key.display_name]** (`[action_id]`)
  * *Status:* [🔒 **Working Ashore** (Unlocks: [deadline_epoch Date] · Day [deadline_epoch]) / 🟢 **Ready for Pickup** (Unlocked: [deadline_epoch Date])]
  * *Assignment & Expected Outcome:* [Action `notes`]

  ---

*Respectfully submitted,*  

### 🪶 **_[first_mate_name]_**

*Executive Officer, [vessel_name]*

⚜️ ─── ✦ 🧭 ۞ ⚓ ✦ ─── ⚜️
