# snippets.py - a collection of HTML snippets with repetitions inside
#
# Copyright (c) 2020 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

from PIL import Image


def make_link(addr):
    return f'<a href="//{addr}" target="_blank">{addr}</a>'


def make_tel(num):
    f_num = f'{num[0:2]} ({num[2:5]}) {num[5:8]}-{num[8:10]}-{num[10:12]}'
    return f'т. <a href="tel:{num}">{f_num}</a>'


def make_email(addr):
    return f'<a href="mailto:{addr}">{addr}</a>'


def make_image(real_path, src, alt):
    image = Image.open(real_path)
    w, h = image.size
    return f'<img src="/{src}" width="{w}" height="{h}" alt="{alt}">'
