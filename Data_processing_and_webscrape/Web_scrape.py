# Webscrape and data from the website
from Utils import *

class dimension_conversion:
    def ft_to_cm(df_column):
        df_column = df_column * 30.48
        return df_column
    def inch_to_cm(df_column):
        df_column = df_column * 2.54
        return df_column
    def str_to_int_convers(df_column):
        df_column = pd.to_numeric(df_column, errors = 'coerce')
        return df_column
def webscrape_function(array):
    df = pd.DataFrame()
    for i in array:
        df = pd.concat([df, pd.read_html('http://ufcstats.com/statistics/fighters?char=' + i + '&page=all')[0]])
    return df

# Array to obtain all fighters
alphabet_array = ['a', 'b', 'c', 'd',
                  'e', 'f', 'g', 'h',
                  'i', 'j', 'k', 'l',
                  'm', 'n', 'o', 'p',
                  'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x',
                  'y', 'z']

# Choosing the event based on the link provided in the input function
event_name = input('Please enter link to event -> from ( http://www.ufcstats.com/statistics/events/completed ): ')
# Taking the event and putting it into a dataframe
most_recent_event = pd.read_html(event_name)

# Concatenating the data to one dataframe
all_fighter_df = webscrape_function(alphabet_array)
