import json

if __name__ == '__main__':
    with open('hotspots_cleaned.json', encoding='utf-8') as f:
        hotspots = json.loads(f.read())

    with open('removed_topics.txt', encoding='utf-8') as f:
        removed_topics = [w.strip().lower() for w in f.read().split('\n')]

    final_hotspots = {}
    for date, hotspot in hotspots.items():
        final_hotspots[date] = {
            **hotspot,
            'trends': []
        }
        for trend in hotspot['trends']:
            topic = trend['topic'].lower().strip()
            if topic in removed_topics:
                continue
            final_hotspots[date]['trends'].append({
                'topic': trend['topic'],
                'link': trend['link'],
                'tweets': list(set(trend['tweets']))
            })

    with open('hotspots_cleaned_v2.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(final_hotspots, indent=2, ensure_ascii=False))
