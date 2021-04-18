# -*- coding: UTF-8 -*-
# main.py - generates content of /index.htm
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

banner_lines = ['Приветствуем вас на сайте питомника «Фонте Фиделити».',
                'Наш питомник занимается профессиональным разведением собак '
                'породы немецкая овчарка.']


def generate_contacts_section(name, telephones, email, site, output_document):
    output_document.start_paragraph()
    output_document.add_plain('{}:'.format(name))
    output_document.start_list()
    for number in telephones:
        output_document.start_list_item()
        output_document.add_telephone(number)
    if email:
        output_document.start_list_item()
        output_document.add_plain(email)
    if site:
        output_document.start_list_item()
        output_document.add_human_url(site)
    output_document.end_list()


def generate_contacts(output_document):
    output_document.add_header(2, 'Контакты')

    output_document.start_paragraph()
    output_document.add_plain('Группа ВКонтакте: ')
    output_document.add_human_url('vk.com/fontefideliti')
    output_document.add_break()
    output_document.add_plain('Facebook: ')
    output_document.add_human_url('facebook.com/groups/fontefideliti/')

    generate_contacts_section('Наталья Ярыгина', ['+79272110963', '+79171296817'], 'natalia@fontefideliti.ru', 'vk.com/id64586093', output_document)
    generate_contacts_section('Светлана Крыгина', ['+79171254468'], 'svetlana@fontefideliti.ru', 'vk.com/id98166169', output_document)
    generate_contacts_section('Ветеринарный врач, Ольга Никитина', ['+79270231485'], None, None, output_document)
    generate_contacts_section('Дрессировка собак, Ирина Богатова', ['+79272151099'], None, None, output_document)
    generate_contacts_section('Передержка собак, Елена Прохорова', ['+79272125725'], None, None, output_document)


def generate_index(output_document, resources, photos):
    output_document.start_paragraph(['banner'])
    output_document.add_plain(banner_lines[0])
    output_document.add_break()
    output_document.add_plain(banner_lines[1])

    output_document.start_generic_container(['multicolumn'])
    output_document.add_image('2011/06111', 'Фанхил Хаус Хассо', 'h', 540, False)
    output_document.start_generic_container()
    generate_contacts(output_document)
    output_document.end_generic_container()
    output_document.end_generic_container()


def get_root_artifact_list(resources):
    section_pages = [('', 'index', generate_index)]
    return section_pages
