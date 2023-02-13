from __future__ import annotations

import re
import datetime
from collections import OrderedDict, namedtuple, defaultdict
from datetime import datetime
from typing import Dict, Type, DefaultDict

NameTeamNamedTuple: Type[NameTeamNamedTuple] = namedtuple(
    'NameTeamNamedTuple', ['name', 'team'])


def create_racer_abbreviations_dict(file_name) -> \
        DefaultDict[str, NameTeamNamedTuple]:
    """
    Retrieves {'abbreviation': (name, team)}
    format dict from abbreviations.txt
    """
    abbreviations: DefaultDict[str, NameTeamNamedTuple] = \
        defaultdict(NameTeamNamedTuple)
    with open(file_name, 'r') as file:
        for line in file:
            match_obj = re.match(r'^(\w+)_([a-zA-Z\s]+)_([a-zA-Z\s]+)$', line)
            abbreviations[match_obj.group(1)] = NameTeamNamedTuple(
                name=match_obj.group(2),
                team=match_obj.group(3).rstrip()
            )
    return abbreviations


def retrieve_timings_from_log(file_name) -> Dict[str, datetime]:
    """
     matches 2 groups: abbreviation of a racer and time
     returns timing log from start.log or end.log in
      {'abbreviation': time} format
    """

    timing_log = {}
    with open(file_name, 'r') as file:
        for line in file:
            match_obj = re.match(r'^([A-Z]+).*(\d{2}:\d+:\d+\.\d+)$', line)
            # converts time from a string to datetime object
            lap_time = datetime.datetime.strptime(
                match_obj.group(2).rstrip(), '%H:%M:%S.%f')
            timing_log[match_obj.group(1)] = lap_time
    return timing_log


def sorted_individual_results(start_timings: Dict[str, datetime],
                              end_timings: Dict[str, datetime]) \
        -> Dict[str, int]:
    """
    creating dict with best lap results
    Receives start and end timings and returns an OrderedDict with
    {abbreviations:timedelta in minutes}
    """

    keys = set(start_timings.keys()).intersection(set(end_timings.keys()))
    lap_results = {
        key: (end_timings[key] - start_timings[key]).seconds // 60
        for key in keys
    }
    sorted_results = OrderedDict(
        sorted(lap_results.items(), key=lambda x: x[1]))
    return sorted_results


def print_result_board(sorted_lap_results: Dict[str, int],
                       abbreviations: DefaultDict[str, NameTeamNamedTuple]):
    """
    prints result board to a console
    """
    counter = 1
    for abbreviation, time in sorted_lap_results.items():
        racer_name = abbreviations[abbreviation].name
        team_name = abbreviations[abbreviation].team
        print(("{: <3} {: <18} | {: <30}  | {}".format(
            str(counter) + '.', racer_name, team_name, str(time)))
        )
        if counter == 15:
            print('-' * 70)
        counter += 1


def main():
    abbreviations = create_racer_abbreviations_dict('abbreviations.txt')
    start_timings = retrieve_timings_from_log('start.log')
    end_timings = retrieve_timings_from_log('end.log')
    sorted_lap_results = sorted_individual_results(start_timings, end_timings)
    print_result_board(sorted_lap_results, abbreviations)
