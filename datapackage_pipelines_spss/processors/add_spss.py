import os
import urllib
import tempfile
import itertools

import requests

from datapackage_pipelines.generators import slugify
from datapackage_pipelines.wrapper import ingest, spew

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
field_names = [f['name'] for f in descriptor['fields']]
resource_content = [dict(zip(field_names, r)) for r in storage.iter(path)]

resource = {
    'name': filename.lower(),
    'path': 'data/{}.csv'.format(filename)
}

resource['schema'] = descriptor

datapackage['resources'].append(resource)

spew(datapackage, itertools.chain(res_iter, [resource_content]))
