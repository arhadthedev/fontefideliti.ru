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
from database.shows import ShowList
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


database = {}
database['photos'] = PhotoList(args.src_dir / 'img')
database['resources'] = resources # Until the whole database is introduced
database['shows'] = ShowList(resources)

documents = []
for generator in [dogs, main, photos, sale, shows]:
    artifacts = generator.get_root_artifact_list(database)
    for title, path, generator, *extra in artifacts:
        path = path.with_suffix('.html' if path.stem == 'index' else '.htm')

        log.info('Generating %s...', path)
        output_document = tools.document.Document(title, path, database)
        generator(output_document, database, extra)
        output_document.end_document()
        documents.append((output_document, path))

rewrite_existing = False
database['photos'].keep_generation_promises(rewrite_existing)

for document, path in documents:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as output:
        serialized_content = str(document)
        output.write(serialized_content)

log.info('Generating content-independend files...')
generate_styles(resources)
copy_static_files(args.src_dir)
