import pandas as pd


def predict_table(model, features_df):
    X = features_df[['matches','points','goals_for','goals_against','goal_diff']]
    features_df['predicted_points'] = model.predict(X)


    table = features_df.sort_values(
    by=['predicted_points','goal_diff','goals_for'],
    ascending=False
    ).reset_index(drop=True)


    table['predicted_position'] = table.index + 1
    return table