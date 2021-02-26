# -*- coding: UTF-8 -*-

import yaml

site_name = 'Питомник немецких овчарок {}«Fonte Fideliti»{} г. Тольятти'


def write_metainfo(output, title):
    output.write('<!DOCTYPE html><html lang="ru">')
    output.write('<meta charset="utf-8">')
    output.write('<!--[if lt IE 9]><script src="//cdnjs.cloudflare.com/ajax/libs/html5shiv/r29/html5.min.js"></script><![endif]-->')
    output.write('<link rel="stylesheet" href="/style.css">')
    output.write('<link rel="shortcut icon" href="/favicon.png">')
    output.write('<title>{} — {}</title>'.format(title, site_name.format('', '')))


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


def write_main(output, name, youtube_ids):
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


def fill_page(output, name, youtube_ids):
    title = "Видео {}".format(name['gen'])
    write_metainfo(output, title)
    write_header(output, title)
    write_navigation(output)
    write_main(output, name, youtube_ids)
    write_footer(output)


def generate_section(output, resources):
    dog_list = yaml.safe_load(resources.get('doglist.yml'))
    for dog_id, dog_details in dog_list.items():
        output_path = '{}s/{}/video.htm'.format(dog_details['gender'], dog_id)
        page = output.create_file(output_path)
        name = dog_details['name']
        youtube_ids = dog_details['videos']
        fill_page(page, name, youtube_ids)
