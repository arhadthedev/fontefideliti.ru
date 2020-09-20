#!/usr/bin/env python

# build.py - builds /index.html into a folder passed as the first argument
#
# Copyright (c) 2020 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

import os.path
from page_layout import Layout
from snippets import *
import yaml
import sys

config_file = open('database/shows.yml', 'r', encoding='utf-8')
per_year_list = yaml.safe_load(config_file)

list_layout = Layout('shows', 'Выставки')

for year_entry in reversed(per_year_list):
    year = year_entry['год']
    photocard = year_entry['фотокарточка']
    caption = year_entry['подпись']

    card = (f'<h3><a href="{year}.htm">{year}</a></h3>'
            f'<a href="{year}.htm">{make_image(photocard, caption)}</a>')
    list_layout.add(card, element='article', classes=['card', 'compact'])

if len(sys.argv) < 2:
    sys.exit('error: output directory path argument is not specified')
path = os.path.join(sys.argv[1], 'shows/index.html')
output = open(path, 'w', encoding='utf-8')
output.write(list_layout.get_html())


show2020_layout = Layout('shows', 'Выставки 2020 года')
