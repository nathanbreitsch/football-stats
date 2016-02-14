import falcon
import json
from stats import compute_qb_stats, get_actions, group_by_athlete, preprocess

api = application = falcon.API()


with open('../data/games.json', 'r') as f:
    games = json.load(f)
    preprocess(games)

athlete_dict = {}
with open('../data/athletes.json', 'r') as f:
    athletes = json.load(f)
    for a in athletes:
        id = a['_id']['$oid']
        name = a['name']
        athlete_dict[id] = name

def add_headers(response):
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Content-type', 'application/json')

class AthleteResource(object):

    def on_get(self, req, res):
        res.body = json.dumps({'athletes': athletes})


class QuarterbackStatsResource(object):

    def get_qb_stats(self, filter_data):
        actions = get_actions(games, filter_data)
        action_groups = group_by_athlete(actions)
        qb_stats = [{
            'athlete': g['athlete'],
            'stats': compute_qb_stats(g['actions'])
        } for g in action_groups]

        for stat in qb_stats:
            stat['athlete'] = athlete_dict[stat['athlete']]
        return qb_stats


    def on_get(self, req, resp):
        data = req.params
        qb_stats = self.get_qb_stats(data)

        resp.body = json.dumps({'quarterbacks': qb_stats})
        add_headers(resp)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        """Handles POST requests"""
        data = req.params

        qb_stats = self.get_qb_stats(data)

        resp.body = json.dumps({'quarterbacks': qb_stats})
        add_headers(resp)
        resp.status = falcon.HTTP_200


quarterback_resource = QuarterbackStatsResource()
api.add_route('/quarterback/stats', quarterback_resource)
