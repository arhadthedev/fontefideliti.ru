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
from tools.text_chunks import ConditionalText

brand_ru = 'Питомник немецких овчарок «Фонте Фиделити» г. Тольятти'
brand_en = 'Питомник немецких овчарок «Fonte Fideliti» г. Тольятти'

menu = [('Главная', ''),
        ('Производители', 'males/'),
        ('Производительницы', 'females/'),
        ('Наши выпускники', 'dogs/'),
        ('Выставки', 'shows/'),
        ('Фото', 'photos.htm'),
        ('Щенки на продажу', 'sale.htm')]


def _make_html_class_list(class_list):
    has_duplicates = any(class_list.count(element) > 1 for element in class_list)
    if has_duplicates:
        raise ValueError('css classes must not repeat; check for typos')
    if any(('"' in element or ' ' in element) for element in class_list):
        raise ValueError('css classes must not contain quotes and spaces')
    return ' '.join(class_list)


def as_minimal_url(path):
    parts = list(path.parts)
    if parts[-1].startswith('index.'):
         parts[-1] = ''
    return '/'.join(parts)


class Document(object):
    def __init__(self, title, path, database):
        self._resources = database['resources']
        self._photos = database['photos']

        self._content_chunks = []
        self._content_chunks.append('<!DOCTYPE html><html lang="ru">')
        self._content_chunks.append('<meta charset="utf-8">')
        full_title = '{} — {}'.format(title, brand_ru) if title else brand_ru
        self._content_chunks.append('<title>{}</title>'.format(full_title))
        self._content_chunks.append('<link rel="stylesheet" href="/common.css">')
        self._content_chunks.append('<link rel="icon" href="/favicon.png">')

        gallery = ('<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/'
                   'libs/baguettebox.js/1.11.1/baguetteBox.min.css">'
                    '<script src="//cdnjs.cloudflare.com/ajax/libs/'
                    'baguettebox.js/1.11.1/baguetteBox.min.js" async></script>'
                    '<script>addEventListener("load", function() {baguetteBox.'
                    'run("article", {noScrollbars: true})})</script>')
        self._gallery_script = ConditionalText(gallery)
        self._content_chunks.append(self._gallery_script)
        self._content_chunks.append('<header>')
        brand_pretty = brand_en.replace('«', '<span>«').replace('»', '»</span>')
        self._content_chunks.append('<h1>{}</h1>'.format(brand_pretty))

        photo = self._photos.get_card_assignation('site_head')
        photo.set_caption('Логотип')
        self.add_image('', '', 'w', 500, False, photo.get_image())

        self._content_chunks.append('</header>')

        self._content_chunks.append('<nav><ul>')
        page_rel_url = as_minimal_url(path)
        for title, menu_path in menu:
            if not menu_path:
                menu_path = 'index.html'
            if page_rel_url == menu_path:
                item = '<li><span class="current">{}</span></li>'.format(title)
            elif page_rel_url.startswith(menu_path):
                item = '<li><a href="/{}" class="current">{}</a></li>'.format(menu_path, title)
            else:
                item = '<li><a href="/{}">{}</a></li>'.format(menu_path, title)
            self._content_chunks.append(item)
        self._content_chunks.append('</ul></nav>')


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


    def add_image(self, output_name, caption, dimension_type, dimension, is_clickable, input_image=None):
        if is_clickable:
            self._gallery_script.trigger_condition()
            dimension = ('e', 794)
            fullsize = image.get_generation_promise_for_size(dimension, to='img')
            self._content_chunks.append('<a href="/')
            self._content_chunks.append(fullsize.posix_path_chunk)
            self._content_chunks.append('" title="{}">'.format(caption))

        dimension = (dimension_type, dimension_size)
        preview = image.get_generation_promise_for_size(dimension, to='img')
        self._content_chunks.append('<img src="/')
        self._content_chunks.append(preview.posix_path_chunk)
        self._content_chunks.append('" width="')
        self._content_chunks.append(preview.width_chunk)
        self._content_chunks.append('" height="')
        self._content_chunks.append(preview.height_chunk)
        self._content_chunks.append('" alt="{}">'.format(caption))

        if is_clickable:
            self._content_chunks.append('</a>')


    def _add_pedigree_cell(self, dog_id, dog_info, all_dogs, current_depth, max_depth):
        rowspan = 2 ** (max_depth - 1 - current_depth)
        if rowspan > 1:
            self._content_chunks.append('<td rowspan="{}">'.format(rowspan))
        else:
            self._content_chunks.append('<td>')

        self._content_chunks.append('<p>')
        self._content_chunks.append(',<br>'.join(dog_info.get('extra_titles', [])))
        self._content_chunks.append('<p>{}</p>'.format(dog_info['name']['nom']))
        if current_depth == 0:
            photo = self._photos.get_card_assignation(dog_id)
            caption = dog_info['name']['nom']
            self.add_image(photo.get_id(), caption if caption else photo.get_caption(), 'w', 168, True, photo.get_image())

        self._content_chunks.append('</td>')
        self._add_pedigree(dog_info, all_dogs, current_depth + 1, max_depth)


    def _add_pedigree(self, dog_info, all_dogs, current_depth, max_depth):
        if current_depth >= max_depth:
            return

        if not dog_info['father']:
            raise ValueError('A father must be specified for {}'.format(dog_info['name']['nom']))
        father_id = dog_info['father']
        self._add_pedigree_cell(father_id, all_dogs[father_id], all_dogs, current_depth, max_depth)

        self._content_chunks.append('<tr>')

        if not dog_info['mother']:
            raise ValueError('A mother must be specified for {}'.format(dog_info['name']['nom']))
        mother_id = dog_info['mother']
        self._add_pedigree_cell(mother_id, all_dogs[mother_id], all_dogs, current_depth, max_depth)


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
        try:
            human_format = date.strftime('%-d.%m.%Y')
        except ValueError:
            human_format = date.strftime('%d.%m.%Y')
        chunk = '<time datetime="{}">{} г.</time>'.format(html_format, human_format)
        self._content_chunks.append(chunk)


    def start_list(self, css_classes=[]):
        class_list = _make_html_class_list(css_classes)
        class_mixin = ' class="{}"'.format(class_list) if css_classes else ''
        self._content_chunks.append('<ul{}>'.format(class_mixin))


    def start_list_item(self):
        self._content_chunks.append('<li>')


    def end_list_item(self):
        self._content_chunks.append('</li>')


    def end_list(self):
        self._content_chunks.append('</ul>')


    def end_document(self):
        now = datetime.now()
        copyright = '© Ярыгин О. В. (oleg@arhadthedev.net) 2015–{}.'.format(now.year)
        footer = '<footer><p>{}</footer>'.format(copyright)
        self._content_chunks.append(footer)


    def __str__(self):
        return ''.join(map(str, self._content_chunks))
