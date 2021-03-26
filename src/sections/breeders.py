# -*- coding: UTF-8 -*-
# breeders.py - generates content of /females and /males
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

import yaml

def generate_photos(output_document, resources):
    output_document.start_container()

    dog_list = yaml.safe_load(resources.get('doglist.yml'))

    path = output_document.get_path()
    dog_id = path.split('/')[1]
    name = dog_list[dog_id]['name']
    output_document.add_raw('<h1>Фото <a href=".">{}</a></h1>'.format(name['gen']))

    photo_list = yaml.safe_load(resources.get('dogphotos.yml'))
    photos = photo_list.get(dog_id)
    for photo in photos:
        photo['caption'] = photo['caption'] if photo['caption'] != None else ''
        output_document.add_image(photo['path'], photo['caption'], 'h', 152, is_clickable=True)
    output_document.end_container()


def generate_videos(output_document, resources):
    output_document.start_container()

    dog_list = yaml.safe_load(resources.get('doglist.yml'))

    path = output_document.get_path()
    dog_id = path.split('/')[1]
    name = dog_list[dog_id]['name']

    youtube_ids = dog_list[dog_id].get('videos')
    for video_id in youtube_ids:
        youtube_id, *title = video_id.split(' ', 1)
        if title:
            output_document.add_header(3, title[0])
        output_document.add_raw('<p>')
        output_document.add_raw('<iframe width="560" height="315" src="https://www.youtube.com/embed/{}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'.format(video_id))
    output_document.end_container()


def get_root_artifact_list(resources):
    section_pages = []

    dog_list = yaml.safe_load(resources.get('doglist.yml'))
    photo_list = yaml.safe_load(resources.get('dogphotos.yml'))
    for dog_id, dog_details in dog_list.items():
        name = dog_details['name']
        base_url = '{}s/{}/'.format(dog_details['gender'], dog_id)

        photos = photo_list.get(dog_id)
        if photos:
            title = "Фото {}".format(name['gen'])
            page = (title, '{}/photos'.format(base_url), generate_photos)
            section_pages.append(page)

        youtube_ids = dog_details.get('videos')
        if youtube_ids:
            title = "Видео {}".format(name['gen'])
            page = (title, '{}/videos'.format(base_url), generate_videos)
            section_pages.append(page)

    return section_pages
