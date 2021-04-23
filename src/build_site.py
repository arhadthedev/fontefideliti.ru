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
import os
from pathlib import Path
import scss.compiler
from sections import dogs, main, photos, sale, shows
import shutil
import sys
import tools.document
import tools.resources


parser = ArgumentParser(description='Generate fontefideliti.ru content.')
parser.add_argument('src_dir', type=Path, help='path to a file database')

args = parser.parse_args()
resources = tools.resources.Input(args.src_dir)


def copy_static_files(input_directory):
    base = os.path.join(input_directory, 'img/')
    shutil.copyfile('{}favicon.png'.format(base), 'favicon.png')
    shutil.copyfile('{}background.png'.format(base), 'img/background.png')


def generate_styles(resources):
    compiler = scss.Scss(scss_opts={'compress': True})
    original_styles = resources.get_string('common.scss')
    compiled_styles = compiler.compile(original_styles)
    with open('common.css', 'w', encoding='utf-8') as output_file:
        output_file.write(compiled_styles)


# Remove underscore after incorporating all photos into dog cards
photos_ = PhotoList(args.src_dir / 'img')

for generator in [dogs, main, photos, sale, shows]:
    artifacts = generator.get_root_artifact_list(resources)
    for title, path, generator in artifacts:
        extension = 'html' if path.endswith('index') else 'htm'
        output_path = '{}.{}'.format(path, extension)
        print('Generating {}...'.format(output_path), file=sys.stderr)
        output_document = tools.document.Document(title, output_path, resources, photos_)
        generator(output_document, resources, photos_)
        html_content = output_document.finalize()

        output_directory = os.path.dirname(output_path)
        if output_directory:
            os.makedirs(output_directory, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as output:
            output.write(html_content)

print('Generating content-independend files...', file=sys.stderr)
generate_styles(resources)
copy_static_files(args.src_dir)
