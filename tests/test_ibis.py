import logging
import unittest
from decimal import Decimal

import ecdtools
from ecdtools import ibis


class IbisTest(unittest.TestCase):

    maxDiff = None

    def test_load_bushold(self):
        ibis_file = ibis.load_file('tests/files/ibis/pybis/bushold.ibs')

        # General information.
        self.assertEqual(ibis_file.ibis_version, '3.2')
        self.assertEqual(ibis_file.file_name, 'bushold.ibs')
        self.assertEqual(ibis_file.file_revision, '0.2')
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
                         (('2.0', '0.50n'),
                          ('2.0', '0.75n'),
                          ('2.0', '0.35n')))
        self.assertEqual(ibis_file.models[0].ramp.dv_dt_f,
                         (('2.0', '0.50n'),
                          ('2.0', '0.75n'),
                          ('2.0', '0.35n')))
        self.assertEqual(ibis_file.models[0].ramp.r_load,
                         '500')
        self.assertEqual(ibis_file.models[0].falling_waveforms, [])
        self.assertEqual(ibis_file.models[0].rising_waveforms, [])
        self.assertEqual(ibis_file.models[0].add_submodel[0].submodel,
                         'BUS_HOLD')
        self.assertEqual(ibis_file.models[0].add_submodel[0].submodel_mode,
                         'All')

        # Submodels.
        self.assertEqual(len(ibis_file.submodels), 1)

        # First (and only) submodel.
        self.assertEqual(ibis_file.submodels[0].name, 'BUS_HOLD')
        self.assertEqual(ibis_file.submodels[0].submodel_type, 'Bus_hold')

        submodel_spec = ibis_file.submodels[0].submodel_spec

        self.assertEqual(submodel_spec.v_trigger_r.typical, '3.1')
        self.assertEqual(submodel_spec.v_trigger_r.minimum, '2.6')
        self.assertEqual(submodel_spec.v_trigger_r.maximum, '4.6')
        self.assertEqual(submodel_spec.v_trigger_f.typical, '1.3')
        self.assertEqual(submodel_spec.v_trigger_f.minimum, '1.2')
        self.assertEqual(submodel_spec.v_trigger_f.maximum, '1.4')
        self.assertEqual(submodel_spec.off_delay.typical, None)
        self.assertEqual(submodel_spec.off_delay.minimum, None)
        self.assertEqual(submodel_spec.off_delay.maximum, None)

    def test_load_bushold_transform(self):
        ibis_file = ibis.load_file('tests/files/ibis/pybis/bushold.ibs',
                                   transform=True)

        # General information.
        self.assertEqual(ibis_file.ibis_version, '3.2')
        self.assertEqual(ibis_file.file_name, 'bushold.ibs')
        self.assertEqual(ibis_file.file_revision, '0.2')
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
        self.assertEqual(component.package.r_pkg.typical, Decimal('200e-3'))
        self.assertEqual(component.package.r_pkg.minimum, Decimal('100e-3'))
        self.assertEqual(component.package.r_pkg.maximum, Decimal('300e-3'))
        self.assertEqual(component.package.l_pkg.typical, Decimal('4.32e-9'))
        self.assertEqual(component.package.l_pkg.minimum, Decimal('3.34e-9'))
        self.assertEqual(component.package.l_pkg.maximum, Decimal('5.30e-9'))
        self.assertEqual(component.package.c_pkg.typical, Decimal('0.38e-12'))
        self.assertEqual(component.package.c_pkg.minimum, Decimal('0.33e-12'))
        self.assertEqual(component.package.c_pkg.maximum, Decimal('0.43e-12'))
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
        self.assertEqual(ibis_file.models[0].vinl, Decimal('0.8'))
        self.assertEqual(ibis_file.models[0].vinh, Decimal('2.0'))
        self.assertEqual(ibis_file.models[0].c_comp.typical, Decimal('4e-12'))
        self.assertEqual(ibis_file.models[0].c_comp.minimum, Decimal('3e-12'))
        self.assertEqual(ibis_file.models[0].c_comp.maximum, Decimal('5e-12'))
        self.assertEqual(ibis_file.models[0].vmeas, None)
        self.assertEqual(ibis_file.models[0].cref, None)
        self.assertEqual(ibis_file.models[0].vref, None)
        self.assertEqual(ibis_file.models[0].rref, None)
        self.assertEqual(ibis_file.models[0].temperature_range.typical, None)
        self.assertEqual(ibis_file.models[0].temperature_range.minimum, None)
        self.assertEqual(ibis_file.models[0].temperature_range.maximum, None)
        self.assertEqual(ibis_file.models[0].voltage_range.typical, Decimal('5.0'))
        self.assertEqual(ibis_file.models[0].voltage_range.minimum, Decimal('4.5'))
        self.assertEqual(ibis_file.models[0].voltage_range.maximum, Decimal('5.5'))
        self.assertEqual(
            ibis_file.models[0].gnd_clamp,
            [
                (Decimal('-2.0000e+00'), Decimal('-6.158e+17'), None, None),
                (Decimal('-1.9000e+00'), Decimal('-1.697e+16'), None, None),
                (Decimal('-1.8000e+00'), Decimal('-4.679e+14'), None, None),
                (Decimal('-1.7000e+00'), Decimal('-1.290e+13'), None, None),
                (Decimal('-1.6000e+00'), Decimal('-3.556e+11'), None, None),
                (Decimal('-1.5000e+00'), Decimal('-9.802e+09'), None, None),
                (Decimal('-1.4000e+00'), Decimal('-2.702e+08'), None, None),
                (Decimal('-1.3000e+00'), Decimal('-7.449e+06'), None, None),
                (Decimal('-1.2000e+00'), Decimal('-2.053e+05'), None, None),
                (Decimal('-1.1000e+00'), Decimal('-5.660e+03'), None, None),
                (Decimal('-1.0000e+00'), Decimal('-1.560e+02'), None, None),
                (Decimal('-9.0000e-01'), Decimal('-4.308e+00'), None, None),
                (Decimal('-8.0000e-01'), Decimal('-1.221e-01'), None, None),
                (Decimal('-7.0000e-01'), Decimal('-4.315e-03'), None, None),
                (Decimal('-6.0000e-01'), Decimal('-1.715e-04'), None, None),
                (Decimal('-5.0000e-01'), Decimal('-4.959e-06'), None, None),
                (Decimal('-4.0000e-01'), Decimal('-1.373e-07'), None, None),
                (Decimal('-3.0000e-01'), Decimal('-4.075e-09'), None, None),
                (Decimal('-2.0000e-01'), Decimal('-3.044e-10'), None, None),
                (Decimal('-1.0000e-01'), Decimal('-1.030e-10'), None, None),
                (Decimal('0.'), Decimal('0'), None, None),
                (Decimal('5'), Decimal('0'), None, None)
            ])
        self.assertEqual(
            ibis_file.models[0].power_clamp,
            [
                (Decimal('-2.0000e+00'), Decimal('6.158e+17'), None, None),
                (Decimal('-1.9000e+00'), Decimal('1.697e+16'), None, None),
                (Decimal('-1.8000e+00'), Decimal('4.679e+14'), None, None),
                (Decimal('-1.7000e+00'), Decimal('1.290e+13'), None, None),
                (Decimal('-1.6000e+00'), Decimal('3.556e+11'), None, None),
                (Decimal('-1.5000e+00'), Decimal('9.802e+09'), None, None),
                (Decimal('-1.4000e+00'), Decimal('2.702e+08'), None, None),
                (Decimal('-1.3000e+00'), Decimal('7.449e+06'), None, None),
                (Decimal('-1.2000e+00'), Decimal('2.053e+05'), None, None),
                (Decimal('-1.1000e+00'), Decimal('5.660e+03'), None, None),
                (Decimal('-1.0000e+00'), Decimal('1.560e+02'), None, None),
                (Decimal('-9.0000e-01'), Decimal('4.308e+00'), None, None),
                (Decimal('-8.0000e-01'), Decimal('1.221e-01'), None, None),
                (Decimal('-7.0000e-01'), Decimal('4.315e-03'), None, None),
                (Decimal('-6.0000e-01'), Decimal('1.715e-04'), None, None),
                (Decimal('-5.0000e-01'), Decimal('4.959e-06'), None, None),
                (Decimal('-4.0000e-01'), Decimal('1.373e-07'), None, None),
                (Decimal('-3.0000e-01'), Decimal('4.075e-09'), None, None),
                (Decimal('-2.0000e-01'), Decimal('3.044e-10'), None, None),
                (Decimal('-1.0000e-01'), Decimal('1.030e-10'), None, None),
                (Decimal('0.'), Decimal('0'), None, None),
                (Decimal('5'), Decimal('0'), None, None)
            ])
        self.assertEqual(
            ibis_file.models[0].pullup,
            [
                (Decimal('-5'), Decimal('100e-6'), Decimal('80e-6'), Decimal('120e-6')),
                (Decimal('-1'), Decimal('30e-6'), Decimal('25e-6'), Decimal('40e-6')),
                (Decimal('0'), Decimal('0'), Decimal('0'), Decimal('0')),
                (Decimal('1'), Decimal('-30e-6'), Decimal('-25e-6'), Decimal('-40e-6')),
                (Decimal('3'), Decimal('-50e-6'), Decimal('-45e-6'), Decimal('-50e-6')),
                (Decimal('5'), Decimal('-100e-6'), Decimal('-80e-6'), Decimal('-120e-6')),
                (Decimal('10'), Decimal('-120e-6'), Decimal('-90e-6'), Decimal('-150e-6'))
            ])
        self.assertEqual(
            ibis_file.models[0].pulldown,
            [
                (Decimal('-5'), Decimal('-100e-6'), Decimal('-80e-6'), Decimal('-120e-6')),
                (Decimal('-1'), Decimal('-30e-6'), Decimal('-25e-6'), Decimal('-40e-6')),
                (Decimal('0'), Decimal('0'), Decimal('0'), Decimal('0')),
                (Decimal('1'), Decimal('30e-6'), Decimal('25e-6'), Decimal('40e-6')),
                (Decimal('3'), Decimal('50e-6'), Decimal('45e-6'), Decimal('50e-6')),
                (Decimal('5'), Decimal('100e-6'), Decimal('80e-6'), Decimal('120e-6')),
                (Decimal('10'), Decimal('120e-6'), Decimal('90e-6'), Decimal('150e-6'))
            ])
        self.assertEqual(ibis_file.models[0].ramp.dv_dt_r,
                         ((Decimal('2.0'), Decimal('0.50e-9')),
                          (Decimal('2.0'), Decimal('0.75e-9')),
                          (Decimal('2.0'), Decimal('0.35e-9'))))
        self.assertEqual(ibis_file.models[0].ramp.dv_dt_f,
                         ((Decimal('2.0'), Decimal('0.50e-9')),
                          (Decimal('2.0'), Decimal('0.75e-9')),
                          (Decimal('2.0'), Decimal('0.35e-9'))))
        self.assertEqual(ibis_file.models[0].ramp.r_load,
                         Decimal('500'))
        self.assertEqual(ibis_file.models[0].falling_waveforms, [])
        self.assertEqual(ibis_file.models[0].rising_waveforms, [])

    def test_load_sample1(self):
        ibis_file = ibis.load_file('tests/files/ibis/pybis/sample1.ibs')

        # General information.
        self.assertEqual(ibis_file.ibis_version, '3.2')
        self.assertEqual(ibis_file.file_name, 'sample1.ibs')
        self.assertEqual(ibis_file.file_revision, '@(#)$Revision: 0.1')
        self.assertEqual(ibis_file.date, 'September 11, 2015')
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
        self.assertEqual(len(component.diff_pins), 1)
        self.assertEqual(component.diff_pins[0].name, 'E17')
        self.assertEqual(component.diff_pins[0].inv_pin, 'D18')
        self.assertEqual(component.diff_pins[0].vdiff, '2.0')
        self.assertEqual(component.diff_pins[0].tdelay_typ, 'NA')
        self.assertEqual(component.diff_pins[0].tdelay_min, 'NA')
        self.assertEqual(component.diff_pins[0].tdelay_max, 'NA')

        # Model selector.
        self.assertEqual(len(ibis_file.model_selectors), 1)
        model_selector = ibis_file.model_selectors[0]
        self.assertEqual(model_selector.name, 'BUSB6AU')
        self.assertEqual(len(model_selector.models), 2)
        self.assertEqual(model_selector.models[0].name, 'BUSB6AU_HIGH_SPEED')
        self.assertEqual(model_selector.models[0].description, 'USB_HIGH_SPEED')
        self.assertEqual(model_selector.models[1].name, 'BUSB6AU_LOW_SPEED')
        self.assertEqual(model_selector.models[1].description, 'USB_LOW_SPEED')

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

        # Last model.
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
        self.assertEqual(ibis_file.models[11].ramp.dv_dt_r,
                         (('0.950146V', '0.229176ns'),
                          ('0.891184V', '0.260292ns'),
                          ('1.0311V', '0.221583ns')))
        self.assertEqual(ibis_file.models[11].ramp.dv_dt_f,
                         (('0.94062V', '0.319408ns'),
                          ('0.89298V', '0.416034ns'),
                          ('1.00716V', '0.284201ns')))
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

    def test_load_sample1_transform(self):
        ibis_file = ibis.load_file('tests/files/ibis/pybis/sample1.ibs',
                                   transform=True)

        # General information.
        self.assertEqual(ibis_file.ibis_version, '3.2')
        self.assertEqual(ibis_file.file_name, 'sample1.ibs')
        self.assertEqual(ibis_file.file_revision, '@(#)$Revision: 0.1')
        self.assertEqual(ibis_file.date, 'September 11, 2015')
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
        self.assertEqual(component.package.r_pkg.typical, Decimal('0.0e-3'))
        self.assertEqual(component.package.r_pkg.minimum, Decimal('0.0e-3'))
        self.assertEqual(component.package.r_pkg.maximum, Decimal('0.0e-3'))
        self.assertEqual(component.package.l_pkg.typical, Decimal('3.0e-9'))
        self.assertEqual(component.package.l_pkg.minimum, Decimal('2.0e-9'))
        self.assertEqual(component.package.l_pkg.maximum, Decimal('4.0e-9'))
        self.assertEqual(component.package.c_pkg.typical, Decimal('0.5e-12'))
        self.assertEqual(component.package.c_pkg.minimum, Decimal('0.3e-12'))
        self.assertEqual(component.package.c_pkg.maximum, Decimal('0.8e-12'))
        self.assertEqual(len(component.pins), 231)
        self.assertEqual(component.pins[0].name, 'A10')
        self.assertEqual(component.pins[0].signal_name, 'cs1')
        self.assertEqual(component.pins[0].model_name, 'BT2Z50CX')
        self.assertEqual(component.pins[0].r_pin, Decimal('32e-3'))
        self.assertEqual(component.pins[0].l_pin, Decimal('3.44e-9'))
        self.assertEqual(component.pins[0].c_pin, Decimal('0.46e-12'))
        self.assertEqual(component.pins[230].name, 'Y9')
        self.assertEqual(component.pins[230].signal_name, 'sc_moden')
        self.assertEqual(component.pins[230].model_name, 'BPS2P4F_PU50K')
        self.assertEqual(component.pins[230].r_pin, Decimal('32e-3'))
        self.assertEqual(component.pins[230].l_pin, Decimal('3.45e-9'))
        self.assertEqual(component.pins[230].c_pin, Decimal('0.46e-12'))

        # Models.
        self.assertEqual(len(ibis_file.models), 14)

        # First model.
        self.assertEqual(ibis_file.models[0].name, 'BIP00F')
        self.assertEqual(ibis_file.models[0].model_type, 'Input')
        self.assertEqual(ibis_file.models[0].polarity, 'Non-Inverting')
        self.assertEqual(ibis_file.models[0].enable, None)
        self.assertEqual(ibis_file.models[0].vinl, Decimal('0.8'))
        self.assertEqual(ibis_file.models[0].vinh, Decimal('2.0'))
        self.assertEqual(ibis_file.models[0].c_comp.typical, Decimal('0.737e-12'))
        self.assertEqual(ibis_file.models[0].c_comp.minimum, None)
        self.assertEqual(ibis_file.models[0].c_comp.maximum, None)
        self.assertEqual(ibis_file.models[0].vmeas, None)
        self.assertEqual(ibis_file.models[0].cref, None)
        self.assertEqual(ibis_file.models[0].vref, None)
        self.assertEqual(ibis_file.models[0].rref, None)
        self.assertEqual(ibis_file.models[0].temperature_range.typical, Decimal('25'))
        self.assertEqual(ibis_file.models[0].temperature_range.minimum, Decimal('0'))
        self.assertEqual(ibis_file.models[0].temperature_range.maximum, Decimal('125'))
        self.assertEqual(ibis_file.models[0].voltage_range.typical, Decimal('3.3'))
        self.assertEqual(ibis_file.models[0].voltage_range.minimum, Decimal('3.0'))
        self.assertEqual(ibis_file.models[0].voltage_range.maximum, Decimal('3.6'))

        self.assertEqual(len(ibis_file.models[0].gnd_clamp), 67)
        self.assertEqual(
            ibis_file.models[0].gnd_clamp[0],
            (Decimal('-3.30000'),
             Decimal('-11.46380'),
             Decimal('-11.71150'),
             Decimal('-11.40800')))
        self.assertEqual(
            ibis_file.models[0].gnd_clamp[66],
            (Decimal('3.30000'),
             Decimal('6.60800e-12'),
             Decimal('26.57000e-9'),
             Decimal('6.32380e-12')))

        self.assertEqual(len(ibis_file.models[0].power_clamp), 34)
        self.assertEqual(
            ibis_file.models[0].power_clamp[0],
            (Decimal('-3.30000'),
             Decimal('10.22730'),
             Decimal('10.48520'),
             Decimal('10.16810')))
        self.assertEqual(
            ibis_file.models[0].power_clamp[33],
            (Decimal('0.00000'),
             Decimal('6.59380e-12'),
             Decimal('10.90680e-12'),
             Decimal('7.23330e-12')))

        self.assertEqual(ibis_file.models[0].pullup, None)
        self.assertEqual(ibis_file.models[0].pulldown, None)
        self.assertEqual(ibis_file.models[0].ramp, None)
        self.assertEqual(ibis_file.models[0].falling_waveforms, [])
        self.assertEqual(ibis_file.models[0].rising_waveforms, [])

        # Last model.
        self.assertEqual(ibis_file.models[11].name, 'BT2Z50CX_PU50K')
        self.assertEqual(ibis_file.models[11].model_type, 'I/O')
        self.assertEqual(ibis_file.models[11].polarity, 'Non-Inverting')
        self.assertEqual(ibis_file.models[11].enable, 'Active-High')
        self.assertEqual(ibis_file.models[11].vinl, Decimal('0.8'))
        self.assertEqual(ibis_file.models[11].vinh, Decimal('2.0'))
        self.assertEqual(ibis_file.models[11].c_comp.typical, Decimal('1.26e-12'))
        self.assertEqual(ibis_file.models[11].c_comp.minimum, None)
        self.assertEqual(ibis_file.models[11].c_comp.maximum, None)
        self.assertEqual(ibis_file.models[11].vmeas, Decimal('1.65'))
        self.assertEqual(ibis_file.models[11].cref, Decimal('1.0e-12'))
        self.assertEqual(ibis_file.models[11].vref, Decimal('0'))
        self.assertEqual(ibis_file.models[11].rref, Decimal('1e6'))
        self.assertEqual(ibis_file.models[11].temperature_range.typical, Decimal('25'))
        self.assertEqual(ibis_file.models[11].temperature_range.minimum, Decimal('0'))
        self.assertEqual(ibis_file.models[11].temperature_range.maximum, Decimal('125'))
        self.assertEqual(ibis_file.models[11].voltage_range.typical, Decimal('3.3'))
        self.assertEqual(ibis_file.models[11].voltage_range.minimum, Decimal('3.0'))
        self.assertEqual(ibis_file.models[11].voltage_range.maximum, Decimal('3.6'))
        self.assertEqual(len(ibis_file.models[11].gnd_clamp), 35)
        self.assertEqual(len(ibis_file.models[11].power_clamp), 58)
        self.assertEqual(len(ibis_file.models[11].pullup), 100)
        self.assertEqual(len(ibis_file.models[11].pulldown), 100)
        self.assertEqual(ibis_file.models[11].ramp.dv_dt_r,
                         ((Decimal('0.950146'), Decimal('0.229176e-9')),
                          (Decimal('0.891184'), Decimal('0.260292e-9')),
                          (Decimal('1.0311'), Decimal('0.221583e-9'))))
        self.assertEqual(ibis_file.models[11].ramp.dv_dt_f,
                         ((Decimal('0.94062'), Decimal('0.319408e-9')),
                          (Decimal('0.89298'), Decimal('0.416034e-9')),
                          (Decimal('1.00716'), Decimal('0.284201e-9'))))
        self.assertEqual(ibis_file.models[11].ramp.r_load, Decimal('50'))

        # Falling waveforms.
        self.assertEqual(len(ibis_file.models[11].falling_waveforms), 2)

        waveform = ibis_file.models[11].falling_waveforms[0]
        self.assertEqual(waveform.r_fixture, Decimal('50'))
        self.assertEqual(waveform.v_fixture.typical, Decimal('3.3'))
        self.assertEqual(waveform.v_fixture.minimum, Decimal('3.0'))
        self.assertEqual(waveform.v_fixture.maximum, Decimal('3.6'))
        self.assertEqual(len(waveform.table.samples), 100)
        self.assertEqual(
            waveform.table.samples[0],
            (Decimal('0.00000'),
             Decimal('3.30000'),
             Decimal('3.00000'),
             Decimal('3.60000')))
        self.assertEqual(
            waveform.table.samples[99],
            (Decimal('1.50000e-9'),
             Decimal('1.73230'),
             Decimal('1.51170'),
             Decimal('1.92140')))
        waveform = ibis_file.models[11].falling_waveforms[1]
        self.assertEqual(len(waveform.table.samples), 100)
        self.assertEqual(
            waveform.table.samples[0],
            (Decimal('0.00000'),
             Decimal('1.59770'),
             Decimal('1.50670'),
             Decimal('1.73430')))
        self.assertEqual(
            waveform.table.samples[99],
            (Decimal('1.35000e-9'),
             Decimal('14.88300e-3'),
             Decimal('24.09000e-3'),
             Decimal('19.09910e-3')))

        # Rising waveforms.
        self.assertEqual(len(ibis_file.models[11].rising_waveforms), 2)

        waveform = ibis_file.models[11].rising_waveforms[0]
        self.assertEqual(waveform.r_fixture, Decimal('50'))
        self.assertEqual(waveform.v_fixture.typical, Decimal('0.000'))
        self.assertEqual(waveform.v_fixture.minimum, Decimal('0.000'))
        self.assertEqual(waveform.v_fixture.maximum, Decimal('0.000'))
        self.assertEqual(len(waveform.table.samples), 100)
        self.assertEqual(
            waveform.table.samples[0],
            (Decimal('0.00000'),
             Decimal('923.25950e-6'),
             Decimal('493.94600e-6'),
             Decimal('1.40550e-3')))
        self.assertEqual(
            waveform.table.samples[99],
            (Decimal('1.50000e-9'),
             Decimal('1.58450'),
             Decimal('1.48580'),
             Decimal('1.71990')))

    def test_convert_numerical(self):
        self.assertEqual(ibis.convert_numerical('1.1T'), Decimal('1.1e12'))
        self.assertEqual(ibis.convert_numerical('1.1G'), Decimal('1.1e9'))
        self.assertEqual(ibis.convert_numerical('1.1M'), Decimal('1.1e6'))
        self.assertEqual(ibis.convert_numerical('1.1k'), Decimal('1.1e3'))
        self.assertEqual(ibis.convert_numerical('1.1'),  Decimal('1.1'))
        self.assertEqual(ibis.convert_numerical('1.1m'), Decimal('1.1e-3'))
        self.assertEqual(ibis.convert_numerical('1.1u'), Decimal('1.1e-6'))
        self.assertEqual(ibis.convert_numerical('1.1n'), Decimal('1.1e-9'))
        self.assertEqual(ibis.convert_numerical('1.1p'), Decimal('1.1e-12'))
        self.assertEqual(ibis.convert_numerical('1.1f'), Decimal('1.1e-15'))
        self.assertEqual(ibis.convert_numerical('2.123E-5'), Decimal('0.00002123'))
        self.assertEqual(ibis.convert_numerical('2.123e5'), Decimal('2.123e5'))
        self.assertEqual(ibis.convert_numerical('2.123E+5'), Decimal('2.123e5'))
        self.assertEqual(ibis.convert_numerical('1.1Ohm'), Decimal('1.1'))
        self.assertEqual(ibis.convert_numerical('1.1kOhm'), Decimal('1.1e3'))
        self.assertEqual(ibis.convert_numerical('5.1e-3V'), Decimal('0.0051'))

    def test_split_numerical(self):
        self.assertEqual(ibis.split_numerical('1.1T'), ('1.1', 'T', ''))
        self.assertEqual(ibis.split_numerical('1.1G'), ('1.1', 'G', ''))
        self.assertEqual(ibis.split_numerical('1.1M'), ('1.1', 'M', ''))
        self.assertEqual(ibis.split_numerical('1.1k'), ('1.1', 'k', ''))
        self.assertEqual(ibis.split_numerical('1.1'),  ('1.1', '', ''))
        self.assertEqual(ibis.split_numerical('1.1m'), ('1.1', 'm', ''))
        self.assertEqual(ibis.split_numerical('1.1u'), ('1.1', 'u', ''))
        self.assertEqual(ibis.split_numerical('1.1n'), ('1.1', 'n', ''))
        self.assertEqual(ibis.split_numerical('1.1p'), ('1.1', 'p', ''))
        self.assertEqual(ibis.split_numerical('1.1f'), ('1.1', 'f', ''))
        self.assertEqual(ibis.split_numerical('2.123E-5'), ('2.123E-5', '', ''))
        self.assertEqual(ibis.split_numerical('2.123e5'), ('2.123e5', '', ''))
        self.assertEqual(ibis.split_numerical('2.123E+5'), ('2.123E+5', '', ''))
        self.assertEqual(ibis.split_numerical('1.1Ohm'), ('1.1', '', 'Ohm'))
        self.assertEqual(ibis.split_numerical('1.1kOhm'), ('1.1', 'k', 'Ohm'))
        self.assertEqual(ibis.split_numerical('5.1e-3V'), ('5.1e-3', '', 'V'))

    def test_get_model_selector_by_name(self):
        ibis_file = ibis.load_file('tests/files/ibis/pybis/sample1.ibs')

        model_selector = ibis_file.get_model_selector_by_name('BUSB6AU')
        self.assertEqual(model_selector.name, 'BUSB6AU')

        with self.assertRaises(ecdtools.ibis.Error) as cm:
            ibis_file.get_model_selector_by_name('Missing')

        self.assertEqual(
            str(cm.exception),
            'Expected model selector name BUSB6AU, but got Missing.')

    def test_get_model_by_name(self):
        ibis_file = ibis.load_file('tests/files/ibis/pybis/bushold.ibs')

        model = ibis_file.get_model_by_name('TOP_MODEL_BUS_HOLD')
        self.assertEqual(model.name, 'TOP_MODEL_BUS_HOLD')

        with self.assertRaises(ecdtools.ibis.Error) as cm:
            ibis_file.get_model_by_name('Missing')

        self.assertEqual(
            str(cm.exception),
            'Expected model name TOP_MODEL_BUS_HOLD, but got Missing.')

    def test_get_component_by_name(self):
        ibis_file = ibis.load_file('tests/files/ibis/pybis/bushold.ibs')

        component = ibis_file.get_component_by_name('BUS-HOLD-SAMPLE')
        self.assertEqual(component.name, 'BUS-HOLD-SAMPLE')

        with self.assertRaises(ecdtools.ibis.Error) as cm:
            ibis_file.get_component_by_name('Missing')

        self.assertEqual(
            str(cm.exception),
            'Expected component name BUS-HOLD-SAMPLE, but got Missing.')

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
