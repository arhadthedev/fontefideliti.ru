# -*- coding: UTF-8 -*-
# text_chunks.py - text placeholders that may be reconfigured from external code
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.


class DynamicText:
    def __init__(self):
        self._content = ''


    def set_content(self, new_content):
        self._content = new_content


    def __str__(self):
        return self._content


class ConditionalText:
    def __init__(self, content):
        self._condition = False
        self._content = content


    def trigger_condition(self):
        self._condition = True


    def __str__(self):
        return self._content if self._condition else ''


