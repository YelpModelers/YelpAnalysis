import pandas as pd

data = pd.read_csv('data/vegas_yelp_dataset.csv')

data = data.drop(columns=['Unnamed: 0'])

all_columns = data.columns

business_dataset = ['business'] * 46
review_dataset = ['reviews'] * 14
user_dataset = ['users'] * 15

dataset_origin = business_dataset + review_dataset + user_dataset

metadata = ['string, the full address of the business',
    'string, 22 character unique string business id',
    'city (vegas)',
    'latitude',
    'longitude',
    'business name',
    'US postal code',
    'number of reviews for the business',
    'star rating for the business',
    'state',
    'top category from within the list of possible business types',
    'has bike parking y/n',
    'price range',
    'restaurant has TV', 
    'restaurant is good for groups', 
    'outdoor seating',
    'restaurants has reservations', 
    'good for kids', 
    'alcohol served', 
    'noiseLevel',
    'accepts credit cards', 
    'WiFi', 
    'restaurant attire', 
    'caters',
    'takeOut', 
    'delivery', 
    'garage', 
    'lot', 
    'street',
    'valet', 
    'validated', 
    'casual', 
    'classy', 
    'divey', 
    'hipster',
    'intimate', 
    'romantic', 
    'touristy', 
    'trendy', 
    'upscale', 
    'breakfast',
    'brunch', 
    'dessert', 
    'dinner', 
    'latenight', 
    'lunch',
    'checkin_count',
    'number of months restaurant has been open', 
    'number of reviews for the business from reviews (duplicate?)',
    'number of reviews tagged as cool',
    'number of reviews tagged as funny', 
    'number of reviews tagged as useful', 
    'response variable - overall measure of popularity by combining number of reviews and checkins (sum)',
    'number of cool reviews per month', 
    'number of funny reviews per month', 
    'number of useful reviews per month',
    'mean number of cool reviews', 
    'mean number of funny reviews', 
    'mean number of review stars',
    'mean number of useful reviews', 
    'mean number of average stars per user who reviewed', 
    'mean number of cool votes by users who reviewed',
    'number of users who have ever been elite, who reviewed', 
    'sum total number of fans of all those who reviewed', 
    'mean number of fans of all those who reviewed',
    'mean number of funny votes by users who reviewed', 
    'total number of reviews written by users who reviewed', 
    'mean number of reviews written by users who reviewed',
    'total number of useful votes by users who reviewed', 
    'mean number of useful votes by users who reviewed', 
    'sum total number of friends of all those who reviewed',
    'mean number of friends of all those who reviewed', 
    'mean number of reviews written per month by those who reviewed', 
    'number of users who reviewed who are considered an outlier in terms of their number of fans',
    'number of users who reviewed who are considered an outlier in terms of their number of friends']

meta_data = pd.DataFrame(data={'id':all_columns, 'dataset':dataset_origin, 'description':metadata})
meta_data.to_csv('data/yelp_metadata.csv')