# -*- coding: UTF-8 -*-
# shows.py - maintains information about shows
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

import yaml


class ShowList:
    def __init__(self, resources):
        self._shows = resources.get_yaml('shows.yml')
