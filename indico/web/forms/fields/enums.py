# This file is part of Indico.
# Copyright (C) 2002 - 2017 European Organization for Nuclear Research (CERN).
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

from __future__ import absolute_import, unicode_literals

from operator import attrgetter

from wtforms import HiddenField, SelectFieldBase
from wtforms.widgets import RadioInput, Select

from indico.web.forms.widgets import JinjaWidget


class _EnumFieldMixin(object):
    def process_formdata(self, valuelist):
        if valuelist:
            if valuelist[0] in ('', '__None') and self.none is not None:
                self.data = None
            else:
                try:
                    self.data = self.enum[valuelist[0]]
                except KeyError:
                    raise ValueError(self.gettext('Not a valid choice'))


class IndicoEnumSelectField(_EnumFieldMixin, SelectFieldBase):
    """Select field backed by a :class:`RichEnum`"""

    widget = Select()

    def __init__(self, label=None, validators=None, enum=None, sorted=False, only=None, skip=None, none=None,
                 titles=None, **kwargs):
        super(IndicoEnumSelectField, self).__init__(label, validators, **kwargs)
        self.enum = enum
        self.sorted = sorted
        self.only = set(only) if only is not None else None
        self.skip = set(skip or set())
        self.none = none
        self.titles = titles

    def iter_choices(self):
        items = (x for x in self.enum if x not in self.skip and (self.only is None or x in self.only))
        if self.sorted:
            items = sorted(items, key=attrgetter('title'))
        if self.none is not None:
            yield ('__None', self.none, self.data is None)
        for item in items:
            title = item.title if self.titles is None else self.titles[item]
            yield (item.name, title, item == self.data)


class IndicoEnumRadioField(IndicoEnumSelectField):
    widget = JinjaWidget('forms/radio_buttons_widget.html', orientation='horizontal', single_kwargs=True)
    option_widget = RadioInput()


class HiddenEnumField(_EnumFieldMixin, HiddenField):
    """Hidden field that only accepts values from an Enum"""

    def __init__(self, label=None, validators=None, enum=None, only=None, skip=None, none=None, **kwargs):
        super(HiddenEnumField, self).__init__(label, validators, **kwargs)
        self.enum = enum
        self.only = only
        self.skip = skip or set()
        self.none = none

    def process_formdata(self, valuelist):
        old_data = self.data
        super(HiddenEnumField, self).process_formdata(valuelist)
        if self.data is not None and (self.data in self.skip or (self.only is not None and self.data not in self.only)):
            self.data = old_data
            raise ValueError(self.gettext('Not a valid choice'))
