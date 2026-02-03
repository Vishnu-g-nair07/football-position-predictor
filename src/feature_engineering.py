import pandas as pd

def build_team_table(df, upto_matchweek):
    df = df[df['matchweek'] <= upto_matchweek]

    teams = pd.unique(df[['home_team', 'away_team']].values.ravel())

    data = []
    for team in teams:
        played = df[(df.home_team == team) | (df.away_team == team)]

        points = 0
        goals_for = 0
        goals_against = 0

        for _, r in played.iterrows():
            if r.home_team == team:
                gf, ga = r.home_goals, r.away_goals
            else:
                gf, ga = r.away_goals, r.home_goals

            goals_for += gf
            goals_against += ga

            if gf > ga:
                points += 3
            elif gf == ga:
                points += 1

        matches = len(played)
        goal_diff = goals_for - goals_against

        data.append([team, matches, points, goals_for, goals_against, goal_diff])

    cols = ['team', 'matches', 'points', 'goals_for', 'goals_against', 'goal_diff']
    df_result = pd.DataFrame(data, columns=cols)
    return df_result
