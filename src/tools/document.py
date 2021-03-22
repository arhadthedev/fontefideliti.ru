# -*- coding: UTF-8 -*-

from datetime import datetime
import os
from PIL import Image

brand_ru = 'Питомник немецких овчарок «Фонте Фиделити» г. Тольятти'
brand_en = 'Питомник немецких овчарок «Fonte Fideliti» г. Тольятти'

menu = [('Главная', '//fontefideliti.ru'),
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
    def __init__(self, title, path, output_directory):
        self._output_directory = output_directory

        self._content_chunks = []
        self._content_chunks.append('<!DOCTYPE html><html lang="ru">')
        self._content_chunks.append('<meta charset="utf-8">')
        full_title = '{} — {}'.format(title, brand_ru) if title else brand_ru
        self._content_chunks.append('<title>{}</title>'.format(full_title))
        self._content_chunks.append('<link rel="stylesheet" href="/common.css">')
        self._content_chunks.append('<link rel="icon" href="/favicon.png">')

        self._content_chunks.append('<header>')
        brand_pretty = brand_en.replace('«', '<span>«').replace('»', '»</span>')
        self._content_chunks.append('<h1>{}</h1>'.format(brand_pretty))
        self.add_image('title', 'Логотип', 'w', 500, False)
        self._content_chunks.append('</header>')

        self._content_chunks.append('<nav><ul>')
        for title, menu_path in menu:
            if path.startswith(menu_path):
                item = '<li><span class="current">{}'.format(title)
            else:
                item = '<li><a href="{}">{}</a>'.format(menu_path, title)
            self._content_chunks.append(item)
        self._content_chunks.append('</nav>')


    def start_container(self, css_classes=[]):
        class_list = _make_html_class_list(css_classes)
        class_mixin = ' class="{}"'.format(class_list) if css_classes else ''
        self._content_chunks.append('<article{}>'.format(class_mixin))

    def end_container(self):
        self._content_chunks.append('</article>')


    def start_paragraph(self, css_classes=[]):
        class_list = _make_html_class_list(css_classes)
        class_mixin = ' class="{}"'.format(class_list) if css_classes else ''
        self._content_chunks.append('<p{}>'.format(class_mixin))


    def add_plain(self, text):
        text_safe = text.replace('&', '&amp;').replace('<', '&lt;')
        self._content_chunks.append(text_safe)


    def add_image(self, name, caption, dimension_type, dimension, is_clickable):
        size = '{}{}'.format(dimension_type, dimension)
        if dimension_type == 'w':
            max_size = dimension, 9999
        elif dimension_type == 'h':
            max_size = 9999, dimension
        else:
            raise ValueError('dimension_type can be "w" or "h" only')

        original = Image.open('img/{}.jpg'.format(name))
        imgdir = '{}/img'.format(self._output_directory)
        output_path = '{}/{}-{}.jpg'.format(imgdir, name, size)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        width = None
        height = None
        if not os.path.isfile(output_path):
            preview = original.copy()
            preview.thumbnail(max_size, Image.LANCZOS, None)
            preview.save(output_path, quality=94, optimize=True, progressive=True)
            width, height = preview.size
        else:
            with Image.open(output_path) as existing:
                width, height = existing.size
        self._content_chunks.append('<img src="/img/{}-{}{}.jpg" width="{}" height="{}" alt="{}">'.format(name, dimension_type, dimension, width, height, caption))


    def finalize(self):
        now = datetime.now()
        copyright = '© Ярыгин О. В. (oleg@arhadthedev.net) 2015–{}.'.format(now.year)
        footer = '<footer><p>{}</footer>'.format(copyright)
        self._content_chunks.append(footer)
        return ''.join(self._content_chunks)
