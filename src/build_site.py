#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# build_site.py - a script that generates a site using per-section modules
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

from argparse import ArgumentParser
from database.photos import PhotoList
from pathlib import Path
import logging
import sass
from sections import dogs, main, photos, sale, shows
import shutil
import tools.document
import tools.resources


parser = ArgumentParser(description='Generate fontefideliti.ru content.')
parser.add_argument('src_dir', type=Path, help='path to a file database')

args = parser.parse_args()
resources = tools.resources.Input(args.src_dir)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def copy_static_files(input_directory):
    base = input_directory / 'img'
    shutil.copyfile(base / 'favicon.png', 'favicon.png')
    shutil.copyfile(base / 'background.png', Path('img', 'background.png'))


def generate_styles(resources):
    original = resources.get_string('common.scss')
    compiled = sass.compile(string=original, output_style='compressed')
    with open('common.css', 'w', encoding='utf-8') as output_file:
        output_file.write(compiled)


# Remove underscore after incorporating all photos into dog cards
photos_ = PhotoList(args.src_dir / 'img')

for generator in [dogs, main, photos, sale, shows]:
    artifacts = generator.get_root_artifact_list(resources, photos_)
    for title, path, generator, *extra in artifacts:
        path = path.with_suffix('.html' if path.stem == 'index' else '.htm')

        log.info('Generating %s...', path)
        output_document = tools.document.Document(title, path, resources, photos_)
        generator(output_document, resources, photos_, extra)
        html_content = output_document.finalize()

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as output:
            output.write(html_content)

log.info('Generating content-independend files...')
generate_styles(resources)
copy_static_files(args.src_dir)
