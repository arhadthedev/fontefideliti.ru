# -*- coding: UTF-8 -*-
# sale.py - generates content of /sale.htm
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

from datetime import datetime
import yaml

def _print_list(output, resources):
    dog_list = yaml.safe_load(resources.get('doglist.yml'))

    output.start_container(['card'])
    output.add_raw('<h1 style="font-size: 100%">Продаются щенки</h1>')
    output.add_raw('<h2 style="font-size: 90%">тел. ')
    output.add_telephone('+79277893501')
    output.add_raw(', Марина</h2>')
    output.add_raw('<h2 style="font-size: 90%">Дата рождения: ')
    output.add_date(datetime(2021, 2, 10))
    output.add_raw('</h2>')
    output.add_raw('<p>Мать: Антенор Хоф Нальмира.</p>')
    output.add_raw('<p>Отец: <a href="/males/itan/">Фонте Фиделити Итан</a>.</p>')
    dog_record = {'father': 'itan', 'mother': 'nalmira'}
    output.add_pedigree(dog_record, dog_list, depth=3)

    output.add_raw('<h2 style="font-size: 100%">Суки:</h2>')
    output.add_raw('<h3 style="font-size: 11pt">Фонте Фиделити Циана</h3>')
    output.add_raw('<p><a href="http://www.pedigreedatabase.com/german_shepherd_dog/dog.html?id=3069915">Родословная</a></p>')
    output.add_image('2021/03281', 'Фонте Фиделити Циана, 1,5 месяца', 'h', 152, True)
    output.add_plain(' ')
    output.add_image('2021/03282', 'Фонте Фиделити Циана, 1,5 месяца', 'h', 152, True)
    output.add_plain(' ')
    output.add_image('2021/03283', 'Фонте Фиделити Циана, 1,5 месяца', 'h', 152, True)
    output.end_container()


def generate_sale(output, resources):
    output.start_container(['card', 'notification'])
    output.start_paragraph()
    output.add_plain('Питомник «Фонте Фиделити» предлагает на продажу ')
    output.add_plain('породистых щенков немецкой овчарки. Наши щенки ')
    output.add_plain('профессионально выращены, привиты, клеймёны, имеют ')
    output.add_plain('метрику щенка, зарегистрированную в РКФ.')
    output.start_paragraph()
    output.add_plain('Мы всегда готовы помочь в выращивании, дрессировке ')
    output.add_plain('и ветеринарном обслуживании. По желанию владельца ')
    output.add_plain('оказываем помощь в подготовке и показе на выставках.')
    output.end_container()

    _print_list(output, resources)

    if False:
        output.start_paragraph()
        output.add_plain('Купить щенка немецкой овчарки в Тольтти: ')
        output.add_plain('Наталья (т. 8 (927) 211-09-63, natalia@fontefideliti.ru), ')
        output.add_plain('Светлана (т. 8 (917) 125-44-68, svetlana@fontefideliti.ru).')

def get_root_artifact_list(resources):
    return [('Щенки на продажу', 'sale', generate_sale)]
