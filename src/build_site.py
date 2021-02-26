#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import dogs.section_breeders
import os
import sys


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


resources = Input('res')
output = Output(sys.argv[1])

dogs.section_breeders.generate_section(output, resources)
