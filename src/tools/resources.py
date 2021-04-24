# -*- coding: UTF-8 -*-
# resources.py - manages content of a directory with source resources
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

import csv
import datetime
import os
import PIL
import yaml


# based on https://russkiiyazyk.ru/chasti-rechi/sushhestvitelnoe/tipyi-skloneniya-imen-sushhestvitelnyih.html
def _declense(word, case, gender):
    if case == 'gen':
        if word[-2:] == 'ия':
            return ''.join(word[:-2] + 'ии')
        elif word[-2:] == 'ие':
            return ''.join(word[:-2] + 'ия')
        elif word[-1] == 'а':
            return ''.join(word[:-1] + 'ы')
        elif word[-1] == 'я':
            return ''.join(word[:-1] + 'и')
        #elif word[-1] == 'о':  -- Хассо proves that this is a bad idea
        #    return ''.join(word[:-1] + 'а')
        #elif word[-1] == 'е':
        #    return ''.join(word[:-1] + 'я')
        elif word[-1] == 'ь':
            if gender == 'f':
                return ''.join(word[-1:] + 'и')
            else:
                return ''.join(word[-1:] + 'я')
        else:
            return word
    else:
        raise NotImplementedError('only genitive case is supported for now')


def _get_genitive_dog_name(name, case, gender):
    # Non-russian name, do not declense
    if not 'А' <= name[0].capitalize() <= 'Я':
        return name

    name_first_features = ['оф', 'с']
    words = name.split(' ')
    if any(word in name_first_features for word in words):
        words[0] = _declense(words[0], case, gender)
    else:
        words[-1] = _declense(words[-1], case, gender)
    return ' '.join(words)


class Input(object):
    def __init__(self, base_path):
        self._base_path = base_path
        self._cached_parsed_resources = {}


    def get_string(self, rel_path):
        full_path = os.path.join(self._base_path, rel_path)
        with open(full_path, 'r', encoding='utf-8') as file:
            return file.read()


    # All modifications of the returned object will be observable by the
    # following calls of get_yaml() with the same rel_path.
    def get_yaml(self, rel_path):
        full_path = os.path.join(self._base_path, rel_path)
        if not rel_path in self._cached_parsed_resources:
            with open(full_path, 'r', encoding='utf-8') as file:
               self._cached_parsed_resources[rel_path] = yaml.safe_load(file)
               if rel_path == 'doglist.yml':
                    dl_full_path = os.path.join(self._base_path, 'dog_list.csv')
                    with open(dl_full_path, 'r', encoding='utf-8') as csv_data:
                        for line in csv.DictReader(csv_data):
                            if line['ID'] not in self._cached_parsed_resources[rel_path]:
                                self._cached_parsed_resources[rel_path][line['ID']] = {}
                            dog = self._cached_parsed_resources[rel_path][line['ID']]
                            types = {'': 'nonbreeder', 'b': 'breeder', 'r': 'retired'}
                            dog['type'] = types[line['Type']] if line['DOB'] else 'pedigree-only'
                            if 'name' not in dog:
                                dog['name'] = {}
                            dog['name']['nom'] = line['Name']
                            dog['name']['gen'] = _get_genitive_dog_name(line['Name'], 'gen', line['Gender'])
                            if line['Gender']:
                                genders = {'f': 'female', 'm': 'male'}
                                dog['gender'] = genders[line['Gender']]
                            if line['DOB']:
                                dog['dob'] = datetime.date.fromisoformat(line['DOB'])
                            dog['father'] = line['Father']
                            dog['mother'] = line['Mother']
                            dog['pedigree'] = {}
                            dog['pedigree']['pd'] = line['Pedigree Database #']
                            dog['pedigree']['gsdog'] = line['GSDOG #']
                            if line['Renter']:
                                dog['renter'] = 'питомник «{}»'.format(line['Renter'])
                            dog['after'] = format(line['Display After'])
        return self._cached_parsed_resources[rel_path]


    def get_image(self, rel_path):
        full_path = os.path.join(self._base_path, rel_path)
        return PIL.Image.open(full_path)
