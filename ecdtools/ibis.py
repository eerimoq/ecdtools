import re
import logging
from decimal import Decimal

import textparser
from textparser import Sequence
from textparser import choice
from textparser import ZeroOrMore
from textparser import OneOrMore
from textparser import AnyUntil
from textparser import Not
from textparser import Tag
from textparser import tokenize_init
from textparser import Token
from textparser import TokenizeError
from textparser import Optional


__version__ = '0.1.0'

LOGGER = logging.getLogger(__name__)

RE_NUMERICAL = re.compile(r'(-?\d+\.?\d*([eE][+-]?\d+)?)(\w?)(\w*)')

SUFFIX_TO_VALUE = {
    'T': Decimal('1e12'),
    'G': Decimal('1e9'),
    'M': Decimal('1e6'),
    'k': Decimal('1e3'),
    'm': Decimal('1e-3'),
    'u': Decimal('1e-6'),
    'n': Decimal('1e-9'),
    'p': Decimal('1e-12'),
    'f': Decimal('1e-15')
}


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


class DiffPin(object):

    def __init__(self):
        self.name = None
        self.inv_pin = None
        self.vdiff = None
        self.tdelay_typ = None
        self.tdelay_min = None
        self.tdelay_max = None


class Component(object):

    def __init__(self):
        self.name = None
        self.si_location = None
        self.timing_location = None
        self.manufacturer = None
        self.package = Package()
        self.pins = []
        self.diff_pins = []


class AddSubmodel(object):

    def __init__(self):
        self.submodel = None
        self.submodel_mode = None


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


class ModelSelectorModel(object):

    def __init__(self, name, description):
        self.name = name
        self.description = description


class ModelSelector(object):

    def __init__(self):
        self.name = None
        self.models = []


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
        self.add_submodel = []


class SubmodelSpec(object):

    def __init__(self):
        self.v_trigger_r = TypMinMax()
        self.v_trigger_f = TypMinMax()
        self.off_delay = TypMinMax()


