# -*- coding: UTF-8 -*-
# document.py - a document generation class and related utilities
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

from datetime import datetime
import os
from PIL import Image
import re

brand_ru = 'Питомник немецких овчарок «Фонте Фиделити» г. Тольятти'
brand_en = 'Питомник немецких овчарок «Fonte Fideliti» г. Тольятти'

menu = [('Главная', ''),
        ('Производители', 'males/'),
        ('Производительницы', 'females/'),
        ('Выставки', 'shows/'),
        ('Наши выпускники', 'dogs.htm'),
        ('Фото', 'photos.htm'),
        ('Щенки на продажу', 'sale.htm')]


def _make_html_class_list(class_list):
    has_duplicates = any(class_list.count(element) > 1 for element in class_list)
    if has_duplicates:
        raise ValueError('css classes must not repeat; check for typos')
    if any(('"' in element or ' ' in element) for element in class_list):
        raise ValueError('css classes must not contain quotes and spaces')
    return ' '.join(class_list)


class Document(object):
    def __init__(self, title, path, resources):
        self._path = path
        self._resources = resources

        self._content_chunks = []
        self._content_chunks.append('<!DOCTYPE html><html lang="ru">')
        self._content_chunks.append('<meta charset="utf-8">')
        full_title = '{} — {}'.format(title, brand_ru) if title else brand_ru
        self._content_chunks.append('<title>{}</title>'.format(full_title))
        self._content_chunks.append('<link rel="stylesheet" href="/common.css">')
        self._content_chunks.append('<link rel="icon" href="/favicon.png">')

        self._content_placeholder_id = len(self._content_chunks)
        self._content_chunks.append('')
        self._content_chunks.append('')
        self._content_chunks.append('')
        self._content_chunks.append('<header>')
        brand_pretty = brand_en.replace('«', '<span>«').replace('»', '»</span>')
        self._content_chunks.append('<h1>{}</h1>'.format(brand_pretty))
        self.add_image('title', 'Логотип', 'w', 500, False)
        self._content_chunks.append('</header>')

        self._content_chunks.append('<nav><ul>')
        compact_path = re.sub(r'index\.html?$', '', path)
        for title, menu_path in menu:
            if not menu_path:
                menu_path = 'index.html'
            if compact_path == menu_path:
                item = '<li><span class="current">{}'.format(title)
            elif path.startswith(menu_path):
                item = '<li><a href="/{}" class="current">{}</a>'.format(menu_path, title)
            else:
                item = '<li><a href="/{}">{}</a>'.format(menu_path, title)
            self._content_chunks.append(item)
        self._content_chunks.append('</nav>')


    def get_path(self):
        return self._path


    def start_container(self, css_classes=[]):
        class_list = _make_html_class_list(css_classes)
        class_mixin = ' class="{}"'.format(class_list) if css_classes else ''
        self._content_chunks.append('<article{}>'.format(class_mixin))

    def end_container(self):
        self._content_chunks.append('</article>')


    def start_generic_container(self, css_classes=[]):
        class_list = _make_html_class_list(css_classes)
        class_mixin = ' class="{}"'.format(class_list) if css_classes else ''
        self._content_chunks.append('<div{}>'.format(class_mixin))


    def end_generic_container(self):
        self._content_chunks.append('</div>')


    def add_header(self, level, text):
        text_safe = text.replace('&', '&amp;').replace('<', '&lt;')
        self._content_chunks.append('<h{0}>{1}</h{0}>'.format(level, text_safe))


    def start_paragraph(self, css_classes=[]):
        class_list = _make_html_class_list(css_classes)
        class_mixin = ' class="{}"'.format(class_list) if css_classes else ''
        self._content_chunks.append('<p{}>'.format(class_mixin))


    def add_plain(self, text):
        text_safe = text.replace('&', '&amp;').replace('<', '&lt;')
        self._content_chunks.append(text_safe)


    def add_raw(self, text):
        self._content_chunks.append(text)


    def add_image(self, name, caption, dimension_type, dimension, is_clickable):
        size = '{}{}'.format(dimension_type, dimension)
        if dimension_type == 'w':
            max_size = dimension, 9999
        elif dimension_type == 'h':
            max_size = 9999, dimension
        else:
            raise ValueError('dimension_type can be "w" or "h" only')

        base = 'img/{}'.format(name)
        fullsize_path = '{}.jpg'.format(base)
        preview_path = '{}-p.jpg'.format(base)
        try:
            legacy_preview_test = self._resources.get_image(preview_path)
            legacy_preview_test.close()
        except FileNotFoundError:
            preview_path = '{}-{}.jpg'.format(base, size)

        os.makedirs(os.path.dirname(preview_path), exist_ok=True)
        original = self._resources.get_image('img/{}.jpg'.format(name))
        width = None
        height = None
        if not os.path.isfile(preview_path):
            preview = original.copy()
            preview.thumbnail(max_size, Image.LANCZOS, None)
            preview.save(preview_path, quality=94, optimize=True, progressive=True)
            width, height = preview.size
        else:
            with Image.open(preview_path) as existing:
                width, height = existing.size

        if is_clickable:
            if not os.path.isfile(fullsize_path):
                preview = original.copy()
                full_size = 794, 794
                preview.thumbnail(full_size, Image.LANCZOS, None)
                preview.save(fullsize_path, quality=94, optimize=True, progressive=True)
            i = self._content_placeholder_id
            self._content_chunks[i + 0] = '<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/baguettebox.js/1.11.1/baguetteBox.min.css">'
            self._content_chunks[i + 1] = '<script src="//cdnjs.cloudflare.com/ajax/libs/baguettebox.js/1.11.1/baguetteBox.min.js" async></script>'
            self._content_chunks[i + 2] = '<script>addEventListener("load", function() {baguetteBox.run("article", {noScrollbars: true})})</script>'
            self._content_chunks.append('<a href="/{}" title="{}">'.format(fullsize_path, caption))
        self._content_chunks.append('<img src="/{}" width="{}" height="{}" alt="{}">'.format(preview_path, width, height, caption))
        if is_clickable:
            self._content_chunks.append('</a>')


    def _add_pedigree_cell(self, dog_info, all_dogs, current_depth, max_depth):
        rowspan = 2 ** (max_depth - 1 - current_depth)
        if rowspan > 1:
            self._content_chunks.append('<td rowspan="{}">'.format(rowspan))
        else:
            self._content_chunks.append('<td>')

        self._content_chunks.append('<p>')
        self._content_chunks.append(',<br>'.join(dog_info.get('extra_titles', [])))
        self._content_chunks.append('<p>{}</p>'.format(dog_info['name']['nom']))
        if current_depth == 0:
            if 'photo' not in dog_info:
                raise ValueError('A photo must be specified for {}'.format(dog_info['name']['nom']))
            if dog_info['photo'] != 'none':
                self.add_image(dog_info['photo'], dog_info['name']['nom'], 'w', 168, is_clickable=True)

        self._content_chunks.append('</td>')
        self._add_pedigree(dog_info, all_dogs, current_depth + 1, max_depth)


    def _add_pedigree(self, dog_info, all_dogs, current_depth, max_depth):
        if current_depth >= max_depth:
            return

        if 'father' not in dog_info:
            raise ValueError('A father must be specified for {}'.format(dog_info['name']['nom']))
        father_id = dog_info['father']
        self._add_pedigree_cell(all_dogs[father_id], all_dogs, current_depth, max_depth)

        self._content_chunks.append('<tr>')

        if 'mother' not in dog_info:
            raise ValueError('A mother must be specified for {}'.format(dog_info['name']['nom']))
        mother_id = dog_info['mother']
        self._add_pedigree_cell(all_dogs[mother_id], all_dogs, current_depth, max_depth)


    def add_pedigree(self, dog_info, all_dogs, depth=3):
        self._content_chunks.append('<table class="pedigree">')
        self._content_chunks.append('<tr>')
        self._add_pedigree(dog_info, all_dogs, 0, depth)
        self._content_chunks.append('</table>')


    def add_human_url(self, url):
        text = '<a href="//{0}">{0}</a>'.format(url)
        self._content_chunks.append(text)

    def add_telephone(self, number):
        f_num = '{} ({}) {}-{}-{}'.format(number[0:2], number[2:5], number[5:8], number[8:10], number[10:12])
        text = 'т. <a href="tel:{}">{}</a>'.format(number, f_num)
        self._content_chunks.append(text)

    def add_break(self):
        self._content_chunks.append('<br>')


    def add_date(self, date):
        html_format = date.isoformat()
        human_format = date.strftime('%-d.%m.%Y')
        chunk = '<time datetime="{}">{} г.</time>'.format(html_format, human_format)
        self._content_chunks.append(chunk)


    def start_list(self):
        self._content_chunks.append('<ul>')


    def new_list_item(self):
        self._content_chunks.append('<li>')


    def end_list(self):
        self._content_chunks.append('</ul>')


    def finalize(self):
        now = datetime.now()
        copyright = '© Ярыгин О. В. (oleg@arhadthedev.net) 2015–{}.'.format(now.year)
        footer = '<footer><p>{}</footer>'.format(copyright)
        self._content_chunks.append(footer)
        return ''.join(self._content_chunks)
