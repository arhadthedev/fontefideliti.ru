# -*- coding: UTF-8 -*-
# shows.py - generates content of /shows.htm
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

import re
import yaml

def generate_shows(output_document, resources):
    per_year_list_raw = resources.get('show_years.yml')
    per_year_list = yaml.safe_load(per_year_list_raw)

    for year_entry in reversed(per_year_list):
        year = year_entry['год']
        photocard = year_entry['фотокарточка']
        caption = year_entry['подпись']

        output_document.start_container(css_classes=['card', 'compact'])
        output_document.add_raw('<a href="{0}.htm"><h3>{0}</h3>'.format(year))
        output_document.add_image(photocard, caption, 'h', 152, False)
        output_document.add_raw('</a>')
        output_document.end_container()


def generate_year_page(output_document, resources):
    path = output_document.get_path()
    year = path.split('/')[1]
    source = resources.get('../_shows/{}'.format(year)).read()

    end_of_frontmatter = source.find('---', 1) + 3
    source = source[end_of_frontmatter:]

    first_image = source.find('{%')
    output_document.add_raw(source[:first_image])

    matches = re.findall(r'{% include photo.html path="([^"]*)" title="([^"]*)"([^{]*)', source)
    for path, title, rest in matches:
        output_document.add_image(path, title, 'h', 152, is_clickable=True)
        output_document.add_raw(rest)


def get_root_artifact_list(resources):
    section_pages = [('Выставки', 'shows/index', generate_shows)]

    per_year_list_raw = resources.get('show_years.yml')
    per_year_list = yaml.safe_load(per_year_list_raw)
    for year_entry in per_year_list:
        year = year_entry['год']
        section_pages.append(('Выставки {} года'.format(year), 'shows/{}'.format(year), generate_year_page))

    return section_pages

