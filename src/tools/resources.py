# -*- coding: UTF-8 -*-
# resources.py - manages content of a directory with source resources
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

import os
import PIL
import yaml

class Input(object):
    def __init__(self, base_path):
        self._base_path = base_path
        self._cached_parsed_resources = {}


    def get_string(self, rel_path):
        full_path = os.path.join(self._base_path, rel_path)
        with open(full_path, 'r', encoding='utf-8') as file:
            return file.read()


    # All modifications of the returned object will be observable by the
    # following calls of get_yaml() with the same rel_path.
    def get_yaml(self, rel_path):
        full_path = os.path.join(self._base_path, rel_path)
        if not rel_path in self._cached_parsed_resources:
            with open(full_path, 'r', encoding='utf-8') as file:
               self._cached_parsed_resources[rel_path] = yaml.safe_load(file)
        return self._cached_parsed_resources[rel_path]


    def get_image(self, rel_path):
        full_path = os.path.join(self._base_path, rel_path)
        return PIL.Image.open(full_path)
