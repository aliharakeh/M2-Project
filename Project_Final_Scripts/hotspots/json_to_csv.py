import json
import pandas as pd

if __name__ == '__main__':
    with open('hotspots_locations.json', encoding='utf-8') as f:
        hotspots = json.loads(f.read())

    columns = ['date', 'prev_cases', 'new_cases', 'cases_diff', 'source', 'location', 'latitude', 'longitude', 'event']
    rows = []
    for date, details in hotspots.items():
        for location in details['locations']:
            rows.append([
                date,
                details['prev_cases'],
                details['new_cases'],
                details['cases_diff'],
                details['source'],
                location['place'],
                location['latitude'],
                location['longitude'],
                location['event']
            ])

    df = pd.DataFrame(rows, columns=columns)
    df.to_csv('hotspots.csv', index=False)
