# -*- coding: UTF-8 -*-
# shows.py - generates content of /shows
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

from collections import OrderedDict
import re
import tools.shows

def generate_shows(output_document, resources):
    per_year_list = resources.get_yaml('show_years.yml')

    for year_entry in reversed(per_year_list):
        year = year_entry['год']
        photocard = year_entry['фотокарточка']
        caption = year_entry['подпись']

        output_document.start_container(css_classes=['card', 'compact'])
        output_document.add_raw('<a href="{0}.htm"><h3>{0}</h3>'.format(year))
        output_document.add_image(photocard, caption, 'h', 152, False)
        output_document.add_raw('</a>')
        output_document.end_container()


def generate_legacy_year_page(output_document, resources):
    path = output_document.get_path()
    year = path.split('/')[1]
    source = resources.get_string('../_shows/{}'.format(year))

    end_of_frontmatter = source.find('---', 1) + 3
    source = source[end_of_frontmatter:]

    output_document.start_container(css_classes=['card'])
    matches = re.findall(r'([^{]*){% include photo.html path="([^"]*)" title="([^"]*)" [^%]*%}', source)
    if not matches:
        output_document.add_raw(source)
    for rest, path, title in matches:
        output_document.add_raw(rest)
        output_document.add_image(path, title, 'h', 152, is_clickable=True)
    output_document.end_container()


def generate_year_page(output_document, resources):
    path = output_document.get_path()
    file_name = path.split('/')[1]
    displayed_year = int(file_name[0:4])
    if displayed_year != 2021:
        generate_legacy_year_page(output_document, resources)
        return

    show_list = resources.get_yaml('shows.yml')
    all_experts = resources.get_yaml('people.yml')
    dogs = resources.get_yaml('doglist.yml')

    output_document.start_container(css_classes=['card'])
    displayed_dates = [(date, events) for (date, events) in show_list.items() if date.year == displayed_year]
    displayed_dates.sort(key=lambda x: x, reverse=True)
    gallery = OrderedDict()
    for date, events in reversed(displayed_dates):
        for event in events:
            output_document.add_raw('<h2 style="font-size: 90%">')
            output_document.add_date(date)
            experts = tools.shows.get_experts(event, all_experts)
            normalized_rank = event['rank'][0].upper() + event['rank'][1:]
            output_document.add_raw(', г. {}, {} выставка, {}</h2>'.format(event['city'], normalized_rank, experts))
            for dog_id, dog_performance in event['dogs'].items():
                dog_details = dogs[dog_id]

                output_document.add_raw('<p style="text-align: left"><strong>')
                output_document.add_plain(dog_details['name']['nom'])
                output_document.add_raw('</strong>, класс ')
                output_document.add_plain(dog_performance['class'])
                output_document.add_raw(', ')
                place = dog_performance['place'].replace(' ', ' ', 1)
                achievements = tools.shows.stringify_title_list(dog_performance['achievements'])
                if achievements:
                    place = '{}, {}'.format(place, achievements)
                output_document.add_plain(place)
                output_document.add_raw('</p>')

                if 'photos' in dog_performance:
                    photos = dog_performance['photos']
                    for photo in photos:
                        if photo['path'] not in gallery:
                            gallery[photo['path']] = photo['caption']

        output_document.add_raw('<p>')
        for path, caption in gallery.items():
            output_document.add_image(path, caption, 'h', 152, True)
            output_document.add_plain(' ')
        output_document.add_raw('</p>')

        output_document.add_raw('<hr>')
    output_document.end_container()


def get_root_artifact_list(resources):
    section_pages = [('Выставки', 'shows/index', generate_shows)]

    per_year_list = resources.get_yaml('show_years.yml')
    for year_entry in per_year_list:
        year = year_entry['год']
        section_pages.append(('Выставки {} года'.format(year), 'shows/{}'.format(year), generate_year_page))

    return section_pages

