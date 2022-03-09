# create different subsets of islands that might be interesting to analyse

import pandas as pd


# import the data
# ---

dir_out = '../../data/processed/island_subsets/'

df_group = pd.read_csv('../../data/processed/island_group_membership.csv')
df_src = pd.read_csv('../../data/processed/island_data_source.csv')


# Create subsets
# ---

# all
df_sub = pd.DataFrame( df_group['island_name'] )
df_sub.to_csv(dir_out + 'all.csv', index=False)

# Riau only
df_sub = pd.DataFrame( df_group[df_group['group_name'] == 'riau_bangka_belitung']['island_name'] )
df_sub.to_csv(dir_out + 'riau_only.csv', index=False)

# Peninsula only
df_sub = pd.DataFrame( df_group[df_group['group_name'] == 'peninsula']['island_name'] )
df_sub.to_csv(dir_out + 'peninsula_only.csv', index=False)


# Surveys only
df_sub = pd.DataFrame( df_src[df_src['data_source'] == 'survey']['island_name'] )
df_sub.to_csv(dir_out + 'survey_only.csv', index=False)

'''
# import the data
# ---

dir_out = '../../data/processed/island_subsets/'

df = pd.read_csv('../../data/raw/island_properties.csv') # columns: Island Name,Island Group,Area (m^2),Data Source


# Certain archipelagos only
# ---

# Riau-Lingga only
df_sub = pd.DataFrame( df[df['Island Group'] == 'Riau-Lingga']['Island Name'] )
df_sub.to_csv(dir_out + 'riau_lingga_only.csv', index=False)

# Peninsula West only
df_sub = pd.DataFrame( df[df['Island Group'] == 'Peninsula West']['Island Name'] )
df_sub.to_csv(dir_out + 'pen_west_only.csv', index=False)

# Singapore only
df_sub = pd.DataFrame( df[df['Island Group'] == 'Singapore']['Island Name'] )
df_sub.to_csv(dir_out + 'singapore_only.csv', index=False)


# Surveys only
# ---

df_sub = pd.DataFrame( df[df['Data Source'] == 'Survey']['Island Name'] )
df_sub.to_csv(dir_out + 'survey_only.csv', index=False)

'''
