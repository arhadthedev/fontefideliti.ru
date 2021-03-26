# -*- coding: UTF-8 -*-
# shows.py - generates content of /shows.htm
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

import yaml

def generate_shows(output_document, resources):
    per_year_list_raw = resources.get('shows.yml')
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

def get_root_artifact_list(resources):
    section_pages = [('Выставки', 'shows/index', generate_shows)]
    return section_pages

