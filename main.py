from src.utils import load_data
from src.feature_engineering import build_team_table
from src.fixtures import load_fixtures, predict_fixture_results
import pandas as pd

def main():
    MATCHWEEK_CURRENT = 24
    MATCHWEEK_PREDICT = 38

    df_matches = load_data('data/matches.csv')
    current_stats = build_team_table(df_matches, upto_matchweek=MATCHWEEK_CURRENT)
    df_fixtures = load_fixtures('data/fixtures.csv')

    possible_mw_cols = ['matchweek', 'week', 'gw', 'round', 'GameWeek', 'GW']
    mw_col = None
    for col in possible_mw_cols:
        if col in df_fixtures.columns:
            mw_col = col
            break

    if mw_col is None:
        raise Exception(f"No matchweek column found in fixtures.csv. Found columns: {df_fixtures.columns}")

    print(f"Using fixture matchweek column: {mw_col}")

    df_fixtures[mw_col] = (
        df_fixtures[mw_col]
        .astype(str)
        .str.extract(r'(\d+)')[0]
    )

    df_fixtures[mw_col] = pd.to_numeric(df_fixtures[mw_col], errors='coerce')
    df_fixtures = df_fixtures.dropna(subset=[mw_col])
    df_fixtures[mw_col] = df_fixtures[mw_col].astype(int)

    future_fixtures = df_fixtures[
        (df_fixtures[mw_col] > MATCHWEEK_CURRENT) &
        (df_fixtures[mw_col] <= MATCHWEEK_PREDICT)
    ]

    print(f"Future fixtures used: {len(future_fixtures)} matches")

    expected_points_df = predict_fixture_results(future_fixtures, current_stats)

    merged = pd.merge(current_stats, expected_points_df, on='team', how='left')
    merged['expected_points_from_fixtures'].fillna(0, inplace=True)

    merged['total_predicted_points'] = merged['points'] + merged['expected_points_from_fixtures']

    predicted_table = merged.sort_values(
        by=['total_predicted_points', 'goal_diff', 'goals_for'],
        ascending=False
    ).reset_index(drop=True)

    predicted_table['predicted_position'] = predicted_table.index + 1

    predicted_table.to_csv('outputs/predicted_table_mw38.csv', index=False)

    print("\n=== Predicted League Table at Matchweek 38 ===\n")
    print(predicted_table[['predicted_position', 'team', 'total_predicted_points', 'goal_diff', 'goals_for']])

if __name__ == "__main__":
    main()
