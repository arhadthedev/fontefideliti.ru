#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import PIL
import sections.breeders
import sections.main
import sections.sale
import sections.shows
import sys
import tools.document


class Input(object):
    def __init__(self, base_path):
        self._base_path = base_path

    def get(self, rel_path):
        full_path = os.path.join(self._base_path, rel_path)
        return open(full_path, 'r', encoding='utf-8')

    def get_image(self, rel_path):
        full_path = os.path.join(self._base_path, 'img/{}.jpg'.format(rel_path))
        return PIL.Image.open(full_path)


if len(sys.argv) < 2:
    sys.exit('error: output directory path argument is not specified')
input_base_path = sys.argv[1]
resources = Input(input_base_path)

for generator in [sections.breeders, sections.main, sections.sale, sections.shows]:
    artifacts = generator.get_root_artifact_list(resources)
    for title, path, generator in artifacts:
        extension = 'html' if path.endswith('index') else 'htm'
        output_path = '{}.{}'.format(path, extension)
        output_document = tools.document.Document(title, output_path, resources)
        generator(output_document, resources)
        html_content = output_document.finalize()

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as output:
            output.write(html_content)
