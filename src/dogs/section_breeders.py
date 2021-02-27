# -*- coding: UTF-8 -*-

import datetime
import yaml

site_name = 'Питомник немецких овчарок {}«Fonte Fideliti»{} г. Тольятти'


def write_metainfo(output, title, allow_interactive_images, use_modern_styles):
    output.write('<!DOCTYPE html><html lang="ru">')
    output.write('<meta charset="utf-8">')
    output.write('<!--[if lt IE 9]><script src="//cdnjs.cloudflare.com/ajax/libs/html5shiv/r29/html5.min.js"></script><![endif]-->')
    if use_modern_styles:
        output.write('<link rel="stylesheet" href="/common.css">')
    else:
        output.write('<link rel="stylesheet" href="/style.css">')
    output.write('<link rel="shortcut icon" href="/favicon.png">')
    output.write('<title>{} — {}</title>'.format(title, site_name.format('', '')))
    if allow_interactive_images:
        output.write('<link rel="stylesheet" href="/fancybox/jquery.fancybox.css">')
        output.write('<script src="/jquery-1.11.0.min.js"></script>')
        output.write('<script src="/fancybox/jquery.fancybox.pack.js" defer></script>')


def write_header(output, title):
    output.write('<header><h1>')
    output.write(site_name.format('<span>', '</span>'))
    output.write('</h1><img src="/img/title.jpg" width="500" height="260" alt="Логотип">')
    output.write('</header>')


def write_navigation(output):
    output.write('<nav>')
    output.write('<ul>')
    output.write('<li><a href="/">Главная</a>')
    output.write('<li><a href="/males/">Производители</a>')
    output.write('<li><a href="/females/">Производительницы</a>')
    output.write('<li><a href="/shows/">Выставки</a>')
    output.write('<li><a href="/dogs.htm">Наши выпускники</a>')
    output.write('<li><a href="/photos.htm">Фото</a>')
    output.write('<li><a href="/sale.htm">Щенки на продажу</a>')
    output.write('</ul>')
    output.write('</nav>')


def write_photo_main(output, name, photos):
    output.write('<article>')
    output.write('<h1>Фото <a href="/males/itan/">{}</a></h1>'.format(name['gen']))
    for photo in photos:
        preview = photo.get('preview') if photo.get('preview') else 'p'
        output.write('<a href="/img/{p}.jpg" title="{c}" rel="a"><img src="/img/{p}-{pr}.jpg" alt="{c}" height="152"></a>'.format(p=photo['path'], pr=preview, c=photo['caption']))
    output.write('</article>')

def write_video_main(output, name, youtube_ids):
    output.write('<article class="filled">')
    output.write('<h1>Видео <a href="/males/itan/">{}</a></h1>'.format(name['gen']))
    for video_id in youtube_ids:
        output.write('<p>')
        output.write('<iframe width="560" height="315" src="https://www.youtube.com/embed/{}" style="border:0px" allow="gyroscope; picture-in-picture" allowfullscreen></iframe>'.format(video_id))
    output.write('</article>')


def write_footer(output):
    output.write('<footer>')
    output.write('<p>Copyright © 2015–2021 <a href="//vk.com/arhad95" rel="author">Олег Ярыгин</a>.</p>')
    output.write('</footer>')
    output.write('</html>')


def fill_photo_page(output, name, photos):
    title = "Фото {}".format(name['gen'])
    write_metainfo(output, title, True, False)
    write_header(output, title)
    write_navigation(output)
    write_photo_main(output, name, photos)
    write_footer(output)


def fill_video_page(output, name, youtube_ids):
    title = "Видео {}".format(name['gen'])
    write_metainfo(output, title, False, False)
    write_header(output, title)
    write_navigation(output)
    write_video_main(output, name, youtube_ids)
    write_footer(output)


def generate_section(output, resources):
    dog_list = yaml.safe_load(resources.get('doglist.yml'))
    photo_list = yaml.safe_load(resources.get('dogphotos.yml'))
    for dog_id, dog_details in dog_list.items():
        name = dog_details['name']

        output_path = '{}s/{}/photos.htm'.format(dog_details['gender'], dog_id)
        page = output.create_file(output_path)
        photos = photo_list.get(dog_id)
        if photos == None:
            photos = []
        fill_photo_page(page, name, photos)

        output_path = '{}s/{}/video.htm'.format(dog_details['gender'], dog_id)
        page = output.create_file(output_path)
        youtube_ids = dog_details.get('videos')
        if youtube_ids == None:
            youtube_ids = []
        fill_video_page(page, name, youtube_ids)
