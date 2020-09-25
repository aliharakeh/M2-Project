import json

count = 0
with open('hotspots_cleaned.json', encoding='utf-8') as f:
    hotspots = json.loads(f.read())
    for date, hotspot in hotspots.items():
        for trend in hotspot['trends']:
            for tweet in list(set(trend['tweets'])):
                if tweet:
                    count += 1

print(count)
