from collections import namedtuple
from itertools import groupby


"""
input: list of actions
output: list of athlete_groups
"""
def group_by_athlete(actions):
    #one must sort before grouping
    actions_sorted = sorted(actions, key = lambda a: a['athlete'])
    actions_grouped = groupby(actions_sorted, lambda a: a['athlete'])
    action_groups = [{'athlete': key, 'actions': list(group)} for key, group in actions_grouped]
    return action_groups

def safe_parse_int(text):
    if text.isdigit():
        return int(text)
    else:
        return 0

def parse_dropback(text):
    if 'SG' in text or 'UC' in text:
        return 1
    else:
        return 0


def compute_qb_stats(qb_action_group):
    actions = qb_action_group
    drop_back_count = len([1 for a in actions
                           if a['observations']['SG/UC'] in ['SG', 'UC']])

    attempts = sum([1 for a in actions
                       if a['observations']['Att'] == '1'])

    completions = completions = sum([1 for a in actions
                       if a['observations']['Comp'] == '1'])

    total_yards = sum(map(
        lambda a: safe_parse_int(a['observations']['Tyds']),
        actions
    ))

    air_yards = sum(map(
        lambda a: safe_parse_int(a['observations']['AirYds']),
        actions
    ))

    pressured_count = sum([1 for a in actions
                       if a['observations']['Press'] == '1'])

    touchdown_count = sum([1 for a in actions
                       if a['observations']['TD'] == '1'])

    interception_count = sum([1 for a in actions
                       if a['observations']['Int'] == '1'])

    throwaway_count = sum([1 for a in actions
                       if a['observations']['TA'] == '1'])

    sack_count = sum([1 for a in actions
                       if a['observations']['Sk'] == '1'])

    hit_count = sum([1 for a in actions
                       if a['observations']['Ht'] == '1'])

    hurried_count = sum([1 for a in actions
                       if a['observations']['Hur'] == '1'])

    drop_count = sum([1 for a in actions
                       if a['observations']['Drop'] == '1'])

    action_count = len(actions)

    completion_rate = (round(completions / attempts, 3) if attempts > 0 else 0 )

    air_yards_per_attempt = (round(air_yards / attempts, 3) if attempts > 0 else 0)





    return {
        'dropback_count': drop_back_count,
        'attempts': attempts,
        'completions': completions,
        'completion_rate': completion_rate,
        'total_yards': total_yards,
        'air_yards': air_yards,
        'air_yards_per_attempt': air_yards_per_attempt,
        'pressured_count': pressured_count,
        'touchdown_count': touchdown_count,
        'interception_count': interception_count,
        'throwaway_count': throwaway_count,
        'drop_count': drop_count,
        'sack_count': sack_count,
        'hit_count': hit_count,
        'hurried_count': hurried_count
    }


def preprocess(games):
    for game in games:
        for quarter in game['quarters']:
            for play in quarter['plays']:
                for action in play['actions']:
                    if 'athlete' in action:
                        action['athlete'] = action['athlete']['$oid']

                    if action['action_type'] == 'quarterback':
                        receiver_actions = [a for a in play['actions']
                                            if a['action_type'] == 'receiver']
                        if(len(receiver_actions) == 1):
                            action['observations']['Drop'] = receiver_actions[0]['observations']['Drop']
                        else:
                            action['observations']['Drop'] = 0




def get_actions(games, game_filter):
    action_type = game_filter['action_type']

    actions = []
    for game in games:
        for quarter in game['quarters']:
            for play in quarter['plays']:
                for action in play['actions']:
                    if 'athlete' in action:
                        if action['action_type'] == action_type:
                            actions.append(action)



    return actions
