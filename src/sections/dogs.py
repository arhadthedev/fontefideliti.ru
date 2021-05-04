# -*- coding: UTF-8 -*-
# breeders.py - generates content of /dogs, /females, and /males
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

from pathlib import Path
import tools.shows

def generate_photos(output_document, database, extra):
    resources = database['resources']
    output_document.start_container()

    dog_list = resources.get_yaml('doglist.yml')

    dog_id = extra[0]
    name = dog_list[dog_id]['name']
    output_document.add_raw('<h1>Фото <a href=".">{}</a></h1>'.format(name['gen']))

    photo_list = resources.get_yaml('dogphotos.yml')
    photos = photo_list.get(dog_id, [])
    for photo in photos:
        caption = photo['caption'] if photo['caption'] != None else ''
        photo_ = database['photos'].get_for_id(photo['path'])
        output_document.add_image(photo_.get_id(), caption if caption else photo_.get_caption(), 'h', 152, True, photo_.get_image())
        output_document.add_plain(' ')
    output_document.end_container()


def generate_videos(output_document, database, extra):
    resources = database['resources']
    output_document.start_container()

    dog_list = resources.get_yaml('doglist.yml')

    dog_id = extra[0]
    name = dog_list[dog_id]['name']

    youtube_ids = dog_list[dog_id].get('videos')
    for video_id in youtube_ids:
        youtube_id, *title = video_id.split(' ', 1)
        if title:
            output_document.add_header(3, title[0])
        output_document.add_raw('<p>')
        output_document.add_raw('<iframe width="560" height="315" src="https://www.youtube.com/embed/{}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'.format(video_id))
    output_document.end_container()


def generate_shows(output_document, database, extra):
    resources = database['resources']
    output_document.start_container(css_classes=['card'])
    dog_list = resources.get_yaml('doglist.yml')
    all_experts = resources.get_yaml('people.yml')

    dog_id = extra[0]
    name = dog_list[dog_id]['name']
    output_document.add_raw('<h1>Результаты выставок <a href=".">{}</a></h1>'.format(name['gen']))

    personal_shows = database['shows'].get_for_dog(dog_id)
    mono_shows = [x for x in personal_shows if x['rank'] == 'монопородная']
    if mono_shows:
        output_document.start_container()
        output_document.add_raw('<h1>Монопородные выставки</h2>')
        output_document.add_raw('<ol class="chrono-list">')
        for show in mono_shows:
            place = show['place'].replace(' ', ' ', 1)
            achievements = tools.shows.stringify_title_list(show['achievements'])
            if achievements:
                place = '{}, {}'.format(place, achievements)
            experts = tools.shows.get_experts(show, all_experts)
            output_document.add_raw('<li>')
            output_document.add_date(show['date'])
            cup = '«Кубок {}»'.format(show['cup']) if 'cup' in show else 'КЧК'
            notes = '({})'.format(show['note']) if 'note' in show else ''
            output_document.add_raw(' Монопородная выставка {cp}, г. {ci}, класс {cl}, <strong>{a}</strong> {n} ({e}).'.format(cp=cup, ci=show['city'], cl=show['class'], a=achievements, e=experts, n=notes))
        output_document.add_raw('</ol>')
        output_document.end_container()

    nonmono_shows = [x for x in personal_shows if x['rank'] != 'монопородная']
    if nonmono_shows:
        output_document.start_container()
        output_document.add_raw('<h1>Всепородные выставки</h2>')
        output_document.add_raw('<ol class="chrono-list">')
        for show in nonmono_shows:
            place = show['place'].replace(' ', ' ', 1)
            achievements = tools.shows.stringify_title_list(show['achievements'])
            if achievements:
                place = '{}, {}'.format(place, achievements)
            experts = tools.shows.get_experts(show, all_experts)
            output_document.add_raw('<li>')
            output_document.add_date(show['date'])
            normalized_rank = show['rank'][0].upper() + show['rank'][1:]
            output_document.add_raw(' {s}, г. {ci}, класс {cl}, <strong>{a}</strong> ({e}).'.format(s=normalized_rank, ci=show['city'], cl=show['class'], a=achievements, e=experts))
        output_document.add_raw('</ol>')
        output_document.end_container()
    output_document.end_container()

    output_document.end_container()


def to_roman(number):
    numbers = ['Ⅰ', 'Ⅱ', 'Ⅲ', 'Ⅳ', 'Ⅴ', 'Ⅵ', 'Ⅶ', 'Ⅷ', 'Ⅸ', 'Ⅹ']
    return numbers[number - 1]


