# Football Position Predictor

This project predicts football league table positions at a future matchweek based on:

- Historical match results up to a current matchweek
- Upcoming fixtures from the current matchweek to the target matchweek
- Simple heuristic model predicting match outcomes from current team strength

## How to use

1. Clone the repo
2. Prepare your data files:
   - `data/matches.csv` with historical results (MW 1 to current)
   - `data/fixtures.csv` with fixture list for upcoming matches
3. Create and activate a virtual environment:
