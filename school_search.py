import csv
import time

US_STATES = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AS": "American Samoa",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "District Of Columbia",
    "FM": "Federated States Of Micronesia",
    "FL": "Florida",
    "GA": "Georgia",
    "GU": "Guam",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MH": "Marshall Islands",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "MP": "Northern Mariana Islands",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PW": "Palau",
    "PA": "Pennsylvania",
    "PR": "Puerto Rico",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VI": "Virgin Islands",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
    # One row in the data has state = 'C'
    "C": "District Of Columbia",
}


def print_row(data, row_idx, position):
    print(f"{position}. {data['SCHNAM05'][row_idx]}")
    print(f"{data['LCITY05'][row_idx]}, {data['LSTATE05'][row_idx]}")


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
    """ Get a single row of data by row ID
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


def preprocess(data):
    search_columns = ['SCHNAM05', 'LCITY05', 'LSTATE05']

    redundant_cols = [col_name for col_name in data.keys() if col_name not in search_columns]

    for redundant_col in redundant_cols:
        del data[redundant_col]

    return data


def word_count_search(seed, data, top=3):
    size = len(data['SCHNAM05'])
    results = []
    for i in range(size):
        row, columns = data_row(i, data)
        txt = row[columns.index('SCHNAM05')].lower()

        city = row[columns.index('LCITY05')].lower()
        state_code = row[columns.index('LSTATE05')]
        if state_code in US_STATES:
            state = US_STATES[state_code].lower()
        else:
            state = 'unknown'

        seed_words = seed.split()
        txt_words = txt.split()
        city_words = city.split()
        state_words = state.split()

        txt_matches = 0
        city_matches = 0
        state_matches = 0
        miss_matches = 0

        for word in seed_words:
            if word in ['school', 'elementary']:
                score = 0.5
            else:
                score = 1.0

            if word in city_words:
                city_matches = score
                score -= 0.5
            if word in state_words:
                state_matches = score
                score -= 0.5
            if word in txt_words:
                txt_matches += score

            if word not in txt_words and word not in city_words and word not in state_words:
                miss_matches += 1

        score = txt_matches + city_matches + state_matches - miss_matches
        # Bonus for match in name, city, and state
        if txt_matches > 0 and city_matches > 0 and state_matches > 0:
            score += 1
        # Bonus for match in two out of three
        elif (txt_matches > 0 and city_matches) or (txt_matches > 0 and state_matches):
            score += 0.5

        results.append({
            'score': score,
            'entry_idx': i
        })

    sorted_results = sorted(results, key=lambda k: k['score'], reverse=True)

    return [res for res in sorted_results[:top] if res['score'] > 0]


def search_schools(seed):
    # Load data & preprocess
    data = load_csv_data_dict('school_data.csv', encoding='cp1252')
    search_data = preprocess(data)

    start_time = time.time()

    results = word_count_search(seed.lower(), search_data)

    search_time = time.time() - start_time
    print(f'Results for "{seed}" (search took: {search_time}s)')
    for i in range(len(results)):
        print_row(search_data, results[i]['entry_idx'], i + 1)
        # print('score: ' + str(results[i]['score']))


if __name__ == '__main__':
    search_schools("elementary school highland park")
    search_schools("jefferson belleville")
    search_schools("riverside school 44")
    search_schools("granada charter school")
    search_schools("foley high alabama")
    search_schools("KUSKOKWIM")
