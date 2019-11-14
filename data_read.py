import pandas as pd
import numpy as np

# Constants
city_name = 'Las Vegas'
output_review_name = 'data/LV_reviews.csv'
output_users_name = 'data/LV_users.csv'

# Get business IDS
business = pd.read_json('data/business.json', lines=True)
subset_business_ids = set(business[business['city']==city_name]['business_id'])

# Get chunks from large datasets
user_chunks = pd.read_json('data/user.json', lines=True, chunksize=100000)
review_chunks = pd.read_json('data/review.json', lines=True, chunksize=100000)

# Set up empty df columns
for chunk in user_chunks:
    columns_users = chunk.columns
    break

for chunk in review_chunks:
    columns_reviews = chunk.columns
    break

# Get reviews from the business subet
reviews_df = pd.DataFrame(columns=columns_reviews)
for chunk in review_chunks:
    subset = chunk[chunk['business_id'].isin(subset_business_ids)]
    reviews_df = reviews_df.append(subset, ignore_index = True)

# Subset Users by Reviews
subset_user_ids = set(reviews_df['user_id'])

# Get users from reviews
users_df = pd.DataFrame(columns=columns_users)
for chunk in user_chunks:
    subset = chunk[chunk['user_id'].isin(subset_user_ids)]
    users_df = users_df.append(subset, ignore_index = True)

# Write files
users_df.to_csv(output_users_name)
reviews_df.to_csv(output_review_name)