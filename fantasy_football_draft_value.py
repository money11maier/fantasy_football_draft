import pandas as pd

# define our functions
# we need to update the fantasy points column
# offense functions


def update_fantasy_points(df):
    df['FantasyPoints'] = (df['PassingYards'] * offensive_fantasy_points['PassingYards']) + (df['PassingTouchdowns'] * offensive_fantasy_points['PassingTd']) + (df['RushingYards'] * offensive_fantasy_points['RushingYards']) + (df['RushingTouchdowns'] * offensive_fantasy_points['RushingTd']) + (
        df['Receptions'] * offensive_fantasy_points['Receptions']) + (df['ReceivingYards'] * offensive_fantasy_points['ReceivingYards']) + (df['ReceivingTouchdowns'] * offensive_fantasy_points['ReceivingTd']) + (df['PassingInterceptions'] * offensive_fantasy_points['Interceptions'])

# this is used to split each year into the different positions


def split_position(df, position):
    # need to pass in a dataframe and a position. Dataframe needs at least 2 columns: Position, FantasyPoints
    temp = df.loc[df['Position'] == position]
    temp = temp.sort_values(by='FantasyPoints', ascending=False)
    temp = temp.reset_index(drop=True)
    temp = temp[['Position', 'FantasyPoints']]
    # print(temp)
    season_by_position.append(temp)


# now we merge the different years by position so we end up with 4 years of a position in one df
# also including the pos_merged empty df here so they aren't forgotten later.
qb_merged = None
rb_merged = None
wr_merged = None
te_merged = None
def_merged = None


def position_merges(position, positon_merged):
    positon_merged = position[0].join(position[1], how='outer', rsuffix='_1')
    positon_merged = positon_merged.join(
        position[2], how='outer', rsuffix='_2')
    positon_merged = positon_merged.join(
        position[3], how='outer', rsuffix='_3')
    positon_merged = positon_merged.drop(
        ['Position_1', 'Position_2', 'Position_3'], axis=1)
    positon_merged['Position'] = positon_merged['Position'].fillna(0)
    positon_merged['FantasyPoints'] = positon_merged['FantasyPoints'].fillna(0)
    positon_merged['FantasyPoints_1'] = positon_merged['FantasyPoints_1'].fillna(
        0)
    positon_merged['FantasyPoints_2'] = positon_merged['FantasyPoints_2'].fillna(
        0)
    positon_merged['Average'] = (positon_merged['FantasyPoints'] + positon_merged['FantasyPoints_1'] +
                                 positon_merged['FantasyPoints_2'] + positon_merged['FantasyPoints_3']) / 4
    positon_merged = positon_merged[['Position', 'Average']]
    return positon_merged

# now we get our positional values


def position_values(merged_df, pos_start, pos_roster):
    pos_total = pos_roster * teams
    pos_starters = pos_start * teams
    pos_sub = int(((pos_total - pos_starters) / 2) + pos_starters)
    pos_elite = int(pos_starters / 2)
    merged_df['Roster'] = merged_df['Average'] - merged_df.iat[pos_total, 1]
    merged_df['Sub'] = merged_df['Average'] - merged_df.iat[pos_sub, 1]
    merged_df['Starter'] = merged_df['Average'] - \
        merged_df.iat[pos_starters, 1]
    merged_df['Elite'] = merged_df['Average'] - merged_df.iat[pos_elite, 1]
    zero = merged_df._get_numeric_data()
    zero[zero < 0] = 0
    merged_df['TotalValue'] = merged_df['Roster'] + \
        merged_df['Sub'] + merged_df['Starter'] + merged_df['Elite']

# defensive functions
# get defensive fantasy points


def defense_fp_update(df):
    df['FantasyPoints'] = (df['Sacks'] * defense_fantasy_points['Sack']) + (df['Interceptions'] * defense_fantasy_points['Interceptions']) + (df['FumblesRecovered'] * defense_fantasy_points['Fumbles']
                                                                                                                                              ) + (df['Safeties'] * defense_fantasy_points['Safety']) + ((df['DefensiveTouchdowns'] + df['SpecialTeamsTouchdowns']) * defense_fantasy_points['Touchdowns'])

# sort the fantasy points and then output to a list


def sort_defense(df):
    # need to pass in a dataframe and a position. Dataframe needs at least 2 columns: Position, FantasyPoints
    temp = df.loc[df['Position'] == 'DST']
    temp = temp.sort_values(by='FantasyPoints', ascending=False)
    temp = temp.reset_index(drop=True)
    temp = temp[['Position', 'FantasyPoints']]
    # print(temp)
    season_defense.append(temp)
