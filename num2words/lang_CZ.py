# -*- coding: utf-8 -*-
# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA

from __future__ import unicode_literals

from .base import Num2Word_Base
from .utils import get_digits, splitbyx

ZERO = ('nula',)

ONES = {
    1: ('jedna',),
    2: ('dva',),
    3: ('tři',),
    4: ('čtyři',),
    5: ('pět',),
    6: ('šest',),
    7: ('sedm',),
    8: ('osm',),
    9: ('devět',),
}

TENS = {
    0: ('deset',),
    1: ('jedenáct',),
    2: ('dvanáct',),
    3: ('třináct',),
    4: ('čtrnáct',),
    5: ('patnáct',),
    6: ('šestnáct',),
    7: ('sedmnáct',),
    8: ('osmnáct',),
    9: ('devatenáct',),
}

TWENTIES = {
    2: ('dvacet',),
    3: ('třicet',),
    4: ('čtyřicet',),
    5: ('padesát',),
    6: ('šedesát',),
    7: ('sedmdesát',),
    8: ('osmdesát',),
    9: ('devadesát',),
}

HUNDREDS = {
    1: ('sto',),
    2: ('dvě stě',),
    3: ('tři sta',),
    4: ('čtyři sta',),
    5: ('pět set',),
    6: ('šest set',),
    7: ('sedm set',),
    8: ('osm set',),
    9: ('devět set',),
}

THOUSANDS = {
    1: ('tisíc', 'tisíce', 'tisíc'),  # 10^3
    2: ('milion', 'miliony', 'milionů'),  # 10^6
    3: ('miliarda', 'miliardy', 'miliard'),  # 10^9
    4: ('bilion', 'biliony', 'bilionů'),  # 10^12
    5: ('biliarda', 'biliardy', 'biliard'),  # 10^15
    6: ('trilion', 'triliony', 'trilionů'),  # 10^18
    7: ('triliarda', 'triliardy', 'triliard'),  # 10^21
    8: ('kvadrilion', 'kvadriliony', 'kvadrilionů'),  # 10^24
    9: ('kvadriliarda', 'kvadriliardy', 'kvadriliard'),  # 10^27
    10: ('quintillion', 'quintilliony', 'quintillionů'),  # 10^30
}

ZERO_ORD = ('nultý',)

ONES_ORD = {
    1: ('první',),
    2: ('druhý',),
    3: ('třetí',),
    4: ('čtvrtý',),
    5: ('pátý',),
    6: ('šestý',),
    7: ('sedmý',),
    8: ('osmý',),
    9: ('devátý',),
}

TENS_ORD = {
    0: ('desátý',),
    1: ('jedenáctý',),
    2: ('dvanáctý',),
    3: ('třináctý',),
    4: ('čtrnáctý',),
    5: ('patnáctý',),
    6: ('šestnáctý',),
    7: ('sedmnáctý',),
    8: ('osmnáctý',),
    9: ('devatenáctý',),
}

TWENTIES_ORD = {
    2: ('dvacátý',),
    3: ('třicátý',),
    4: ('čtyřicátý',),
    5: ('padesátý',),
    6: ('šedesátý',),
    7: ('sedmdesátý',),
    8: ('osmdesátý',),
    9: ('devadesátý',),
}

HUNDREDS_ORD = {
    1: ('stý',),
    2: ('dvou stý',),
    3: ('tří stý',),
    4: ('čtyř stý',),
    5: ('pěti stý',),
    6: ('šesti stý',),
    7: ('sedmi stý',),
    8: ('osmi stý',),
    9: ('devíti stý',),
}

THOUSANDS_ORD = {
    1: ('tisící'),  # 10^3
    2: ('miliontý'),  # 10^6
    3: ('miliardtý'),  # 10^9
    4: ('biliontý'),  # 10^12
    5: ('biliardý'),  # 10^15
    6: ('triliontý'),  # 10^18
    7: ('triliardtý'),  # 10^21
    8: ('kvadriliontý'),  # 10^24
    9: ('kvadriliardtý'),  # 10^27
    10: ('quintilliontý'),  # 10^30
}

class Num2Word_CZ(Num2Word_Base):
    CURRENCY_FORMS = {
        'CZK': (
            ('koruna', 'koruny', 'korun'), ('halíř', 'halíře', 'haléřů')
        ),
        'EUR': (
            ('euro', 'euro', 'euro'), ('cent', 'centy', 'centů')
        ),
    }

    def setup(self):
        self.negword = "mínus"
        self.pointword = "celá"

    def to_cardinal(self, number):
        n = str(number).replace(',', '.')
        if '.' in n:
            left, right = n.split('.')
            leading_zero_count = len(right) - len(right.lstrip('0'))
            decimal_part = ((ZERO[0] + ' ') * leading_zero_count +
                            self._int2word(int(right)))
            return u'%s %s %s' % (
                self._int2word(int(left)),
                self.pointword,
                decimal_part
            )
        else:
            return self._int2word(int(n))

    def pluralize(self, n, forms):
        if n == 1:
            form = 0
        elif 5 > n % 10 > 1 and (n % 100 < 10 or n % 100 > 20):
            form = 1
        else:
            form = 2
        return forms[form]

    def to_ordinal(self, number):
        if number == 0:
            return ZERO_ORD[0]
        words = []
        chunks = list(splitbyx(str(number), 3))
        i = len(chunks)
        for x in chunks:
            i -= 1

            if x == 0:
                continue

            n1, n2, n3 = get_digits(x)

            if n3 > 0:
                words.append(HUNDREDS_ORD[n3][0])

            if n2 > 1:
                words.append(TWENTIES_ORD[n2][0])

            if n2 == 1:
                words.append(TENS_ORD[n1][0])
            elif n1 > 0 and not (i > 0 and x == 1):
                words.append(ONES_ORD[n1][0])

            if i > 0:
                words.append(THOUSANDS_ORD[i])
        return ' '.join(words)

    def _int2word(self, n):
        if n == 0:
            return ZERO[0]

        words = []
        chunks = list(splitbyx(str(n), 3))
        i = len(chunks)
        for x in chunks:
            i -= 1

            if x == 0:
                continue

            n1, n2, n3 = get_digits(x)

            if n3 > 0:
                words.append(HUNDREDS[n3][0])

            if n2 > 1:
                words.append(TWENTIES[n2][0])

            if n2 == 1:
                words.append(TENS[n1][0])
            elif n1 > 0 and not (i > 0 and x == 1):
                words.append(ONES[n1][0])

            if i > 0:
                words.append(self.pluralize(x, THOUSANDS[i]))

        return ' '.join(words)
