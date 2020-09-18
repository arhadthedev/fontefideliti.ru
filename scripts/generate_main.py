#!/usr/bin/env python3

# build.py - builds /index.html into a current folder
#
# Copyright (c) 2020 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

from PIL import Image

img_path = 'img/main.jpg'
hasso = Image.open(img_path)
w, h = hasso.size
img = f'<img src="{img_path}" width="{w}" height="{h}" alt="Фанхил Хаус Хассо">'
