# Getting the data and manipulating it
import pandas as pd
import sklearn.model_selection
from Web_scrape import all_fighter_df, ft_to_cm, inch_to_cm, str_to_int_convers, most_recent_event
from Packages import *

# Null Value Function. Basically takes index, figures out if even, drops that specific row and their opponent.

def even_or_odd_index(null_df_fighter, df):
    for i in null_df_fighter.index:
        df = df.drop(index=i)
        if i % 2 != 0:
            df = df.drop(index = i - 1)
        elif i % 2 == 0:
            df = df.drop(index = i + 1)
    return df

def normalization_minmax(df):
    df = (df - min(df)) / (max(df) - min(df))
    return df

# Creating the test and training sets for the KNN model

raw_data = pd.read_csv('C:/Users/t0ys0r/OneDrive/Desktop/UFC Model/Data_for_model_no_organization.csv').dropna()\
    .drop(columns=['Winner','Stance','Fighter'])

y = pd.DataFrame(raw_data['Winner_binary'])
X = raw_data.drop(columns='Winner_binary')

X['Reach'] = normalization_minmax(X['Reach'])
X['Ht.'] = normalization_minmax(X['Ht.'])
X['L'] = normalization_minmax(X['L'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.05, random_state = 0, shuffle = False)

event_fighter_names = most_recent_event[0]
event_fighter_names = pd.DataFrame(event_fighter_names['Fighter'].str.split('  ', 1, expand = True).stack().\
    reset_index(level=1, drop=True))
event_fighter_names[['First', 'Last']] = event_fighter_names[0].str.split(' ', 1, expand = True)
event_fighter_names = event_fighter_names[['First', 'Last']]

columns = ['Fighter', 'W/L', 'Kd',
           'Str', 'Td', 'Sub', 'Weight class',
           'Method', 'Round', 'Time']

# Manipulating the webscraping dataframe. This is used for the real life test

null_number = 100000000
all_fighter_df = all_fighter_df.fillna(null_number)
all_fighter_df = all_fighter_df[all_fighter_df.First != null_number].drop(columns = ['Nickname', 'Wt.', 'Belt',
                                                                                     'W', 'D'])

all_fighter_df['Stance_Orth'] = all_fighter_df.apply(lambda x: x['Stance'] == 'Orthodox', axis = 1)
all_fighter_df['Stance_South'] = all_fighter_df.apply(lambda x: x['Stance'] == 'Southpaw', axis = 1)
all_fighter_df['Stance_Switch'] = all_fighter_df.apply(lambda x: x['Stance'] == 'Switch', axis = 1)

all_fighter_df['Stance_Orth'] = all_fighter_df['Stance_Orth'].replace([True, False], [1,0])
all_fighter_df['Stance_South'] = all_fighter_df['Stance_South'].replace([True, False], [1,0])
all_fighter_df['Stance_Switch'] = all_fighter_df['Stance_Switch'].replace([True, False], [1,0])
all_fighter_df = all_fighter_df.drop(columns = 'Stance')

# MAKE THIS INTO A FUNCTION BASED ON INPUT
# fighter_1_row = all_fighter_df.loc[(all_fighter_df['First'] == 'Jorge') & (all_fighter_df['Last'] == 'Masvidal')]

all_fighter_df['Ht.'] = all_fighter_df['Ht.'].replace("\'", '', regex = True).replace('"', '', regex = True).replace(
    ' ', '', regex = True).replace('--', '', regex = True)
all_fighter_df = all_fighter_df[all_fighter_df['Ht.'] != '']
all_fighter_df = all_fighter_df[all_fighter_df['Reach'] != '--']

# need a boolean statement for the concat. This is because if you do .str[2], not every fighter has an inch reach of
# greater than 9 --> Probably use len(1) [basically if len(str[1 + 2]) = 2 then use that, if it's np.nan then use str[1]

# Converting the height to cm. This splits the string up in ft & inches to cm then sums both
all_fighter_df['Ht.inch_0'] = all_fighter_df['Ht.'].str[0]
all_fighter_df['Ht.inch_1'] = all_fighter_df['Ht.'].str[1]
all_fighter_df['Ht.inch_2'] = all_fighter_df['Ht.'].str[2]
all_fighter_df = all_fighter_df.fillna('')
all_fighter_df['Ht.inch_0'] = all_fighter_df['Ht.inch_0']
all_fighter_df['Ht.inch_1'] = all_fighter_df['Ht.inch_1']
all_fighter_df['Ht.inch_2'] = all_fighter_df['Ht.inch_2']
all_fighter_df['Ht.inch_3'] = all_fighter_df['Ht.inch_1'] + all_fighter_df['Ht.inch_2']
all_fighter_df['Ht.inch_1'] = all_fighter_df['Ht.inch_3']
all_fighter_df['Ht.inch_0'] = ft_to_cm(str_to_int_convers(all_fighter_df['Ht.inch_0']))
all_fighter_df['Ht.inch_1'] = inch_to_cm(str_to_int_convers(all_fighter_df['Ht.inch_1']))
all_fighter_df['Ht.'] = all_fighter_df['Ht.inch_1'] + all_fighter_df['Ht.inch_0']
all_fighter_df = all_fighter_df.drop(columns=['Ht.inch_3', 'Ht.inch_2', 'Ht.inch_1', 'Ht.inch_0'])

# Converting the reach to cm. This splits the string up in inches to cm then sums both

all_fighter_df['Reach'] = all_fighter_df['Reach'].replace('"','', regex = True)
all_fighter_df['Reach'] = inch_to_cm(str_to_int_convers(all_fighter_df['Reach']))
# The dataframe you're gonna use for the model (depending on who you're picking)
real_test_set = pd.merge(all_fighter_df, event_fighter_names, how = 'right', on = ['First','Last'])
Null_fighter_information = real_test_set[real_test_set.isna().any(axis=1)]

Null_fighter_information = Null_fighter_information.drop(columns=['Ht.', 'Reach', 'L', 'Stance_Orth',
                                                                  'Stance_South', 'Stance_Switch'])

#.index[0]
# Null_fighter_information['index'] = Null_fighter_information[[]].index


real_test_set = even_or_odd_index(Null_fighter_information, real_test_set)

export_dataframe = real_test_set[['First', 'Last']]
export_dataframe.columns = ['First', 'Last']
real_test_set = real_test_set.drop(columns = ['First','Last'])

real_test_set = real_test_set[['L', 'Stance_Orth', 'Stance_South', 'Stance_Switch','Ht.', 'Reach']]
real_test_set['Reach'] = normalization_minmax(real_test_set['Reach'])
real_test_set['Ht.'] = normalization_minmax(real_test_set['Ht.'])
real_test_set['L'] = normalization_minmax(real_test_set['L'])

# need to figure out how to get the row you're looking for. Basically, I want it to go over the list of fighters and pull their information out
# try putting the list of names in the same dataframe as the all_fighter_df and comparing it then.
