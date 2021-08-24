import time
import datetime
import calendar
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
    print('\nHello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).
    print("\nEnter the name of the city to analyze (Chicago, New York City or Washington)")
    input_city = input()
    cities = ['chicago', 'new york city', 'washington']
    while True:
        if input_city.lower().strip() in cities:
            city = input_city.lower().strip()
            break
        else:
            print("Invalid entry. Enter the city name correctly.")
        input_city = input()


    def get_month():
        """Gets the user input for month and validates it."""

        print("\nWhich month? January, February, March, April, May or June?")
        input_month = input()
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        while True:
            if input_month.lower().strip() in months:
                return input_month.lower().strip()
            else:
                print("Invalid entry. Enter the month correctly.")
            input_month = input()

    def get_day():
        """Gets the user input for day of week and validates it."""

        print("\nWhich day? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or Saturday?")
        input_day = input()
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        while True:
            if input_day.lower().strip() in days:
                return input_day.lower().strip()
            else:
                print("Invalid entry. Enter the day correctly.")
            input_day = input()

    # get user input for month (january, february, ... june)
    # get user input for day of week (sunday, monday, tuesday, ... saturday)
    print('\nWould you like to filter the data by month, day, both, or not at all? Type "none" for no time filter.')
    user_input = input()
    while True:
        if user_input.lower().strip() == 'none':
            month = 'all'
            day = 'all'
            break
        elif user_input.lower().strip() == 'both':
            month = get_month()
            day = get_day()
            break
        elif user_input.lower().strip() == 'day':
            month = 'all'
            day = get_day()
            break
        elif user_input.lower().strip() == 'month':
            month = get_month()
            day = 'all'
            break
        else:
            print("Invalid entry. Enter month, day, both or none.")
        user_input = input()

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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    popular_month_count = df['month'].value_counts().max()
    print('Most Popular Month: {}    Count: {}'.format(calendar.month_name[popular_month], popular_month_count))

    # display the most common day of week
    popular_dow = df['day_of_week'].mode()[0]
    popular_dow_count = df['day_of_week'].value_counts().max()
    print('Most Popular Day: {}    Count: {}'.format(popular_dow, popular_dow_count))

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    popular_hour_count = df['hour'].value_counts().max()
    print('Most Frequent Start Hour: {}:00 hours    Count: {}'.format(popular_hour, popular_hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    popular_start_count = df['Start Station'].value_counts().max()
    print('Most Commonly Used Start Station: {}    Count: {}'.format(popular_start, popular_start_count))

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    popular_end_count = df['End Station'].value_counts().max()
    print('Most Commonly Used End Station: {}    Count: {}'.format(popular_end, popular_end_count))

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    popular_trip = df['Trip'].mode()[0]
    popular_trip_count = df['Trip'].value_counts().max()
    print('Most Frequent Trip: from {}    Count: {}'.format(popular_trip, popular_trip_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    total_travel_time = datetime.timedelta(seconds=int(total_trip_duration))
    print('Total Travel Time (days, hh:mm:ss):', total_travel_time)

    # display mean travel time
    mean_trip_duration = df['Trip Duration'].mean()
    mean_travel_time = datetime.timedelta(seconds=int(mean_trip_duration))
    print('Average Travel Time (hh:mm:ss):', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Breakdown of User Types:")
    user_type = df['User Type'].value_counts()
    for index in range(len(user_type)):
        print("    {}: {}".format(user_type.index[index], user_type[index]))

    # Display counts of gender
    try:
        print("Breakdown of Gender:")
        gender_type = df['Gender'].value_counts()
        for index in range(len(gender_type)):
            print("    {}: {}".format(gender_type.index[index], gender_type[index]))
    except:
        print("    No data to share")

    # Display earliest, most recent, and most common year of birth
    try:
        print("Birth Year details:")
        print("    Oldest User was born in {}".format(int(df['Birth Year'].min())))
        print("    Youngest User was born in {}".format(int(df['Birth Year'].max())))
        print("    Most common year of birth is {}".format(int(df['Birth Year'].mode()[0])))
    except:
        print("    No data to share")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df, city):
    """Displays raw data 5 rows at a time based on user input."""

    # get user input, validate it and display the raw data if applicable
    i = 0
    print("Would you like to see the raw data? Enter yes or no.")
    input_raw = input()
    pd.set_option('display.max_columns',300)
    while True:
        if input_raw.lower().strip() == 'no':
            break
        elif input_raw.lower().strip() == 'yes':
            if city == 'washington':
                print(df.iloc[i:i+5,1:7])
            else:
                print(df.iloc[i:i+5,1:9])
            print("\nWould you like to see the next 5 rows? Enter yes or no.")
            i += 5
        else:
            print("Invalid entry. Enter yes or no.")
        input_raw = input()


def main():
    while True:
        city, month, day = get_filters()

        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        while True:
            if restart.lower().strip() == 'yes' or restart.lower().strip() == 'no':
                break
            else:
                print("Invalid entry. Enter yes or no.")
            restart = input()

        if restart.lower().strip() != 'yes':
            break


if __name__ == "__main__":
	main()
