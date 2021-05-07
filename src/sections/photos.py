# -*- coding: UTF-8 -*-
# photos.py - generates content of /photos.htm
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

from pathlib import Path

def generate_photos(output, database, extra):
    output.start_container()
    output.add_header(1, 'Фотографии всех наших собак')

    photos = database['photos'].get_card_assignation('allphotos', multiphoto_group=True)
    for photo in photos:
        output.add_image(photo, 'h', 152, is_clickable=True)
        output.add_plain(' ')
    output.end_container()


def get_root_artifact_list(database):
    return [('Фотографии', Path('photos'), generate_photos)]
