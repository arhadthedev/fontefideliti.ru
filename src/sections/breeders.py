# -*- coding: UTF-8 -*-
# breeders.py - generates content of /females and /males
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

from collections import OrderedDict
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


def filter_shows_for(filtered_dog_id, show_tree):
    filtered_shows = []
    for date, eventset in show_tree.items():
        for event in eventset['events']:
            for dog_id, dog_details in event['dogs'].items():
                if dog_id == filtered_dog_id:
                    element = {}
                    element['date'] = date
                    element['rank'] = event['rank']
                    element['city'] = eventset['city']
                    element['class'] = dog_details['class']
                    element['expert'] = event['expert']
                    element['figurant'] = event.get('figurant', '')
                    element['place'] = dog_details['place']
                    element['achievements'] = dog_details.get('achievements', [])
                    filtered_shows.append(element)
    return filtered_shows


def get_proper_expert_name(last_name, registry):
    first_name, patronymic = registry[last_name].split(' ')
    return '{} {}. {}.'.format(last_name, first_name[0], patronymic[0])


# Items are printed in the order they specified here
printable_ranks = OrderedDict()
printable_ranks['cw'] = 'Победитель класса'
printable_ranks['лб'] = 'Лучший бэби'
printable_ranks['лю'] = 'Лучший юниор'
printable_ranks['лк'] = 'Лучший кобель'
printable_ranks['jcac'] = 'JunCAC'
printable_ranks['cac'] = 'CAC'
printable_ranks['кчф рфлс'] = 'Кандидат в Чемпионы Федерации РФЛС'
printable_ranks['кчф оанкоо'] = 'Кандидат в Чемпионы Федерации ОАНКОО'
printable_ranks['чф оанкоо'] = 'Чемпион Федерации ОАНКОО'
printable_ranks['лпп'] = 'Лучший представитель породы'
printable_ranks['big 2'] = 'BIG-2'
printable_ranks['чркф'] = 'Чемпион РКФ'
printable_ranks['bos'] = 'BOS'
printable_ranks['cnd'] = 'Победитель в конкурсе «Ребёнок и собака»'


def assembly_achievements(place, ranks):
    place_formatted = ' '.join(place.split(' ', 1))
    ranks_count = {}
    for source_rank in ranks:
        ranks_count.setdefault(source_rank, 0)
        ranks_count[source_rank] += 1

    def id_to_name(rank_id):
        count = ranks_count.get(rank_id, 0)
        if count > 1:
            return '{}x {}'.format(count, printable_ranks[rank_id])
        elif count == 1:
            return printable_ranks[rank_id]
        else:
            raise RuntimeError('undefined rank should be filtered by a caller')
    titles = ', '.join((id_to_name(x) for x in printable_ranks if x in ranks))
    return '{}, {}'.format(place, titles) if titles else place

def generate_shows(output_document, resources):
    output_document.start_container(css_classes=['filled'])
    show_list = yaml.safe_load(resources.get('shows.yml'))
    dog_list = yaml.safe_load(resources.get('doglist.yml'))
    experts = yaml.safe_load(resources.get('people.yml'))

    path = output_document.get_path()
    dog_id = path.split('/')[1]
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
            achievements = assembly_achievements(place, show['achievements'])
            expert = get_proper_expert_name(show['expert'], experts)
            if show['figurant']:
                figurant_name = get_proper_expert_name(show['figurant'], experts)
                figurant = ', фигурант {}'.format(figurant_name)
            else:
                figurant = ''
            output_document.add_raw('<li>')
            output_document.add_date(show['date'])
            output_document.add_raw(' Монопородная выставка КЧК, г. {ci}, класс {cl}, <strong>{a}</strong> (эксперт {e}{f}).'.format(ci=show['city'], cl=show['class'], a=achievements, e=expert, f=figurant))
        output_document.add_raw('</ol>')
        output_document.end_container()

    nonmono_shows = [x for x in personal_shows if x['rank'] != 'монопородная']
    if nonmono_shows:
        output_document.start_container()
        output_document.add_raw('<h1>Всепородные выставки</h2>')
        output_document.add_raw('<ol class="chrono-list">')
        for show in nonmono_shows:
            achievements = assembly_achievements(show['place'], show['achievements'])
            expert = get_proper_expert_name(show['expert'], experts)
            output_document.add_raw('<li>')
            output_document.add_date(show['date'])
            output_document.add_raw(' {s}, г. {ci}, класс {cl}, <strong>{a}</strong> (эксперт {e}).'.format(s=show['rank'].capitalize().replace(' чркф', ' ЧРКФ'), ci=show['city'], cl=show['class'], a=achievements, e=expert))
        output_document.add_raw('</ol>')
        output_document.end_container()
    output_document.end_container()

    output_document.end_container()


def generate_index(output_document, resources):
    dog_list = yaml.safe_load(resources.get('doglist.yml'))
    show_list = yaml.safe_load(resources.get('shows.yml'))

    path = output_document.get_path()
    dog_id = path.split('/')[1]
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

        shows_url = '{}/shows'.format(base_url)
        if dog_id in ['aleks', 'eiko', 'zheneva']:
            title = "Результаты выставок {}".format(name['gen'])
            page = (title, shows_url, generate_shows)
            section_pages.append(page)

    section_pages.append(('Производители', 'males/index', generate_list))
    section_pages.append(('Производительницы', 'females/index', generate_list))

    return section_pages
