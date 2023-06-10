"""
Copyright 2014 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json

from cafe.engine.models.base import AutoMarshallingModel


class CreateChassis(AutoMarshallingModel):

    def __init__(self, description=None, extra=None):
        super(CreateChassis, self).__init__()
        extra = extra or {}

        self.description = description
        self.extra = extra

    def _obj_to_json(self):
        create_request = {
            'description': self.description,
            'extra': self.extra
        }
        self._remove_empty_values(create_request)
        return json.dumps(create_request)
