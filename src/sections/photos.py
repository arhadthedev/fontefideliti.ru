# -*- coding: UTF-8 -*-
# photos.py - generates content of /photos.htm
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

def generate_photos(output, resources, photos, extra):
    output.start_container()
    output.add_header(1, 'Фотографии всех наших собак')

    dog_list = resources.get_yaml('dogphotos.yml')
    photo_list = dog_list['$']
    for photo in photo_list:
        output.add_image(photo['path'], photo['caption'], 'h', 152, is_clickable=True)
        output.add_plain(' ')
    output.end_container()


def get_root_artifact_list(resources):
    return [('Фотографии', 'photos', generate_photos)]
