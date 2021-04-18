#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# build_site.py - a script that generates a site using per-section modules
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

from database.photos import PhotoList
import os
import scss.compiler
import sections.dogs
import sections.main
import sections.photos
import sections.sale
import sections.shows
import shutil
import sys
import tools.document
import tools.resources


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


if len(sys.argv) < 2:
    sys.exit('error: output directory path argument is not specified')
input_base_path = sys.argv[1]
resources = tools.resources.Input(input_base_path)

photos = PhotoList(os.path.join(input_base_path, 'img'))

for generator in [sections.dogs, sections.main, sections.photos, sections.sale, sections.shows]:
    artifacts = generator.get_root_artifact_list(resources)
    for title, path, generator in artifacts:
        extension = 'html' if path.endswith('index') else 'htm'
        output_path = '{}.{}'.format(path, extension)
        print('Generating {}...'.format(output_path), file=sys.stderr)
        output_document = tools.document.Document(title, output_path, resources)
        generator(output_document, resources, photos)
        html_content = output_document.finalize()

        output_directory = os.path.dirname(output_path)
        if output_directory:
            os.makedirs(output_directory, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as output:
            output.write(html_content)

print('Generating content-independend files...', file=sys.stderr)
generate_styles(resources)
copy_static_files(input_base_path)
