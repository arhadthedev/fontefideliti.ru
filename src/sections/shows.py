# -*- coding: UTF-8 -*-
# shows.py - generates content of /shows
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

from collections import OrderedDict
from datetime import date
from pathlib import Path
import re
import tools.shows

def generate_shows(output_document, resources, photos, extra):
    output_document.start_list(css_classes=['cards'])

    for year, photo in extra[0]:
        output_document.start_list_item()
        output_document.add_raw('<a href="{0}.htm">{0} '.format(year))
        output_document.add_image(photo.get_id(), photo.get_caption(), 'h', 152, False, photo.get_image())
        output_document.add_raw('</a>')
        output_document.end_list_item()
    output_document.end_list()


def generate_legacy_year_page(output_document, resources, year):
    source = resources.get_string('../_shows/{}.htm'.format(year))

    end_of_frontmatter = source.find('---', 1) + 3
    source = source[end_of_frontmatter:]

    output_document.start_container(css_classes=['card'])
    source = re.sub(r'<a href="/img/([^.]+).jpg" title="([^"]+)" rel="a"><img [^<]+</a>',
                    r'{% include photo.html path="\1" title="\2" %}',
                    source)
    matches = re.findall(r'([^{]*){% include photo.html path="([^"]*)" title="([^"]*)" [^%]*%}', source)
    if not matches:
        output_document.add_raw(source)
    for rest, path, title in matches:
        output_document.add_raw(rest)
        output_document.add_image(path, title, 'h', 152, is_clickable=True)
    output_document.end_container()


def human_date(date):
    month_names = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    return '{} {} {} г.'.format(date.day, month_names[date.month - 1], date.year)


def generate_year_page(output_document, resources, photos, extra):
    displayed_year = extra[0]
    if displayed_year == 2016:
        generate_legacy_year_page(output_document, resources, displayed_year)
        return

    show_list = resources.get_yaml('shows.yml')
    all_experts = resources.get_yaml('people.yml')
    dogs = resources.get_yaml('doglist.yml')

    output_document.start_container(css_classes=['card'])
    displayed_dates = [(date, events) for (date, events) in show_list.items() if date.year == displayed_year]
    displayed_dates.sort(key=lambda x: x[0], reverse=True)
    for date, events in displayed_dates:
        gallery = OrderedDict()
        for event in events:
            output_document.add_raw('<h2 style="font-size: 90%">')
            output_document.add_date(date)
            experts = tools.shows.get_experts(event, all_experts)
            normalized_rank = event['rank'][0].upper() + event['rank'][1:]
            output_document.add_raw(', {}, {} выставка, {}</h2>'.format(event['city'], normalized_rank, experts))
            for dog_id, dog_performance in event['dogs'].items():
                dog_details = dogs[dog_id]

                output_document.add_raw('<p style="text-align: left"><strong>')
                output_document.add_plain(dog_details['name']['nom'])
                output_document.add_raw('</strong>')
                if 'longhair' in dog_details and dog_details['longhair']:
                    output_document.add_raw(' (д/ш),')
                output_document.add_raw(' класс ')
                output_document.add_plain(dog_performance['class'])
                output_document.add_raw(', ')
                place = dog_performance['place'].replace(' ', ' ', 1)
                achievements = tools.shows.stringify_title_list(dog_performance.get('achievements', []))
                if achievements:
                    place = '{}, {}'.format(place, achievements)
                output_document.add_plain(place)
                output_document.add_raw('</p>')

                if 'photos' in dog_performance:
                    photos2 = dog_performance['photos']
                    for photo in photos2:
                        if photo['path'] not in gallery:
                            gallery[photo['path']] = photo['caption']

        output_document.add_raw('<p>')
        photo_gallery = photos.get_for_date(date)
        for photo in photo_gallery:
            dog_ids = photo.get_attributes()['dogs']
            dog_names = [dogs[i]['name']['nom'] for i in dog_ids]
            glued_dog_names = ', '.join(dog_names)
            caption = '{}, г. {}, {}'.format(glued_dog_names, event['city'], human_date(date))
            photo.set_caption(caption)
            output_document.add_image(photo.get_id(), photo.get_caption(), 'h', 152, True, photo.get_image())
            output_document.add_plain(' ')

        for path, caption in gallery.items():
            output_document.add_image(path, caption, 'h', 152, True)
            output_document.add_plain(' ')
        output_document.add_raw('</p>')

        output_document.add_raw('<hr>')
    output_document.end_container()


def get_root_artifact_list(resources, photos):
    section_pages = []
    year_list = []

    shows = Path('shows')
    FIRST_SHOW_YEAR = 2010
    for year in range(date.today().year, FIRST_SHOW_YEAR - 1, -1):
        photo = photos.get_for_attribute('t=', year)
        if photo:
            section_pages.append(('Выставки {} года'.format(year), shows / str(year), generate_year_page, year))
            year_list.append((year, photo[0]))

    section_pages.append(('Выставки', shows / 'index', generate_shows, year_list))

    return section_pages

