import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = pd.Series(data = ['chicago.csv','new_york_city.csv','washington.csv'],
                        index = ['chicago','new york city','washington'])
months = ['january', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november', 'december']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

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
    print('\nPlease select a city:\n1. Chicago\n2. New York\n3. Washington, DC\n')
    while 1:
        try:
            city_index = int(input('Enter number: '))
            if city_index >= 1 and city_index <=3:
                break
        except ValueError:
            print('Oops! Please enter 1, 2, or 3')
        except KeyboardInterrupt:
            print('\n')
            exit()
        else:
            print('Oops! Please enter 1, 2, or 3')
    city = CITY_DATA.index[city_index-1]

    # get user input for month (all, january, february, ... , june)
    print('\nPlease select a month:\n1. January\n2. February\n3. March\n4. April')
    print('5. May\n6. June\n7. July\n8. August\n9. September\n10. October\n11. November\n12. December\n')
    while 1:
        try:
            month_index = input('Enter number (or leave blank to include all months): ')
            if month_index == '':
                break
            month_index = int(month_index)
            if month_index >= 1 and month_index <= 12:
                break
        except ValueError:
            print('Oops! Please enter a number 1-12')
        except KeyboardInterrupt:
            print('\n')
            exit()
        else:
            print('Oops! Please enter a number 1-12')
    if month_index == '':
        month = 'all'
    else:
        month = months[month_index-1]

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('\nPlease select a day:\n1. Monday\n2. Tuesday\n3. Wednesday\n4. Thursday')
    print('5. Friday\n6. Saturday\n7. Sunday\n')
    while 1:
        try:
            day_index = input('Enter number (or leave blank to include all days of the week): ')
            if day_index == '':
                break
            day_index = int(day_index)
            if day_index >= 1 and day_index <= 7:
                break
        except ValueError:
            print('Oops! Please enter a number 1-7')
        except KeyboardInterrupt:
            print('\n')
            exit()
        else:
            print('Oops! Please enter a number 1-7')
    if day_index == '':
        day = 'all'
    else:
        day = days[day_index-1]

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

    if city == 'washington':
        df['Gender'] = 'N/A'
        df['Birth Year'] = 'N/A'

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month_number = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month_number]

        month_text = 'during the month of {}'.format(month.title())
    else:
        month_text = 'across all months'

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day_number = days.index(day)
        df = df[df['day_of_week'] == day_number]

        day_text = 'on {}s'.format(day.title())
    else:
        day_text = 'for every day of the week'

    print()
    print('*'*80)
    print('Calculating metrics for {} {} {}'.format(city.title(), month_text, day_text))
    print('*'*80)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_index = df['month'].mode()[0] - 1
    popular_month = months[month_index]

    print('The most common month is:', popular_month.title())

    # display the most common day of week
    day_index = df['day_of_week'].mode()[0]
    popular_day = days[day_index]

    print('The most common day is:', popular_day.title())

    # display the most common start hour (Practice Solution #1)
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    print('The most common start hour is:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station is {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The most common end station is {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df['start_and_end_station'] = df['Start Station'] + ' -> ' + df['End Station']
    print('The most common route is {}'.format(df['start_and_end_station'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time_seconds = int(df['Trip Duration'].sum())
    travel_time = str(datetime.timedelta(seconds=travel_time_seconds))
    print('The total travel time is {}'.format(travel_time))

    # display mean travel time
    mean_time_seconds = int(df['Trip Duration'].mean())
    mean_time = str(datetime.timedelta(seconds=mean_time_seconds))
    print('The mean travel time is {}'.format(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The number of each user type is:')
    print(user_types)

    # Display counts of gender
    genders = df['Gender'].value_counts()
    print('\nThe number of each gender is:')
    print(genders)

    # Display earliest, most recent, and most common year of birth
    birth_years = df['Birth Year'].value_counts()
    asc_years = birth_years.sort_index()
    desc_years = birth_years.sort_index(ascending=False)
    asc_val = asc_years.index[0]
    desc_val = desc_years.index[0]
    common_val = birth_years.index[0]
    print('\nThe earliest birth year is {}'.format(str(int(asc_val)) if asc_val != 'N/A' else 'N/A'))
    print('The most recent birth year is {}'.format(str(int(desc_val)) if desc_val != 'N/A' else 'N/A'))
    print('The most common birth year is {}'.format(str(int(common_val)) if common_val != 'N/A' else 'N/A'))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while 1:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        try:
            show_raw_data = input('\nWould you like to see the first 5 lines of raw data? Enter yes or no.\n')
            if show_raw_data.lower() == 'yes':
                pd.set_option('display.max_columns', None)
                print(df.head())
                index = 5
                while 1:
                    try:
                        show_raw_data = input('\nWould you like to see 5 more lines of raw data? Enter yes or no.\n')
                        if show_raw_data.lower() == 'yes':
                            print(df.iloc[index:index+5])
                            index += 5
                        else:
                            break
                    except KeyboardInterrupt:
                        print('\n')
                        exit()
        except KeyboardInterrupt:
            print('\n')
            exit()

        try:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
        except KeyboardInterrupt:
            print('\n')
            exit()


if __name__ == "__main__":
	main()
