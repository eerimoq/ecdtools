import re
import logging
from decimal import Decimal

import textparser
from textparser import Sequence
from textparser import choice
from textparser import ZeroOrMore
from textparser import OneOrMore
from textparser import Any
from textparser import Not
from textparser import Tag
from textparser import tokenize_init
from textparser import Token
from textparser import TokenizeError
from textparser import Optional


__version__ = '0.1.0'

LOGGER = logging.getLogger(__name__)


class Error(Exception):
    pass


class InternalError(Exception):
    pass


class TypMinMax(object):

    def __init__(self):
        self.typical = None
        self.minimum = None
        self.maximum = None


class Package(object):

    def __init__(self):
        self.r_pkg = TypMinMax()
        self.l_pkg = TypMinMax()
        self.c_pkg = TypMinMax()


class Pin(object):

    def __init__(self):
        self.name = None
        self.signal_name = None
        self.model_name = None
        self.r_pin = None
        self.l_pin = None
        self.c_pin = None


class Component(object):

    def __init__(self):
        self.name = None
        self.si_location = None
        self.timing_location = None
        self.manufacturer = None
        self.package = Package()
        self.pins = []


class Ramp(object):

    def __init__(self):
        self.dv_dt_r = None
        self.dv_dt_f = None
        self.r_load = None


class WaveformTable(object):

    def __init__(self):
        self.samples = []


class Waveform(object):

    def __init__(self):
        self.r_fixture = None
        self.v_fixture = TypMinMax()
        self.table = WaveformTable()


class Model(object):

    def __init__(self):
        self.name = None
        self.model_type = None
        self.polarity = None
        self.enable = None
        self.vinl = None
        self.vinh = None
        self.c_comp = TypMinMax()
        self.vmeas = None
        self.cref = None
        self.vref = None
        self.rref = None
        self.temperature_range = TypMinMax()
        self.voltage_range = TypMinMax()
        self.gnd_clamp = None
        self.power_clamp = None
        self.pullup = None
        self.pulldown = None
        self.ramp = None
        self.falling_waveforms = []
        self.rising_waveforms = []


KEYWORDS = set([
    '[ibis ver]',
    '[comment char]',
    '[file name]',
    '[file rev]',
    '[date]',
    '[source]',
    '[notes]',
    '[disclaimer]',
    '[copyright]',
    '[component]',
    '[manufacturer]',
    '[package]',
    '[pin]',
    '[diff pin]',
    '[series switch groups]',
    '[model selector]',
    '[model]',
    '[add submodel]',
    '[temperature range]',
    '[voltage range]',
    '[pullup reference]',
    '[pulldown reference]',
    '[gnd clamp]',
    '[power clamp]',
    '[pullup]',
    '[pulldown]',
    '[ramp]',
    '[falling waveform]',
    '[rising waveform]',
    '[submodel]',
    '[end]'
])


