#!/usr/bin/env python

# build.py - builds /sale.htm into a folder passed as the first argument
#
# Copyright (c) 2020 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

import os.path
from page_layout import Layout
import sys

layout = Layout('sale', 'Щенки на продажу')

pitch = ('<p><strong><em>Питомник «Фонте Фиделити» предлагает на продажу '
         'породистых щенков немецкой овчарки. Наши щенки профессионально '
         'выращены, привиты, клеймёны, имеют метрику щенка, '
         'зарегистрированную в РКФ.</em></strong>'
         '<p><strong><em>Мы всегда готовы помочь в выращивании, дрессировке '
         'и ветеринарном обслуживании. По желанию владельца оказываем помощь '
         'в подготовке и показе на выставках.</em></strong>')
layout.add(pitch, element='article', classes=['card'])

call = ('Купить щенка немецкой овчарки в Тольтти: '
        'Наталья (т. 8 (927) 211-09-63, natalia@fontefideliti.ru), '
        'Светлана (т. 8 (917) 125-44-68, svetlana@fontefideliti.ru).')
layout.add(call, element='p')

if len(sys.argv) < 2:
    sys.exit('error: output directory path argument is not specified')
path = os.path.join(sys.argv[1], 'sale.html')
output = open(path, 'w', encoding='utf-8')
output.write(layout.get_html())
