# -*- coding: UTF-8 -*-
# shows.py - maintains information about shows
#
# Copyright (c) 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

import yaml


class ShowList:
    def __init__(self, resources):
        self._shows = resources.get_yaml('shows.yml')


    def get_for_year(self, year):
        events = [(date, events) for (date, events) in self._shows.items() if date.year == year]
        events.sort(key=lambda x: x[0], reverse=True)
        return events

    def get_for_dog(self, dog_id):
        filtered_shows = []
        for date, events in self._shows.items():
            for event in events:
                for current_dog_id, dog_details in event['dogs'].items():
                    if current_dog_id == dog_id:
                        element = {}
                        element['date'] = date
                        element['rank'] = event['rank']
                        if 'cup' in event:
                            element['cup'] = event['cup']
                        element['city'] = event['city']
                        element['class'] = dog_details['class']
                        element['expert'] = event['expert']
                        if 'figurant' in element:
                            element['figurant'] = event['figurant']
                        element['place'] = dog_details['place']
                        if 'note' in dog_details:
                            element['note'] = dog_details['note']
                        element['achievements'] = dog_details.get('achievements', [])
                        filtered_shows.append(element)
        return filtered_shows
