import os
import urllib
import tempfile
import itertools

import requests

from datapackage_pipelines.generators import slugify
from datapackage_pipelines.wrapper import ingest, spew
from datapackage_pipelines.utilities.resources import PROP_STREAMING

from tableschema_spss import Storage
from tabulator.helpers import detect_scheme_and_format

import logging
log = logging.getLogger(__name__)

parameters, datapackage, res_iter = ingest()

source = parameters['source']
source_scheme, source_format = detect_scheme_and_format(source)
filename = slugify(urllib.parse.unquote(os.path.basename(source)))

# source_format must be 'sav' or 'zsav', right?
if source_format not in ['sav', 'zsav']:
    raise RuntimeError('Source format must be either .sav or .zsav.')

if source_scheme == 'file':
    path = source
elif source_scheme in ['http', 'https']:
    content = requests.get(source).content
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.write(content)
    path = tmp.name
else:
    raise RuntimeError('Source scheme must be either a file path or url.')

storage = Storage()
descriptor = storage.describe(path)

resource = {
    'name': filename.lower(),
    'path': 'data/{}.csv'.format(filename),
    PROP_STREAMING: True
}

resource['schema'] = descriptor

datapackage['resources'].append(resource)


def process_resource(path, descriptor):
    field_names = [f['name'] for f in descriptor['fields']]
    for r in storage.iter(path):
        yield dict(zip(field_names, r))


spew(datapackage, itertools.chain(res_iter, [process_resource(path,
                                                              descriptor)]))
