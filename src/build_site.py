#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import dogs.section_breeders
import os
import sys
import tools.document


class Input(object):
    def __init__(self, base_path):
        self._base_path = base_path

    def get(self, rel_path):
        full_path = os.path.join(self._base_path, rel_path)
        return open(full_path, 'r', encoding='utf-8')


class Output(object):
    def __init__(self, base_path):
        self._base_path = base_path

    def create_file(self, rel_path):
        full_path = os.path.join(self._base_path, rel_path)
        if not os.path.exists(os.path.dirname(full_path)):
            os.makedirs(os.path.dirname(full_path))
        return open(full_path, 'w', encoding='utf-8')


if len(sys.argv) < 2:
    sys.exit('error: output directory path argument is not specified')
output_base_path = sys.argv[1]

resources = Input('res')
output = Output(sys.argv[1])

dogs.section_breeders.generate_section(output, resources)

for generator in []:
    artifacts = generator.get_root_artifact_list()
    for title, path, generator in artifacts:
        output_path = '{}.htm'.format(path)
        output_document = tools.document.Document(title, output_path)
        generator(output_document, resources)
        html_content = output_document.finalize()

        path = os.path.join(output_base_path, output_path)
        with open(path, 'w', encoding='utf-8') as output:
            output.write(html_content)
