# SPSS Plugin for datapackage-pipelines

[![Travis](https://img.shields.io/travis/frictionlessdata/datapackage-pipelines-spss/master.svg)](https://travis-ci.org/frictionlessdata/datapackage-pipelines-spss)
[![Coveralls](http://img.shields.io/coveralls/frictionlessdata/datapackage-pipelines-spss/master.svg)](https://coveralls.io/r/frictionlessdata/datapackage-pipelines-spss?branch=master)
[![PyPi](https://img.shields.io/pypi/v/datapackage-pipelines-spss.svg)](https://pypi.python.org/pypi/datapackage-pipelines-spss)
[![SemVer](https://img.shields.io/badge/versions-SemVer-brightgreen.svg)](http://semver.org/)
[![Gitter](https://img.shields.io/gitter/room/frictionlessdata/chat.svg)](https://gitter.im/frictionlessdata/chat)

## Install

```
# clone the repo and install it with pip

git clone https://github.com/frictionlessdata/datapackage-pipelines-spss.git
pip install -e .
```

## Usage

You can use datapackage-pipelines-spss as a plugin for [dpp](https://github.com/frictionlessdata/datapackage-pipelines#datapackage-pipelines). In the pipeline-spec.yaml it will look like this:

```yaml
  ...
  - run: spss.add_spss
    parameters:
      path: data/my-file.sav
```

This will add the file defined at `path` as a tabular resource to the pipeline.

