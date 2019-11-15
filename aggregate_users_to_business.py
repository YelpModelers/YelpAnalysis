import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import datetime

# Constants
city_name = 'Las Vegas'

# ------------------------- #
#    READ AND CLEAN DATA
# ------------------------- #
# Read data
users = pd.read_csv('data/LV_users.csv', low_memory=False)
users = users.drop('Unnamed: 0', axis=1)

reviews = pd.read_csv('data/LV_reviews.csv', low_memory=False)
reviews = reviews.drop('Unnamed: 0', axis=1)
# Clean NAs (only 1 for vegas)
reviews = reviews.dropna()

business = pd.read_csv('data/business.csv', low_memory=False)
business = business.drop('Unnamed: 0', axis=1)

business = business[business['city'] == 'Las Vegas']


# Clean Reviews
# Get the last review to represent the end of the dataset
latest_review = sorted(reviews['date'], reverse=True)[0]

# Convert dates
latest_review = datetime.datetime.strptime(latest_review, '%Y-%m-%d %H:%M:%S')
users['yelping_since_date'] = [datetime.datetime.strptime(x[-1], '%Y-%m-%d %H:%M:%S') for x in users.itertuples()]

# average days per month
av_day_per_month = 30.44

# ------------------------- #
#   CALCULATE USER STATS
# ------------------------- #
users['count_friends'] = [len(row[-8].split(',')) for row in users.itertuples()]
users['months_of_activity'] = latest_review - users['yelping_since_date']
users['months_of_activity'] = [x.days for x in users['months_of_activity']]
users['months_of_activity'] = round(users['months_of_activity']/av_day_per_month)
# Prevent users from have zero months and therefore infinite averages
users['months_of_activity'] = [1 if month==0 else month for month in users['months_of_activity']]
users['reviews_per_month'] = users['review_count'] / users['months_of_activity']
users['elite_binary'] = np.where(pd.isna(users['elite']), 0, 1)

# Friends
Q1, Q3 = np.percentile(users['count_friends'], [25 ,75])
IQR = Q3 - Q1
influencer_friend_threshold = Q3 + (IQR*1.5)

# Fans
Q1, Q3 = np.percentile(users['fans'], [25 ,75])
IQR = Q3 - Q1
influencer_fan_threshold = Q3 + (IQR*1.5)

users['fan_outlier'] = np.where(users['fans']>influencer_fan_threshold, 1, 0)
users['friend_outlier'] = np.where(users['count_friends']>influencer_friend_threshold, 1, 0)

# ------------------------- #
#          JOINING
# ------------------------- #
# Ensure all ids are string
reviews.loc[:,'user_id'] = reviews['user_id'].astype(str)
reviews.loc[:,'business_id'] = reviews['business_id'].astype(str)
users.loc[:,'user_id'] = users['user_id'].astype(str)
business.loc[:,'business_id'] = business['business_id'].astype(str)

# Ensure there are no leading or trailing spaces
reviews['user_id'] = [string.strip(" ") for string in reviews['user_id']]
reviews['business_id'] = [string.strip(" ") for string in reviews['business_id']]
users['user_id'] = [string.strip(" ") for string in users['user_id']]
business['business_id'] = [string.strip(" ") for string in business['business_id']]

# JOIN
reviews_join = reviews.copy()
reviews_join= reviews_join.rename(columns={'cool':'cool_review', 'funny':'funny_review', 'useful':'useful_review'})
reviews_join = reviews_join.merge(users, how='left', left_on='user_id', right_on='user_id')

print("Number of NA users in all business reviews: {}".format(len(reviews_join[pd.isna(reviews_join['count_friends'])])))
print('Totals rows in all business reviews: {}'.format(len(reviews_join)))

# Keep only relevant columns for now
reviews_join_user = reviews_join.loc[:,['business_id', 'cool_review', 'funny_review',
       'stars', 'useful_review', 'average_stars', 'cool', 'elite_binary', 'fans',
       'funny', 'review_count', 'useful', 'count_friends', 'reviews_per_month', 
       'fan_outlier', 'friend_outlier']]

# Subset to just food businesses
unique_food_business = set(business['business_id'])

# Subset reviews to just food
reviews_join_user_food = reviews_join_user[reviews_join_user['business_id'].isin(unique_food_business)]

print("Number of NA users in all business reviews: {}".format(len(reviews_join_user_food[pd.isna(reviews_join_user_food['count_friends'])])))
print('Totals rows in all business reviews: {}'.format(len(reviews_join_user_food)))

# Correct column dtypes
reviews_join_user_food['cool_review'] = reviews_join_user_food['cool_review'].astype(int)

# Aggregate to business level
reviews_join_user_food = reviews_join_user_food.groupby('business_id').agg({'cool_review':np.mean, 'funny_review':np.mean,
    'stars':np.mean, 'useful_review':np.mean, 
    'average_stars':np.mean, 'cool':np.mean, 'elite_binary':sum,
    'fans':[sum, np.mean],
    'funny':np.mean, 'review_count':[sum, np.mean],
    'useful':[sum, np.mean], 'count_friends':[sum, np.mean],
    'reviews_per_month':np.mean, 'fan_outlier':sum,
    'friend_outlier':sum})

print("Number of NAs in output: {}".format(np.count_nonzero(np.isnan(reviews_join_user_food['average_stars']['mean'].values))))
print("Number of Total in output: {}".format(len(reviews_join_user_food)))

# Ensure sums are NA where the mean values are NA (aka fake zeros)
reviews_join_user_food['elite_binary']['sum'] = np.where(pd.isna(reviews_join_user_food['average_stars']['mean']), 
                                                         np.nan, 
                                                         reviews_join_user_food['elite_binary']['sum'])
reviews_join_user_food['fans']['sum'] = np.where(pd.isna(reviews_join_user_food['average_stars']['mean']), 
                                                         np.nan, 
                                                         reviews_join_user_food['fans']['sum'])
reviews_join_user_food['review_count']['sum'] = np.where(pd.isna(reviews_join_user_food['average_stars']['mean']), 
                                                         np.nan, 
                                                         reviews_join_user_food['review_count']['sum'])
reviews_join_user_food['useful']['sum'] = np.where(pd.isna(reviews_join_user_food['average_stars']['mean']), 
                                                         np.nan, 
                                                         reviews_join_user_food['useful']['sum'])
reviews_join_user_food['count_friends']['sum'] = np.where(pd.isna(reviews_join_user_food['average_stars']['mean']), 
                                                         np.nan, 
                                                         reviews_join_user_food['count_friends']['sum'])
reviews_join_user_food['fan_outlier']['sum'] = np.where(pd.isna(reviews_join_user_food['average_stars']['mean']), 
                                                         np.nan, 
                                                         reviews_join_user_food['fan_outlier']['sum'])
reviews_join_user_food['friend_outlier']['sum'] = np.where(pd.isna(reviews_join_user_food['average_stars']['mean']), 
                                                         np.nan, 
                                                         reviews_join_user_food['friend_outlier']['sum'])

# Reindex multiindex columns
new_flat_cols = ['_'.join(col).strip() for col in reviews_join_user_food.columns.values]
reviews_join_user_food.columns = new_flat_cols
reviews_join_user_food.reset_index(inplace=True)

reviews_join_user_food.to_csv('data/vegas_business_user_info.csv', index=False)
