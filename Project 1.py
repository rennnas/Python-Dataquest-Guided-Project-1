#!/usr/bin/env python
# coding: utf-8

# # Apps Profile: a study for profitable apps
# 
# The following project intends to analyse what kind of app our users interact the most. Considering that all of our apps are free, is fundamental the revenue we obtain with ads engagement inside the apps. We intend with this project to present the profile of the apps that attract more users.
# 
# ### Data Source
# 
# Analysing the data for the more than 4 million apps available on Google Play and in the App Store (Source: Statista) would be complex and expensive task for our company. So for the purposes of this study, we will analyze the mobile apps data previously collected. The two data sets used are:
# 
# - A data set containing data about approximately 10,000 Android apps from Google Play; the data was collected in August 2018.
# 
# - A data set containing data about approximately 7,000 iOS apps from the App Store; the data was collected in July 2017. 

# In[14]:


#Importing the data set#
from csv import reader

##Google Store Data##

file = open('googleplaystore.csv')
read_file = reader(file)
android = list(read_file)

android_header = android[0]
android = android[1:]

##App Store Data##

file1 = open('AppleStore.csv')
read_file1 = reader(file1)
ios = list(read_file1)

ios_header = ios[0]
ios = ios[1:]


# ###### Exploring the data
# To be able to better visualize the data and to make it easier to interpret it, we are creating a function to print the rows in a readlabe way.

# In[15]:


#Creating a function to print rows in a readable way#

def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# In[16]:


#Exploring the Data from Google Store
explore_data(android, 0, 5, rows_and_columns = True)

#Exploring the Data from App Store
explore_data(ios, 0, 5, rows_and_columns = True)


# Analysing the data, we can see that the data that may be useful for our project is:
# 
# Google - 10842 entrances, 13 columns - out of 7 that may be useful:
# * 'Category'
# * 'Rating', 
# * 'Reviews'
# * 'Installs'
# * 'Type'
# * 'Price' 
# * 'Genres'
# 
# Documentation: 
# Apple - 7198 entrances, 16 columns - out of 7 that may be useful:
# 
# * 'price'
# * 'rating_count_tot'
# * 'rating_count_ver'
# * 'user_rating'
# * 'user_rating_ver'
# * 'cont_rating'
# * 'prime_genre'

# ### Data Cleaning
# In the discussion section of the Google Play data, we can see that one of the discussions outlines an error for row 10472. Let's compare this row if a random one.

# In[17]:


print(android[0]) #correct one
print(android[10472]) #incorrect row
print(android_header) #header


# We can see that the error is in the column category, that is missing. Instead, the value 19 is in a column where the maximum value allowed is 5.
# We need to delete this row.

# In[18]:


del (android[10472]) #delting the wrong cell


# ### Deleting duplicated values
# Before we go on, is important to also analyse if the data set has duplicated values. Let's see:

# In[19]:


duplicate_apps = []
unique_apps = []

for app in android:
    name = app[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)
    
print('Number of duplicate apps:', len(duplicate_apps))
print('\n')
print('Examples of duplicate apps:', duplicate_apps[:15])


# We confirmed that the data set has 1181 duplicate rows. We could delete them randomly, but we choose to keep the rows for duplicate apps with the most reviews. We believe that the higher the number of reviews an app has, the more accurate the rating will be.
# So we'll:
# 
# * Create a dictionary where each key is a unique app name, and the value is the highest number of reviews of that app
# 
# * Use the dictionary to create a new data set, which will have only one entry per app (and we only select the apps with the highest number of reviews)

# In[20]:


reviews_max = {}

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
        
    elif name not in reviews_max:
        reviews_max[name] = n_reviews


# In[21]:


print('Actual length:', len(reviews_max))


# Now we can see that the cleaned data has 9659 values. Let's add these entrances to a clean list so we can continue to work.

# We start by initializing two empty lists, android_clean and already_added.
# 
# We loop through the android data set, and for every iteration:
# We isolate the name of the app and the number of reviews.
# We add the current row (app) to the android_clean list, and the app name (name) to the already_added list if:
# The number of reviews of the current app matches the number of reviews of that app as described in the reviews_max dictionary; and
# The name of the app is not already in the already_added list. We need to add this supplementary condition to account for those cases where the highest number of reviews of a duplicate app is the same for more than one entry (for example, the Box app has three entries, and the number of reviews is the same). If we just check for reviews_max[name] == n_reviews, we'll still end up with duplicate entries for some apps.

