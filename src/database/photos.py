# -*- coding: UTF-8 -*-
# photos.py - maintains photos and their metainformation
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

from datetime import date
from pathlib import Path
from PIL import Image


class Photo:
    def __init__(self, id, date):
        self._id = id
        self._date = date
        self._caption = ''


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
    def __init__(self, gallery_path):
        self._dates = {}
        self._by_attribute = {}

        for photo_path in gallery_path.glob('*/*.jpg'):
            relative_photo_path = photo_path.relative_to(gallery_path)
            year, id_and_attributes = relative_photo_path.with_suffix('').parts
            month_date_seq, *attributes = id_and_attributes.split(' ')
            month, day, sequence = month_date_seq[0:2], month_date_seq[2:4], month_date_seq[4:]

            # Image loading is lazy so we can open hundreds of photos fast
            photo_id = Path(year, month + day + sequence)
            photo_date = date(int(year), int(month), int(day))
            photo = Photo(photo_id, photo_date)
            self._dates.setdefault(photo_date, []).append(photo)

            dogs = []
            image = Image.open(photo_path)
            for attribute in attributes:
                name, value = attribute[:2], attribute[2:]
                attribute_group = self._by_attribute.setdefault(name, {})
                attribute_group.setdefault(value, []).append(photo)
                if name == 'd=':
                    dogs.append(value)
                if name == 'c=':
                    crop_margins = value.split(',')
                    crop_left = int(crop_margins[0])
                    crop_top = int(crop_margins[1])
                    crop_right = image.width - int(crop_margins[2])
                    crop_bottom = image.height - int(crop_margins[3])
                    crop_rect = (crop_left, crop_top, crop_right, crop_bottom)
                    image = image.crop(crop_rect)

            photo._dogs = dogs
            photo._image = image


    def get_for_date(self, date):
        return self._dates[date] if date in self._dates else []


    def get_card_assignation(self, assignation_name):
        assigned = self._by_attribute.get('t=', {}).get(str(assignation_name))
        if assigned == None:
            raise ValueError('There must be a photo assigned to {} card'.format(assignation_name))
        if len(assigned) > 1:
            raise ValueError('Only a single photo may be assigned to {} card'.format(assignation_name))
        return assigned[0]


    def get_for_id(self, id):
        year, month, day, sequence = id[0:4], id[5:7], id[7:9], id[9]
        prefix_group = self.get_for_date(date(int(year), int(month), int(day)))
        return [e for e in prefix_group if str(e.get_id())[-1] == sequence][0]
