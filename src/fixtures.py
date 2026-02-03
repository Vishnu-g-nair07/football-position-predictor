import pandas as pd

def load_fixtures(path):
    return pd.read_csv(path)

def predict_fixture_results(fixtures_df, current_stats_df):
    points_map = dict(zip(current_stats_df['team'], current_stats_df['points']))
    pred_points = {team: 0 for team in current_stats_df['team']}

    for _, row in fixtures_df.iterrows():
        home = row['home_team']
        away = row['away_team']
        home_points = points_map.get(home, 0)
        away_points = points_map.get(away, 0)

        # Simple heuristic: team with higher points expected to win
        if home_points > away_points:
            pred_points[home] += 3
        elif home_points < away_points:
            pred_points[away] += 3
        else:
            pred_points[home] += 1
            pred_points[away] += 1

    pred_points_df = pd.DataFrame(list(pred_points.items()), columns=['team', 'expected_points_from_fixtures'])
    return pred_points_df
