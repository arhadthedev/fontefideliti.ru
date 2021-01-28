#!/usr/bin/env python

# build.py - builds /index.html into a folder passed as the first argument
#
# Copyright (c) 2020 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

import os.path
from page_layout import Layout
from snippets import *
import sys

if len(sys.argv) < 2:
    sys.exit('error: output directory path argument is not specified')
real_path = sys.argv[1]

layout = Layout('main')

banner = ('Приветствуем вас на сайте питомника «Фонте Фиделити».<br>'
          'Наш питомник занимается профессиональным разведением собак породы '
          'немецкая овчарка.')
layout.add(banner, element='p', classes=['banner'])

head_real_path = os.path.join(real_path, 'img/main.jpg')
body = (make_image(head_real_path, 'img/main.jpg', 'Фанхил Хаус Хассо') +
        '<div><h3>Контакты</h3>'
        '<p><strong>Группа ВКонтакте:</strong> ' +
        make_link('vk.com/fontefideliti') +
        '<br><strong>Facebook:</strong> ' +
        make_link('facebook.com/groups/fontefideliti/') +
        '<p><strong>Наталья Ярыгина:</strong>'
        '<ul>'
        '' '<li>' + make_tel('+79272110963') +
        '' '<li>' + make_tel('+79171296817') +
        '' '<li>' + make_email('natalia@fontefideliti.ru') +
        '' '<li>' + make_link('vk.com/id64586093') +
        '</ul>'
        '<p><strong>Светлана Крыгина:</strong>'
        '<ul>'
        '' '<li>' + make_tel('+79171254468') +
        '' '<li>' + make_email('svetlana@fontefideliti.ru') +
        '' '<li>' + make_link('vk.com/id98166169') +
        '</ul>'
        '<p><strong>Ветеринарный врач, Ольга Никитина:</strong>'
        '<ul>'
        '' '<li>' + make_tel('+79270231485') +
        '</ul>'
        '<p><strong>Дрессировка собак, Ирина Богатова</strong>'
        '<ul>'
        '' '<li>' + make_tel('+79272151099') +
        '</ul>'
        '<p><strong>Передержка собак, Елена Прохорова</strong>'
        '<ul>'
        '' '<li>' + make_tel('+79272125725') +
        '</ul></div>')
layout.add(body, element='article', classes=['multicolumn'])

path = os.path.join(real_path, 'index.html')
output = open(path, 'w', encoding='utf-8')
output.write(layout.get_html())
