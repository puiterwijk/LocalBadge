#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2015  Patrick Uiterwijk <patrick@puiterwijk.org>
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions
# of the GNU General Public License v2, or (at your option) any later
# version.  This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.  You
# should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#


from setuptools import setup

setup(name='LocalBadgeIssuance',
      version='1.0',
      description='Issue badges at an event',
      author='Patrick Uiterwijk',
      author_email='patrick@puiterwijk.org/',
      url='https://github.com/puiterwijk/LocalBadge',
      license='GPLv2+',
      install_requires=['Flask',
                        'Flask-SQLAlchemy'],
     )
