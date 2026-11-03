#!/usr/bin/env python3
"""Check the built publication list against the captured Scholar inventory."""
import json
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class PublicationPage(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.cards, self.links, self.images = [], [], []
        self.current = None
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'article' and 'data-paper' in values:
            self.current = {
                'slug': values.get('data-slug'),
                'ids': values.get('data-scholar-ids', '').split(),
                'images': [],
                'publishedAt': values.get('data-published-at'),
                'times': [],
            }
        if tag == 'time' and self.current is not None:
            self.current['times'].append(values.get('datetime'))
        if tag == 'img':
            source = values.get('src')
            self.images.append(source)
            if self.current is not None:
                self.current['images'].append(source)
                assert values.get('alt'), 'Publication image needs alt text'
        if tag == 'a':
            self.links.append(values.get('href', ''))

    def handle_endtag(self, tag):
        if tag == 'article' and self.current is not None:
            self.cards.append(self.current)
            self.current = None


def main():
    snapshot = json.loads((ROOT / 'src/data/scholar-records.json').read_text())
    image_index = json.loads((ROOT / 'src/data/publication-images.json').read_text())
    date_index = json.loads((ROOT / 'src/data/publication-dates.json').read_text())
    assert set(date_index) == set(image_index), 'Publication date inventory does not cover all works'
    expected_ids = {record['scholarUrl'].rsplit(':', 1)[1] for record in snapshot['records']}
    assert len(expected_ids) == len(snapshot['records']), 'Duplicate IDs in Scholar source inventory'

    page_orders = []
    for relative in ['index.html', 'research/index.html']:
        page = PublicationPage((ROOT / 'dist' / relative).read_text())
        counts = Counter(item for card in page.cards for item in card['ids'])
        assert set(counts) == expected_ids, (
            f'{relative}: missing {expected_ids - set(counts)}, unexpected {set(counts) - expected_ids}'
        )
        assert all(count == 1 for count in counts.values()), f'{relative}: Scholar records counted twice'
        assert {card['slug'] for card in page.cards} == set(image_index), f'{relative}: omitted or extra work'
        assert len(page.cards) == len(image_index), f'{relative}: repeated work'
        order = [card['slug'] for card in page.cards]
        page_orders.append(order)
        assert order[:2] == ['seed-2-1', 'seed-2-0'], f'{relative}: requested Seed report order changed'
        months = [card['publishedAt'] for card in page.cards[2:]]
        assert months == sorted(months, reverse=True), f'{relative}: other publications are not newest first by month'
        for card in page.cards:
            record = image_index[card['slug']]
            expected_image = record.get('thumbnail', record)['src']
            assert card['images'] == [expected_image], f'{relative}: incorrect figure for {card["slug"]}'
            expected_month = date_index[card['slug']]['month']
            assert card['publishedAt'] == expected_month, f'{relative}: incorrect publication month for {card["slug"]}'
            assert card['times'] == [expected_month], f'{relative}: publication month is not displayed'
            assert date_index[card['slug']]['sources'], f'{card["slug"]}: date source missing'

    assert page_orders[0] == page_orders[1], 'Home and research use different publication orders'

    for slug, image in image_index.items():
        detail = PublicationPage((ROOT / 'dist/research' / slug / 'index.html').read_text())
        assert image['src'] in detail.images, f'{slug}: figure missing on detail page'
        assert image['source'] in detail.links, f'{slug}: original source credit missing'

    home = PublicationPage((ROOT / 'dist/index.html').read_text())
    projects = PublicationPage((ROOT / 'dist/projects/index.html').read_text())
    assert '/projects/stethoscope/' not in home.links, 'Stethoscope still promoted on homepage'
    assert '/projects/stethoscope/' in projects.links, 'Secondary project link missing'
    assert (ROOT / 'dist/projects/stethoscope/index.html').is_file(), 'Stethoscope detail page missing'
    print(f'PASS: all {len(expected_ids)} Scholar records covered once in {len(image_index)} illustrated works on both home and research pages.')
    print('PASS: original image credits preserved; stethoscope available only through secondary navigation.')
    print('PASS: home and research share the requested Seed report priority; all other work is newest first by publication month, with visible dates.')


if __name__ == '__main__':
    main()
