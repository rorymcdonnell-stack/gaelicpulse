# PULSE/26 - Football Data Backbone

Generated: 2026-07-01

**27 county files, 121 game records, 121 fully reconciled (zero gaps).**

Every scorer tally traces to a named primary source; all margins and cross-file checks clean.

## Complete (27)

| County file | Games | Reconciled |
|---|---|---|
| antrim-football-2026_verified.json | 4 | 4/4 |
| armagh-football-2026_verified.json | 7 | 7/7 |
| carlow-football-2026_verified.json | 3 | 3/3 |
| cavan-football-2026_verified.json | 3 | 3/3 |
| clare-football-2026_verified.json | 3 | 3/3 |
| cork-football-2026_verified.json | 6 | 6/6 |
| derry-football-2026_verified.json | 4 | 4/4 |
| donegal-football-2026_verified.json | 4 | 4/4 |
| fermanagh-football-2026_verified.json | 6 | 6/6 |
| galway-football-2026_verified.json | 4 | 4/4 |
| kildare-football-2026_verified.json | 4 | 4/4 |
| laois-football-2026_verified.json | 5 | 5/5 |
| leitrim-football-2026_verified.json | 5 | 5/5 |
| limerick-football-2026_verified.json | 3 | 3/3 |
| london-football-2026_verified.json | 4 | 4/4 |
| longford-football-2026_verified.json | 4 | 4/4 |
| meath-football-2026_verified.json | 4 | 4/4 |
| monaghan-football-2026_verified.json | 7 | 7/7 |
| new-york-football-2026_verified.json | 2 | 2/2 |
| offaly-football-2026_verified.json | 5 | 5/5 |
| roscommon-football-2026_verified.json | 5 | 5/5 |
| sligo-football-2026_verified.json | 5 | 5/5 |
| tipperary-football-2026_verified.json | 5 | 5/5 |
| tyrone-football-2026_verified.json | 4 | 4/4 |
| waterford-football-2026_verified.json | 3 | 3/3 |
| westmeath-football-2026_verified.json | 7 | 7/7 |
| wexford-football-2026_verified.json | 5 | 5/5 |

## Held - build after finals (6)

Kerry, Dublin, Mayo, Louth - after Sam Maguire semis (Kerry v Dublin, Mayo v Louth)

Down, Wicklow - after Tailteann Cup final, 11 July

Opponent-side scorer data for these six is pre-cached in held_scorer_cache.json (16 entries).

## Tooling

- tools/setsc.py - scorer writer; refuses any list that does not sum exactly to the team score
- tools/audit.py - margin, cross-file, and scorer-sum integrity checker
