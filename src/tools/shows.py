# -*- coding: UTF-8 -*-
# shows.py - routines related to processing of show records and titles
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

from collections import OrderedDict
import itertools

# Items are printed in the order they specified here
known_titles = OrderedDict()
known_titles['cw'] = 'Победитель класса'
known_titles['пмк'] = 'Победитель младшего класса'
known_titles['пкп'] = 'Победитель класса подростков'
known_titles['пкю'] = 'Победитель класса юниоров'
known_titles['лб'] = 'Лучший бэби'
known_titles['лщ'] = 'Лучший щенок'
known_titles['лп'] = 'Лучший подросток'
known_titles['лю'] = 'Лучший юниор'
known_titles['лв'] = 'Лучший ветеран'
known_titles['лк'] = 'Лучший кобель'
known_titles['лс'] = 'Лучшая сука'
known_titles['лсдг'] = 'Лучшая сука до года'
known_titles['jcac'] = 'JunCAC'
known_titles['cac'] = 'CAC'
known_titles['rcac'] = 'RCAC'
known_titles['vcac'] = 'VCAC'
known_titles['юсс'] = 'ЮСС'
known_titles['юкчк'] = 'Юный кандидат в Чемпионы клуба'
known_titles['кчк'] = 'Кандидат в Чемпионы клуба'
known_titles['кчф рфлс'] = 'Кандидат в Чемпионы Федерации РФЛС'
known_titles['кчф оанкоо'] = 'Кандидат в Чемпионы Федерации ОАНКОО'
known_titles['чф рфлс'] = 'Чемпион Федерации РФЛС'
known_titles['чф рфсс'] = 'Чемпион Федерации РФСС'
known_titles['чф рфос'] = 'Чемпион Федерации РФОС'
known_titles['ючф рфос'] = 'Юный Чемпион Федерации РФОС'
known_titles['ючф рфлс'] = 'Юный Чемпион Федерации РФЛС'
known_titles['ючф рфсс'] = 'Юный Чемпион Федерации РФСС'
known_titles['кчфсс'] = 'КЧФСС'
known_titles['чф оанкоо'] = 'Чемпион Федерации ОАНКОО'
known_titles['ч кз'] = 'Чемпион Казахстана'
known_titles['ч тат'] = 'Чемпион Татарстана'
known_titles['лпп'] = 'Лучший представитель породы' # BOB
known_titles['big 2'] = 'BIG-2'
known_titles['rcacib'] = 'RCACIB'
# Baby ones
known_titles['bis-b-1'] = 'BIS-B-I'
known_titles['bis-b-3'] = 'BIS-B-III'
# Non-baby ones
known_titles['bis-3'] = 'BIS-III'
known_titles['чркф'] = 'Чемпион РКФ'
known_titles['bos'] = 'BOS' # Лучший представитель противоположного пола
known_titles['вице cnd'] = 'Вице-победитель в конкурсе «Ребёнок и собака»'
known_titles['cnd'] = 'Победитель в конкурсе «Ребёнок и собака»'
known_titles['best г3'] = 'BEST группы 3 место!'
known_titles['best г2'] = 'BEST группы 2 место!'
known_titles['best г1'] = 'BEST группы 1 место!'
known_titles['вице best'] = 'Вице-победитель BEST щенков'
known_titles['best щ1'] = 'Победитель Best щенков'
known_titles['best 3'] = 'Best щенков 3 место'
known_titles['best в4'] = 'Best щенков призовое 4 место'
known_titles['best 1г'] = 'Победитель BEST 1 группы' # BIG-1?
known_titles['big-3'] = 'Победитель BEST 3 группы' # BIG-3?
known_titles['best в1'] = 'Победитель Best ветеранов'
known_titles['best в4'] = 'Бест щенков призовое 4 место'
known_titles['best ю2'] = 'ВEST юниоров 2 место!'
known_titles['best в2'] = 'ВEST ветеранов 2 место!'
known_titles['best в3'] = 'ВEST ветеранов 3 место!'
known_titles['bis 1'] = 'Победитель Best in Show'
known_titles['пкп'] = 'Победитель конкурса пар'


def _stringify_title(count, name):
    if count == 1:
        return name
    else:
        return '{}x {}'.format(count, name)


def stringify_title_list(titles):
    unknown_titles = [x for x in titles if (x not in known_titles)]
    if unknown_titles:
        raise ValueError('unknown titles {}'.format(', '.join(unknown_titles)))

    grouped_titles = itertools.groupby(titles, lambda x: x)
    counted_titles = dict(map(lambda x: (x[0], len(list(x[1]))), grouped_titles))

    stringified = [_stringify_title(counted_titles[x], known_titles[x]) for x in known_titles if x in counted_titles]
    return ', '.join(stringified)


def get_full_person_name(last_name, registry):
    first_name, *patronymic = registry[last_name].split(' ')
    if patronymic:
        return '{} {}. {}.'.format(last_name, first_name[0], patronymic[0][0])
    else:
        return '{} {}'.format(first_name, last_name)


def get_experts(event, all_people):
    expert_name = get_full_person_name(event['expert'], all_people)
    if 'figurant' in event:
        figurant_name = get_full_person_name(event['figurant'], all_people)
        return 'эксперт {}, фигурант {}'.format(expert_name, figurant_name)
    else:
        return 'эксперт {}'.format(expert_name)
