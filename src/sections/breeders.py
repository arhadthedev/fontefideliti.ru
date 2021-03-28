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
        output_document.add_plain(' ')
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


def generate_list(output_document, resources):
    dog_list = yaml.safe_load(resources.get('doglist.yml'))

    path = output_document.get_path()
    gender = path.split('/')[0][:-1]

    for dog_id, dog_info in [dog for dog in dog_list.items() if dog[1]['gender'] == gender]:
        output_document.start_container(css_classes=['compact', 'card'])
        output_document.add_raw('<span class="note">')
        if dog_info.get('is_veteran', False):
            output_document.add_plain('Заслуженный ветеран')
        link = '<a href="/{}/{}/">'.format(dog_info['gender'], dog_id)
        output_document.add_raw('</span>')
        output_document.add_raw('<h1>{}{}</a></h1>'.format(link, dog_info['name']['nom']))
        output_document.add_raw(link)
        caption = 'Фотография {}'.format(dog_info['name']['gen'])
        output_document.add_image(dog_info['photo'], dog_info['name']['nom'], 'w', 200, is_clickable=False)
        output_document.add_raw('</a>')
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

    section_pages.append(('Производители', 'males/index', generate_list))

    return section_pages
