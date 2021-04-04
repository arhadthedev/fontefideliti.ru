# -*- coding: UTF-8 -*-
# dogs.py - generates content of /dogs.htm
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

import yaml


def get_dog_records_key(dog_list):
    def _key_generator(value):
        dog_id, dog_payload = value

        ordering_components = []
        next_component_id = dog_payload.get('after')
        if dog_id == next_component_id:
            raise ValueError('A record can not follow itself')
        while next_component_id:
            next_component = dog_list[next_component_id]
            ordering_components.append(next_component_id)
            next_component_id = next_component.get('after', '')
        ordering_components.reverse()
        return '>'.join(ordering_components)
    return _key_generator


def generate_dogs(output_document, resources):
    dog_list = yaml.safe_load(resources.get('doglist.yml'))
    dogs = [dog for dog in dog_list.items() if dog[1]['type'] == 'nonbreeder']
    dogs.sort(key=get_dog_records_key(dog_list))
    for dog_id, dog_details in dogs:
        output_document.start_container(css_classes=['filled'])
        output_document.add_header(3, dog_details['name']['nom'])
        output_document.add_raw(dog_details.get('content', ''))
        output_document.add_raw('<p>Дата рождения: ')
        output_document.add_date(dog_details['dob'])
        output_document.add_raw('</p>')
        father_details = dog_list[dog_details['father']]
        mother_details = dog_list[dog_details['mother']]
        output_document.add_raw('<p>{} × {}</p>'.format(father_details['name']['nom'], mother_details['name']['nom']))
        output_document.add_raw('<p><a href="http://www.pedigreedatabase.com/german_shepherd_dog/dog.html?id={}">Родословная</a></p>'.format(dog_details['pedigree']['pd']))
        output_document.add_image(dog_details['photo'], dog_details['name']['nom'], 'h', 250, True)
        output_document.end_container()


def get_root_artifact_list(resources):
    return [('Собаки питомника', 'dogs', generate_dogs)]
