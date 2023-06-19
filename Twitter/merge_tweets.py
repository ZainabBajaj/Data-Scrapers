import pandas as pd
import glob

# merge csv of different keypwrds, hashtags and user_ids
def merge_csv():
  path = ''
  all_files = glob.glob(path + "/*.csv")

  csv_files = []

  for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    csv_files.append(df)

  merged_csv = pd.concat(csv_files, axis=0, ignore_index=True)
  
  return merged_csv


# merge and filter dataframes scraped from tweepy and twint
def mergeandfilter(data_tweepy, data_twint):

  # merge dataframes
  merged_tweets = pd.concat([data_tweepy,data_twint])
  common=['tweet_id', 'text', 'favorite_count',
       'retweet_count', 'created_at', 'geo', 'place', 'lang',
       'username', 'hashtags']
  for column in merged_tweets.columns:
    if column not in common:
      merged_tweets.drop(column,axis=1, inplace=True)

  # filter tweets
  merged_tweets.drop_duplicates(subset=['tweet_id'],inplace=True)
  merged_tweets = list(set(merged_tweets))
  return merged_tweets
