#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
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


if len(sys.argv) < 2:
    sys.exit('error: output directory path argument is not specified')
output_base_path = sys.argv[1]

resources = Input('res')

for generator in [sections.breeders, sections.main, sections.sale, sections.shows]:
    artifacts = generator.get_root_artifact_list(resources)
    for title, path, generator in artifacts:
        extension = 'html' if path.endswith('index') else 'htm'
        output_path = '{}.{}'.format(path, extension)
        output_document = tools.document.Document(title, output_path, output_base_path)
        generator(output_document, resources)
        html_content = output_document.finalize()

        path = os.path.join(output_base_path, output_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as output:
            output.write(html_content)
