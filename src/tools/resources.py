# -*- coding: UTF-8 -*-
# resources.py - manages content of a directory with source resources
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

import os
import PIL

class Input(object):
    def __init__(self, base_path):
        self._base_path = base_path


    def get(self, rel_path):
        full_path = os.path.join(self._base_path, rel_path)
        return open(full_path, 'r', encoding='utf-8')


    def get_image(self, rel_path):
        full_path = os.path.join(self._base_path, rel_path)
        return PIL.Image.open(full_path)
