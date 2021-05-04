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

    dog_list = database['resources'].get_yaml('dogphotos.yml')
    photo_list = dog_list['$']
    for photo in photo_list:
        photo_ = database['photos'].get_for_id(photo['path'])
        output.add_image(photo_.get_id(), photo['caption'] if photo['caption'] else photo_.get_caption(), 'h', 152, True, photo_.get_image())
        output.add_plain(' ')
    output.end_container()


def get_root_artifact_list(database):
    return [('Фотографии', Path('photos'), generate_photos)]
