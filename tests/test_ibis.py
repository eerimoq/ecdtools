import logging
import unittest
from decimal import Decimal

from ecdtools import ibis


class IbisTest(unittest.TestCase):

    maxDiff = None

    def test_load_bushold(self):
        ibis_file = ibis.load_file('tests/files/ibis/pybis/bushold.ibs')

        # General information.
        self.assertEqual(ibis_file.version, '3.2')
        self.assertEqual(ibis_file.file_name, 'bushold.ibs')
        self.assertEqual(ibis_file.file_rev, '0.2')
        self.assertEqual(ibis_file.date, 'June 24, 1998')
        self.assertEqual(ibis_file.source, 'Artifical Data')
        self.assertEqual(ibis_file.notes, 'This data is a sample, only.')
        self.assertEqual(
            ibis_file.disclaimer,
            'This information is for modeling purposes and is not')
        self.assertEqual(ibis_file.copyright, 'None - public sample')

        # Components.
        self.assertEqual(len(ibis_file.components), 1)

        # First (and only) component.
        component = ibis_file.components[0]

        self.assertEqual(component.name, 'BUS-HOLD-SAMPLE')
        self.assertEqual(component.si_location, None)
        self.assertEqual(component.timing_location, None)
        self.assertEqual(component.manufacturer, 'None')
        self.assertEqual(component.package.r_pkg.typical, '200m')
        self.assertEqual(component.package.r_pkg.minimum, '100m')
        self.assertEqual(component.package.r_pkg.maximum, '300m')
        self.assertEqual(component.package.l_pkg.typical, '4.32nH')
        self.assertEqual(component.package.l_pkg.minimum, '3.34nH')
        self.assertEqual(component.package.l_pkg.maximum, '5.30nH')
        self.assertEqual(component.package.c_pkg.typical, '0.38pF')
        self.assertEqual(component.package.c_pkg.minimum, '0.33pF')
        self.assertEqual(component.package.c_pkg.maximum, '0.43pF')
        self.assertEqual(len(component.pins), 3)
        self.assertEqual(component.pins[0].name, '1')
        self.assertEqual(component.pins[0].signal_name, 'Sample1')
        self.assertEqual(component.pins[0].model_name, 'TOP_MODEL_BUS_HOLD')
        self.assertEqual(component.pins[0].r_pin, None)
        self.assertEqual(component.pins[0].l_pin, None)
        self.assertEqual(component.pins[0].c_pin, None)
        self.assertEqual(component.pins[1].name, '12')
        self.assertEqual(component.pins[1].signal_name, 'GND')
        self.assertEqual(component.pins[1].model_name, 'GND')
        self.assertEqual(component.pins[1].r_pin, None)
        self.assertEqual(component.pins[1].l_pin, None)
        self.assertEqual(component.pins[1].c_pin, None)
        self.assertEqual(component.pins[2].name, '24')
        self.assertEqual(component.pins[2].signal_name, 'VCC')
        self.assertEqual(component.pins[2].model_name, 'POWER')
        self.assertEqual(component.pins[2].r_pin, None)
        self.assertEqual(component.pins[2].l_pin, None)
        self.assertEqual(component.pins[2].c_pin, None)

        # Models.
        self.assertEqual(len(ibis_file.models), 1)

        # First (and only) model.
        self.assertEqual(ibis_file.models[0].name, 'TOP_MODEL_BUS_HOLD')
        self.assertEqual(ibis_file.models[0].model_type, 'Input')
        self.assertEqual(ibis_file.models[0].polarity, None)
        self.assertEqual(ibis_file.models[0].enable, None)
        self.assertEqual(ibis_file.models[0].vinl, '0.8')
        self.assertEqual(ibis_file.models[0].vinh, '2.0')
        self.assertEqual(ibis_file.models[0].c_comp.typical, '4pF')
        self.assertEqual(ibis_file.models[0].c_comp.minimum, '3pF')
        self.assertEqual(ibis_file.models[0].c_comp.maximum, '5pF')
        self.assertEqual(ibis_file.models[0].vmeas, None)
        self.assertEqual(ibis_file.models[0].cref, None)
        self.assertEqual(ibis_file.models[0].vref, None)
        self.assertEqual(ibis_file.models[0].rref, None)
        self.assertEqual(ibis_file.models[0].temperature_range.typical, None)
        self.assertEqual(ibis_file.models[0].temperature_range.minimum, None)
        self.assertEqual(ibis_file.models[0].temperature_range.maximum, None)
        self.assertEqual(ibis_file.models[0].voltage_range.typical, '5.0')
        self.assertEqual(ibis_file.models[0].voltage_range.minimum, '4.5')
        self.assertEqual(ibis_file.models[0].voltage_range.maximum, '5.5')
        self.assertEqual(
            ibis_file.models[0].gnd_clamp,
            [
                ('-2.0000e+00', '-6.158e+17', 'NA', 'NA'),
                ('-1.9000e+00', '-1.697e+16', 'NA', 'NA'),
                ('-1.8000e+00', '-4.679e+14', 'NA', 'NA'),
                ('-1.7000e+00', '-1.290e+13', 'NA', 'NA'),
                ('-1.6000e+00', '-3.556e+11', 'NA', 'NA'),
                ('-1.5000e+00', '-9.802e+09', 'NA', 'NA'),
                ('-1.4000e+00', '-2.702e+08', 'NA', 'NA'),
                ('-1.3000e+00', '-7.449e+06', 'NA', 'NA'),
                ('-1.2000e+00', '-2.053e+05', 'NA', 'NA'),
                ('-1.1000e+00', '-5.660e+03', 'NA', 'NA'),
                ('-1.0000e+00', '-1.560e+02', 'NA', 'NA'),
                ('-9.0000e-01', '-4.308e+00', 'NA', 'NA'),
                ('-8.0000e-01', '-1.221e-01', 'NA', 'NA'),
                ('-7.0000e-01', '-4.315e-03', 'NA', 'NA'),
                ('-6.0000e-01', '-1.715e-04', 'NA', 'NA'),
                ('-5.0000e-01', '-4.959e-06', 'NA', 'NA'),
                ('-4.0000e-01', '-1.373e-07', 'NA', 'NA'),
                ('-3.0000e-01', '-4.075e-09', 'NA', 'NA'),
                ('-2.0000e-01', '-3.044e-10', 'NA', 'NA'),
                ('-1.0000e-01', '-1.030e-10', 'NA', 'NA'),
                ('0.', '0', 'NA', 'NA'),
                ('5', '0', 'NA', 'NA')
            ])
        self.assertEqual(
            ibis_file.models[0].power_clamp,
            [
                ('-2.0000e+00', '6.158e+17', 'NA', 'NA'),
                ('-1.9000e+00', '1.697e+16', 'NA', 'NA'),
                ('-1.8000e+00', '4.679e+14', 'NA', 'NA'),
                ('-1.7000e+00', '1.290e+13', 'NA', 'NA'),
                ('-1.6000e+00', '3.556e+11', 'NA', 'NA'),
                ('-1.5000e+00', '9.802e+09', 'NA', 'NA'),
                ('-1.4000e+00', '2.702e+08', 'NA', 'NA'),
                ('-1.3000e+00', '7.449e+06', 'NA', 'NA'),
                ('-1.2000e+00', '2.053e+05', 'NA', 'NA'),
                ('-1.1000e+00', '5.660e+03', 'NA', 'NA'),
                ('-1.0000e+00', '1.560e+02', 'NA', 'NA'),
                ('-9.0000e-01', '4.308e+00', 'NA', 'NA'),
                ('-8.0000e-01', '1.221e-01', 'NA', 'NA'),
                ('-7.0000e-01', '4.315e-03', 'NA', 'NA'),
                ('-6.0000e-01', '1.715e-04', 'NA', 'NA'),
                ('-5.0000e-01', '4.959e-06', 'NA', 'NA'),
                ('-4.0000e-01', '1.373e-07', 'NA', 'NA'),
                ('-3.0000e-01', '4.075e-09', 'NA', 'NA'),
                ('-2.0000e-01', '3.044e-10', 'NA', 'NA'),
                ('-1.0000e-01', '1.030e-10', 'NA', 'NA'),
                ('0.', '0', 'NA', 'NA'),
                ('5', '0', 'NA', 'NA')
            ])
        self.assertEqual(
            ibis_file.models[0].pullup,
            [
                ('-5V', '100uA', '80uA', '120uA'),
                ('-1V', '30uA', '25uA', '40uA'),
                ('0V', '0', '0', '0'),
                ('1V', '-30uA', '-25uA', '-40uA'),
                ('3V', '-50uA', '-45uA', '-50uA'),
                ('5V', '-100uA', '-80uA', '-120uA'),
                ('10v', '-120uA', '-90uA', '-150uA')
            ])
        self.assertEqual(
            ibis_file.models[0].pulldown,
            [
                ('-5V', '-100uA', '-80uA', '-120uA'),
                ('-1V', '-30uA', '-25uA', '-40uA'),
                ('0V', '0', '0', '0'),
                ('1V', '30uA', '25uA', '40uA'),
                ('3V', '50uA', '45uA', '50uA'),
                ('5V', '100uA', '80uA', '120uA'),
                ('10v', '120uA', '90uA', '150uA')
            ])
        self.assertEqual(ibis_file.models[0].ramp.dv_dt_r,
                         ('2.0/0.50n', '2.0/0.75n', '2.0/0.35n'))
        self.assertEqual(ibis_file.models[0].ramp.dv_dt_f,
                         ('2.0/0.50n', '2.0/0.75n', '2.0/0.35n'))
        self.assertEqual(ibis_file.models[0].ramp.r_load,
                         '500')
        self.assertEqual(ibis_file.models[0].falling_waveforms, [])
        self.assertEqual(ibis_file.models[0].rising_waveforms, [])

    def test_load_sample1(self):
        ibis_file = ibis.load_file('tests/files/ibis/pybis/sample1.ibs')

        # General information.
        self.assertEqual(ibis_file.version, '3.2')
        self.assertEqual(ibis_file.file_name, 'sample1.ibs')
        self.assertEqual(ibis_file.file_rev, '0')
        self.assertEqual(ibis_file.date, '10/23/2001')
        self.assertEqual(ibis_file.source, 'Company_ABC, Adapted From Real IBIS Model')
        self.assertEqual(ibis_file.notes, None)
        self.assertEqual(ibis_file.disclaimer, None)
        self.assertEqual(ibis_file.copyright, 'Public Sample')

        # Components.
        self.assertEqual(len(ibis_file.components), 1)

        # First (and only) component.
        component = ibis_file.components[0]

        self.assertEqual(component.name, 'WXY123')
        self.assertEqual(component.si_location, None)
        self.assertEqual(component.timing_location, None)
        self.assertEqual(component.manufacturer, 'Company_ABC')
        self.assertEqual(component.package.r_pkg.typical, '0.0m')
        self.assertEqual(component.package.r_pkg.minimum, '0.0m')
        self.assertEqual(component.package.r_pkg.maximum, '0.0m')
        self.assertEqual(component.package.l_pkg.typical, '3.0nH')
        self.assertEqual(component.package.l_pkg.minimum, '2.0nH')
        self.assertEqual(component.package.l_pkg.maximum, '4.0nH')
        self.assertEqual(component.package.c_pkg.typical, '0.5pF')
        self.assertEqual(component.package.c_pkg.minimum, '0.3pF')
        self.assertEqual(component.package.c_pkg.maximum, '0.8pf')
        self.assertEqual(len(component.pins), 231)
        self.assertEqual(component.pins[0].name, 'A10')
        self.assertEqual(component.pins[0].signal_name, 'cs1')
        self.assertEqual(component.pins[0].model_name, 'BT2Z50CX')
        self.assertEqual(component.pins[0].r_pin, '32m')
        self.assertEqual(component.pins[0].l_pin, '3.44nH')
        self.assertEqual(component.pins[0].c_pin, '0.46pF')
        self.assertEqual(component.pins[230].name, 'Y9')
        self.assertEqual(component.pins[230].signal_name, 'sc_moden')
        self.assertEqual(component.pins[230].model_name, 'BPS2P4F_PU50K')
        self.assertEqual(component.pins[230].r_pin, '32m')
        self.assertEqual(component.pins[230].l_pin, '3.45nH')
        self.assertEqual(component.pins[230].c_pin, '0.46pF')

        # Models.
        self.assertEqual(len(ibis_file.models), 14)

        # First model.
        self.assertEqual(ibis_file.models[0].name, 'BIP00F')
        self.assertEqual(ibis_file.models[0].model_type, 'Input')
        self.assertEqual(ibis_file.models[0].polarity, 'Non-Inverting')
        self.assertEqual(ibis_file.models[0].enable, None)
        self.assertEqual(ibis_file.models[0].vinl, '0.8V')
        self.assertEqual(ibis_file.models[0].vinh, '2.0V')
        self.assertEqual(ibis_file.models[0].c_comp.typical, '0.737pF')
        self.assertEqual(ibis_file.models[0].c_comp.minimum, 'NA')
        self.assertEqual(ibis_file.models[0].c_comp.maximum, 'NA')
        self.assertEqual(ibis_file.models[0].vmeas, None)
        self.assertEqual(ibis_file.models[0].cref, None)
        self.assertEqual(ibis_file.models[0].vref, None)
        self.assertEqual(ibis_file.models[0].rref, None)
        self.assertEqual(ibis_file.models[0].temperature_range.typical, '25')
        self.assertEqual(ibis_file.models[0].temperature_range.minimum, '0')
        self.assertEqual(ibis_file.models[0].temperature_range.maximum, '125')
        self.assertEqual(ibis_file.models[0].voltage_range.typical, '3.3V')
        self.assertEqual(ibis_file.models[0].voltage_range.minimum, '3.0V')
        self.assertEqual(ibis_file.models[0].voltage_range.maximum, '3.6V')

        self.assertEqual(len(ibis_file.models[0].gnd_clamp), 67)
        self.assertEqual(
            ibis_file.models[0].gnd_clamp[0],
            ('-3.30000', '-11.46380A', '-11.71150A', '-11.40800A'))
        self.assertEqual(
            ibis_file.models[0].gnd_clamp[66],
            ('3.30000', '6.60800pA', '26.57000nA', '6.32380pA'))

        self.assertEqual(len(ibis_file.models[0].power_clamp), 34)
        self.assertEqual(
            ibis_file.models[0].power_clamp[0],
            ('-3.30000', '10.22730A', '10.48520A', '10.16810A'))
        self.assertEqual(
            ibis_file.models[0].power_clamp[33],
            ('0.00000', '6.59380pA', '10.90680pA', '7.23330pA'))

        self.assertEqual(ibis_file.models[0].pullup, None)
        self.assertEqual(ibis_file.models[0].pulldown, None)
        self.assertEqual(ibis_file.models[0].ramp, None)
        self.assertEqual(ibis_file.models[0].falling_waveforms, [])
        self.assertEqual(ibis_file.models[0].rising_waveforms, [])

        #  model.
        self.assertEqual(ibis_file.models[11].name, 'BT2Z50CX_PU50K')
        self.assertEqual(ibis_file.models[11].model_type, 'I/O')
        self.assertEqual(ibis_file.models[11].polarity, 'Non-Inverting')
        self.assertEqual(ibis_file.models[11].enable, 'Active-High')
        self.assertEqual(ibis_file.models[11].vinl, '0.8V')
        self.assertEqual(ibis_file.models[11].vinh, '2.0V')
        self.assertEqual(ibis_file.models[11].c_comp.typical, '1.26pF')
        self.assertEqual(ibis_file.models[11].c_comp.minimum, 'NA')
        self.assertEqual(ibis_file.models[11].c_comp.maximum, 'NA')
        self.assertEqual(ibis_file.models[11].vmeas, '1.65V')
        self.assertEqual(ibis_file.models[11].cref, '1.0pF')
        self.assertEqual(ibis_file.models[11].vref, '0V')
        self.assertEqual(ibis_file.models[11].rref, '1Mohms')
        self.assertEqual(ibis_file.models[11].temperature_range.typical, '25')
        self.assertEqual(ibis_file.models[11].temperature_range.minimum, '0')
        self.assertEqual(ibis_file.models[11].temperature_range.maximum, '125')
        self.assertEqual(ibis_file.models[11].voltage_range.typical, '3.3V')
        self.assertEqual(ibis_file.models[11].voltage_range.minimum, '3.0V')
        self.assertEqual(ibis_file.models[11].voltage_range.maximum, '3.6V')
        self.assertEqual(len(ibis_file.models[11].gnd_clamp), 35)
        self.assertEqual(len(ibis_file.models[11].power_clamp), 58)
        self.assertEqual(len(ibis_file.models[11].pullup), 100)
        self.assertEqual(len(ibis_file.models[11].pulldown), 100)

        self.assertEqual(
            ibis_file.models[11].ramp.dv_dt_r,
            ('0.950146V/0.229176ns', '0.891184V/0.260292ns', '1.0311V/0.221583ns'))
        self.assertEqual(
            ibis_file.models[11].ramp.dv_dt_f,
            ('0.94062V/0.319408ns', '0.89298V/0.416034ns', '1.00716V/0.284201ns'))
        self.assertEqual(ibis_file.models[11].ramp.r_load, '50')

        # Falling waveforms.
        self.assertEqual(len(ibis_file.models[11].falling_waveforms), 2)

        waveform = ibis_file.models[11].falling_waveforms[0]
        self.assertEqual(waveform.r_fixture, '50')
        self.assertEqual(waveform.v_fixture.typical, '3.3')
        self.assertEqual(waveform.v_fixture.minimum, '3.0')
        self.assertEqual(waveform.v_fixture.maximum, '3.6')
        self.assertEqual(len(waveform.table.samples), 100)
        self.assertEqual(
            waveform.table.samples[0],
            ('0.00000S', '3.30000V', '3.00000V', '3.60000V'))
        self.assertEqual(
            waveform.table.samples[99],
            ('1.50000nS', '1.73230V', '1.51170V', '1.92140V'))
        waveform = ibis_file.models[11].falling_waveforms[1]
        self.assertEqual(len(waveform.table.samples), 100)
        self.assertEqual(
            waveform.table.samples[0],
            ('0.00000S', '1.59770V', '1.50670V', '1.73430V'))
        self.assertEqual(
            waveform.table.samples[99],
            ('1.35000nS', '14.88300mV', '24.09000mV', '19.09910mV'))

        # Rising waveforms.
        self.assertEqual(len(ibis_file.models[11].rising_waveforms), 2)

        waveform = ibis_file.models[11].rising_waveforms[0]
        self.assertEqual(waveform.r_fixture, '50')
        self.assertEqual(waveform.v_fixture.typical, '0.000')
        self.assertEqual(waveform.v_fixture.minimum, '0.000')
        self.assertEqual(waveform.v_fixture.maximum, '0.000')
        self.assertEqual(len(waveform.table.samples), 100)
        self.assertEqual(
            waveform.table.samples[0],
            ('0.00000S', '923.25950uV', '493.94600uV', '1.40550mV'))
        self.assertEqual(
            waveform.table.samples[99],
            ('1.50000nS', '1.58450V', '1.48580V', '1.71990V'))

    def test_load_numerical(self):
        self.assertEqual(ibis.load_numerical('1.1T'), Decimal('1.1e12'))
        self.assertEqual(ibis.load_numerical('1.1G'), Decimal('1.1e9'))
        self.assertEqual(ibis.load_numerical('1.1M'), Decimal('1.1e6'))
        self.assertEqual(ibis.load_numerical('1.1k'), Decimal('1.1e3'))
        self.assertEqual(ibis.load_numerical('1.1'),  Decimal('1.1'))
        self.assertEqual(ibis.load_numerical('1.1m'), Decimal('1.1e-3'))
        self.assertEqual(ibis.load_numerical('1.1u'), Decimal('1.1e-6'))
        self.assertEqual(ibis.load_numerical('1.1n'), Decimal('1.1e-9'))
        self.assertEqual(ibis.load_numerical('1.1p'), Decimal('1.1e-12'))
        self.assertEqual(ibis.load_numerical('1.1f'), Decimal('1.1e-15'))
        self.assertEqual(ibis.load_numerical('2.123E-5'), Decimal('0.00002123'))
        self.assertEqual(ibis.load_numerical('2.123e5'), Decimal('2.123e5'))
        self.assertEqual(ibis.load_numerical('2.123E+5'), Decimal('2.123e5'))
        self.assertEqual(ibis.load_numerical('1.1Ohm'), Decimal('1.1'))
        self.assertEqual(ibis.load_numerical('1.1kOhm'), Decimal('1.1e3'))

    def test_load_pybis_files(self):
        filenames = [
            'sterm.ibs',
            'sample2.ibs',
            'sample1(original).ibs',
            'sample1.ibs',
            'ideal_driver.ibs',
            'diff_pecl_term.ibs',
            'dclamptr.ibs',
            'dclampst.ibs',
            'cbt.ibs',
            'bushold.ibs',
            'bird57ex.ibs',
            'bugs/bug74.ibs',
            'bugs/bug81.ibs',
            'bugs/bug82.ibs',
            'bugs/bug86.ibs',
            'bugs/bug87.ibs'
        ]

        for filename in filenames:
            ibis.load_file('tests/files/ibis/pybis/' + filename)


logging.basicConfig(level=logging.DEBUG)
