# -*- coding: UTF-8 -*-
# photos.py - maintains photos and their metainformation
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

from datetime import date
from pathlib import Path
from PIL import Image, ImageEnhance


class Photo:
    def __init__(self, gallery_root, relative_input_path, date):
        self._gallery_root = gallery_root
        self._relative_input_path = relative_input_path
        self._date = date
        self._caption = ''

        self._blackening = None
        self._crop_margins = None


    def get_path(self):
        return self._path


    def get_image(self):
        image = Image.open(self._input_path)
        if self._blackening:
            image = ImageEnhance.Contrast(image).enhance(self._blackening)
        if self._crop_margins:
            left, top, right, bottom = self._crop_margins
            abs_right = image.width - right
            abs_bottom = image.height - bottom
            cropping_rectangle = left, top, abs_right, abs_bottom
            image = image.crop(cropping_rectangle)

        return image


    def get_id(self):
        return None


    def set_caption(self, caption):
        if not self._caption:
            self._caption = caption


    def get_caption(self):
        return self._caption


    def get_attributes(self,):
        return {'dogs': self._dogs}


class PhotoList:
    def __init__(self, gallery_path):
        self._dates = {}
        self._by_attribute = {}
        self._gallery_root = gallery_path

        for photo_path in gallery_path.glob('**/*.jpg'):
            relative_photo_path = photo_path.relative_to(gallery_path)

            try:
                year, id_and_attributes = relative_photo_path.with_suffix('').parts
                month_date_seq, *attributes = id_and_attributes.split(' ')
                month, day = month_date_seq[0:2], month_date_seq[2:4]
                photo_date = date(int(year), int(month), int(day))

            except ValueError:
                id_and_attributes = relative_photo_path.with_suffix('').parts[0]
                _, *attributes = id_and_attributes.split(' ')
                photo_date = None

            photo = Photo(self._gallery_root, relative_photo_path, photo_date)
            self._dates.setdefault(photo_date, []).append(photo)

            dogs = []
            for attribute in attributes:
                name, value = attribute[:2], attribute[2:]
                if name == 'b=':
                    photo._blackening = float(value)
                if name == 'c=':
                    raw_crop_margins = value.split(',')
                    photo._crop_margins = tuple(map(int, raw_crop_margins))
                else:
                    attribute_group = self._by_attribute.setdefault(name, {})
                    attribute_group.setdefault(value, []).append(photo)
                    if name == 'd=':
                        dogs.append(value)

            photo._dogs = dogs


    def get_for_date(self, date):
        return self._dates[date] if date in self._dates else []


    def get_for_dog(self, dog_id):
        return self._by_attribute.get('d=', {}).get(dog_id)


    def get_card_assignation(self, assignation_name):
        assigned = self._by_attribute.get('t=', {}).get(str(assignation_name))
        if assigned == None:
            raise ValueError('There must be a photo assigned to {} card'.format(assignation_name))
        if len(assigned) > 1:
            raise ValueError('Only a single photo may be assigned to {} card'.format(assignation_name))
        return assigned[0]
