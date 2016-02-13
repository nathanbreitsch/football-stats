import falcon
import json

api = application = falcon.API()

class DataContext():

    def __init__(self):
        with open('../data/games.json', 'r') as f:
            self.games = json.load(f)

    # some shit i copied and pasted off of s.o.
    # http://stackoverflow.com/questions/8477550/flattening-a-list-of-dicts-of-lists-of-dicts-etc-of-unknown-depth-in-python-n
    def flatten(self, structure, key="", path="", flattened=None):
        if flattened is None:
            flattened = {}
        if type(structure) not in(dict, list):
            flattened[((path + "_") if path else "") + key] = structure
        elif isinstance(structure, list):
            for i, item in enumerate(structure):
                flatten(item, "%d" % i, path + "_" + key, flattened)
        else:
            for new_key, value in structure.items():
                flatten(value, new_key, path + "_" + key, flattened)
        return flattened

dc = DataContext()

class GameResource(object):

    def on_get(self, req, resp):
        resp.body = json.dumps(dc.games)
        resp.status = falcon.HTTP_200

        json.loads


resource = GameResource()
api.add_route('/hello', resource)
