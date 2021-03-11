# -*- coding: UTF-8 -*-

from datetime import datetime

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
    def __init__(self, title, path):
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
        self._content_chunks.append('<img src="/img/title.jpg" alt="Логотип" width="500" height="260">')
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


    def finalize(self):
        now = datetime.now()
        copyright = '© Ярыгин О. В. (oleg@arhadthedev.net) 2015–{}.'.format(now.year)
        footer = '<footer><p>{}</footer>'.format(copyright)
        self._content_chunks.append(footer)
        return ''.join(self._content_chunks)
