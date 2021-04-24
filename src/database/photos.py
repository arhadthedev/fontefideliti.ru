# -*- coding: UTF-8 -*-
# photos.py - maintains photos and their metainformation
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

from datetime import date
from os import listdir, sep
from os.path import isdir, isfile, join, splitext
from PIL import Image


class Photo:
    def __init__(self, image, id, date):
        self._image = image
        self._id = id
        self._date = date
        self._caption = ''
        self._dogs = []


    def get_path(self):
        return self._path


    def get_id(self):
        return self._id


    def set_caption(self, caption):
        if not self._caption:
            self._caption = caption


    def get_caption(self):
        return self._caption


    def get_attributes(self,):
        return {'dogs': self._dogs}


    def get_image(self):
        return self._image


class PhotoList:
    def __init__(self, path):
        self._dates = {}

        years = [d for d in listdir(path) if isdir(join(path, d))]
        for year in years:
            if year == 'photos':
                continue
            photos = [f for f in listdir(join(path, year))]
            photos.sort()
            for filename in photos:
                full_path = join(year, filename)
                photo_id, *attributes = splitext(full_path)[0].split(' ')
                photo_id = photo_id.replace(sep, '/')
                month, day, sequence = filename[0:2], filename[2:4], filename[4:]

                photo_path = join(path, year, filename)
                photo_date = date.fromisoformat('{}-{}-{}'.format(year, month, day))

                # Image loading is lazy so we can open hundreds of photos fast
                image = Image.open(photo_path)
                photo = Photo(image, photo_id, photo_date)
                self._dates.setdefault(photo_date, []).append(photo)

                for attribute in attributes:
                    name, value = attribute[:2], attribute[2:]
                    if name == 'd=':
                        photo._dogs.append(value)


    def get_for_date(self, date):
        return self._dates[date] if date in self._dates else []


    def get_for_id(self, id):
        year, month, day, sequence = id[0:4], id[5:7], id[7:9], id[9]
        prefix_group = self.get_for_date(date.fromisoformat('{}-{}-{}'.format(year, month, day)))
        return [e for e in prefix_group if e.get_id()[-1] == sequence][0]