# In[22]:


android_clean = []
already_added = []

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if (reviews_max[name] == n_reviews) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)


# In[23]:


print(len(android_clean))


# ## Removing non-english apps
# 
# Considering that we use English for the apps we develop at our company, and we'd like to analyze only the apps that are directed toward an English-speaking audience, if we explore the data long enough, we'll find that both data sets have apps with names that suggest they are not directed toward an English-speaking audience.
# 
# We'll do it creating a new function using a built-in function inside the argument: the function ord(). In Python every character has a correspondent number. The English ones hae the number lower than 127. The ord() function presents corresponding number of each character using.

# In[24]:


#Creating a function to remove non-english strings

def is_english(string):
    for character in string:
        if ord(character) > 127:
            return False
        
    return True


# In[25]:


print(is_english('Instagram'))
print(is_english('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))


# In[26]:


print(ord('™'))
print(ord('😜'))


# The function seems to work fine, however, the apps 'Docs To Go™ Free Office Suite' and 'Instachat 😜' weren't recognized as English apps, because the characters '™' and '😜' have an index number greater than 127.

# To minimize data loss, we'll only delete the apps if their names havem more than 3 characters with the index number bigger than 127. Let's reformulate the function.

# In[27]:


def is_english(string):
    non_english = 0
    
    for character in string:
        if ord(character) > 127:
            non_english += 1
        
    if non_english > 3:
        return False
    else:
        return True


# In[28]:


print(is_english('Instagram'))
print(is_english('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))


# It is indeed a better function, however, probably we'll still loose some data. The main point here is that in this way we'll still be able to save some.

# ## Cleaning ios data

# The same should be done in the app store with the ios database. Let's check first if there's some duplicate apps and then if there's non-english ones.

# In[29]:


ios_duplicate_apps = []
ios_unique_apps = []

for app in ios:
    name = app[1]
    if name in ios_unique_apps:
        ios_duplicate_apps.append(name)
    else:
        ios_unique_apps.append(name)
    
print('Number of duplicate apps:', len(ios_duplicate_apps))
print('\n')
print('Examples of duplicate apps:', ios_duplicate_apps[:15])


# There's only two duplicate apps in the app stoer, so we shouldn't bother deleting them. 

# So let's erase the non-english apps in the ios using the is_english() function.

# In[30]:


android_english = []
ios_english = []

for app in android_clean:
    name = app[0]
    if is_english(name):
        android_english.append(app)
        
for app in ios:
    name = app[1]
    if is_english(name):
        ios_english.append(app)
        
explore_data(android_english, 0, 3, True)
print('\n')
explore_data(ios_english, 0, 3, True)


# After the process of data cleaning, we can see that we have left 9614 Android apps and 6183 iOS apps.

# ## Cleaning non-free apps

# So far we have:
# * Removed inaccurate data
# * Removed duplicate app entries
# * Removed non-English apps
# 
# Now, since our company only works with free apps, let's remove the non-free apps from our analysis.

# In the android data_set, the column showing the price of the app is the 8th, so, the index number [7].
# 
# In the ios data_set, the column showing the price of the app is the 5th, and is an interger (0.0) so, the index number [4].
# 
# The current data set we're using are the ones filtred for english.

# In[31]:


android_final = []
ios_final = []

for app in android_english:
    price = app[7]
    if price == '0':
        android_final.append(app)
        
for app in ios_english:
    price = app[4]
    if price == '0.0':
        ios_final.append(app)
        
print(len(android_final))
print(len(ios_final))


# We're left with 8864 Android apps and 3222 iOS apps for our analysis.

# # Data Analysis
# 
# Our main goal with this study is to:
# 
# * Build a minimal Android version of the app, and add it to Google Play.
# * If the app has a good response from users, we develop it further.
# * If the app is profitable after six months, we build an iOS version of the app and add it to the App Store.
# 
# Let's begin the analysis by getting a sense of what are the most common genres for each market. For this, we'll need to build frequency tables for a few columns in our data sets. we'll build a frequency table for the prime_genre column of the App Store data set, and the Genres and Category columns of the Google Play data set.
# 
# We'll build two functions we can use to analyze the frequency tables:
# 
# * One function to generate frequency tables that show percentages
# * Another function we can use to display the percentages in a descending order

# In[32]:


def freq_table(dataset, index):
    table = {}
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
    
    table_percentages = {}
    for key in table:
        percentage = (table[key] / total) * 100
        table_percentages[key] = percentage 
    
    return table_percentages


# In[33]:


def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# ## Examining the data

# In[34]:


display_table(ios_final, -5)


# In[35]:


display_table(android_final, 1) # Category


# In[36]:


display_table(android_final, -4)


# * We can see that among the free English apps, more than a half (58.16%) are games. Entertainment apps are close to 8%, followed by photo and video apps, which are close to 5%. Only 3.66% of the apps are designed for education, followed by social networking apps which amount for 3.29% of the apps in our data set.
# 
# * The general impression is that App Store (at least the part containing free English apps) is dominated by apps that are designed for fun (games, entertainment, photo and video, social networking, sports, music, etc.), while apps with practical purposes (education, shopping, utilities, productivity, lifestyle, etc.) are more rare. However, the fact that fun apps are the most numerous doesn't also imply that they also have the greatest number of users — the demand might not be the same as the offer.
# 
# * On Google Play: the landscape seems significantly different on Google Play: there are not that many apps designed for fun, and it seems that a good number of apps are designed for practical purposes . However, if we investigate this further, we can see that the family category (which accounts for almost 19% of the apps) means mostly games for kids.
# 
# * Up to this point, we found that the App Store is dominated by apps designed for fun, while Google Play shows a more balanced landscape of both practical and for-fun apps. Now we'd like to get an idea about the kind of apps that have most users.

# ### Most popular apps by Genre (number of installs/number of ratings)
# 
# One way to find out what genres are the most popular (have the most users) is to calculate the average number of installs for each app genre. For the Google Play data set, we can find this information in the Installs column, but this information is missing for the App Store data set. As a workaround, we'll take the total number of user ratings as a proxy, which we can find in the rating_count_tot app.
# 
# 
# 
# 

# In apple using the number of ratings.

# In[37]:


genres_ios = freq_table(ios_final, -5)

for genre in genres_ios:
    total = 0
    len_genre = 0
    for app in ios_final:
        genre_app = app[-5]
        if genre_app == genre:            
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    avg_n_ratings = total / len_genre
    print(genre, ':', avg_n_ratings)


# With this data, let's analyse the ones with the most users: Social Networking, Music, Reference, Weather, Navigation, Food & Drink, Book and Finance.

# In[38]:


#Navigation apps

for app in ios_final:
    if app[-5] == 'Navigation':
        print(app[1], ':', app[5])


# In[39]:


#Social Networking apps

for app in ios_final:
    if app[-5] == 'Social Networking':
        print(app[1], ':', app[5])


# While Navigation and Social Networking have the biggest numbers of ratings among iOS users, the fields are controlled for a few gigants - like Waze and Google maps for the first category and Facebook and Instagram in the second.

# The problem with the remaining categories are that weather apps don't seem to hang user's attention for long and Finance seems overly hard for our company to build. Lets check the others.

# In[42]:


#Reference apps

for app in ios_final:
    if app[-5] == 'Reference':
        print(app[1], ':', app[5])


# In[43]:


# Food & Drink 
for app in ios_final:
    if app[-5] == 'Food & Drink':
        print(app[1], ':', app[5])


# In[44]:


# Book 
for app in ios_final:
    if app[-5] == 'Book':
        print(app[1], ':', app[5])


# We can see that the first that Reference apps are mainly regarinds the bible an dictionary apps. Food & Drink apps are controlled by big food chains. While books at the first glance looks like a potential field to explore. Let's check if the same goes on with the Google Store Apps.

# ## Analysing Google Store Apps

# In[45]:


categories_android = freq_table(android_final, 1)

for category in categories_android:
    total = 0
    len_category = 0
    for app in android_final:
        category_app = app[1]
        if category_app == category:            
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)


# Let's give a look to the genre Books & References, since we found a potential market in the Apple Store.

# In[46]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE':
        print(app[0], ':', app[5])


# # Conclusions
# 
# In this project, we analyzed data about the App Store and Google Play mobile apps with the goal of recommending an app profile that can be profitable for both markets.
# 
# We concluded that taking a popular book (perhaps a more recent book) and turning it into an app could be profitable for both the Google Play and the App Store markets. The markets are already full of libraries, so we need to add some special features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes on the book, a forum where people can discuss the book, etc.

# In[ ]:




