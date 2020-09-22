from google_maps.google_maps import search_google_maps
import json
import time

if __name__ == '__main__':
    with open('hotspots.json', encoding='utf-8') as f:
        hotspots = json.loads(f.read())

    hotspots_locations = {}

    # iterate hotspots
    for date, hotspot in hotspots.items():
        hotspots_locations[date] = {}

        # iterate trends
        for trend in hotspot['trends']:
            hotspots_locations[date][trend['topic']] = []

            # iterate tweets
            for tweet in trend['tweets']:
                # split text into words
                words = tweet.split()

                # check if any word refers to a location
                for word in words:
                    place = search_google_maps(word)
                    if place:
                        hotspots_locations[date][trend].append(place)

                    time.sleep(1)

        if input('Continue? [y/n]') != 'y':
            break

    with open('hotspots_locations.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(hotspots_locations, indent=2, ensure_ascii=False))
