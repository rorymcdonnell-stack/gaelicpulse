# Gaelic Pulse — PULSE/26 Data Contract (v2)

**This supersedes v1.** As of the July 2026 data refresh, the single source of
truth for all PULSE/26 championship data is the master workbook:

    PULSE26_MASTER.xlsx  ·  sheet: "Master Fixtures"

There are **no canonical JSON county files** any more. The book pipeline reads
the workbook directly through the `pulse_data.py` access layer. One source of
truth, visible and editable, with no JSON-vs-spreadsheet drift.

---

## Two rules above all (unchanged)

1. **Every fact traces to a named primary source.** If a value cannot be found
   in a primary source, the cell is left blank — **never guessed**. A blank
   attendance is honest; a fabricated one is not.
2. **Facts and signals are separate.** Results, scorers, referees, attendances,
   venues = facts. Editorial observation and "watch" items live only in the
   book's prose layer, never in the data.

---

## The master table — "Master Fixtures"

One row per unique game. Columns:

| Column | Meaning | Completeness (Jul 2026) |
|---|---|---|
| `#` | Row index | — |
| `Date` | ISO date `YYYY-MM-DD` | all games |
| `Competition` | e.g. `Ulster SFC`, `All-Ireland SFC`, `Tailteann Cup` | all games |
| `Round` | e.g. `Round 1`, `Quarter-Final`, `Final` | all games |
| `Venue` | Ground name | all games |
| `Team A` | First county (the recorded/home-ish side) | all games |
| `Score A` | Team A score, goals-points `2-20` | all games |
| `Team B` | Opponent | all games |
| `Score B` | Team B score | all games |
| `2pt A` / `2pt B` | Count of two-point scores each side | all games |
| `AET` | `Yes` if after extra time | as applicable |
| `Referee` | Referee, county in brackets where known | **all games** |
| `Attendance` | Reported attendance | reported games only |
| `Team A Scorers` | `Player G-P (notes); …` reconciled to Score A | all games |
| `Team B Scorers` | `Player G-P (notes); …` reconciled to Score B | all games |
| `Both Sides?` | `Yes` when both scorer lists present | — |
| `Source` | Named primary source(s), links where available | all games |
| `Notes` | Editorial/context notes, corrections + provenance | as needed |

### Scorer string format

    Player Name G-P (optional notes); Player Name G-P; …

Examples:

    Michael Langan 0-5; Oisín Gallen 0-5; Ciarán Moore 1-1
    David Clifford 0-04 (1tp, 0-01f); Tony Brosnan 0-04 (2tp)

Parenthetical notes may record two-pointers (`tp`/`2pt`), frees (`f`), and match
detail. The `pulse_data.py` parser extracts name, goals, points, and note; each
side's tallies **must** sum exactly to that side's score.

---

## Data discipline (enforced by `pulse_data.verify()`)

- Every side's scorer tallies sum exactly to that side's score. Zero tolerance.
- Referee present on every played game.
- Attendance present where reported; blank (not zero, not guessed) where not.
- Corrections carry their provenance in `Notes` (e.g. a fixed date names the
  source that resolved it).

---

## Structural completeness (verified Jul 2026)

Provincial championships reconcile to the 2026 format **including byes**:
Ulster 8 · Leinster 8 (byes) · Munster 5 · Connacht 6.
All-Ireland and Tailteann rounds reconcile to the double-elimination structure.

**Calendar-gated remainder:** the two Sam Maguire semi-finals, the Sam Maguire
final, and the Tailteann Cup final (11 July). The six held counties — Kerry,
Dublin, Mayo, Louth, Down, Wicklow — gain their remaining rows as those games
are played and recorded.

---

## Reading the data (for any pipeline)

    import pulse_data as pd
    games = pd.load_master()          # list[Game], straight from the workbook
    pd.verify(games)                  # reconciliation report
    pd.games_for_county(games, 'Armagh')
    pd.all_scorers(games)

No pipeline reads the spreadsheet format directly. `pulse_data.py` is the only
module that knows the column layout; everything else consumes structured
`Game`/`Scorer` objects. Change the workbook, and every output follows.