def generate_index(output_document, database, extra):
    resources = database['resources']
    dog_list = resources.get_yaml('doglist.yml')

    dog_id = extra[0]
    dog_info = dog_list[dog_id]

    output_document.start_container(['dog', 'card'])
    output_document.add_header(1, dog_info['name']['nom'])
    if dog_info.get('renter', ''):
        output_document.add_raw('<p><em>Находится в аренде. Владелец — {}</em></p>'.format(dog_info['renter']))
    if dog_info.get('is_long_hair', False):
        output_document.add_raw('<p>(длинношёрстная)</p>')
    output_document.add_raw('<p>Дата рождения: ')
    output_document.add_date(dog_info['dob'])
    output_document.add_raw('</p>')
    output_document.add_raw(dog_info.get('content', ''))
    if 'tests' in dog_info:
        training_group = []
        if dog_info['tests'][2] == '?' and dog_info['tests'][3] == '?':
            training_group.append('ОКД/ЗКС')
        else:
            if dog_info['tests'][2]:
                fields = dog_info['tests'][2].split(' ')
                if len(fields) > 1 and fields[1].lower() == 'кд':
                    training_group.append('КД-{}'.format(fields[0]))
                else:
                    training_group.append('ОКД-{}'.format(fields[0]))
            if dog_info['tests'][3]:
                training_group.append('ЗКС-{}'.format(dog_info['tests'][3]))
            if dog_info['tests'][4]:
                training_group.append('IPO-{}'.format(to_roman(int(dog_info['tests'][4]))))
        training_group = ', '.join(training_group)

        health_group = []
        if dog_info['tests'][0]:
            health_group.append('HD-{}'.format(dog_info['tests'][0].upper()))
        if dog_info['tests'][1]:
            health_group.append('ED-{}'.format(dog_info['tests'][1]))
        health_group = ', '.join(health_group)

        kaerklass_group = []
        if dog_info['tests'][5]:
            kaerklass_group.append('Kkl {}'.format(dog_info['tests'][5].upper()))
        kaerklass_group = ', '.join(kaerklass_group)

        short_test_info = '; '.join(filter(bool, [training_group, health_group, kaerklass_group]))
        output_document.add_raw('<p>')
        output_document.add_raw(short_test_info)
        output_document.add_raw('</p>')
    caption = 'Фотография {}'.format(dog_info['name']['gen'])
    photo = database['photos'].get_card_assignation(dog_id)
    output_document.add_image(photo.get_id(), caption if caption else photo.get_caption(), 'w', 558, False, photo.get_image())

    subsections = []
    photo_list = resources.get_yaml('dogphotos.yml')
    photos = photo_list.get(dog_id)
    if photos:
        subsections.append('<a href="photos.htm">Фотографии</a>')
    videos = dog_list[dog_id].get('videos', [])
    if videos:
        subsections.append('<a href="videos.htm">Видео</a>')
    if database['shows'].get_for_dog(dog_id):
        subsections.append('<a href="shows.htm">Результаты выставок</a>')

    if subsections:
        output_document.start_paragraph()
        output_document.add_raw(' | '.join(subsections))

    output_document.start_paragraph()
    output_document.add_plain('Родословная: ')
    pedigree = []
    if dog_info['pedigree'].get('pd', ''):
        pedigree.append('<a href="http://www.pedigreedatabase.com/dog.html?id={}">Pedigree Database</a>'.format(dog_info['pedigree']['pd']))
    if dog_info['pedigree'].get('gsdog', ''):
        pedigree.append('<a href="http://database.gsdog.ru/dog.php?screen=1&amp;id={}">GSDOG</a>'.format(dog_info['pedigree']['gsdog']))
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


def generate_list(output_document, database, extra):
    dog_list = database['resources'].get_yaml('doglist.yml')

    category = extra[0]
    if category == 'dog':
        dogs = [dog for dog in dog_list.items() if dog[1]['type'] == 'nonbreeder']
    else:
        dogs = [dog for dog in dog_list.items() if dog[1]['type'] in ['breeder', 'retired'] and dog[1]['gender'] == category]
    dogs.sort(key=get_dog_records_key(dog_list))

    output_document.start_list(css_classes=['cards'])
    for dog_id, dog_info in dogs:
        output_document.start_list_item()
        if dog_info['type'] == 'retired':
            output_document.add_plain('Заслуженный ветеран ')
        output_document.add_raw('<a href="/{}s/{}/">'.format(category, dog_id))
        output_document.add_raw(dog_info['name']['nom'])
        output_document.add_plain(' ')
        caption = 'Фотография {}'.format(dog_info['name']['gen'])
        photo = database['photos'].get_card_assignation(dog_id)
        output_document.add_image(photo.get_id(), caption, 'h', 152, False, photo.get_image())
        output_document.add_raw('</a>')
        output_document.end_list_item()
    output_document.end_list()


def for_pedigree_only(dog):
    _, dog_details = dog
    return 'dob' not in dog_details


def get_root_artifact_list(database):
    resources = database['resources']
    section_pages = []
    categories = {'dog': Path('dogs'), 'female': Path('females'), 'male': Path('males')}

    dog_list = resources.get_yaml('doglist.yml')
    photo_list = resources.get_yaml('dogphotos.yml')
    dogs = [dog for dog in dog_list.items() if not for_pedigree_only(dog)]
    for dog_id, dog_details in dogs:

        name = dog_details['name']
        category = 'dog' if dog_details['type'] == 'nonbreeder' else dog_details['gender']
        directory = categories[category] / dog_id

        section_pages.append((name['nom'], directory / 'index', generate_index, dog_id))

        photos = photo_list.get(dog_id)
        if photos:
            title = "Фото {}".format(name['gen'])
            page = (title, directory / 'photos', generate_photos, dog_id)
            section_pages.append(page)

        youtube_ids = dog_details.get('videos')
        if youtube_ids:
            title = "Видео {}".format(name['gen'])
            page = (title, directory / 'videos', generate_videos, dog_id)
            section_pages.append(page)

        if database['shows'].get_for_dog(dog_id):
            title = "Результаты выставок {}".format(name['gen'])
            page = (title, directory / 'shows', generate_shows, dog_id)
            section_pages.append(page)

    section_pages.append(('Производители', Path('males', 'index'), generate_list, 'male'))
    section_pages.append(('Производительницы', Path('females', 'index'), generate_list, 'female'))
    section_pages.append(('Собаки питомника', Path('dogs', 'index'), generate_list, 'dog'))

    return section_pages
