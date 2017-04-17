# Copyright (c) 2017 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import sys

import jsonschema

_return = 0


def validate_release(release, validator):
    global _return
    data = json.load(open(release, 'r'))
    for error in validator.iter_errors(data):
        print("{filename}: {message}".format(
            filename=release, message=error.message))
        _return = 1


def walk_releases(arg, dirname, fnames):
    for fname in fnames:
        validate_release(os.path.join(dirname, fname), arg)


def main():
    global _return
    schema = json.load(open('schema.json', 'r'))
    validator = jsonschema.Draft4Validator(schema)
    for (dirpath, dirnames, filenames) in os.walk('releases'):
        for fname in filenames:
            validate_release(os.path.join(dirpath, fname), validator)
    return _return


if __name__ == '__main__':
    sys.exit(main())
