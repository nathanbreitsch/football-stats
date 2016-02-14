import falcon
import json
from stats import compute_qb_stats, get_actions, group_by_athlete, preprocess

api = application = falcon.API()


with open('../data/games.json', 'r') as f:
    games = json.load(f)
    preprocess(games)



class QuarterbackStatsResource(object):

    def on_get(self, req, resp):
        actions = get_actions(games, {'action_type': 'quarterback'})
        action_groups = group_by_athlete(actions)
        qb_stats = [{
            'athlete': g['athlete'],
            'stats': compute_qb_stats(g['actions'])
        } for g in action_groups]

        resp.body = json.dumps({'quarterbacks': qb_stats})
        resp.status = falcon.HTTP_200


quarterback_resource = QuarterbackStatsResource()
api.add_route('/quarterback/stats', quarterback_resource)
