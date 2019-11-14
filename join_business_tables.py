import numpy as np
import pandas as pd

clean_business = pd.read_csv('data/vegas_food_businesses_cleaned.csv')
clean_reviews = pd.read_csv('data/review_checkin_final.csv')
clean_users = pd.read_csv('data/vegas_business_user_info.csv')

clean_business.drop('Unnamed: 0', axis=1, inplace=True) 

# Rename review dataset for clarity
clean_reviews = clean_reviews.rename(columns={'cool_stand':'cool_review_pm', 'funny_stand':'funny_review_pm',
                                              'useful_stand':'useful_review_pm', 'useful':'useful_review_count',
                                              'funny':'funny_review_count', 'cool':'cool_review_count',
                                              'review':'review_count', 'checkin':'checkin_count'})

clean_users = clean_users.rename(columns={'stars_mean':'stars_review_mean', 'average_stars_mean':'stars_users_mean',
                                          'cool_mean':'cool_users_mean', 'elite_binary_sum':'elite_users_sum',
                                          'fans_sum':'fans_users_sum', 'fans_mean':'fans_users_mean',
                                          'funny_mean':'funny_users_mean', 'review_count_sum':'review_users_sum',
                                          'review_count_mean':'review_users_mean', 'useful_sum':'useful_users_sum',
                                          'useful_mean':'useful_users_mean', 'count_friends_sum':'friend_number_count',
                                          'count_friends_mean':'friend_number_mean', 'reviews_per_month_mean':'reviews_users_pm_mean',
                                          'fan_outlier_sum':'fan_outlier_count','friend_outlier_sum':'friend_outlier_count'})

clean_business = clean_business.rename(columns={'review_count':'review_count_business', 'stars':'stars_business'})

vegas_yelp_dataset = pd.merge(clean_business, clean_reviews, how='left', left_on='business_id', right_on='business_id')
vegas_yelp_dataset = pd.merge(vegas_yelp_dataset, clean_users, how='left', left_on='business_id', right_on='business_id')
vegas_yelp_dataset.to_csv('data/vegas_yelp_dataset.csv')

print('Overall columns:')
print(vegas_yelp_dataset.columns)
