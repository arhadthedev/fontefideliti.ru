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


def generate_index(output_document, resources):
    dog_list = yaml.safe_load(resources.get('doglist.yml'))

    path = output_document.get_path()
    dog_id = path.split('/')[1]
    dog_info = dog_list[dog_id]

    output_document.start_container(['dog', 'card'])
    output_document.add_header(1, dog_info['name']['nom'])
    if dog_info.get('renter', ''):
        output_document.add_raw('<p><em>Находится в аренде. Владелец — {}</em></p>'.format(dog_info['renter']))
    if dog_info.get('is_long_hair', False):
        output_document.add_raw('<p>(длинношёрстная)</p>')
        output_document.add_raw('<p>Дата рождения: {% include date.html value=page.dob %}</p>')
        output_document.add_date(dog_info['dob'])
        output_document.add_raw('</p>')
    output_document.add_raw(dog_info['content'])

    output_document.start_paragraph()
    subsections = []
    photo_list = yaml.safe_load(resources.get('dogphotos.yml'))
    photos = photo_list.get(dog_id)
    if photos:
        subsections.append('<a href="photos.htm">Фотографии</a>')
    videos = dog_list[dog_id].get('videos', [])
    if videos:
        subsections.append('<a href="videos.htm">Видео</a>')
    subsections.append('<a href="shows.htm">Результаты выставок</a>')
    output_document.add_raw(' | '.join(subsections))

    output_document.start_paragraph()
    output_document.add_plain('Родословная: ')
    pedigree = []
    if dog_info['pedigree'].get('pd', ''):
        pedigree.append('<a href="http://www.pedigreedatabase.com/german_shepherd_dog/dog.html?id={}">Pedigree Database</a>'.format(dog_info['pedigree']['pd']))
    if dog_info['pedigree'].get('gsdog', ''):
        pedigree.append('<a href="http://database.gsdog.ru/dog.php?screen=1&amp;id={}" target="_blank">GSDOG</a>'.format(dog_info['pedigree']['gsdog']))
    output_document.add_raw(',<br>'.join(pedigree))

    if 'father' in dog_info:
        output_document.add_pedigree(dog_info, dog_list)

    output_document.add_raw(dog_info.get('content2', ''))
    output_document.end_container()


def get_dog_records_key(dog_list):
    def _key_generator(value):
        dog_id, dog_payload = value

        ordering_components = []
        next_component_id = dog_payload.get('after')
        if dog_id == next_component_id:
            raise ValueError('A record can not follow itself')
        while next_component_id:
            next_component = dog_list[next_component_id]
            ordering_components.append(next_component_id)
            next_component_id = next_component.get('after', '')
        ordering_components.reverse()
        return '>'.join(ordering_components)
    return _key_generator


def generate_list(output_document, resources):
    dog_list = yaml.safe_load(resources.get('doglist.yml'))

    path = output_document.get_path()
    gender = path.split('/')[0][:-1]
    dogs = [dog for dog in dog_list.items() if dog[1]['type'] in ['breeder', 'retired'] and dog[1]['gender'] == gender]
    dogs.sort(key=get_dog_records_key(dog_list))

    for dog_id, dog_info in dogs:
        output_document.start_container(css_classes=['compact', 'card'])
        output_document.add_raw('<span class="note">')
        if dog_info['type'] == 'retired':
            output_document.add_plain('Заслуженный ветеран')
        link = '<a href="/{}s/{}/">'.format(dog_info['gender'], dog_id)
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
    dogs = [dog for dog in dog_list.items() if dog[1]['type'] in ['breeder', 'retired']]
    for dog_id, dog_details in dogs:

        name = dog_details['name']
        base_url = '{}s/{}/'.format(dog_details['gender'], dog_id)

        section_pages.append((name['nom'], '{}index'.format(base_url), generate_index))

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
    section_pages.append(('Производительницы', 'females/index', generate_list))

    return section_pages
