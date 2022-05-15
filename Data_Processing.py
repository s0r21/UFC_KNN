# Getting the data and manipulating it
from Web_scrape import all_fighter_df, dimension_conversion, most_recent_event
from Utils import *

# All the functions & classes used in this program
class stance_conversion:
    def Orthadox_stance_conversion(df):
        df['Stance_Orth'] = df.apply(lambda x: x['Stance'] == 'Orthodox', axis = 1)
        df['Stance_Orth'] = df['Stance_Orth'].replace([True, False], [1, 0])
        return df
    def Southpaw_stance_conversion(df):
        df['Stance_South'] = df.apply(lambda x: x['Stance'] == 'Southpaw', axis=1)
        df['Stance_South'] = df['Stance_South'].replace([True, False], [1, 0])
        return df
    def Switch_stance_conversion(df):
        df['Stance_Switch'] = df.apply(lambda x: x['Stance'] == 'Switch', axis=1)
        df['Stance_Switch'] = df['Stance_Switch'].replace([True, False], [1, 0])
        df = df.drop(columns='Stance')
        return df
class Normalization:
    def normalization_minmax(df):
        df = (df - min(df)) / (max(df) - min(df))
        return df
    def normalization_of_df(df):
        df['Reach'] = Normalization.normalization_minmax(df['Reach'])
        df['Ht.'] = Normalization.normalization_minmax(df['Ht.'])
        df['L'] = Normalization.normalization_minmax(df['L'])
        return df
class ht_reach_manipulation:
    def removing_str_from_int(df):
        df['Ht.'] = df['Ht.'].replace("\'", '', regex=True).replace('"', '', regex=True).replace(
            ' ', '', regex=True).replace('--', '', regex=True)
        df = df[df['Ht.'] != '']
        df = df[df['Reach'] != '--']
        return df
    def ht_manipulation(df):
        df['Ht.inch_0'] = df['Ht.'].str[0]
        df['Ht.inch_1'] = df['Ht.'].str[1]
        df['Ht.inch_2'] = df['Ht.'].str[2]
        df = df.fillna('')
        df['Ht.inch_0'] = df['Ht.inch_0']
        df['Ht.inch_1'] = df['Ht.inch_1']
        df['Ht.inch_2'] = df['Ht.inch_2']
        df['Ht.inch_3'] = df['Ht.inch_1'] + df['Ht.inch_2']
        df['Ht.inch_1'] = df['Ht.inch_3']
        df['Ht.inch_0'] = dimension_conversion.ft_to_cm(dimension_conversion.str_to_int_convers(df['Ht.inch_0']))
        df['Ht.inch_1'] = dimension_conversion.inch_to_cm(dimension_conversion.str_to_int_convers(df['Ht.inch_1']))
        df['Ht.'] = df['Ht.inch_1'] + df['Ht.inch_0']
        df = df.drop(columns=['Ht.inch_3', 'Ht.inch_2', 'Ht.inch_1', 'Ht.inch_0'])
        return df
    def reach_manipulation(df):
        df['Reach'] = df['Reach'].replace('"', '', regex=True)
        df['Reach'] = dimension_conversion.inch_to_cm(dimension_conversion.str_to_int_convers(all_fighter_df['Reach']))
        return df
class event_test_set:
    def fighter_name_latest_event(df):
        df = pd.DataFrame(df['Fighter'].str.split('  ', 1, expand=True).stack(). \
                          reset_index(level=1, drop=True))
        df[['First', 'Last']] = df[0].str.split(' ', 1, expand=True)
        df = df[['First', 'Last']]
        return df
    def real_event_test_set(webscrape_df):
        webscrape_df = webscrape_df.fillna(null_number)
        webscrape_df = webscrape_df[webscrape_df.First != null_number].drop(columns=['Nickname', 'Wt.', 'Belt',
                                                                                     'W', 'D'])
        return webscrape_df
    def removing_null_fighter(df):
        Null_fighter_information = df[df.isna().any(axis=1)]
        Null_fighter_information = Null_fighter_information.drop(columns=['Ht.', 'Reach', 'L', 'Stance_Orth',
                                                                          'Stance_South', 'Stance_Switch'])
        return Null_fighter_information
    @staticmethod
    def real_test_set_manipulation():
        real_test_set = even_or_odd_index(event_test_set.removing_null_fighter(merged_test_set), merged_test_set)
        real_test_set = real_test_set.drop(columns=['First', 'Last'])
        real_test_set = real_test_set[['L', 'Stance_Orth', 'Stance_South', 'Stance_Switch', 'Ht.', 'Reach']]
        real_test_set['Reach'] = Normalization.normalization_minmax(real_test_set['Reach'])
        real_test_set['Ht.'] = Normalization.normalization_minmax(real_test_set['Ht.'])
        real_test_set['L'] = Normalization.normalization_minmax(real_test_set['L'])
        return real_test_set
def even_or_odd_index(null_df_fighter, df):
    for i in null_df_fighter.index:
        df = df.drop(index=i)
        if i % 2 != 0:
            df = df.drop(index = i - 1)
        elif i % 2 == 0:
            df = df.drop(index = i + 1)
    return df
def exporting_names_to_excel(df):
    export_dataframe = df[['First', 'Last']]
    export_dataframe.columns = ['First', 'Last']
    return export_dataframe

# The array used to represent the column names to drop
columns_to_drop_from_raw_df = ['Winner','Stance','Fighter', 'W',
                               'Wt.', 'Date of Fight', 'Birth Date',
                               'Age at Fight']

# Random value to signify null. column != np.nan isn't working. Converted the null to this value and dropped it from df
null_number = 100000000

# Importing the raw data used in the KNN (Note: this is a CSV file located on my computer)
raw_data = pd.read_csv('Input/Data_for_model_no_organization.csv').dropna()\
    .drop(columns=columns_to_drop_from_raw_df)

# Creating the X and Y values
y = pd.DataFrame(raw_data['Winner_binary'])
X = raw_data.drop(columns='Winner_binary')

# Normalizing the X Values
X = Normalization.normalization_of_df(X)

# Creating the training & test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.05, random_state = 0, shuffle = False)

# Manipulating the webscraping dataframe.
all_fighter_df = event_test_set.real_event_test_set(all_fighter_df)

# Converting the stances into binary columns
all_fighter_df = stance_conversion.Orthadox_stance_conversion(all_fighter_df)
all_fighter_df = stance_conversion.Southpaw_stance_conversion(all_fighter_df)
all_fighter_df = stance_conversion.Switch_stance_conversion(all_fighter_df)

# Removing the following: ' ', ' -- ', or '\' from the column to get only integers
ht_reach_manipulation.removing_str_from_int(all_fighter_df)

# Manipulating the height column to get the height in cm
all_fighter_df = ht_reach_manipulation.ht_manipulation(all_fighter_df)

# Manipulating the reach column to get the reach in cm
all_fighter_df = ht_reach_manipulation.reach_manipulation(all_fighter_df)

# Merging the people from the input event I'm looking for and removing anyone who isn't on the card.
merged_test_set = pd.merge(all_fighter_df, event_test_set.fighter_name_latest_event(most_recent_event[0]),
                         how='right', on=['First', 'Last'])

# Creating the real test set to see who will win the chosen card
real_test_set = event_test_set.real_test_set_manipulation()

# Creating a dataframe that has the name of the fighters. This is used to export to Excel on my desktop
export_dataframe = exporting_names_to_excel(merged_test_set)
