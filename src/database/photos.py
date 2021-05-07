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
from tools.text_chunks import DynamicText


class GenerationPromise:
    def __init__(self):
        self.posix_path_chunk = DynamicText()
        self.width_chunk = DynamicText()
        self.height_chunk = DynamicText()


    def __repr__(self):
        return 'GenerationPromise(path={}, w={}, h={})'.format(self.posix_path_chunk, self.width_chunk, self.height_chunk)


class Photo:
    def __init__(self, gallery_root, relative_input_path, date):
        self._gallery_root = gallery_root
        self._relative_input_path = relative_input_path
        self._date = date
        self._caption = ''

        self._generation_promises = {}

        self._blackening = None
        self._crop_margins = None


    def get_path(self):
        return self._path


    def get_generation_promise_for_size(self, dimension, to):
        key = dimension, Path(to)
        promise = self._generation_promises.setdefault(key, GenerationPromise())
        return promise


    def keep_generation_promises(self, rewrite_existing, photo_logger):
        photo_logger(self._relative_input_path)

        for (dimension, output_directory), promise in self._generation_promises.items():
            dimension_type, dimension_size = dimension
            REASONABLY_LARGE_SIZE = 9_999
            if dimension_type == 'w':
                max_size = dimension_size, REASONABLY_LARGE_SIZE
                output_infix = '-w{}'.format(dimension_size)

            elif dimension_type == 'h':
                max_size = REASONABLY_LARGE_SIZE, dimension_size
                output_infix = '-h{}'.format(dimension_size)

            elif dimension_type == 'e':
                max_size = REASONABLY_LARGE_SIZE, REASONABLY_LARGE_SIZE

                output_infix = ''
            else:
                raise ValueError('dimension_type can be "w", "h", or "e" only')

            noattrib_stem = self._relative_input_path.stem.split(' ')[0]
            output_stem = '{}{}'.format(noattrib_stem, output_infix)
            output_name = self._relative_input_path.with_name(output_stem + self._relative_input_path.suffix)
            output_path = output_directory / output_name

            if output_path.exists() and not rewrite_existing:
                continue

            image = Image.open(self._gallery_root / self._relative_input_path)

            if self._blackening:
                image = ImageEnhance.Contrast(image).enhance(self._blackening)
            if self._crop_margins:
                left, top, right, bottom = self._crop_margins
                crop_rect = (left, top, image.width - right, image.height - bottom)
                image = image.crop(crop_rect)

            image.thumbnail(max_size, Image.LANCZOS)

            promise.posix_path_chunk.set_content(output_path.as_posix())
            promise.width_chunk.set_content(str(image.width))
            promise.height_chunk.set_content(str(image.height))

            output_path.parent.mkdir(exist_ok=True)
            image.save(output_path, quality=94, optimize=True, progressive=True)


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


    def get_card_assignation(self, assignation_name, multiphoto_group=False):
        assigned = self._by_attribute.get('t=', {}).get(str(assignation_name))
        if assigned == None:
            raise ValueError('There must be a photo assigned to {} card'.format(assignation_name))
        if multiphoto_group:
            return assigned
        else:
            if len(assigned) > 1:
                raise ValueError('Only a single photo may be assigned to {} card'.format(assignation_name))
            return assigned[0]


    def keep_generation_promises(self, rewrite_existing, photo_logger):
        # each photo belongs to a single date unlike other categories
        for date, date_group in self._dates.items():
            for photo in date_group:
                photo.keep_generation_promises(rewrite_existing, photo_logger)
