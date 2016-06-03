# This file is part of Indico.
# Copyright (C) 2002 - 2016 European Organization for Nuclear Research (CERN).
#
# Indico is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# Indico is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Indico; if not, see <http://www.gnu.org/licenses/>.

from operator import itemgetter

from ipaddress import ip_network

from indico.web.forms.fields import MultiStringField


class MultiIPNetworkField(MultiStringField):
    """A field to enter multiple IPv4 or IPv6 networks.

    The field data is a set of ``IPNetwork``s not bound to a DB session.
    The ``unique`` and ``sortable`` parameters of the parent class cannot be used with this class.
    """

    def __init__(self, *args, **kwargs):
        super(MultiIPNetworkField, self).__init__(*args, **kwargs)
        self._data_converted = False

    def _value(self):
        if self.data is None:
            return []
        elif self._data_converted:
            data = [{self.field_name: unicode(network)} for network in self.data or []]
            return sorted(data, key=itemgetter(self.field_name))
        else:
            return self.data

    def process_formdata(self, valuelist):
        super(MultiIPNetworkField, self).process_formdata(valuelist)
        self.data = {ip_network(entry[self.field_name]) for entry in self.data}
        self._data_converted = True

    def pre_validate(self, form):
        pass