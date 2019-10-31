# YelpAnalysis


## Assumptions

* Only interested in the restaurant industry (including food drinks and all subsets therein) - we will manually look at the list of top business types and select those of interest. We will however likely miss a small number (negligible)

* Only including restaurants that are currently open


## EDA Approach

* Write out the questions we want to answer or problem we're trying to solve
* Give an indication of what we're 

#### Response (Claire)

* How do checkins and reviews relate?
* Are they from the same user at the same time period?
* Can we deduplicate and add?

Need to:

* Average out to monthly


#### Business Variables (Nikhil)

Categories

* Investigate and choose specific subcategories (only food + restaurants)
* Get the specific subtype and extract into our features
* Try to ignore "restaurant" or "food" and just keep the most representative category (take the first category unless restaurant, then take the second)
* Count how many of each we have and plot the distribution

Attributes

* Flatten out the nested list of attributed
* Find the most common types of attribute
* Threshold to some chosen level (only include attributes that are in at least 10% of restaurants?)
* Fill in the blanks with FALSE


#### Review Variables (Claire)

Business Age

* date of last review - date of oldest review (in months)


Count of Reviews

* Investigate the reviews table
* 'funny', 'cool' and 'useful' 
* Gather reviews for our specific businesses
* Group by business and count tags


#### User Variables (Hayden)

Friends and Fans

* Investigate (for a few businesses) - the distribution of friends for those user who left a review
* Check for "outlier" users who have more friends than the IQR * 1.5
* Same for fans
* Calculate average number of friends per restaurants
* Calculate average number of fans per restaurants
* Count of reviews by outlier reviewers per restaurant

Number of Reviews

* Average number of reviews per reviewer for each restaurant
* Average number of reviers per month per reviewer for each restaurant (user activity) (divide by Yelping since)



