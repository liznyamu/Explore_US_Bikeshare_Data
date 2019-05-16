import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_request = 'Would you like to see data for Chicago, New York City or Washington? \n'
    city = input(city_request).lower()
    while city not in CITY_DATA:
        city = input(city_request).lower()

    filter_by = input('Would you like to filter data by month, day, both or not at all? Type "none" for no time filter. \n')

    month = 'all'
    day = 'all'
    if filter_by in ['month', 'both']:
        # get user input for month (all, january, february, ... , june)
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_request = 'Which month? January, February, March, April, May, June : '
        month = input(month_request).lower()
        while month not in months:
            month = input(month_request).lower()
    elif filter_by in ['day', 'both']:
        # get user input for day of week (all, monday, tuesday, ... sunday)
        days = {1: 'sunday',2: 'monday', 3: 'tuesday', 4: 'wednesday', 5: 'thursday', 5: 'friday', 6: 'saturday', 0: 'all'}
        day_request = 'Which day? Please type your response as an integer (eg.. 1=Sunday) : '
        day = input(day_request).astype(int)
        while day not in days:
            day = int(input(day_request))
        day = days.get(day)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA.get(city))

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1 # from http://bit.ly/2IaNmfJ

        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, hour and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    most_common = 'The most common {} is: {}'
    most_common_hour = 'The most common {} is: {0:0>2}' # from http://bit.ly/2I5ur5V

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    common_month = months[df['month'].mode().loc[0] - 1].title() # mode returns a pandas Series
    print(most_common.format('month', common_month))
    print('')

    # display the most common day of week
    common_weekday = df['day_of_week'].mode().loc[0]
    print(most_common.format('day of week', common_weekday))
    print('')

    # display the most common start hour
    common_hour = df['hour'].mode().loc[0]
    print(most_common.format('hour', common_hour))
    print('')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_common = 'The most commonly used {} is: {}'
    most_combination = 'The most frequent combination is Start Station : \'{}\' to End Station : \'{}\', count {}'

    # display most commonly used start station
    print(most_common.format('Start Station', df['Start Station'].mode().loc[0]))
    print('')

    # display most commonly used end station
    print(most_common.format('End Station', df['End Station'].mode().loc[0]))
    print('')

    # display most frequent combination of start station and end station trip
    # using example on http://bit.ly/2JMt7SI
    cols = ['Start Station', 'End Station']
    grouped_df = df.groupby(cols).size().reset_index()
    frequent_combination = grouped_df[0].idxmax()
    frequent_start_station = grouped_df.iloc[frequent_combination]['Start Station']
    frequent_end_station = grouped_df.iloc[frequent_combination]['End Station']
    combination_count =  grouped_df.iloc[frequent_combination][0]

    print(most_combination.format(frequent_start_station,
                                  frequent_end_station, combination_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    travel_time = 'The {} Travel Time is : {}'

    # get total travel time in seconds
    total_travel_time = df['Trip Duration'].sum()

    # break down total_travel_time to days-hours-minutes-seconds from http://bit.ly/2w5VnOo
    minutes, seconds = divmod(total_travel_time, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    periods = [('days', days), ('hours', hours), ('minutes', minutes), ('seconds', seconds)]
    time_string = ', '.join('{} {}'.format(value, name)
                            for name, value in periods
                            if value)

    # display total travel time in days-hours-minutes-seconds
    print(travel_time.format('Total', time_string))
    print('')


    # get mean travel time in seconds
    mean_travel_time = df['Trip Duration'].mean()

    # break down mean_travel_time to minutes-seconds from http://bit.ly/2w5VnOo
    minutes, seconds = divmod(mean_travel_time, 60)

    periods = [('minutes', minutes), ('seconds', seconds)]
    time_string = ', '.join('{} {}'.format(value, name)
                            for name, value in periods
                            if value)

    # display mean travel time in minutes-seconds
    print(travel_time.format('Mean', time_string))
    print('')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    sorry_message = 'Sorry, the Washington data does not have a \'{}\' column'
    # Display counts of user types
    print(df['User Type'].value_counts())
    print('')

    # Display counts of gender
    if 'Gender' in df:
        print(df['Gender'].value_counts())
    else:
        print(sorry_message.format('Gender'))
    print('')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('The Earliest Year of Birth : {}'.format(df['Birth Year'].min().astype(int)))
        print('The Most Recent Year of Birth : {}'.format(df['Birth Year'].max().astype(int)))
        print('The Most Common Year of Birth : {}'.format(df['Birth Year'].mode().loc[0].astype(int)))
    else:
        print(sorry_message.format('Birth Year'))
    print('')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # print first 5 rows of the DataFrame and request user to view more data
        # from http://bit.ly/2wbov6R
        start_at, end_at, print5_more = -5, 0, 'yes'
        while print5_more.lower() != 'no' :
            start_at += 5
            end_at += 5
            print(df.to_dict(orient='records')[start_at:end_at])
            print5_more = input('\nWould you like to view individual data? Enter yes or no.\n')


        # request user to restart process
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
