import itertools

from datapackage_pipelines.generators import slugify
from datapackage_pipelines.wrapper import ingest, spew

from tableschema_spss import Storage

import logging
log = logging.getLogger(__name__)

parameters, datapackage, res_iter = ingest()

path = parameters['path']

storage = Storage()

descriptor = storage.describe(path)
field_names = [f['name'] for f in descriptor['fields']]
resource_content = [dict(zip(field_names, r)) for r in storage.iter(path)]

resource = {
    'name': slugify(path).lower(),
    'path': 'data/{}.csv'.format(slugify(path))
}

resource['schema'] = descriptor

datapackage['resources'].append(resource)

spew(datapackage, itertools.chain(res_iter, [resource_content]))
