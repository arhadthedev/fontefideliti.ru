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
    def __init__(self, input_path, id, date):
        self._input_path = input_path
        self._id = id
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
        return self._id


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

        for photo_path in gallery_path.glob('*/**/*.jpg'):
            relative_photo_path = photo_path.relative_to(gallery_path)

            if relative_photo_path.parts[0] == 'photos':
                photo_id = relative_photo_path.with_suffix('').as_posix()
                photo_date = photo_id
            else:
                year, id_and_attributes = relative_photo_path.with_suffix('').parts
                month_date_seq, *attributes = id_and_attributes.split(' ')
                month, day, sequence = month_date_seq[0:2], month_date_seq[2:4], month_date_seq[4:]

                photo_id = Path(year, month + day + sequence)
                photo_date = date(int(year), int(month), int(day))
            photo = Photo(photo_path, photo_id, photo_date)
            self._dates.setdefault(photo_date, []).append(photo)

            dogs = []
            for attribute in attributes:
                name, value = attribute[:2], attribute[2:]
                attribute_group = self._by_attribute.setdefault(name, {})
                attribute_group.setdefault(value, []).append(photo)
                if name == 'd=':
                    dogs.append(value)
                if name == 'b=':
                    photo._blackening = float(value)
                if name == 'c=':
                    raw_crop_margins = value.split(',')
                    photo._crop_margins = tuple(map(int, raw_crop_margins))

            photo._dogs = dogs


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
        year, month, day, sequence = id[0:4], id[5:7], id[7:9], id[9:]
        try:
            prefix_group = self.get_for_date(date(int(year), int(month), int(day)))
            return [e for e in prefix_group if str(e.get_id())[9:] == sequence][0]
        except ValueError:
            return self._dates[id][0]
