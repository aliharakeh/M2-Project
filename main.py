import random
from Locations.locations import LocationParser

LocationParser.load_locations_details()

# extract cities keys in a list
keys = list(LocationParser.Cities_Details.keys())
total = len(keys)

# variables needed for creating users data
places_lat_longs = []
places_lat_longs_length = None

"""###################################################################################################"""


def get_random_lat_long():
    # get random city
    random_city = keys[random.randint(0, total)]
    details = LocationParser.Cities_Details[random_city]
    return details['latitude'], details['longitude']


def create_random_places_samples(limit=1000):
    global places_lat_longs, places_lat_longs_length

    # header data
    data = [
        ['place', 'lat', 'long', 'mention_count', 'date']
    ]

    # loop till limit
    for i in range(limit):
        # random day
        tmp_d = random.randint(1, 31)
        d = tmp_d if tmp_d >= 10 else f'0{tmp_d}'

        # random month
        m = f'0{random.randint(2, 8)}'

        # random city [lat, long]
        lat, long = get_random_lat_long()

        # update known places [lat, long] data for future use
        places_lat_longs.append([lat, long])

        # add data
        data.append([
            f'place_{i}',
            lat,
            long,
            str(random.randint(100, 1000)),
            f'{d}-{m}-2020'
        ])

    # update places length variable for future use
    places_lat_longs_length = len(places_lat_longs)

    # save data
    with open('hotspots.csv', 'w', newline='') as f:
        for d in data:
            f.write(",".join(d) + '\n')


"""###################################################################################################"""


def get_random_limited_lat_long():
    # get a random number
    rand_num = random.randint(0, total)

    # if even, return some known places [lat, long]
    if rand_num % 2 == 0:
        return places_lat_longs[random.randint(0, places_lat_longs_length - 1)]

    # if odd, return a random city [lat, long]
    random_city = keys[rand_num]
    details = LocationParser.Cities_Details[random_city]
    return details['latitude'], details['longitude']


def create_random_confirmed_cases_sample(limit=5000):
    # header data
    data = [
        ['user_id', 'lat', 'long', 'date']
    ]

    # helping variables
    current_user_id = 0
    total_count = 0

    # loop until limit is reached
    while True:
        # create user id and increment it for next user
        user_id = f'user_{current_user_id}'
        current_user_id += 1

        # user rows count
        user_data_count = random.randint(1, 10)

        # check how many rows can we add
        slots_available = abs(limit - total_count)

        # limit reached
        if slots_available == 0:
            break

        # random count is more than available rows to add so we use the available row count instead
        if slots_available < user_data_count:
            user_data_count = slots_available

        # add to total rows count
        total_count += user_data_count

        # get random month
        m = f'0{random.randint(2, 8)}'

        # fill user rows
        for i in range(user_data_count):
            # random day
            tmp_d = random.randint(1, 31)
            d = tmp_d if tmp_d >= 10 else f'0{tmp_d}'

            # random [lat, long]
            lat, long = get_random_limited_lat_long()

            # add data
            data.append([
                user_id,
                lat,
                long,
                f'{d}-{m}-2020'
            ])

    # save data
    with open('confirmed_cases.csv', 'w', newline='') as f:
        for d in data:
            f.write(",".join(d) + '\n')


"""###################################################################################################"""

if __name__ == '__main__':
    create_random_places_samples()
    create_random_confirmed_cases_sample()
