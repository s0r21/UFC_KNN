# Trying to webscrape data & data manipulation

from Packages import *
# Functions used in the script
def ft_to_cm(df_column):
    df_column = df_column * 30.48
    return df_column

def inch_to_cm(df_column):
    df_column = df_column * 2.54
    return df_column

def str_to_int_convers(df_column):
    df_column = pd.to_numeric(df_column, errors = 'coerce')
    return df_column

event_name = input('Please enter link to event -> from ( www.ufcstats.com/event ): ')

most_recent_event = pd.read_html(event_name)

# use this array to create a function to webscrape all the fighters data
alphabet_array = ['a', 'b', 'c', 'd',
                  'e', 'f', 'g', 'h',
                  'i', 'j', 'k', 'l',
                  'm', 'n', 'o', 'p',
                  'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x',
                  'y', 'z']

def webscrape_function(array):
    df = pd.DataFrame()
    for i in array:
        df = pd.concat([df, pd.read_html('http://ufcstats.com/statistics/fighters?char=' + i + '&page=all')[0]])
    return df

# Appending the data to one dataframe
all_fighter_df = webscrape_function(alphabet_array)
