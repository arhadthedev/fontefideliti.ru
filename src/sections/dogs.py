# -*- coding: UTF-8 -*-
# breeders.py - generates content of /dogs, /females, and /males
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

from pathlib import Path
import tools.shows

def generate_photos(output_document, resources, photos, extra):
    output_document.start_container()

    dog_list = resources.get_yaml('doglist.yml')

    dog_id = extra[0]
    name = dog_list[dog_id]['name']
    output_document.add_raw('<h1>Фото <a href=".">{}</a></h1>'.format(name['gen']))

    photo_list = resources.get_yaml('dogphotos.yml')
    photos_ = photo_list.get(dog_id)
    for photo in photos_:
        caption = photo['caption'] if photo['caption'] != None else ''
        try:
            photo_ = photos.get_for_id(photo['path'])
            output_document.add_image(photo_.get_id(), caption if caption else photo_.get_caption(), 'h', 152, True, photo_.get_image())
        except:
            output_document.add_image(photo['path'], caption, 'h', 152, is_clickable=True)
        output_document.add_plain(' ')
    output_document.end_container()


def generate_videos(output_document, resources, photos, extra):
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


def filter_shows_for(filtered_dog_id, show_tree):
    filtered_shows = []
    for date, events in show_tree.items():
        for event in events:
            for dog_id, dog_details in event['dogs'].items():
                if dog_id == filtered_dog_id:
                    element = {}
                    element['date'] = date
                    element['rank'] = event['rank']
                    if 'cup' in event:
                        element['cup'] = event['cup']
                    element['city'] = event['city']
                    element['class'] = dog_details['class']
                    element['expert'] = event['expert']
                    if 'figurant' in element:
                        element['figurant'] = event['figurant']
                    element['place'] = dog_details['place']
                    if 'note' in dog_details:
                        element['note'] = dog_details['note']
                    element['achievements'] = dog_details.get('achievements', [])
                    filtered_shows.append(element)
    return filtered_shows


def generate_shows(output_document, resources, photos, extra):
    output_document.start_container(css_classes=['card'])
    show_list = resources.get_yaml('shows.yml')
    dog_list = resources.get_yaml('doglist.yml')
    all_experts = resources.get_yaml('people.yml')

    dog_id = extra[0]
    name = dog_list[dog_id]['name']
    output_document.add_raw('<h1>Результаты выставок <a href=".">{}</a></h1>'.format(name['gen']))

    personal_shows = filter_shows_for(dog_id, show_list)
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


def generate_index(output_document, resources, photos, extra):
    dog_list = resources.get_yaml('doglist.yml')
    show_list = resources.get_yaml('shows.yml')

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
    caption = 'Фотография {}'.format(dog_info['name']['gen'])
    try:
        photo = photos.get_for_id(dog_info['photo'])
        output_document.add_image(photo.get_id(), caption if caption else photo.get_caption(), 'w', 558, False, photo.get_image())
    except:
        output_document.add_image(dog_info['photo'], caption, 'w', 588, is_clickable=False)

    subsections = []
    photo_list = resources.get_yaml('dogphotos.yml')
    photos = photo_list.get(dog_id)
    if photos:
        subsections.append('<a href="photos.htm">Фотографии</a>')
    videos = dog_list[dog_id].get('videos', [])
    if videos:
        subsections.append('<a href="videos.htm">Видео</a>')
    shows = filter_shows_for(dog_id, show_list)
    if shows:
        subsections.append('<a href="shows.htm">Результаты выставок</a>')

    if subsections:
        output_document.start_paragraph()
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


def generate_list(output_document, resources, photos, extra):
    dog_list = resources.get_yaml('doglist.yml')

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
        try:
            photo = photos.get_for_id(dog_info['photo'])
            output_document.add_image(photo.get_id(), caption, 'w', 200, False, photo.get_image())
        except:
            output_document.add_image(dog_info['photo'], dog_info['name']['nom'], 'w', 200, is_clickable=False)
        output_document.add_raw('</a>')
        output_document.end_list_item()
    output_document.end_list()


def for_pedigree_only(dog):
    _, dog_details = dog
    return 'dob' not in dog_details


def get_root_artifact_list(resources):
    section_pages = []
    categories = {'dog': Path('dogs'), 'female': Path('females'), 'male': Path('males')}

    dog_list = resources.get_yaml('doglist.yml')
    photo_list = resources.get_yaml('dogphotos.yml')
    show_list = resources.get_yaml('shows.yml')
    dogs = [dog for dog in dog_list.items() if not for_pedigree_only(dog)]
    for dog_id, dog_details in dogs:

        name = dog_details['name']
        category = 'dog' if dog_details['type'] == 'nonbreeder' else dog_details['gender']
        directory = categories[category] / dog_id

        section_pages.append((name['nom'], directory / 'index', generate_index, dog_id))

        youtube_ids = dog_details.get('videos')
        if youtube_ids:
            title = "Видео {}".format(name['gen'])
            page = (title, directory / 'videos', generate_videos, dog_id)
            section_pages.append(page)

        shows = filter_shows_for(dog_id, show_list)
        if shows:
            title = "Результаты выставок {}".format(name['gen'])
            page = (title, directory / 'shows', generate_shows, dog_id)
            section_pages.append(page)

    section_pages.append(('Производители', Path('males', 'index'), generate_list, 'male'))
    section_pages.append(('Производительницы', Path('females', 'index'), generate_list, 'female'))
    section_pages.append(('Собаки питомника', Path('dogs', 'index'), generate_list, 'dog'))

    return section_pages