class Parser(textparser.Parser):

    def tokenize(self, string):
        token_specs = [
            ('SKIP',     r'\r+|\s*\|[^\n]*'),
            ('NL',       r'\n'),
            ('KEYWORD',  r'\[.+?\]'),
            ('WORD',     r'[^ \n\t\r\f\v=]+'),
            ('WS',       r'[ \t\r\f\v]+'),
            ('EQ',       r'='),
            ('MISMATCH', r'.')
        ]

        tokens, token_regex = tokenize_init(token_specs)

        for mo in re.finditer(token_regex, string, re.DOTALL):
            kind = mo.lastgroup

            if kind == 'SKIP':
                pass
            elif kind != 'MISMATCH':
                value = mo.group(kind)

                if kind == 'KEYWORD':
                    keyword = value.lower().replace('_', ' ')

                    if keyword in KEYWORDS:
                        kind = keyword

                tokens.append(Token(kind, value, mo.start()))
            else:
                raise TokenizeError(string, mo.start())

        return tokens

    def grammar(self):
        nls = OneOrMore('NL')

        any_until_keyword = ZeroOrMore(
            Sequence(Not(Sequence('NL', choice(*KEYWORDS))), Any()))

        any_until_nl = ZeroOrMore(Sequence(Not(choice('NL', '__EOF__')), Any()))

        sub_parameter = Tag('SubParameter',
                            Sequence(nls, 'WORD', 'WS', 'WORD'))

        sub_parameter_typ_min_max = Tag('SubParameterTypMinMax',
                                        Sequence(nls, 'WORD',
                                                 'WS', 'WORD',
                                                 'WS', 'WORD',
                                                 'WS', 'WORD'))

        numerical_sub_parameter = Tag('NumericalSubParameter',
                                      Sequence(nls,
                                               'WORD',
                                               Optional('WS'),
                                               'EQ',
                                               Optional('WS'),
                                               'WORD'))

        ibis_ver = Sequence(Optional(nls),
                            '__SOF__',
                            Optional(nls),
                            '[ibis ver]', 'WS', 'WORD')

        comment_char = Sequence(nls, '[comment char]')

        file_name = Sequence(nls, '[file name]', 'WS', 'WORD')

        file_rev = Sequence(nls, '[file rev]', 'WS', 'WORD')

        date = Sequence(nls, '[date]', any_until_nl)

        source = Sequence(nls, '[source]', any_until_keyword)

        notes = Sequence(nls, '[notes]', any_until_keyword)

        disclaimer = Sequence(nls, '[disclaimer]', any_until_keyword)

        copyright_ = Sequence(nls, '[copyright]', any_until_keyword)

        component = Sequence(nls, '[component]', any_until_nl,
                             ZeroOrMore(Sequence(nls, 'WORD', 'WS', 'WORD')))

        manufacturer = Sequence(nls, '[manufacturer]', any_until_nl)

        package = Sequence(nls, '[package]',
                           ZeroOrMore(Sequence(nls, 'WORD',
                                               'WS', 'WORD',
                                               'WS', 'WORD',
                                               'WS', 'WORD')))

        pin = Sequence(nls, '[pin]',
                       'WS', 'WORD',
                       'WS', 'WORD',
                       'WS', 'WORD',
                       'WS', 'WORD',
                       'WS', 'WORD',
                       ZeroOrMore(choice(Tag('All',
                                             Sequence(nls,
                                                      Optional('WS'), 'WORD',
                                                      'WS', 'WORD',
                                                      'WS', 'WORD',
                                                      'WS', 'WORD',
                                                      'WS', 'WORD',
                                                      'WS', 'WORD')),
                                         Tag('Triple',
                                             Sequence(nls,
                                                      Optional('WS'), 'WORD',
                                                      'WS', 'WORD',
                                                      'WS', 'WORD')))))

        diff_pin = Sequence(nls, '[diff pin]',
                            'WS', 'WORD',
                            'WS', 'WORD',
                            'WS', 'WORD',
                            'WS', 'WORD',
                            'WS', 'WORD',
                            ZeroOrMore(Sequence(nls, 'WORD',
                                                'WS', 'WORD',
                                                'WS', 'WORD',
                                                'WS', 'WORD',
                                                'WS', 'WORD',
                                                'WS', 'WORD')))

        series_switch_groups = Sequence(nls, '[series switch groups]',
                                        ZeroOrMore(Sequence(nls, any_until_nl)))

        model_selector = Sequence(nls, '[model selector]', 'WS', 'WORD',
                                  ZeroOrMore(Sequence(nls, 'WORD', any_until_nl)))

        model = Sequence(nls, '[model]', 'WS', 'WORD',
                         ZeroOrMore(choice(Tag('Quad',
                                               Sequence(nls, 'WORD',
                                                        'WS', 'WORD',
                                                        'WS', 'WORD',
                                                        'WS', 'WORD')),
                                           sub_parameter,
                                           numerical_sub_parameter)))

        add_submodel = Sequence(nls, '[add submodel]',
                                ZeroOrMore(Sequence(nls, 'WORD', 'WS', 'WORD')))

        temperature_range = Sequence(nls, '[temperature range]',
                                     'WS', 'WORD',
                                     'WS', 'WORD',
                                     'WS', 'WORD')

        voltage_range = Sequence(nls, '[voltage range]',
                                 'WS', 'WORD',
                                 'WS', 'WORD',
                                 'WS', 'WORD')

        pullup_reference = Sequence(nls, '[pullup reference]',
                                    'WS', 'WORD',
                                    'WS', 'WORD',
                                    'WS', 'WORD')

        pulldown_reference = Sequence(nls, '[pulldown reference]',
                                      'WS', 'WORD',
                                      'WS', 'WORD',
                                      'WS', 'WORD')

        quad_table = ZeroOrMore(Sequence(nls,
                                         Optional('WS'), 'WORD',
                                         'WS', 'WORD',
                                         'WS', 'WORD',
                                         'WS', 'WORD'))

        gnd_clamp = Sequence(nls, '[gnd clamp]', quad_table)

        power_clamp = Sequence(nls, '[power clamp]', quad_table)

        pullup = Sequence(nls, '[pullup]', quad_table)

        pulldown = Sequence(nls, '[pulldown]', quad_table)

        ramp = Sequence(nls, '[ramp]',
                        ZeroOrMore(choice(numerical_sub_parameter,
                                          sub_parameter_typ_min_max)))

        waveform = ZeroOrMore(choice(Tag('TableEntry',
                                         Sequence(nls,
                                                  Optional('WS'), 'WORD',
                                                  'WS', 'WORD',
                                                  'WS', 'WORD',
                                                  'WS', 'WORD')),
                                     numerical_sub_parameter))

        falling_waveform = Sequence(nls, '[falling waveform]', waveform)

        rising_waveform = Sequence(nls, '[rising waveform]', waveform)

        submodel = Sequence(nls, '[submodel]', 'WS', 'WORD',
                            OneOrMore(sub_parameter))

        unknown_keyword = Sequence(nls, 'KEYWORD', any_until_keyword)

        end = Sequence(nls, '[end]')

        ibis_file = Sequence(ibis_ver,
                             ZeroOrMore(choice(comment_char,
                                               file_name,
                                               file_rev,
                                               date,
                                               source,
                                               notes,
                                               disclaimer,
                                               copyright_,
                                               component,
                                               manufacturer,
                                               package,
                                               pin,
                                               diff_pin,
                                               series_switch_groups,
                                               model_selector,
                                               model,
                                               add_submodel,
                                               temperature_range,
                                               voltage_range,
                                               pullup_reference,
                                               pulldown_reference,
                                               gnd_clamp,
                                               power_clamp,
                                               pullup,
                                               pulldown,
                                               ramp,
                                               falling_waveform,
                                               rising_waveform,
                                               submodel,
                                               unknown_keyword,
                                               end)))

        return ibis_file


