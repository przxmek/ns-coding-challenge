import csv


def load_csv_data_dict(filename, encoding='utf-8'):
    with open(filename, encoding=encoding) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader, None)
        data = {}
        for h in headers:
            data[h] = []

        for row in csv_reader:
            for h, v in zip(headers, row):
                data[h].append(v)

        return data


def data_row(row_id, data):
    """ Get row from data
    :param row_id: Index of a row
    :param data: Data collection
    :return: A single row of data for given index
    """
    row = []
    headers = []
    for k, v in data.items():
        row.append(v[row_id])
        headers.append(k)

    return row, headers


def add_citystate_col(data):
    """ Add CITY_STATE combined (City, State) column

    :param data: data
    """
    size = len(data['NCESSCH'])
    city_state = []
    for i in range(size):
        row, columns = data_row(i, data)
        city_idx = columns.index('LCITY05')
        city = row[city_idx]
        state_idx = columns.index('LSTATE05')
        state = row[state_idx]
        city_state.append(f'{city}, {state}')

    data['CITY_STATE'] = city_state


def unique(column, data):
    """ Get count of unique items in a single column of data
    :param column: column name
    :param data: input list
    :return: unique items count in the specified column
    """
    return list(set(data[column]))


def unique_count(column, data):
    """ Get count of unique items in a single column of data
    :param column: column name
    :param data: input list
    :return: unique items count in the specified column
    """
    return len(set(data[column]))


def count_group_by(data, groupby_column):
    """
    Group by column and count items
    :param data: data
    :param groupby_column: column to group by
    :return: Dict with counts of each group value
    """
    size = len(data['NCESSCH'])
    groupby_result = {}

    for i in range(size):
        row, columns = data_row(i, data)
        group_idx = columns.index(groupby_column)
        group_val = row[group_idx]
        if group_val not in groupby_result:
            groupby_result[group_val] = 0
        groupby_result[group_val] += 1

    return groupby_result


def question1(data):
    # print("How many total schools are in this data set?")

    # NCESSCH - NCES school ID.
    # Each record includes a unique 12-character identifier for the school.
    # NCESSCH is unique for each row in the data.
    result = len(data['NCESSCH'])
    print(f'Total Schools: {result}')


def question2(data):
    # print("How many schools are in each state?")

    # LSTATE05 - Location USPS State Abbreviation

    states = count_group_by(data, 'LSTATE05')

    print(f'Schools by State:')
    # Sort dict keys for convenience
    for state in sorted(states):
        print(f'{state}: {states[state]}')


def question3(data):
    # print("How many schools are in each Metro-centric locale?")

    # MLOCALE - Metro-centric locale code (from 1 to 8, N - not assigned)

    metroc = count_group_by(data, 'MLOCALE')

    print(f'Schools by Metro-centric locale:')
    # Sort dict keys for convenience
    for metro in sorted(metroc):
        print(f'{metro}: {metroc[metro]}')


def question4(data):
    # print("What city has the most schools in it? How many schools does it have in it?")

    # LCITY05 - Location City Name
    # CITY_STATE - combined LCITY05, and LSTATE05
    cities = count_group_by(data, 'CITY_STATE')
    max_count = 0
    max_city = None
    for city, count in cities.items():
        if count > max_count:
            max_count = count
            max_city = city

    print(f'City with most schools: {max_city} ({max_count} schools)')


def question5(data):
    # print("How many unique cities have at least one school in it?")

    cities = count_group_by(data, 'CITY_STATE')

    # Find unique cities (city name that is unique)
    city_counts = {}
    city_states = [city.split(', ') for city in sorted(cities)]
    for row in city_states:
        if row[0] not in city_counts:
            city_counts[row[0]] = 0
        city_counts[row[0]] += 1

    unique_cities = {}
    for city, count in cities.items():
        city_name = city.split(', ')[0]
        if city_counts[city_name] == 1:
            unique_cities[city_name] = count

    print(f'Unique cities with at least one school: {len(unique_cities)}')


def compute_stats(data):
    question1(data)
    question2(data)
    question3(data)
    question4(data)
    question5(data)


def print_counts():
    data = load_csv_data_dict('school_data.csv', encoding='cp1252')
    add_citystate_col(data)

    compute_stats(data)


if __name__ == '__main__':
    print_counts()
