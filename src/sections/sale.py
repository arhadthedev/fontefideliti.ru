# -*- coding: UTF-8 -*-
# sale.py - generates content of /sale.htm
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

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

    output.start_paragraph()
    output.add_plain('Купить щенка немецкой овчарки в Тольтти: ')
    output.add_plain('Наталья (т. 8 (927) 211-09-63, natalia@fontefideliti.ru), ')
    output.add_plain('Светлана (т. 8 (917) 125-44-68, svetlana@fontefideliti.ru).')

def get_root_artifact_list(resources):
    return [('Щенки на продажу', 'sale', generate_sale)]