class IbsFile(object):

    def __init__(self, string):
        self._version = None
        self._file_name = None
        self._file_rev = None
        self._date = None
        self._source = None
        self._notes = None
        self._disclaimer = None
        self._copyright = None
        self._components = []
        self._models = []

        string = string.replace('\r', '')
        string = re.sub(r'[ \t]+\n', '\n', string)
        tokens = Parser().parse(string, token_tree=True, match_sof=True)

        self._version = tokens[0][5].value

        for item in tokens[1]:
            keyword = item[1].kind
            data = item[2:]

            if keyword == '[file name]':
                self._file_name = data[1].value
            elif keyword == '[file rev]':
                self._file_rev = data[1].value
            elif keyword == '[date]':
                self._date = _load_string(data)
            elif keyword == '[source]':
                self._source = _load_string(data)
            elif keyword == '[notes]':
                self._notes = _load_string(data)
            elif keyword == '[disclaimer]':
                self._disclaimer = _load_string(data)
            elif keyword == '[copyright]':
                self._copyright = _load_string(data)
            elif keyword == '[component]':
                self._load_component(data)
            elif keyword == '[manufacturer]':
                self._components[-1].manufacturer = _load_string(data)
            elif keyword == '[package]':
                self._load_package(data)
            elif keyword == '[pin]':
                self._load_pin(data)
            elif keyword == '[model]':
                self._load_model(data)
            elif keyword == '[temperature range]':
                self._load_temperature_range(data)
            elif keyword == '[voltage range]':
                self._load_voltage_range(data)
            elif keyword == '[gnd clamp]':
                self._models[-1].gnd_clamp = _load_4_columns(data)
            elif keyword == '[power clamp]':
                self._models[-1].power_clamp = _load_4_columns(data)
            elif keyword == '[pullup]':
                self._models[-1].pullup = _load_4_columns(data)
            elif keyword == '[pulldown]':
                self._models[-1].pulldown = _load_4_columns(data)
            elif keyword == '[ramp]':
                self._load_ramp(data)
            elif keyword == '[falling waveform]':
                waveform = self._load_waveform(data)
                self._models[-1].falling_waveforms.append(waveform)
            elif keyword == '[rising waveform]':
                waveform = self._load_waveform(data)
                self._models[-1].rising_waveforms.append(waveform)
            elif keyword == '[end]':
                pass
            else:
                LOGGER.debug('Unsupported keyword %s.', item[1].value)

    def _load_component(self, tokens):
        component = Component()
        component.name = tokens[0][1][1].value

        for sub_param in tokens[1]:
            if sub_param[1].value == 'Si_location':
                component.si_location = sub_param[3].value
            elif sub_param[1].value == 'Timing_location':
                component.timing_location = sub_param[3].value
            else:
                LOGGER.debug('Unsupported [Component] sub-parameter %s.',
                             sub_param[1].value)

        self._components.append(component)

    def _load_package(self, tokens):
        package = self._components[-1].package

        for _, sub_param, _, typical, _, minimum, _, maximum in tokens[0]:
            if sub_param.value == 'R_pkg':
                package.r_pkg.typical = typical.value
                package.r_pkg.minimum = minimum.value
                package.r_pkg.maximum = maximum.value
            elif sub_param.value == 'L_pkg':
                package.l_pkg.typical = typical.value
                package.l_pkg.minimum = minimum.value
                package.l_pkg.maximum = maximum.value
            elif sub_param.value == 'C_pkg':
                package.c_pkg.typical = typical.value
                package.c_pkg.minimum = minimum.value
                package.c_pkg.maximum = maximum.value
            else:
                raise Error('Invalid [Package] sub-parameter %s.',
                            sub_param.value)

    def _load_pin(self, tokens):
        pins = self._components[-1].pins

        for tag, data in tokens[10]:
            pin = Pin()

            if tag == 'All':
                pin.name = data[2].value
                pin.signal_name = data[4].value
                pin.model_name = data[6].value
                pin.r_pin = data[8].value
                pin.l_pin = data[10].value
                pin.c_pin = data[12].value
            elif tag == 'Triple':
                pin.name = data[2].value
                pin.signal_name = data[4].value
                pin.model_name = data[6].value
            else:
                raise InternalError('Bad tag {}.'.format(tag))

            pins.append(pin)

    def _load_model(self, tokens):
        model = Model()
        model.name = tokens[1].value

        for tag, data in tokens[2]:
            if tag == 'SubParameter':
                name, value = _load_sub_parameter(data)

                if name == 'Model_type':
                    model.model_type = value
                elif name == 'Polarity':
                    model.polarity = value
                elif name == 'Enable':
                    model.enable = value
                else:
                    LOGGER.debug('Unsupported [Model] sub-parameter %s.', name)
            elif tag == 'NumericalSubParameter':
                name, value = _load_numerical_sub_parameter(data)

                if name == 'Vinl':
                    model.vinl = value
                elif name == 'Vinh':
                    model.vinh = value
                elif name == 'Vmeas':
                    model.vmeas = value
                elif name == 'Cref':
                    model.cref = value
                elif name == 'Vref':
                    model.vref = value
                elif name == 'Rref':
                    model.rref = value
                else:
                    LOGGER.debug('Unsupported [Model] numerical sub-parameter %s.',
                                 name)
            elif tag == 'Quad':
                if data[1].value =='C_comp':
                    model.c_comp.typical = data[3].value
                    model.c_comp.minimum = data[5].value
                    model.c_comp.maximum = data[7].value
                else:
                    LOGGER.debug('Unsupported [Model] data %s.', data[1].value)
            else:
                raise InternalError('Bad tag {}.'.format(tag))

        self._models.append(model)

    def _load_temperature_range(self, tokens):
        self._models[-1].temperature_range.typical = tokens[1].value
        self._models[-1].temperature_range.minimum = tokens[5].value
        self._models[-1].temperature_range.maximum = tokens[3].value

    def _load_voltage_range(self, tokens):
        self._models[-1].voltage_range.typical = tokens[1].value
        self._models[-1].voltage_range.minimum = tokens[3].value
        self._models[-1].voltage_range.maximum = tokens[5].value

    def _load_ramp(self, tokens):
        ramp = Ramp()

        for tag, data in tokens[0]:
            if tag == 'SubParameterTypMinMax':
                name, typical, minimum, maximum = _load_sub_parameter_typ_min_max(
                    data)

                if name == 'dV/dt_r':
                    ramp.dv_dt_r = (typical, minimum, maximum)
                elif name == 'dV/dt_f':
                    ramp.dv_dt_f = (typical, minimum, maximum)
                else:
                    LOGGER.debug('Unsupported [Ramp] sub-parameter %s.', name)
            elif tag == 'NumericalSubParameter':
                name, value = _load_numerical_sub_parameter(data)

                if name == 'R_load':
                    ramp.r_load = value
                else:
                    LOGGER.debug('Unsupported [Ramp] numerical sub-parameter %s.',
                                 name)
            else:
                raise InternalError('Bad tag {}.'.format(tag))

        self._models[-1].ramp = ramp

    def _load_waveform(self, tokens):
        waveform = Waveform()

        for tag, data in tokens[0]:
            if tag == 'NumericalSubParameter':
                name, value = _load_numerical_sub_parameter(data)

                if name == 'R_fixture':
                    waveform.r_fixture = value
                elif name == 'V_fixture_min':
                    waveform.v_fixture.minimum = value
                elif name == 'V_fixture_max':
                    waveform.v_fixture.maximum = value
                elif name == 'V_fixture':
                    waveform.v_fixture.typical = value
                else:
                    LOGGER.debug(
                        'Unsupported [Rising/Falling Waveform] numerical '
                        'sub-parameter %s.',
                        name)
            elif tag == 'TableEntry':
                waveform.table.samples.append((data[2].value,
                                               data[4].value,
                                               data[6].value,
                                               data[8].value))
            else:
                raise InternalError('Bad tag {}.'.format(tag))

        return waveform

    @property
    def version(self):
        """The IBIS version.

        """

        return self._version

    @property
    def file_name(self):
        """The .ibs file name.

        """

        return self._file_name

    @property
    def file_rev(self):
        """The .ibs file revision.

        """

        return self._file_rev

    @property
    def date(self):
        """The .ibs date.

        """

        return self._date

    @property
    def source(self):
        """The .ibs file source.

        """

        return self._source

    @property
    def notes(self):
        """The .ibs file notes.

        """

        return self._notes

    @property
    def disclaimer(self):
        """The disclaimer string.

        """

        return self._disclaimer

    @property
    def copyright(self):
        """The Copyright string.

        """

        return self._copyright

    @property
    def components(self):
        """A list of all components.

        """

        return self._components

    @property
    def models(self):
        """A list of all models.

        """

        return self._models


