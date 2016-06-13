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

from __future__ import unicode_literals

from sqlalchemy.orm import joinedload, undefer

from indico.modules.categories.controllers.base import RHManageCategoryBase
from indico.modules.categories.models.categories import Category
from indico.modules.categories.views import WPCategoryManagement


class RHManageCategoryContent(RHManageCategoryBase):
    @property
    def _category_query_options(self):
        children_strategy = joinedload('children')
        children_strategy.undefer('deep_children_count')
        children_strategy.undefer('deep_events_count')
        return children_strategy,

    def _process(self):
        return WPCategoryManagement.render_template('management/content.html', self.category, 'content',
                                                    categories=self.category.children)