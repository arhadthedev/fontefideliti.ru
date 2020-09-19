# page_layout.py - a class to generate a page
#
# Copyright (c) 2020 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

from datetime import datetime
from collections import OrderedDict
from snippets import *

site_menu = OrderedDict()
site_menu['main'] = ('Главная', '/')
site_menu['males'] = ('Производители', '/males/')
site_menu['females'] = ('Производительницы', '/females/')
site_menu['shows'] = ('Выставки', '/shows/')
site_menu['dogs'] = ('Наши выпускники', '/dogs.htm')
site_menu['photos'] = ('Фото', '/photos.htm')
site_menu['sale'] = ('Щенки на продажу', '/sale.htm')

style = ('html{background:fixed #caecfd url("/img/background.png")}'
         'body{margin:0pt auto;width:912pt;text-align:center}'
         'footer{border-top:1pt solid #021835;margin:24pt 12pt 0pt}'
         'img{border-radius:7pt}'
         'h1,h2,h3{color:#572325;font-family:Verdana;margin-top:1em;'
         '' 'margin-bottom:1em}'

         'header{display:flex;align-items:center}'
         'header h1{font-family:serif;flex-grow:1}'
         'header span{display:block;font:italic normal 270% Georgia;'
         '' 'text-shadow:1pt 1pt 2pt rgba(0,0,0,0.5)}'

         'nav{margin:33pt 24pt 23pt;position:relative}'
         'nav::before{border-bottom:solid #ddd 1pt;'
         '' 'box-shadow:1px 1px #fafafa;content:" ";display:block;'
         '' 'position:absolute;top:50%;width:100%}'
         'nav ul{padding:0pt;position:relative}'
         'nav li{display:inline-block}'
         'nav .current,nav a{border-radius:3pt;color:#fff;margin:6px;'
         '' 'box-shadow:1pt 1pt 2pt rgba(0,0,0,0.5);'
         '' 'padding:6pt 10pt;text-decoration:none}'
         'nav .current{background:#175ebf;font-weight:bold}'
         'nav a{background:#021835}')

multicol = ('.multicolumn {display:flex;justify-content:space-evenly;'
            '' 'text-align:left;align-items:center}')

multicol_ul = '.multicolumn ul{margin-top:-1em}'

banner_style = ('.banner{color:#572325;font-size:14pt;font-style:italic;'
                'font-weight:bold}')

extra_style = {'multicolumn': multicol + multicol_ul, 'banner': banner_style}


def render_all_styles(used_styles):
    out = ''
    for style in used_styles:
        if style not in extra_style:
            sys.exit(f'error: unknown class {style} is used')
        out += extra_style[style]
    return style + out


class Layout:
    def __init__(self, menu_section, title):
        self.title = title
        self.used_styles = set()
        self.menu_section = menu_section
        self.body = ''

    def add(self, content, element, classes):
        class_list = ' '.join(classes)
        self.body += f'<{element} class="{class_list}">{content}</{element}>'
        self.used_styles |= set(classes)

    def get_html(self):
        out = ('<!DOCTYPE html>'
               '<html lang="ru">'
               '<meta charset="utf-8">'
               '' f'<title>{self.title}</title>'
               '' f'<style>{render_all_styles(self.used_styles)}</style>'
               '<link rel="shortcut icon" href="/favicon.png">'
               '<header>'
               '' '<h1>Питомник немецких овчарок <span>«Fonte Fideliti»'
               '' '</span> г. Тольятти</h1>'
               '' + make_image('img/title.jpg', 'Логотип') +
               '</header>')

        out += '<nav><ul>'
        for key, value in site_menu.items():
            title, path = value
            if key == self.menu_section:
                out += f'<li><span class="current">{title}'
            else:
                out += f'<li><a href="{path}">{title}</a>'
        out += '</nav>'

        out += self.body

        now = datetime.now()
        year = now.year
        out += f'<footer><p>© Ярыгин О. В. (oleg@arhadthedev.net) 2015–{year}.'
        return out
