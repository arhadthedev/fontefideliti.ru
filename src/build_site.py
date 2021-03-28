#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import PIL
import sections.breeders
import sections.main
import sections.photos
import sections.sale
import sections.shows
import shutil
import sys
import tools.document


class Input(object):
    def __init__(self, base_path):
        self._base_path = base_path

    def get(self, rel_path):
        full_path = os.path.join(self._base_path, rel_path)
        return open(full_path, 'r', encoding='utf-8')

    def get_image(self, rel_path):
        full_path = os.path.join(self._base_path, rel_path)
        return PIL.Image.open(full_path)


def _copy_missing_recursive(entries, src, dst):
    os.makedirs(dst, exist_ok=True)

    for srcentry in entries:
        srcname = os.path.join(src, srcentry.name)
        dstname = os.path.join(dst, srcentry.name)
        if srcentry.is_dir():
            copy_missing_recursive(srcentry, dstname)
        else:
            if not os.path.exists(dstname):
                shutil.copy2(srcentry, dstname)


def copy_missing_recursive(src, dst):
    with os.scandir(src) as itr:
        entries = list(itr)
    _copy_missing_recursive(entries, src, dst)


def copy_static_files(input_directory):
    base = os.path.join(input_directory, 'img/')
    shutil.copyfile('{}favicon.png'.format(base), 'favicon.png')
    shutil.copyfile('{}background.png'.format(base), 'img/background.png')
    copy_missing_recursive(base, 'img')


if len(sys.argv) < 2:
    sys.exit('error: output directory path argument is not specified')
input_base_path = sys.argv[1]
resources = Input(input_base_path)

for generator in [sections.breeders, sections.main, sections.photos, sections.sale, sections.shows]:
    artifacts = generator.get_root_artifact_list(resources)
    for title, path, generator in artifacts:
        extension = 'html' if path.endswith('index') else 'htm'
        output_path = '{}.{}'.format(path, extension)
        output_document = tools.document.Document(title, output_path, resources)
        generator(output_document, resources)
        html_content = output_document.finalize()

        output_directory = os.path.dirname(output_path)
        if output_directory:
            os.makedirs(output_directory, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as output:
            output.write(html_content)

copy_static_files(input_base_path)