def _load_sub_parameter(data):
    return data[1].value, data[3].value


def _load_numerical_sub_parameter(data):
    return data[1].value, data[5].value


def _load_sub_parameter_typ_min_max(data):
    return data[1].value, data[3].value, data[5].value, data[7].value


def _load_string(data):
    return ''.join([
        text.value for _, text in data[0][1:]
    ])


def _load_4_columns(data):
    return [
        (v1.value, v2.value, v3.value, v4.value)
        for _, _, v1, _, v2, _, v3, _, v4 in data[0]
    ]


def split_numerical(string):
    """Split given string into a number, suffix and unit tuple.

    """

    mo = re.match(r'(-?\d+\.?\d*([eE][+-]?\d+)?)(\w?)(\w*)', string)

    if not mo:
        raise Error('Expected a numerical string, but got {}.'.format(string))

    number, _, suffix, unit = mo.groups()

    if suffix not in ['T', 'G', 'M', 'k', 'm', 'u', 'n', 'p', 'f']:
        unit = suffix + unit
        suffix = ''

    return number, suffix, unit


def load_numerical(string):
    """Convert given string to a Decimal value.

    """

    number, suffix, _ = split_numerical(string)

    value = Decimal(number)

    if suffix:
        value *= {
            'T': Decimal('1e12'),
            'G': Decimal('1e9'),
            'M': Decimal('1e6'),
            'k': Decimal('1e3'),
            'm': Decimal('1e-3'),
            'u': Decimal('1e-6'),
            'n': Decimal('1e-9'),
            'p': Decimal('1e-12'),
            'f': Decimal('1e-15')
        }[suffix]

    return value


def load_file(filename):
    with open(filename, 'r') as fin:
        string = fin.read()

    return IbsFile(string)