class Submodel(object):

    def __init__(self):
        self.name = None
        self.submodel_type = None
        self.submodel_spec = None


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
    '[submodel spec]',
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

        any_until_keyword = AnyUntil(Sequence('NL', choice(*KEYWORDS)))

        any_until_nl = AnyUntil(choice('NL', '__EOF__'))

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
                            '[ibis ver]', any_until_nl)

        comment_char = Sequence('[comment char]')

        file_name = Sequence('[file name]', any_until_nl)

        file_rev = Sequence('[file rev]', any_until_nl)

        date = Sequence('[date]', any_until_nl)

        source = Sequence('[source]', any_until_keyword)

        notes = Sequence('[notes]', any_until_keyword)

        disclaimer = Sequence('[disclaimer]', any_until_keyword)

        copyright_ = Sequence('[copyright]', any_until_keyword)

        component = Sequence('[component]', any_until_nl,
                             ZeroOrMore(Sequence(nls, 'WORD', 'WS', 'WORD')))

        manufacturer = Sequence('[manufacturer]', any_until_nl)

        package = Sequence('[package]',
                           ZeroOrMore(Sequence(nls, 'WORD',
                                               'WS', 'WORD',
                                               'WS', 'WORD',
                                               'WS', 'WORD')))

        pin = Sequence('[pin]',
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

        diff_pin = Sequence('[diff pin]',
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

        series_switch_groups = Sequence('[series switch groups]',
                                        ZeroOrMore(Sequence(nls, any_until_nl)))

        model_selector = Sequence('[model selector]', 'WS', 'WORD',
                                  ZeroOrMore(Sequence(nls,
                                                      'WORD',
                                                      'WS',
                                                      any_until_nl)))

        model = Sequence('[model]', 'WS', 'WORD',
                         ZeroOrMore(choice(Tag('Quad',
                                               Sequence(nls, 'WORD',
                                                        'WS', 'WORD',
                                                        'WS', 'WORD',
                                                        'WS', 'WORD')),
                                           sub_parameter,
                                           numerical_sub_parameter)))

        add_submodel = Sequence('[add submodel]',
                                ZeroOrMore(Sequence(nls, 'WORD', 'WS', 'WORD')))

        temperature_range = Sequence('[temperature range]',
                                     'WS', 'WORD',
                                     'WS', 'WORD',
                                     'WS', 'WORD')

        voltage_range = Sequence('[voltage range]',
                                 'WS', 'WORD',
                                 'WS', 'WORD',
                                 'WS', 'WORD')

        pullup_reference = Sequence('[pullup reference]',
                                    'WS', 'WORD',
                                    'WS', 'WORD',
                                    'WS', 'WORD')

        pulldown_reference = Sequence('[pulldown reference]',
                                      'WS', 'WORD',
                                      'WS', 'WORD',
                                      'WS', 'WORD')

        quad_table = ZeroOrMore(Sequence(nls,
                                         Optional('WS'), 'WORD',
                                         'WS', 'WORD',
                                         'WS', 'WORD',
                                         'WS', 'WORD'))

        gnd_clamp = Sequence('[gnd clamp]', quad_table)

        power_clamp = Sequence('[power clamp]', quad_table)

        pullup = Sequence('[pullup]', quad_table)

        pulldown = Sequence('[pulldown]', quad_table)

        ramp = Sequence('[ramp]',
                        ZeroOrMore(choice(numerical_sub_parameter,
                                          sub_parameter_typ_min_max)))

        waveform = ZeroOrMore(choice(Tag('TableEntry',
                                         Sequence(nls,
                                                  Optional('WS'), 'WORD',
                                                  'WS', 'WORD',
                                                  'WS', 'WORD',
                                                  'WS', 'WORD')),
                                     numerical_sub_parameter))

        falling_waveform = Sequence('[falling waveform]', waveform)

        rising_waveform = Sequence('[rising waveform]', waveform)

        submodel = Sequence('[submodel]', 'WS', 'WORD',
                            OneOrMore(sub_parameter))

        submodel_spec = Sequence('[submodel spec]',
                                 OneOrMore(sub_parameter_typ_min_max))

        unknown_keyword = Sequence('KEYWORD', any_until_keyword)

        end = Sequence('[end]')

        ibis_file = Sequence(
            ibis_ver,
            ZeroOrMore(Sequence(nls,
                                choice(comment_char,
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
                                       submodel_spec,
                                       unknown_keyword,
                                       end))))

        return ibis_file


class IbsFile(object):
    """An .ibs file.

    """

    def __init__(self, string, transform):
        self._ibis_version = None
        self._file_name = None
        self._file_revision = None
        self._date = None
        self._source = None
        self._notes = None
        self._disclaimer = None
        self._copyright = None
        self._components = []
        self._model_selectors = []
        self._models = []
        self._submodels = []
        self._transform = transform

        string = string.replace('\r', '')
        string = re.sub(r'[ \t]+\n', '\n', string)
        tokens = Parser().parse(string, token_tree=True, match_sof=True)

        self._ibis_version = self._load_string([tokens[0][4]])

        for item in tokens[1]:
            keyword = item[1][0].kind
            data = item[1][1:]

            if keyword == '[file name]':
                self._file_name = self._load_string(data)
            elif keyword == '[file rev]':
                self._file_revision = self._load_string(data)
            elif keyword == '[date]':
                self._date = self._load_string(data)
            elif keyword == '[source]':
                self._source = self._load_string(data)
            elif keyword == '[notes]':
                self._notes = self._load_string(data)
            elif keyword == '[disclaimer]':
                self._disclaimer = self._load_string(data)
            elif keyword == '[copyright]':
                self._copyright = self._load_string(data)
            elif keyword == '[component]':
                self._load_component(data)
            elif keyword == '[manufacturer]':
                self._components[-1].manufacturer = self._load_string(data)
            elif keyword == '[package]':
                self._load_package(data)
            elif keyword == '[pin]':
                self._load_pin(data)
            elif keyword == '[diff pin]':
                self._load_diff_pin(data)
            elif keyword == '[model selector]':
                self._load_model_selector(data)
            elif keyword == '[model]':
                self._load_model(data)
            elif keyword == '[add submodel]':
                self._load_add_submodel(data)
            elif keyword == '[temperature range]':
                self._load_temperature_range(data)
            elif keyword == '[voltage range]':
                self._load_voltage_range(data)
            elif keyword == '[gnd clamp]':
                self._models[-1].gnd_clamp = self._load_4_columns(data)
            elif keyword == '[power clamp]':
                self._models[-1].power_clamp = self._load_4_columns(data)
            elif keyword == '[pullup]':
                self._models[-1].pullup = self._load_4_columns(data)
            elif keyword == '[pulldown]':
                self._models[-1].pulldown = self._load_4_columns(data)
            elif keyword == '[ramp]':
                self._load_ramp(data)
            elif keyword == '[falling waveform]':
                waveform = self._load_waveform(data)
                self._models[-1].falling_waveforms.append(waveform)
            elif keyword == '[rising waveform]':
                waveform = self._load_waveform(data)
                self._models[-1].rising_waveforms.append(waveform)
            elif keyword == '[submodel]':
                self._load_submodel(data)
            elif keyword == '[submodel spec]':
                self._load_submodel_spec(data)
            elif keyword == '[end]':
                pass
            else:
                LOGGER.debug('Unsupported keyword %s.', item[1][0].value)

    @property
    def component_names(self):
        """A list of all component names.

        """

        return sorted([component.name for component in self._components])

    @property
    def model_selector_names(self):
        """A list of all model selector names.

        """

        return sorted([model_selector.name for model_selector in self._model_selectors])

    @property
    def model_names(self):
        """A list of all model names.

        """

        return sorted([model.name for model in self._models])

    def get_component_by_name(self, name):
        """Get the component named `name`.

        """

        for component in self._components:
            if component.name == name:
                return component

        raise Error('Expected component name {}, but got {}.'.format(
            format_or(self.component_names),
            name))

    def get_model_selector_by_name(self, name):
        """Get the model selector named `name`.

        """

        for model_selector in self._model_selectors:
            if model_selector.name == name:
                return model_selector

        raise Error('Expected model selector name {}, but got {}.'.format(
            format_or(self.model_selector_names),
            name))

    def get_model_by_name(self, name):
        """Get the model named `name`.

        """

        for model in self._models:
            if model.name == name:
                return model

        raise Error('Expected model name {}, but got {}.'.format(
            format_or(self.model_names),
            name))

    def _load_component(self, tokens):
        component = Component()
        component.name = tokens[0][1].value

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
                package.r_pkg.typical = self._load_numerical(typical)
                package.r_pkg.minimum = self._load_numerical(minimum)
                package.r_pkg.maximum = self._load_numerical(maximum)
            elif sub_param.value == 'L_pkg':
                package.l_pkg.typical = self._load_numerical(typical)
                package.l_pkg.minimum = self._load_numerical(minimum)
                package.l_pkg.maximum = self._load_numerical(maximum)
            elif sub_param.value == 'C_pkg':
                package.c_pkg.typical = self._load_numerical(typical)
                package.c_pkg.minimum = self._load_numerical(minimum)
                package.c_pkg.maximum = self._load_numerical(maximum)
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
                pin.r_pin = self._load_numerical(data[8])
                pin.l_pin = self._load_numerical(data[10])
                pin.c_pin = self._load_numerical(data[12])
            elif tag == 'Triple':
                pin.name = data[2].value
                pin.signal_name = data[4].value
                pin.model_name = data[6].value
            else:
                raise InternalError('Bad tag {}.'.format(tag))

            pins.append(pin)

    def _load_diff_pin(self, tokens):
        diff_pins = self._components[-1].diff_pins

        for line in tokens[10]:
            diff_pin = DiffPin()
            diff_pin.name = line[1].value
            diff_pin.inv_pin = line[3].value
            diff_pin.vdiff = line[5].value
            diff_pin.tdelay_typ = line[7].value
            diff_pin.tdelay_min = line[9].value
            diff_pin.tdelay_max = line[11].value
            diff_pins.append(diff_pin)

    def _load_model_selector(self, tokens):
        model_selector = ModelSelector()
        model_selector.name = tokens[1].value

        for _, name, _, description in tokens[2]:
            description = ' '.join([token.value for token in description])
            model = ModelSelectorModel(name.value, description)
            model_selector.models.append(model)

        self._model_selectors.append(model_selector)

    def _load_model(self, tokens):
        model = Model()
        model.name = tokens[1].value

        for tag, data in tokens[2]:
            if tag == 'SubParameter':
                name, value = self._load_sub_parameter(data)

                if name == 'Model_type':
                    model.model_type = value
                elif name == 'Polarity':
                    model.polarity = value
                elif name == 'Enable':
                    model.enable = value
                else:
                    LOGGER.debug('Unsupported [Model] sub-parameter %s.', name)
            elif tag == 'NumericalSubParameter':
                name, value = self._load_numerical_sub_parameter(data)

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
                    model.c_comp.typical = self._load_numerical(data[3])
                    model.c_comp.minimum = self._load_numerical(data[5])
                    model.c_comp.maximum = self._load_numerical(data[7])
                else:
                    LOGGER.debug('Unsupported [Model] data %s.', data[1].value)
            else:
                raise InternalError('Bad tag {}.'.format(tag))

        self._models.append(model)

    def _load_add_submodel(self, tokens):
        for _, name, _, value in tokens[0]:
            add_submodel = AddSubmodel()
            add_submodel.submodel = name.value
            add_submodel.submodel_mode = value.value
            self._models[-1].add_submodel.append(add_submodel)

    def _load_temperature_range(self, tokens):
        self._models[-1].temperature_range.typical = self._load_numerical(tokens[1])
        self._models[-1].temperature_range.minimum = self._load_numerical(tokens[5])
        self._models[-1].temperature_range.maximum = self._load_numerical(tokens[3])

    def _load_voltage_range(self, tokens):
        self._models[-1].voltage_range.typical = self._load_numerical(tokens[1])
        self._models[-1].voltage_range.minimum = self._load_numerical(tokens[3])
        self._models[-1].voltage_range.maximum = self._load_numerical(tokens[5])

    def _load_ramp(self, tokens):
        ramp = Ramp()

        for tag, data in tokens[0]:
            if tag == 'SubParameterTypMinMax':
                name, typical, minimum, maximum = self._load_sub_parameter_typ_min_max(
                    data)

                if name == 'dV/dt_r':
                    ramp.dv_dt_r = (self._load_ramp_value(typical),
                                    self._load_ramp_value(minimum),
                                    self._load_ramp_value(maximum))
                elif name == 'dV/dt_f':
                    ramp.dv_dt_f = (self._load_ramp_value(typical),
                                    self._load_ramp_value(minimum),
                                    self._load_ramp_value(maximum))
                else:
                    raise Error('Invalid [Ramp] sub-parameter {}.'.format(name))
            elif tag == 'NumericalSubParameter':
                name, value = self._load_numerical_sub_parameter(data)

                if name == 'R_load':
                    ramp.r_load = value
                else:
                    raise Error(
                        'Invalid [Ramp] numerical sub-parameter {}.'.format(
                            name))
            else:
                raise InternalError('Bad tag {}.'.format(tag))

        self._models[-1].ramp = ramp

    def _load_waveform(self, tokens):
        waveform = Waveform()

        for tag, data in tokens[0]:
            if tag == 'NumericalSubParameter':
                name, value = self._load_numerical_sub_parameter(data)

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
                waveform.table.samples.append((self._load_numerical(data[2]),
                                               self._load_numerical(data[4]),
                                               self._load_numerical(data[6]),
                                               self._load_numerical(data[8])))
            else:
                raise InternalError('Bad tag {}.'.format(tag))

        return waveform

    def _load_submodel(self, tokens):
        submodel = Submodel()
        submodel.name = tokens[1].value

        for tag, data in tokens[2]:
            if tag == 'SubParameter':
                name, value = self._load_sub_parameter(data)

                if name == 'Submodel_type':
                    submodel.submodel_type = value
                else:
                    LOGGER.debug('Unsupported [Submodel] sub-parameter %s.',
                                 name)
            else:
                raise InternalError('Bad tag {}.'.format(tag))

        self._submodels.append(submodel)

    def _load_submodel_spec(self, tokens):
        submodel_spec = SubmodelSpec()

        for tag, data in tokens[0]:
            if tag == 'SubParameterTypMinMax':
                (name,
                 typical,
                 minimum,
                 maximum) = self._load_numerical_sub_parameter_typ_min_max(
                     data)

                if name == 'V_trigger_r':
                    submodel_spec.v_trigger_r.typical = typical
                    submodel_spec.v_trigger_r.minimum = minimum
                    submodel_spec.v_trigger_r.maximum = maximum
                elif name == 'V_trigger_f':
                    submodel_spec.v_trigger_f.typical = typical
                    submodel_spec.v_trigger_f.minimum = minimum
                    submodel_spec.v_trigger_f.maximum = maximum
                elif name == 'Off_delay':
                    submodel_spec.off_delay.typical = typical
                    submodel_spec.off_delay.minimum = minimum
                    submodel_spec.off_delay.maximum = maximum
                else:
                    LOGGER.debug(
                        'Unsupported [Submodel spec] sub-parameter %s.',
                        name)
            else:
                raise InternalError('Bad tag {}.'.format(tag))

        self._submodels[-1].submodel_spec = submodel_spec

    def _load_numerical(self, data):
        value = data.value

        if self._transform:
            if value == 'NA':
                value = None
            else:
                value = convert_numerical(value)

        return value

    def _load_sub_parameter(self, data):
        return data[1].value, data[3].value


    def _load_numerical_sub_parameter(self, data):
        if self._transform:
            value = self._load_numerical(data[5])
        else:
            value = data[5].value

        return data[1].value, value

    def _load_sub_parameter_typ_min_max(self, data):
        return data[1].value, data[3].value, data[5].value, data[7].value

    def _load_numerical_sub_parameter_typ_min_max(self, data):
        return (data[1].value,
                self._load_numerical(data[3]),
                self._load_numerical(data[5]),
                self._load_numerical(data[7]))

    def _load_string(self, data):
        return ''.join([text.value for text in data[0][1:]])

    def _load_4_columns(self, data):
        return [
            (self._load_numerical(v1),
             self._load_numerical(v2),
             self._load_numerical(v3),
             self._load_numerical(v4))
            for _, _, v1, _, v2, _, v3, _, v4 in data[0]
        ]

    def _load_ramp_value(self, data):
        if data == 'NA':
            if self._transform:
                data = None
        else:
            dv, dt = data.split('/')

            if self._transform:
                dv = convert_numerical(dv)
                dt = convert_numerical(dt)

            data = (dv, dt)

        return data

    @property
    def ibis_version(self):
        """The IBIS version string.

        """

        return self._ibis_version

    @property
    def file_name(self):
        """The file name string.

        """

        return self._file_name

    @property
    def file_revision(self):
        """The file revision string.

        """

        return self._file_revision

    @property
    def date(self):
        """The date string.

        """

        return self._date

    @property
    def source(self):
        """The source string.

        """

        return self._source

    @property
    def notes(self):
        """The notes string.

        """

        return self._notes

    @property
    def disclaimer(self):
        """The disclaimer string.

        """

        return self._disclaimer

    @property
    def copyright(self):
        """The copyright string.

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

    @property
    def model_selectors(self):
        """A list of all model selectors.

        """

        return self._model_selectors

    @property
    def submodels(self):
        """A list of all submodels.

        """

        return self._submodels


def split_numerical(string):
    """Split given string into a number, suffix and unit tuple.

    >>> split_numerical('1.1kOhm')
    ('1.1', 'k', 'Ohm')

    """

    mo = RE_NUMERICAL.match(string)

    if not mo:
        raise Error('Expected a numerical string, but got {}.'.format(string))

    number, _, suffix, unit = mo.groups()

    if suffix not in SUFFIX_TO_VALUE:
        unit = suffix + unit
        suffix = ''

    return number, suffix, unit


def convert_numerical(string):
    """Convert given string to a Decimal value.

    >>> convert_numerical('1.1kOhm')
    Decimal('1.1e3')

    """

    number, suffix, _ = split_numerical(string)

    value = Decimal(number)

    if suffix:
        value *= SUFFIX_TO_VALUE[suffix]

    return value


def load_file(filename, transform=False):
    """Load given IBIS file and return an IbsFile object with its
    contents.

    Give `transform` as ``True`` to convert numerical numbers from
    strings to ``decimal.Decimal`` and ``'NA'`` to ``None``.

    """

    with open(filename, 'r') as fin:
        string = fin.read()

    return IbsFile(string, transform)


def format_or(items):
    items = [str(item) for item in items]

    if len(items) == 0:
        return ''
    elif len(items) == 1:
        return items[0]
    else:
        return '{} or {}'.format(', '.join(items[:-1]),
                                 items[-1])
