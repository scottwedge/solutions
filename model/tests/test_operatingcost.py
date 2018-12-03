"""Tests for operatingcost.py."""

import os

from model import advanced_controls
from model import operatingcost
import numpy as np
import pandas as pd
import pytest

csv_files_dir = os.path.dirname(__file__)

def test_soln_pds_annual_operating_cost():
  filename = os.path.join(csv_files_dir, 'oc_soln_pds_annual_breakout_expected.csv')
  breakout = pd.read_csv(filename, header=None, index_col=0, skipinitialspace=True, dtype=np.float64)
  breakout.columns = list(range(2015, 2061))
  breakout.index = breakout.index.astype(int)
  expected = pd.Series(soln_pds_annual_operating_cost_nparray[:, 1],
      index=soln_pds_annual_operating_cost_nparray[:, 0], dtype=np.float64)
  expected.index = expected.index.astype(int)
  oc = operatingcost.OperatingCost(ac=None)
  result = oc.soln_pds_annual_operating_cost(breakout)
  pd.testing.assert_series_equal(result, expected, check_exact=False, check_names=False)

def test_soln_pds_cumulative_operating_cost():
  soln_pds_annual_operating_cost = pd.Series(soln_pds_annual_operating_cost_nparray[:, 1],
      index=soln_pds_annual_operating_cost_nparray[:, 0], dtype=np.float64)
  soln_pds_annual_operating_cost.index = soln_pds_annual_operating_cost.index.astype(int)
  oc = operatingcost.OperatingCost(ac=None)
  result = oc.soln_pds_cumulative_operating_cost(soln_pds_annual_operating_cost)
  expected = pd.Series(soln_pds_cumulative_operating_cost_nparray[:, 1],
      index=soln_pds_cumulative_operating_cost_nparray[:, 0], dtype=np.float64)
  expected.index = expected.index.astype(int)
  pd.testing.assert_series_equal(result, expected, check_exact=False, check_names=False)

def test_conv_ref_annual_operating_cost():
  filename = os.path.join(csv_files_dir, 'oc_conv_ref_annual_breakout_expected.csv')
  breakout = pd.read_csv(filename, header=None, index_col=0, skipinitialspace=True, dtype=np.float64)
  breakout.columns = list(range(2015, 2061))
  breakout.index = breakout.index.astype(int)
  expected = pd.Series(conv_ref_annual_operating_cost_nparray[:, 1],
      index=conv_ref_annual_operating_cost_nparray[:, 0], dtype=np.float64)
  expected.index = expected.index.astype(int)
  oc = operatingcost.OperatingCost(ac=None)
  result = oc.conv_ref_annual_operating_cost(breakout).iloc[0:46]
  pd.testing.assert_series_equal(result, expected, check_exact=False, check_names=False)

def test_conv_ref_cumulative_operating_cost():
  conv_ref_annual_operating_cost = pd.Series(conv_ref_annual_operating_cost_nparray[:, 1],
      index=conv_ref_annual_operating_cost_nparray[:, 0], dtype=np.float64)
  conv_ref_annual_operating_cost.index = conv_ref_annual_operating_cost.index.astype(int)
  oc = operatingcost.OperatingCost(ac=None)
  result = oc.conv_ref_cumulative_operating_cost(conv_ref_annual_operating_cost)
  expected = pd.Series(conv_ref_cumulative_operating_cost_nparray[:, 1],
      index=conv_ref_cumulative_operating_cost_nparray[:, 0], dtype=np.float64)
  expected.index = expected.index.astype(int)
  pd.testing.assert_series_equal(result, expected, check_exact=False, check_names=False)

def test_marginal_annual_operating_cost():
  soln_pds_annual_operating_cost = pd.Series(soln_pds_annual_operating_cost_nparray[:, 1],
      index=soln_pds_annual_operating_cost_nparray[:, 0], dtype=np.float64)
  soln_pds_annual_operating_cost.index = soln_pds_annual_operating_cost.index.astype(int)
  conv_ref_annual_operating_cost = pd.Series(conv_ref_annual_operating_cost_nparray[:, 1],
      index=conv_ref_annual_operating_cost_nparray[:, 0], dtype=np.float64)
  conv_ref_annual_operating_cost.index = conv_ref_annual_operating_cost.index.astype(int)
  oc = operatingcost.OperatingCost(ac=None)
  result = oc.marginal_annual_operating_cost(
      soln_pds_annual_operating_cost=soln_pds_annual_operating_cost,
      conv_ref_annual_operating_cost=conv_ref_annual_operating_cost)
  expected = pd.Series(marginal_annual_operating_cost_nparray[:, 1],
      index=marginal_annual_operating_cost_nparray[:, 0], dtype=np.float64)
  expected.index = expected.index.astype(int)
  pd.testing.assert_series_equal(result, expected, check_exact=False, check_names=False)

def test_soln_new_funits_per_year():
  funits = [['Year', 'World', 'Other'], [2014, 1.0, 0.0], [2015, 3.0, 0.0], [2016, 4.0, 0.0],
      [2017, 8.0, 0.0], [2018, 12.0, 0.0], [2019, 12.0, 0.0], [2020, 20.0, 0.0]]
  soln_net_annual_funits_adopted = pd.DataFrame(funits[1:], columns=funits[0]).set_index('Year')
  v = np.array([[2014, 1.0, 0.0], [2015, 2.0, 0.0], [2016, 1.0, 0.0], [2017, 4.0, 0.0],
      [2018, 4.0, 0.0], [2019, 0.0, 0.0], [2020, 8.0, 0.0]])
  expected = pd.DataFrame(v[:, 1:], columns=['World', 'Other'], index=v[:, 0])
  expected.index = expected.index.map(int)
  oc = operatingcost.OperatingCost(ac=None)
  result = oc.soln_new_funits_per_year(soln_net_annual_funits_adopted)
  pd.testing.assert_frame_equal(result, expected, check_exact=False, check_names=False)

def test_soln_pds_net_annual_iunits_reqd():
  soln_pds_tot_iunits_reqd = pd.DataFrame(soln_pds_tot_iunits_reqd_list[1:],
      columns=soln_pds_tot_iunits_reqd_list[0]).set_index('Year')
  soln_ref_tot_iunits_reqd = pd.DataFrame(soln_ref_tot_iunits_reqd_list[1:],
      columns=soln_ref_tot_iunits_reqd_list[0]).set_index('Year')
  df = pd.DataFrame(soln_pds_net_annual_iunits_reqd_list[1:],
      columns=soln_pds_net_annual_iunits_reqd_list[0]).set_index('Year')
  expected = df['World']
  oc = operatingcost.OperatingCost(ac=None)
  result = oc.soln_pds_net_annual_iunits_reqd(
      soln_pds_tot_iunits_reqd=soln_pds_tot_iunits_reqd,
      soln_ref_tot_iunits_reqd=soln_ref_tot_iunits_reqd)
  pd.testing.assert_series_equal(result['World'], expected, check_exact=False)

def test_soln_pds_new_annual_iunits_reqd():
  soln_pds_net_annual_iunits_reqd = pd.DataFrame(
      soln_pds_net_annual_iunits_reqd_list[1:],
      columns=soln_pds_net_annual_iunits_reqd_list[0]).set_index('Year')
  expected = pd.DataFrame(soln_pds_new_annual_iunits_reqd_list[1:],
      columns=soln_pds_new_annual_iunits_reqd_list[0]).set_index('Year')
  expected.index = expected.index.map(int)
  oc = operatingcost.OperatingCost(ac=None)
  result = oc.soln_pds_new_annual_iunits_reqd(
      soln_pds_net_annual_iunits_reqd=soln_pds_net_annual_iunits_reqd)
  pd.testing.assert_frame_equal(result, expected, check_exact=False, check_names=False)

def test_soln_pds_annual_breakout():
  ac = advanced_controls.AdvancedControls(report_end_year=2050,
      soln_lifetime_capacity=48343.8, soln_avg_annual_use=1841.66857142857,
      soln_var_oper_cost_per_funit=0.0, soln_fuel_cost_per_funit=0.0,
      soln_fixed_oper_cost_per_iunit=23.18791293579)
  oc = operatingcost.OperatingCost(ac=ac)
  soln_new_funits_per_year = pd.DataFrame(soln_new_funits_per_year_list[1:],
      columns=soln_new_funits_per_year_list[0]).set_index('Year')
  soln_new_funits_per_year.index = soln_new_funits_per_year.index.map(int)
  soln_pds_new_annual_iunits_reqd = pd.DataFrame(soln_pds_new_annual_iunits_reqd_list[1:],
      columns=soln_pds_new_annual_iunits_reqd_list[0]).set_index('Year')
  soln_pds_new_annual_iunits_reqd.index = soln_pds_new_annual_iunits_reqd.index.map(int)
  result = oc.soln_pds_annual_breakout(
      soln_new_funits_per_year=soln_new_funits_per_year['World'],
      soln_pds_new_annual_iunits_reqd=soln_pds_new_annual_iunits_reqd['World'])
  filename = os.path.join(csv_files_dir, 'oc_soln_pds_annual_breakout_expected.csv')
  expected = pd.read_csv(filename, header=None, index_col=0, skipinitialspace=True, dtype=np.float64)
  expected.columns = list(range(2015, 2061))
  expected.index = expected.index.map(int)
  pd.testing.assert_frame_equal(result, expected, check_exact=False, check_names=False)

def test_conv_ref_new_annual_iunits_reqd():
  conv_ref_net_annual_iunits_reqd = pd.DataFrame(
      conv_ref_net_annual_iunits_reqd_list[1:],
      columns=conv_ref_net_annual_iunits_reqd_list[0]).set_index('Year')
  expected = pd.DataFrame(conv_ref_new_annual_iunits_reqd_list[1:],
      columns=conv_ref_new_annual_iunits_reqd_list[0]).set_index('Year')
  expected.index = expected.index.map(int)
  oc = operatingcost.OperatingCost(ac=None)
  result = oc.conv_ref_new_annual_iunits_reqd(
      conv_ref_net_annual_iunits_reqd=conv_ref_net_annual_iunits_reqd)
  pd.testing.assert_frame_equal(result, expected, check_exact=False, check_names=False)

def test_conv_ref_annual_breakout():
  ac = advanced_controls.AdvancedControls(report_end_year=2050,
      soln_lifetime_capacity=48343.8, soln_avg_annual_use=1841.66857142857,
      conv_var_oper_cost_per_funit=0.00375269040, conv_fuel_cost_per_funit=0.0731,
      conv_fixed_oper_cost_per_iunit=32.95140431108)
  oc = operatingcost.OperatingCost(ac=ac)
  soln_new_funits_per_year = pd.DataFrame(soln_new_funits_per_year_list[1:],
      columns=soln_new_funits_per_year_list[0]).set_index('Year')
  soln_new_funits_per_year.index = soln_new_funits_per_year.index.map(int)
  conv_ref_new_annual_iunits_reqd = pd.DataFrame(conv_ref_new_annual_iunits_reqd_list[1:],
      columns=conv_ref_new_annual_iunits_reqd_list[0]).set_index('Year')
  conv_ref_new_annual_iunits_reqd.index = conv_ref_new_annual_iunits_reqd.index.map(int)
  result = oc.conv_ref_annual_breakout(
      conv_new_funits_per_year=soln_new_funits_per_year['World'],
      conv_ref_new_annual_iunits_reqd=conv_ref_new_annual_iunits_reqd['World'])
  filename = os.path.join(csv_files_dir, 'oc_conv_ref_annual_breakout_expected.csv')
  expected = pd.read_csv(filename, header=None, index_col=0, skipinitialspace=True, dtype=np.float64)
  expected.columns = list(range(2015, 2061))
  expected.index = expected.index.map(int)
  pd.testing.assert_frame_equal(result, expected, check_exact=False, check_names=False)

def test_lifetime_cost_forecast():
  soln_ref_annual_world_first_cost = pd.Series(
      soln_ref_annual_world_first_cost_nparray[:, 1],
      index=soln_ref_annual_world_first_cost_nparray[:, 0], dtype=np.float64)
  soln_ref_annual_world_first_cost.index = soln_ref_annual_world_first_cost.index.astype(int)
  conv_ref_annual_world_first_cost = pd.Series(
      conv_ref_annual_world_first_cost_nparray[:, 1],
      index=conv_ref_annual_world_first_cost_nparray[:, 0], dtype=np.float64)
  conv_ref_annual_world_first_cost.index = conv_ref_annual_world_first_cost.index.astype(int)
  soln_pds_annual_world_first_cost = pd.Series(
      soln_pds_annual_world_first_cost_nparray[:, 1],
      index=soln_pds_annual_world_first_cost_nparray[:, 0], dtype=np.float64)
  soln_pds_annual_world_first_cost.index = soln_pds_annual_world_first_cost.index.astype(int)
  filename = os.path.join(csv_files_dir, 'oc_conv_ref_annual_breakout_expected.csv')
  conv_ref_annual_breakout = pd.read_csv(filename, header=None, index_col=0,
      skipinitialspace=True, dtype=np.float64)
  conv_ref_annual_breakout.columns = list(range(2015, 2061))
  conv_ref_annual_breakout.index = conv_ref_annual_breakout.index.map(int)
  filename = os.path.join(csv_files_dir, 'oc_soln_pds_annual_breakout_expected.csv')
  soln_pds_annual_breakout = pd.read_csv(filename, header=None, index_col=0,
      skipinitialspace=True, dtype=np.float64)
  soln_pds_annual_breakout.columns = list(range(2015, 2061))
  soln_pds_annual_breakout.index = soln_pds_annual_breakout.index.map(int)
  ac = advanced_controls.AdvancedControls(report_end_year=2050, npv_discount_rate=0.094)
  oc = operatingcost.OperatingCost(ac=ac)
  result = oc.lifetime_cost_forecast(
      soln_ref_annual_world_first_cost=soln_ref_annual_world_first_cost,
      conv_ref_annual_world_first_cost=conv_ref_annual_world_first_cost,
      soln_pds_annual_world_first_cost=soln_pds_annual_world_first_cost,
      conv_ref_annual_breakout=conv_ref_annual_breakout,
      soln_pds_annual_breakout=soln_pds_annual_breakout)
  expected = pd.DataFrame(lifetime_cost_forecast_list[1:],
      columns=lifetime_cost_forecast_list[0]).set_index('Year')
  pd.testing.assert_frame_equal(result, expected, check_exact=False, check_names=False)

def test_soln_vs_conv_single_iunit_cashflow():
  ac = advanced_controls.AdvancedControls(report_end_year=2050,
      soln_lifetime_capacity=48343.8, soln_avg_annual_use=1841.66857142857,
      conv_lifetime_capacity=182411.275767661, conv_avg_annual_use=4946.840187342,
      conv_var_oper_cost_per_funit=0.00375269040, conv_fuel_cost_per_funit=0.0731,
      conv_fixed_oper_cost_per_iunit=32.95140431108,
      soln_var_oper_cost_per_funit=0.0, soln_fuel_cost_per_funit=0.0,
      soln_fixed_oper_cost_per_iunit=23.18791293579)
  oc = operatingcost.OperatingCost(ac=ac)
  soln_pds_install_cost_per_iunit = pd.Series(soln_pds_install_cost_per_iunit_nparray[:, 1],
      index=soln_pds_install_cost_per_iunit_nparray[:, 0], dtype=np.float64)
  conv_ref_install_cost_per_iunit = pd.Series(conv_ref_install_cost_per_iunit_nparray[:, 1],
      index=conv_ref_install_cost_per_iunit_nparray[:, 0], dtype=np.float64)
  result = oc.soln_vs_conv_single_iunit_cashflow(single_iunit_purchase_year=2017,
      soln_pds_install_cost_per_iunit=soln_pds_install_cost_per_iunit,
      conv_ref_install_cost_per_iunit=conv_ref_install_cost_per_iunit)
  expected = pd.Series(soln_vs_conv_single_iunit_cashflow_nparray[:, 1],
      index=soln_vs_conv_single_iunit_cashflow_nparray[:, 0], dtype=np.float64)
  expected.index = expected.index.astype(int)
  pd.testing.assert_series_equal(result, expected, check_exact=False, check_names=False)

def test_soln_vs_conv_single_iunit_cashflow_purchase_year_2026():
  ac = advanced_controls.AdvancedControls(report_end_year=2050,
      soln_lifetime_capacity=48343.8, soln_avg_annual_use=1841.66857142857,
      conv_lifetime_capacity=182411.275767661, conv_avg_annual_use=4946.840187342,
      conv_var_oper_cost_per_funit=0.00375269040, conv_fuel_cost_per_funit=0.0731,
      conv_fixed_oper_cost_per_iunit=32.95140431108,
      soln_var_oper_cost_per_funit=0.0, soln_fuel_cost_per_funit=0.0,
      soln_fixed_oper_cost_per_iunit=23.18791293579)
  oc = operatingcost.OperatingCost(ac=ac)
  soln_pds_install_cost_per_iunit = pd.Series(soln_pds_install_cost_per_iunit_nparray[:, 1],
      index=soln_pds_install_cost_per_iunit_nparray[:, 0], dtype=np.float64)
  conv_ref_install_cost_per_iunit = pd.Series(conv_ref_install_cost_per_iunit_nparray[:, 1],
      index=conv_ref_install_cost_per_iunit_nparray[:, 0], dtype=np.float64)
  result = oc.soln_vs_conv_single_iunit_cashflow(single_iunit_purchase_year=2026,
      soln_pds_install_cost_per_iunit=soln_pds_install_cost_per_iunit,
      conv_ref_install_cost_per_iunit=conv_ref_install_cost_per_iunit)
  assert result[2015] == pytest.approx(-18487649169)
  assert result[2016] == pytest.approx(130616812789)

def test_soln_vs_conv_single_iunit_npv():
  ac = advanced_controls.AdvancedControls(npv_discount_rate=0.094)
  oc = operatingcost.OperatingCost(ac=ac)
  soln_vs_conv_single_iunit_cashflow = pd.Series(soln_vs_conv_single_iunit_cashflow_nparray[:, 1],
      index=soln_vs_conv_single_iunit_cashflow_nparray[:, 0], dtype=np.float64)
  soln_vs_conv_single_iunit_cashflow.index = soln_vs_conv_single_iunit_cashflow.index.astype(int)
  result = oc.soln_vs_conv_single_iunit_npv(single_iunit_purchase_year=2017,
      soln_vs_conv_single_iunit_cashflow=soln_vs_conv_single_iunit_cashflow)
  expected = pd.Series(soln_vs_conv_single_iunit_npv_nparray[:, 1],
      index=soln_vs_conv_single_iunit_npv_nparray[:, 0], dtype=np.float64)
  expected.index = expected.index.astype(int)
  pd.testing.assert_series_equal(result, expected, check_exact=False, check_names=False)

def test_soln_vs_conv_single_iunit_npv_purchase_year_discount_rate():
  ac = advanced_controls.AdvancedControls(npv_discount_rate=0.071)
  oc = operatingcost.OperatingCost(ac=ac)
  soln_vs_conv_single_iunit_cashflow = pd.Series(soln_vs_conv_single_iunit_cashflow_nparray[:, 1],
      index=soln_vs_conv_single_iunit_cashflow_nparray[:, 0], dtype=np.float64)
  result = oc.soln_vs_conv_single_iunit_npv(single_iunit_purchase_year=2025,
      soln_vs_conv_single_iunit_cashflow=soln_vs_conv_single_iunit_cashflow)
  expected = pd.Series(soln_vs_conv_single_iunit_npv_purchase_year_discount_rate_nparray[:, 1],
      index=soln_vs_conv_single_iunit_npv_purchase_year_discount_rate_nparray[:, 0], dtype=np.float64)
  expected.index = expected.index.astype(int)
  pd.testing.assert_series_equal(result, expected, check_exact=False, check_names=False)

def test_soln_vs_conv_single_iunit_payback():
  oc = operatingcost.OperatingCost(ac=None)
  soln_vs_conv_single_iunit_cashflow = pd.Series(soln_vs_conv_single_iunit_cashflow_nparray[:, 1],
      index=soln_vs_conv_single_iunit_cashflow_nparray[:, 0], dtype=np.float64)
  soln_vs_conv_single_iunit_cashflow.index = soln_vs_conv_single_iunit_cashflow.index.astype(int)
  result = oc.soln_vs_conv_single_iunit_payback(soln_vs_conv_single_iunit_cashflow)
  expected = pd.Series(soln_vs_conv_single_iunit_payback_nparray[:, 1],
      index=soln_vs_conv_single_iunit_payback_nparray[:, 0], dtype=np.int64)
  expected.index = expected.index.astype(int)
  pd.testing.assert_series_equal(result, expected, check_exact=False, check_names=False)

def test_soln_vs_conv_single_iunit_payback_discounted():
  oc = operatingcost.OperatingCost(ac=None)
  soln_vs_conv_single_iunit_npv = pd.Series(soln_vs_conv_single_iunit_npv_nparray[:, 1],
      index=soln_vs_conv_single_iunit_npv_nparray[:, 0], dtype=np.float64)
  soln_vs_conv_single_iunit_npv.index = soln_vs_conv_single_iunit_npv.index.astype(int)
  result = oc.soln_vs_conv_single_iunit_payback_discounted(soln_vs_conv_single_iunit_npv)
  expected = pd.Series(soln_vs_conv_single_iunit_payback_discounted_nparray[:, 1],
      index=soln_vs_conv_single_iunit_payback_discounted_nparray[:, 0], dtype=np.int64)
  expected.index = expected.index.astype(int)
  pd.testing.assert_series_equal(result, expected, check_exact=False, check_names=False)

def test_soln_only_single_iunit_cashflow():
  ac = advanced_controls.AdvancedControls(report_end_year=2050,
      soln_lifetime_capacity=48343.8, soln_avg_annual_use=1841.66857142857,
      conv_avg_annual_use=4946.840187342,
      conv_var_oper_cost_per_funit=0.00375269040, conv_fuel_cost_per_funit=0.0731,
      conv_fixed_oper_cost_per_iunit=32.95140431108,
      soln_var_oper_cost_per_funit=0.0, soln_fuel_cost_per_funit=0.0,
      soln_fixed_oper_cost_per_iunit=23.18791293579)
  oc = operatingcost.OperatingCost(ac=ac)
  soln_pds_install_cost_per_iunit = pd.Series(soln_pds_install_cost_per_iunit_nparray[:, 1],
      index=soln_pds_install_cost_per_iunit_nparray[:, 0], dtype=np.float64)
  result = oc.soln_only_single_iunit_cashflow(single_iunit_purchase_year=2017,
      soln_pds_install_cost_per_iunit=soln_pds_install_cost_per_iunit)
  expected = pd.Series(soln_only_single_iunit_cashflow_nparray[:, 1],
      index=soln_only_single_iunit_cashflow_nparray[:, 0], dtype=np.float64)
  expected.index = expected.index.astype(int)
  pd.testing.assert_series_equal(result, expected, check_exact=False, check_names=False)

def test_soln_only_single_iunit_npv():
  ac = advanced_controls.AdvancedControls(npv_discount_rate=0.094)
  oc = operatingcost.OperatingCost(ac=ac)
  soln_only_single_iunit_cashflow = pd.Series(soln_only_single_iunit_cashflow_nparray[:, 1],
      index=soln_only_single_iunit_cashflow_nparray[:, 0], dtype=np.float64)
  soln_only_single_iunit_cashflow.index = soln_only_single_iunit_cashflow.index.astype(int)
  result = oc.soln_only_single_iunit_npv(single_iunit_purchase_year=2017,
      soln_only_single_iunit_cashflow=soln_only_single_iunit_cashflow)
  expected = pd.Series(soln_only_single_iunit_npv_nparray[:, 1],
      index=soln_only_single_iunit_npv_nparray[:, 0], dtype=np.float64)
  expected.index = expected.index.astype(int)
  pd.testing.assert_series_equal(result, expected, check_exact=False, check_names=False)

def test_soln_only_single_iunit_payback():
  oc = operatingcost.OperatingCost(ac=None)
  soln_only_single_iunit_cashflow = pd.Series(soln_only_single_iunit_cashflow_nparray[:, 1],
      index=soln_only_single_iunit_cashflow_nparray[:, 0], dtype=np.float64)
  soln_only_single_iunit_cashflow.index = soln_only_single_iunit_cashflow.index.astype(int)
  result = oc.soln_only_single_iunit_payback(soln_only_single_iunit_cashflow)
  expected = pd.Series(soln_only_single_iunit_payback_nparray[:, 1],
      index=soln_only_single_iunit_payback_nparray[:, 0], dtype=np.int64)
  expected.index = expected.index.astype(int)
  pd.testing.assert_series_equal(result, expected, check_exact=False, check_names=False)

def test_soln_only_single_iunit_payback_discounted():
  oc = operatingcost.OperatingCost(ac=None)
  soln_only_single_iunit_npv = pd.Series(soln_only_single_iunit_npv_nparray[:, 1],
      index=soln_only_single_iunit_npv_nparray[:, 0], dtype=np.float64)
  soln_only_single_iunit_npv.index = soln_only_single_iunit_npv.index.astype(int)
  result = oc.soln_only_single_iunit_payback_discounted(soln_only_single_iunit_npv)
  expected = pd.Series(soln_only_single_iunit_payback_discounted_nparray[:, 1],
      index=soln_only_single_iunit_payback_discounted_nparray[:, 0], dtype=np.int64)
  expected.index = expected.index.astype(int)
  pd.testing.assert_series_equal(result, expected, check_exact=False, check_names=False)


soln_pds_tot_iunits_reqd_list = [["Year", "World", "OECD90", "Eastern Europe", "Asia (Sans Japan)", "Middle East and Africa", "Latin America", "China", "India", "EU", "USA"],
    [2014, 0.06115814489, 0.04072624506, 0.00018047945, 0.01144207203, 0.00085524497, 0.00795507895, 0.00812970502, 0.00149228865, 0.03001194422, 0.00712649942],
    [2015, 0.09569632876, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2016, 0.14770917868, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2017, 0.20813155943, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2018, 0.27658585364, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2019, 0.35269444391, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2020, 0.35511275489, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2021, 0.52636404313, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2022, 0.62316981729, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2023, 0.72611941799, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2024, 0.83483522783, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2025, 0.86627964703, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2026, 1.06805500539, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2027, 1.19180373834, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2028, 1.31980821089, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2029, 1.45169080567, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2030, 1.65078562298, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2031, 1.72557989233, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2032, 1.86683114944, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2033, 2.01045005923, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2034, 2.15605900432, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2035, 2.30328036731, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2036, 2.45173653082, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2037, 2.60104987747, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2038, 2.75084278988, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2039, 2.90073765065, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2040, 3.07612351532, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2041, 3.19932274775, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2042, 3.34725774931, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2043, 3.49378422970, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2044, 3.63852457153, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2045, 3.78110115742, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2046, 3.92113636998, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2047, 4.05825259183, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2048, 4.19207220558, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2049, 4.32221759385, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2050, 4.43499993794, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2051, 4.56997522439, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2052, 4.68683223190, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2053, 4.79850454439, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2054, 4.90461454447, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2055, 5.00478461475, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2056, 5.09863713786, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2057, 5.18579449640, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2058, 5.26587907300, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2059, 5.33851325027, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2060, 5.40331941081, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

soln_ref_tot_iunits_reqd_list = [
    ["Year", "World", "OECD90", "Eastern Europe", "Asia (Sans Japan)", "Middle East and Africa", "Latin America", "China", "India", "EU", "USA"],
    [2014, 0.06115814489, 0.04072624506, 0.00018047945, 0.01144207203, 0.00085524497, 0.00795507895, 0.00812970502, 0.00149228865, 0.03001194422, 0.00712649942],
    [2015, 0.06356811321, 0.04106406734, 0.00018335632, 0.01203213720, 0.00092855523, 0.00837129114, 0.00837997582, 0.00166702867, 0.03027672478, 0.00717613125],
    [2016, 0.06597808152, 0.04140188962, 0.00018623318, 0.01262220236, 0.00100186550, 0.00878750333, 0.00863024663, 0.00184176869, 0.03054150533, 0.00722576309],
    [2017, 0.06838804984, 0.04173971190, 0.00018911004, 0.01321226753, 0.00107517577, 0.00920371553, 0.00888051744, 0.00201650870, 0.03080628588, 0.00727539492],
    [2018, 0.07079801816, 0.04207753419, 0.00019198691, 0.01380233270, 0.00114848604, 0.00961992772, 0.00913078824, 0.00219124872, 0.03107106643, 0.00732502676],
    [2019, 0.07320798648, 0.04241535647, 0.00019486377, 0.01439239787, 0.00122179630, 0.01003613991, 0.00938105905, 0.00236598874, 0.03133584698, 0.00737465859],
    [2020, 0.07561795479, 0.04275317875, 0.00019774064, 0.01498246304, 0.00129510657, 0.01045235210, 0.00963132986, 0.00254072876, 0.03160062754, 0.00742429043],
    [2021, 0.07802792311, 0.04309100103, 0.00020061750, 0.01557252821, 0.00136841684, 0.01086856429, 0.00988160066, 0.00271546877, 0.03186540809, 0.00747392226],
    [2022, 0.08043789143, 0.04342882332, 0.00020349436, 0.01616259338, 0.00144172710, 0.01128477648, 0.01013187147, 0.00289020879, 0.03213018864, 0.00752355410],
    [2023, 0.08284785974, 0.04376664560, 0.00020637123, 0.01675265855, 0.00151503737, 0.01170098867, 0.01038214228, 0.00306494881, 0.03239496919, 0.00757318593],
    [2024, 0.08525782806, 0.04410446788, 0.00020924809, 0.01734272372, 0.00158834764, 0.01211720086, 0.01063241308, 0.00323968882, 0.03265974974, 0.00762281777],
    [2025, 0.08766779638, 0.04444229016, 0.00021212496, 0.01793278889, 0.00166165791, 0.01253341305, 0.01088268389, 0.00341442884, 0.03292453030, 0.00767244960],
    [2026, 0.09007776469, 0.04478011245, 0.00021500182, 0.01852285405, 0.00173496817, 0.01294962525, 0.01113295470, 0.00358916886, 0.03318931085, 0.00772208144],
    [2027, 0.09248773301, 0.04511793473, 0.00021787869, 0.01911291922, 0.00180827844, 0.01336583744, 0.01138322550, 0.00376390887, 0.03345409140, 0.00777171327],
    [2028, 0.09489770133, 0.04545575701, 0.00022075555, 0.01970298439, 0.00188158871, 0.01378204963, 0.01163349631, 0.00393864889, 0.03371887195, 0.00782134511],
    [2029, 0.09730766964, 0.04579357929, 0.00022363241, 0.02029304956, 0.00195489897, 0.01419826182, 0.01188376712, 0.00411338891, 0.03398365250, 0.00787097694],
    [2030, 0.09971763796, 0.04613140157, 0.00022650928, 0.02088311473, 0.00202820924, 0.01461447401, 0.01213403792, 0.00428812893, 0.03424843305, 0.00792060878],
    [2031, 0.10212760628, 0.04646922386, 0.00022938614, 0.02147317990, 0.00210151951, 0.01503068620, 0.01238430873, 0.00446286894, 0.03451321361, 0.00797024061],
    [2032, 0.10453757459, 0.04680704614, 0.00023226301, 0.02206324507, 0.00217482978, 0.01544689839, 0.01263457954, 0.00463760896, 0.03477799416, 0.00801987244],
    [2033, 0.10694754291, 0.04714486842, 0.00023513987, 0.02265331024, 0.00224814004, 0.01586311058, 0.01288485034, 0.00481234898, 0.03504277471, 0.00806950428],
    [2034, 0.10935751123, 0.04748269070, 0.00023801673, 0.02324337541, 0.00232145031, 0.01627932278, 0.01313512115, 0.00498708899, 0.03530755526, 0.00811913611],
    [2035, 0.11176747954, 0.04782051299, 0.00024089360, 0.02383344057, 0.00239476058, 0.01669553497, 0.01338539196, 0.00516182901, 0.03557233581, 0.00816876795],
    [2036, 0.11417744786, 0.04815833527, 0.00024377046, 0.02442350574, 0.00246807084, 0.01711174716, 0.01363566276, 0.00533656903, 0.03583711637, 0.00821839978],
    [2037, 0.11658741618, 0.04849615755, 0.00024664733, 0.02501357091, 0.00254138111, 0.01752795935, 0.01388593357, 0.00551130905, 0.03610189692, 0.00826803162],
    [2038, 0.11899738449, 0.04883397983, 0.00024952419, 0.02560363608, 0.00261469138, 0.01794417154, 0.01413620438, 0.00568604906, 0.03636667747, 0.00831766345],
    [2039, 0.12140735281, 0.04917180212, 0.00025240106, 0.02619370125, 0.00268800165, 0.01836038373, 0.01438647518, 0.00586078908, 0.03663145802, 0.00836729529],
    [2040, 0.12381732113, 0.04950962440, 0.00025527792, 0.02678376642, 0.00276131191, 0.01877659592, 0.01463674599, 0.00603552910, 0.03689623857, 0.00841692712],
    [2041, 0.12622728944, 0.04984744668, 0.00025815478, 0.02737383159, 0.00283462218, 0.01919280811, 0.01488701680, 0.00621026911, 0.03716101913, 0.00846655896],
    [2042, 0.12863725776, 0.05018526896, 0.00026103165, 0.02796389676, 0.00290793245, 0.01960902030, 0.01513728760, 0.00638500913, 0.03742579968, 0.00851619079],
    [2043, 0.13104722608, 0.05052309124, 0.00026390851, 0.02855396193, 0.00298124271, 0.02002523250, 0.01538755841, 0.00655974915, 0.03769058023, 0.00856582263],
    [2044, 0.13345719439, 0.05086091353, 0.00026678538, 0.02914402709, 0.00305455298, 0.02044144469, 0.01563782922, 0.00673448917, 0.03795536078, 0.00861545446],
    [2045, 0.13586716271, 0.05119873581, 0.00026966224, 0.02973409226, 0.00312786325, 0.02085765688, 0.01588810002, 0.00690922918, 0.03822014133, 0.00866508630],
    [2046, 0.13827713103, 0.05153655809, 0.00027253911, 0.03032415743, 0.00320117352, 0.02127386907, 0.01613837083, 0.00708396920, 0.03848492189, 0.00871471813],
    [2047, 0.14068709935, 0.05187438037, 0.00027541597, 0.03091422260, 0.00327448378, 0.02169008126, 0.01638864163, 0.00725870922, 0.03874970244, 0.00876434997],
    [2048, 0.14309706766, 0.05221220266, 0.00027829283, 0.03150428777, 0.00334779405, 0.02210629345, 0.01663891244, 0.00743344923, 0.03901448299, 0.00881398180],
    [2049, 0.14550703598, 0.05255002494, 0.00028116970, 0.03209435294, 0.00342110432, 0.02252250564, 0.01688918325, 0.00760818925, 0.03927926354, 0.00886361364],
    [2050, 0.14791700430, 0.05288784722, 0.00028404656, 0.03268441811, 0.00349441458, 0.02293871783, 0.01713945405, 0.00778292927, 0.03954404409, 0.00891324547],
    [2051, 0.15032697261, 0.05322566950, 0.00028692343, 0.03327448328, 0.00356772485, 0.02335493002, 0.01738972486, 0.00795766928, 0.03980882465, 0.00896287731],
    [2052, 0.15273694093, 0.05356349178, 0.00028980029, 0.03386454845, 0.00364103512, 0.02377114222, 0.01763999567, 0.00813240930, 0.04007360520, 0.00901250914],
    [2053, 0.15514690925, 0.05390131407, 0.00029267715, 0.03445461361, 0.00371434539, 0.02418735441, 0.01789026647, 0.00830714932, 0.04033838575, 0.00906214098],
    [2054, 0.15755687756, 0.05423913635, 0.00029555402, 0.03504467878, 0.00378765565, 0.02460356660, 0.01814053728, 0.00848188934, 0.04060316630, 0.00911177281],
    [2055, 0.15996684588, 0.05457695863, 0.00029843088, 0.03563474395, 0.00386096592, 0.02501977879, 0.01839080809, 0.00865662935, 0.04086794685, 0.00916140465],
    [2056, 0.16237681420, 0.05491478091, 0.00030130775, 0.03622480912, 0.00393427619, 0.02543599098, 0.01864107889, 0.00883136937, 0.04113272741, 0.00921103648],
    [2057, 0.16478678251, 0.05525260320, 0.00030418461, 0.03681487429, 0.00400758645, 0.02585220317, 0.01889134970, 0.00900610939, 0.04139750796, 0.00926066832],
    [2058, 0.16719675083, 0.05559042548, 0.00030706148, 0.03740493946, 0.00408089672, 0.02626841536, 0.01914162051, 0.00918084940, 0.04166228851, 0.00931030015],
    [2059, 0.16960671915, 0.05592824776, 0.00030993834, 0.03799500463, 0.00415420699, 0.02668462755, 0.01939189131, 0.00935558942, 0.04192706906, 0.00935993199],
    [2060, 0.17201668746, 0.05626607004, 0.00031281520, 0.03858506980, 0.00422751726, 0.02710083975, 0.01964216212, 0.00953032944, 0.04219184961, 0.00940956382]]

# 'Operating Cost'!I531:I576
soln_pds_net_annual_iunits_reqd_list = [
    ['Year', 'World'],
    [2014, 0],
    [2015, 0.03212821555], [2016, 0.08173109715], [2017, 0.13974350959], [2018, 0.20578783548],
    [2019, 0.27948645744], [2020, 0.27949480010], [2021, 0.44833612002], [2022, 0.54273192587],
    [2023, 0.64327155825], [2024, 0.74957739977], [2025, 0.77861185065], [2026, 0.97797724069],
    [2027, 1.09931600533], [2028, 1.22491050957], [2029, 1.35438313602], [2030, 1.55106798502],
    [2031, 1.62345228605], [2032, 1.76229357485], [2033, 1.90350251632], [2034, 2.04670149309],
    [2035, 2.19151288776], [2036, 2.33755908296], [2037, 2.48446246130], [2038, 2.63184540538],
    [2039, 2.77933029784], [2040, 2.95230619419], [2041, 3.07309545830], [2042, 3.21862049155],
    [2043, 3.36273700362], [2044, 3.50506737714], [2045, 3.64523399471], [2046, 3.78285923895],
    [2047, 3.91756549248], [2048, 4.04897513792], [2049, 4.17671055787], [2050, 4.28708293365],
    [2051, 4.41964825178], [2052, 4.53409529097], [2053, 4.64335763514], [2054, 4.74705766690],
    [2055, 4.84481776887], [2056, 4.93626032366], [2057, 5.02100771389], [2058, 5.09868232217],
    [2059, 5.16890653112], [2060, 5.23130272335]]

# 'Operating Cost'!K531:K576
soln_pds_new_annual_iunits_reqd_list = [
    ['Year', 'World'],
    [2015,  0.03212821555], [2016,  0.04960288160], [2017,  0.05801241244], [2018,  0.06604432589],
    [2019,  0.07369862196], [2020,  0.00000834266], [2021,  0.16884131992], [2022,  0.09439580585],
    [2023,  0.10053963238], [2024,  0.10630584152], [2025,  0.02903445089], [2026,  0.19936539004],
    [2027,  0.12133876464], [2028,  0.12559450424], [2029,  0.12947262646], [2030,  0.19668484899],
    [2031,  0.07238430103], [2032,  0.13884128880], [2033,  0.14120894148], [2034,  0.14319897677],
    [2035,  0.14481139467], [2036,  0.14604619520], [2037,  0.14690337833], [2038,  0.14738294409],
    [2039,  0.14748489245], [2040,  0.17297589636], [2041,  0.12078926411], [2042,  0.14552503325],
    [2043,  0.14411651207], [2044,  0.14233037351], [2045,  0.14016661757], [2046,  0.13762524424],
    [2047,  0.13470625353], [2048,  0.13140964543], [2049,  0.12773541995], [2050,  0.11037237578],
    [2051,  0.13256531813], [2052,  0.11444703919], [2053,  0.10926234417], [2054,  0.10370003176],
    [2055,  0.09776010197], [2056,  0.09144255479], [2057,  0.08474739023], [2058,  0.07767460828],
    [2059,  0.07022420895], [2060,  0.06239619223]]

# 'Operating Cost'!F19:F64
soln_new_funits_per_year_list = [
    ['Year', 'World'],
    [2015, 59.16952483163], [2016, 91.35206809813], [2017, 106.83963674163], [2018, 121.63175931515],
    [2019, 135.72843581868], [2020, 0.01536441848], [2021, 310.94975244954], [2022, 173.84578890937],
    [2023, 185.16068113296], [2024, 195.78012728656], [2025, 53.47183568578], [2026, 367.16497306821],
    [2027, 223.46578932746], [2028, 231.30345120112], [2029, 238.44566700479], [2030, 362.22830486262],
    [2031, 133.30789227804], [2032, 255.69963799590], [2033, 260.06006951964], [2034, 263.72505497338],
    [2035, 266.69459435714], [2036, 268.96868767092], [2037, 270.54733491470], [2038, 271.43053608851],
    [2039, 271.61829119232], [2040, 318.56427193785], [2041, 222.45379147831], [2042, 268.00888008386],
    [2043, 265.41485090774], [2044, 262.12537566162], [2045, 258.14045434553], [2046, 253.46008695944],
    [2047, 248.08427350337], [2048, 242.01301397732], [2049, 235.24630838128], [2050, 203.26933562993],
    [2051, 244.14138006456], [2052, 210.77351517324], [2053, 201.22502529726], [2054, 190.98108935129],
    [2055, 180.04170733533], [2056, 168.40687924939], [2057, 156.07660509346], [2058, 143.05088486755],
    [2059, 129.32971857165], [2060, 114.91310620577]]

# 'Operating Cost'!J531:J576
conv_ref_net_annual_iunits_reqd_list = [
    ['Year', 'World'],
    [2014, 0],
    [2015, 0.01196107466], [2016, 0.03042782609], [2017, 0.05202537780], [2018, 0.07661314589],
    [2019, 0.10405054647], [2020, 0.10405365238], [2021, 0.16691190950], [2022, 0.20205470416],
    [2023, 0.23948479572], [2024, 0.27906160028], [2025, 0.28987089139], [2026, 0.36409301282],
    [2027, 0.40926645301], [2028, 0.45602427062], [2029, 0.50422588174], [2030, 0.57745005943],
    [2031, 0.60439814896], [2032, 0.65608763726], [2033, 0.70865858350], [2034, 0.76197040377],
    [2035, 0.81588251418], [2036, 0.87025433083], [2037, 0.92494526982], [2038, 0.97981474727],
    [2039, 1.03472217927], [2040, 1.09911970575], [2041, 1.14408857134], [2042, 1.19826636361],
    [2043, 1.25191977485], [2044, 1.30490822116], [2045, 1.35709111864], [2046, 1.40832788339],
    [2047, 1.45847793153], [2048, 1.50740067914], [2049, 1.55495554234], [2050, 1.59604628470],
    [2051, 1.64539927991], [2052, 1.68800698648], [2053, 1.72868447306], [2054, 1.76729115573],
    [2055, 1.80368645061], [2056, 1.83772977379], [2057, 1.86928054139], [2058, 1.89819816950],
    [2059, 1.92434207423], [2060, 1.94757167168]]

# 'Operating Cost'!L531:L576
conv_ref_new_annual_iunits_reqd_list = [
    ['Year', 'World'],
    [2015, 0.01196107466], [2016, 0.01846675143], [2017, 0.02159755171], [2018, 0.02458776809],
    [2019, 0.02743740058], [2020, 0.00000310591], [2021, 0.06285825712], [2022, 0.03514279466],
    [2023, 0.03743009156], [2024, 0.03957680456], [2025, 0.01080929112], [2026, 0.07422212143],
    [2027, 0.04517344019], [2028, 0.04675781761], [2029, 0.04820161112], [2030, 0.07322417769],
    [2031, 0.02694808953], [2032, 0.05168948830], [2033, 0.05257094623], [2034, 0.05331182027],
    [2035, 0.05391211041], [2036, 0.05437181665], [2037, 0.05469093900], [2038, 0.05486947745],
    [2039, 0.05490743200], [2040, 0.06439752648], [2041, 0.04496886559], [2042, 0.05417779227],
    [2043, 0.05365341124], [2044, 0.05298844631], [2045, 0.05218289748], [2046, 0.05123676476],
    [2047, 0.05015004813], [2048, 0.04892274762], [2049, 0.04755486320], [2050, 0.04109074236],
    [2051, 0.04935299521], [2052, 0.04260770657], [2053, 0.04067748657], [2054, 0.03860668267],
    [2055, 0.03639529488], [2056, 0.03404332319], [2057, 0.03155076760], [2058, 0.02891762811],
    [2059, 0.02614390473], [2060, 0.02322959745]]

# "First Cost"!N37:N82
soln_ref_annual_world_first_cost_nparray = np.array([
    [2015, 3482258521.23], [2016, 3441663232.15], [2017, 3402972628.78],
    [2018, 3366034802.32], [2019, 3330714616.02], [2020, 3296891372.34],
    [2021, 3264456867.37], [2022, 3233313758.36], [2023, 3203374186.30],
    [2024, 3174558607.50], [2025, 3146794797.63], [2026, 3120016998.66],
    [2027, 3094165185.10], [2028, 3069184430.14], [2029, 3045024356.02],
    [2030, 3021638655.52], [2031, 2998984674.03], [2032, 2977023043.26],
    [2033, 2955717359.14], [2034, 2935033897.73], [2035, 2914941363.96],
    [2036, 2895410668.80], [2037, 2876414731.01], [2038, 2857928300.45],
    [2039, 2839927800.15], [2040, 2822391184.80], [2041, 2805297813.74],
    [2042, 5577256673.28], [2043, 5544729180.90], [2044, 5512979012.60],
    [2045, 5481974050.47], [2046, 5451684043.61], [2047, 5422080469.25],
    [2048, 5393136406.46], [2049, 5364826421.01], [2050, 5337126460.22],
    [2051, 5310013756.86], [2052, 5283466741.19], [2053, 5257464960.18],
    [2054, 5231989003.48], [2055, 5207020435.23], [2056, 5182541731.37],
    [2057, 5158536221.77], [2058, 5134988036.86], [2059, 5111882058.30],
    [2060, 5089203873.37]])

# "First Cost"!Q37:Q82
conv_ref_annual_world_first_cost_nparray = np.array([
    [2015, 23990922121.35], [2016, 37002006377.58], [2017, 43232696345.06],
    [2018, 49171554733.95], [2019, 54819860759.44], [2020, 6200056.19],
    [2021, 125370011265.80], [2022, 70032952058.20], [2023, 74530163079.95],
    [2024, 78742031667.77], [2025, 21489531621.24], [2026, 147446884706.03],
    [2027, 89673911197.87], [2028, 92752512230.40], [2029, 95549609205.27],
    [2030, 145052369536.31], [2031, 53346752937.10], [2032, 102258245318.98],
    [2033, 103935548708.06], [2034, 105334320183.91], [2035, 106455077787.31],
    [2036, 107298318307.97], [2037, 107864518760.06], [2038, 108154137726.00],
    [2039, 108167616582.81], [2040, 126792530383.75], [2041, 88491006611.85],
    [2042, 106555391090.20], [2043, 105468416516.60], [2044, 104107286794.25],
    [2045, 102472360643.17], [2046, 100563985754.45], [2047, 98382499420.65],
    [2048, 95928229120.13], [2049, 93201493059.41], [2050, 80494723496.87],
    [2051, 96635227949.86], [2052, 83389543648.21], [2053, 102974994195.43],
    [2054, 111601197813.73], [2055, 113349350213.04], [2056, 114547319830.92],
    [2057, 115195820046.09], [2058, 56454480248.00], [2059, 173663804562.34],
    [2060, 113851352078.09], [2061, 426814950937.32], [2062, 404399835480.80],
    [2063, 381838361372.37], [2064, 359188607950.38], [2065, 336508654553.14],
    [2066, 310884303472.73], [2067, 287828970480.61], [2068, 260112337712.87],
    [2069, 229616507406.10], [2070, 198116487900.99], [2071, 165728437874.21],
    [2072, 138795066384.77], [2073, 104979431344.61], [2074, 64397691430.40],
    [2075, 29619106083.51], [2076, 4243948246.16],
    [2077, 0.0], [2078, 0.0], [2079, 0.0], [2080, 0.0], [2081, 0.0], [2082, 0.0],
    [2083, 0.0], [2084, 0.0], [2085, 0.0], [2086, 0.0], [2087, 0.0], [2088, 0.0],
    [2089, 0.0], [2090, 0.0], [2091, 0.0], [2092, 0.0], [2093, 0.0], [2094, 0.0],
    [2095, 0.0], [2096, 0.0], [2097, 0.0], [2098, 0.0], [2099, 0.0], [2100, 0.0],
    [2101, 0.0], [2102, 0.0], [2103, 0.0], [2104, 0.0], [2105, 0.0], [2106, 0.0],
    [2107, 0.0], [2108, 0.0], [2109, 0.0], [2110, 0.0], [2111, 0.0], [2112, 0.0],
    [2113, 0.0], [2114, 0.0], [2115, 0.0], [2116, 0.0], [2117, 0.0], [2118, 0.0],
    [2119, 0.0], [2120, 0.0], [2121, 0.0], [2122, 0.0], [2123, 0.0], [2124, 0.0],
    [2125, 0.0], [2126, 0.0], [2127, 0.0], [2128, 0.0], [2129, 0.0], [2130, 0.0],
    [2131, 0.0], [2132, 0.0], [2133, 0.0], [2134, 0.0], [2135, 0.0], [2136, 0.0],
    [2137, 0.0], [2138, 0.0], [2139, 0.0]])

# "First Cost"!E37:E82
soln_pds_annual_world_first_cost_nparray = np.array([
    [2015, 49905587652.22], [2016, 65547210056.69], [2017, 68345312033.84],
    [2018, 70793825183.87], [2019, 72905511547.32], [2020, 2311551802.55],
    [2021, 144598267254.49], [2022, 77504158926.10], [2023, 78545836569.90],
    [2024, 79377339921.58], [2025, 22692755797.36], [2026, 136318611840.71],
    [2027, 80765154530.75], [2028, 80899562665.54], [2029, 80886051910.78],
    [2030, 117261801295.78], [2031, 43441060367.76], [2032, 80030657599.76],
    [2033, 79493599209.60], [2034, 78838596495.43], [2035, 78069563625.33],
    [2036, 77189918719.57], [2037, 76202640186.00], [2038, 75110313497.79],
    [2039, 73915170091.08], [2040, 84899874943.99], [2041, 58904181250.43],
    [2042, 86010366591.19], [2043, 92328264362.41], [2044, 94195693519.31],
    [2045, 95723401094.42], [2046, 96925449504.10], [2047, 61897446256.67],
    [2048, 133952774785.96], [2049, 98695889425.63], [2050, 93058434017.89],
    [2051, 104130477650.32], [2052, 62867752517.57], [2053, 131893976085.28],
    [2054, 96056663639.89], [2055, 94747261012.30], [2056, 93187121794.96],
    [2057, 117540036750.52], [2058, 63289512079.58], [2059, 87025393821.60],
    [2060, 84481838372.33]])

# "Operating Cost"!D19:D64
soln_pds_annual_operating_cost_nparray = np.array([
    [2015, 744986264.92], [2016, 1895173564.86], [2017, 3240360333.69],
    [2018, 4771790412.36], [2019, 6480707641.83], [2020, 6480901090.75],
    [2021, 10395978916.95], [2022, 12584820644.51], [2023, 14916124886.68],
    [2024, 17381135484.41], [2025, 18054383803.70], [2026, 22677251110.37],
    [2027, 25490843820.50], [2028, 28403118250.01], [2029, 31405318239.85],
    [2030, 35966029394.04], [2031, 37644470264.32], [2032, 40863909980.86],
    [2033, 44138250621.54], [2034, 47458736027.32], [2035, 50816610039.15],
    [2036, 54203116497.98], [2037, 57609499244.77], [2038, 61027002120.46],
    [2039, 64446868966.02], [2040, 68457818990.77], [2041, 71258669930.54],
    [2042, 74633091731.41], [2043, 77974852865.96], [2044, 81275197175.13],
    [2045, 84525368499.90], [2046, 87716610681.19], [2047, 90840167559.98],
    [2048, 93887282977.22], [2049, 96849200773.85], [2050, 97559747865.68],
    [2051, 96438558976.78], [2052, 92803096416.96], [2053, 89537185057.69],
    [2054, 86649581058.02], [2055, 83669862458.27], [2056, 79498779095.17],
    [2057, 77099770653.91], [2058, 74265580648.94], [2059, 71004965239.29],
    [2060, 67696016024.78], [2061, 64347489164.47], [2062, 60968140817.39],
    [2063, 57566727142.59], [2064, 54152004299.12], [2065, 50732728446.03],
    [2066, 46869549216.08], [2067, 43393680372.60], [2068, 39215064504.57],
    [2069, 34617451169.06], [2070, 29868444229.79], [2071, 24985556004.86],
    [2072, 20925026198.50], [2073, 15826912356.53], [2074, 9708726797.02],
    [2075, 4465436610.37], [2076, 639826260.03],
    [2077, 0.0], [2078, 0.0], [2079, 0.0], [2080, 0.0], [2081, 0.0], [2082, 0.0],
    [2083, 0.0], [2084, 0.0], [2085, 0.0], [2086, 0.0], [2087, 0.0], [2088, 0.0],
    [2089, 0.0], [2090, 0.0], [2091, 0.0], [2092, 0.0], [2093, 0.0], [2094, 0.0],
    [2095, 0.0], [2096, 0.0], [2097, 0.0], [2098, 0.0], [2099, 0.0], [2100, 0.0],
    [2101, 0.0], [2102, 0.0], [2103, 0.0], [2104, 0.0], [2105, 0.0], [2106, 0.0],
    [2107, 0.0], [2108, 0.0], [2109, 0.0], [2110, 0.0], [2111, 0.0], [2112, 0.0],
    [2113, 0.0], [2114, 0.0], [2115, 0.0], [2116, 0.0], [2117, 0.0], [2118, 0.0],
    [2119, 0.0], [2120, 0.0], [2121, 0.0], [2122, 0.0], [2123, 0.0], [2124, 0.0],
    [2125, 0.0], [2126, 0.0], [2127, 0.0], [2128, 0.0], [2129, 0.0], [2130, 0.0],
    [2131, 0.0], [2132, 0.0], [2133, 0.0], [2134, 0.0], [2135, 0.0], [2136, 0.0],
    [2137, 0.0], [2138, 0.0], [2139, 0.0]])

# "Operating Cost"!E19:E64
soln_pds_cumulative_operating_cost_nparray = np.array([
    [2015, 744986264.92], [2016, 2640159829.78], [2017, 5880520163.48],
    [2018, 10652310575.84], [2019, 17133018217.67], [2020, 23613919308.42],
    [2021, 34009898225.37], [2022, 46594718869.88], [2023, 61510843756.56],
    [2024, 78891979240.97], [2025, 96946363044.67], [2026, 119623614155.04],
    [2027, 145114457975.54], [2028, 173517576225.55], [2029, 204922894465.40],
    [2030, 240888923859.44], [2031, 278533394123.76], [2032, 319397304104.61],
    [2033, 363535554726.16], [2034, 410994290753.48], [2035, 461810900792.63],
    [2036, 516014017290.61], [2037, 573623516535.37], [2038, 634650518655.84],
    [2039, 699097387621.86], [2040, 767555206612.63], [2041, 838813876543.17],
    [2042, 913446968274.58], [2043, 991421821140.54], [2044, 1072697018315.67],
    [2045, 1157222386815.57], [2046, 1244938997496.76], [2047, 1335779165056.74],
    [2048, 1429666448033.96], [2049, 1526515648807.81], [2050, 1624075396673.49],
    [2051, 1720513955650.27], [2052, 1813317052067.23], [2053, 1902854237124.91],
    [2054, 1989503818182.94], [2055, 2073173680641.21], [2056, 2152672459736.38],
    [2057, 2229772230390.29], [2058, 2304037811039.22], [2059, 2375042776278.51],
    [2060, 2442738792303.29], [2061, 2507086281467.76], [2062, 2568054422285.15],
    [2063, 2625621149427.73], [2064, 2679773153726.86], [2065, 2730505882172.88],
    [2066, 2777375431388.96], [2067, 2820769111761.57], [2068, 2859984176266.13],
    [2069, 2894601627435.19], [2070, 2924470071664.98], [2071, 2949455627669.84],
    [2072, 2970380653868.34], [2073, 2986207566224.87], [2074, 2995916293021.89],
    [2075, 3000381729632.26], [2076, 3001021555892.29],
    [2077, 3001021555892.30], [2078, 3001021555892.30],
    [2079, 3001021555892.30], [2080, 3001021555892.30],
    [2081, 3001021555892.30], [2082, 3001021555892.30],
    [2083, 3001021555892.30], [2084, 3001021555892.30],
    [2085, 3001021555892.30], [2086, 3001021555892.30],
    [2087, 3001021555892.30], [2088, 3001021555892.30],
    [2089, 3001021555892.30], [2090, 3001021555892.30],
    [2091, 3001021555892.30], [2092, 3001021555892.30],
    [2093, 3001021555892.30], [2094, 3001021555892.30],
    [2095, 3001021555892.30], [2096, 3001021555892.30],
    [2097, 3001021555892.30], [2098, 3001021555892.30],
    [2099, 3001021555892.30], [2100, 3001021555892.30],
    [2101, 3001021555892.30], [2102, 3001021555892.30],
    [2103, 3001021555892.30], [2104, 3001021555892.30],
    [2105, 3001021555892.30], [2106, 3001021555892.30],
    [2107, 3001021555892.30], [2108, 3001021555892.30],
    [2109, 3001021555892.30], [2110, 3001021555892.30],
    [2111, 3001021555892.30], [2112, 3001021555892.30],
    [2113, 3001021555892.30], [2114, 3001021555892.30],
    [2115, 3001021555892.30], [2116, 3001021555892.30],
    [2117, 3001021555892.30], [2118, 3001021555892.30],
    [2119, 3001021555892.30], [2120, 3001021555892.30],
    [2121, 3001021555892.30], [2122, 3001021555892.30],
    [2123, 3001021555892.30], [2124, 3001021555892.30],
    [2125, 3001021555892.30], [2126, 3001021555892.30],
    [2127, 3001021555892.30], [2128, 3001021555892.30],
    [2129, 3001021555892.30], [2130, 3001021555892.30],
    [2131, 3001021555892.30], [2132, 3001021555892.30],
    [2133, 3001021555892.30], [2134, 3001021555892.30],
    [2135, 3001021555892.30], [2136, 3001021555892.30],
    [2137, 3001021555892.30], [2138, 3001021555892.30],
    [2139, 3001021555892.30]
    ])

# "Operating Cost"!K19:K64
conv_ref_annual_operating_cost_nparray = np.array([
    [2015, 4941471380.46], [2016, 12570628980.37], [2017, 21493212164.19],
    [2018, 31651141593.59], [2019, 42986337930.23], [2020, 42987621071.08],
    [2021, 68956213971.94], [2022, 83474735000.35], [2023, 98938205582.69],
    [2024, 115288546380.62], [2025, 119754182135.75], [2026, 150417521269.98],
    [2027, 169079996684.73], [2028, 188397024961.77], [2029, 208310526762.77],
    [2030, 238561586016.06], [2031, 249694633583.29], [2032, 271049079926.16],
    [2033, 292767682439.67], [2034, 314792361785.49], [2035, 337065038625.28],
    [2036, 359527633620.71], [2037, 382122067433.47], [2038, 404790260725.21],
    [2039, 427474134157.61], [2040, 454078644454.03], [2041, 472656604091.06],
    [2042, 495039041915.46], [2043, 517204842527.20], [2044, 539095926587.95],
    [2045, 560654214759.38], [2046, 581821627703.17], [2047, 602540086080.97],
    [2048, 622751510554.47], [2049, 642397821785.34], [2050, 647110859171.51],
    [2051, 639674047155.68], [2052, 615560133866.23], [2053, 593897442521.60],
    [2054, 574744052460.14], [2055, 554979669040.13], [2056, 527312999149.92],
    [2057, 511400448661.17], [2058, 492601352012.20], [2059, 470973788541.35],
    [2060, 449025628403.62]])

# "Operating Cost"!E19:E64
conv_ref_cumulative_operating_cost_nparray = np.array([
    [2015, 4941471380.46], [2016, 17512100360.83], [2017, 39005312525.03],
    [2018, 70656454118.62], [2019, 113642792048.85], [2020, 156630413119.94],
    [2021, 225586627091.88], [2022, 309061362092.23], [2023, 407999567674.92],
    [2024, 523288114055.54], [2025, 643042296191.29], [2026, 793459817461.26],
    [2027, 962539814145.99], [2028, 1150936839107.77], [2029, 1359247365870.53],
    [2030, 1597808951886.59], [2031, 1847503585469.88], [2032, 2118552665396.04],
    [2033, 2411320347835.71], [2034, 2726112709621.20], [2035, 3063177748246.47],
    [2036, 3422705381867.18], [2037, 3804827449300.65], [2038, 4209617710025.86],
    [2039, 4637091844183.46], [2040, 5091170488637.49], [2041, 5563827092728.55],
    [2042, 6058866134644.01], [2043, 6576070977171.21], [2044, 7115166903759.16],
    [2045, 7675821118518.54], [2046, 8257642746221.71], [2047, 8860182832302.68],
    [2048, 9482934342857.16], [2049, 10125332164642.50], [2050, 10772443023814.00],
    [2051, 11412117070969.70], [2052, 12027677204835.90], [2053, 12621574647357.50],
    [2054, 13196318699817.70], [2055, 13751298368857.80], [2056, 14278611368007.70],
    [2057, 14790011816668.90], [2058, 15282613168681.10], [2059, 15753586957222.40],
    [2060, 16202612585626.00]])

# "Operating Cost"!D69:D114
marginal_annual_operating_cost_nparray = np.array([
    [2015, 4196485115.54], [2016, 10675455415.51], [2017, 18252851830.50],
    [2018, 26879351181.23], [2019, 36505630288.41], [2020, 36506719980.33],
    [2021, 58560235055.00], [2022, 70889914355.84], [2023, 84022080696.01],
    [2024, 97907410896.21], [2025, 101699798332.05], [2026, 127740270159.61],
    [2027, 143589152864.23], [2028, 159993906711.76], [2029, 176905208522.92],
    [2030, 202595556622.02], [2031, 212050163318.97], [2032, 230185169945.30],
    [2033, 248629431818.13], [2034, 267333625758.16], [2035, 286248428586.13],
    [2036, 305324517122.73], [2037, 324512568188.70], [2038, 343763258604.75],
    [2039, 363027265191.59], [2040, 385620825463.26], [2041, 401397934160.52],
    [2042, 420405950184.05], [2043, 439229989661.24], [2044, 457820729412.82],
    [2045, 476128846259.49], [2046, 494105017021.97], [2047, 511699918520.99],
    [2048, 528864227577.26], [2049, 545548621011.49], [2050, 549551111305.83],
    [2051, 543235488178.90], [2052, 522757037449.27], [2053, 504360257463.92],
    [2054, 488094471402.11], [2055, 471309806581.86], [2056, 447814220054.75],
    [2057, 434300678007.26], [2058, 418335771363.27], [2059, 399968823302.07],
    [2060, 381329612378.83]])

# "Operating Cost"!A19:E64
lifetime_cost_forecast_list = [
    ['Year', 'Investment (Marginal First Cost)', 'Marginal Operating Cost Savings',
      'Net Cash Flow', 'NPV in $2014'],
    [2015, -22432407009.64, 4196485115.54, -18235921894.10, -16669032809.96],
    [2016, -25103540446.96, 10675455415.51, -14428085031.45, -12055189709.74],
    [2017, -21709643060.00, 18252851830.50, -3456791229.50, -2640104913.84],
    [2018, -18256235647.59, 26879351181.23, 8623115533.63, 6019978176.76],
    [2019, -14754936171.86, 36505630288.41, 21750694116.54, 13879905551.81],
    [2020, 991539625.99, 36506719980.33, 37498259606.32, 21872940897.27],
    [2021, -15963799121.32, 58560235055.00, 42596435933.68, 22711823734.61],
    [2022, -4237893109.54, 70889914355.84, 66652021246.30, 32484392409.82],
    [2023, -812299303.65, 84022080696.01, 83209781392.35, 37069649785.36],
    [2024, 2539250353.69, 97907410896.21, 100446661249.90, 40903670928.75],
    [2025, 1943570621.51, 101699798332.05, 103643368953.56, 38579001176.59],
    [2026, 14248289863.97, 127740270159.61, 141988560023.58, 48310940342.91],
    [2027, 12002921852.21, 143589152864.23, 155592074716.44, 48390742499.23],
    [2028, 14922133995.01, 159993906711.76, 174916040706.77, 49726412740.70],
    [2029, 17708581650.51, 176905208522.92, 194613790173.42, 50572425210.92],
    [2030, 30812206896.05, 202595556622.02, 233407763518.07, 55441905125.08],
    [2031, 12904677243.36, 212050163318.97, 224954840562.34, 48842835547.56],
    [2032, 25204610762.49, 230185169945.30, 255389780707.79, 50686431824.69],
    [2033, 27397666857.60, 248629431818.13, 276027098675.73, 50075189632.25],
    [2034, 29430757586.21, 267333625758.16, 296764383344.37, 49211356591.25],
    [2035, 31300455525.94, 286248428586.13, 317548884112.07, 48133432026.13],
    [2036, 33003810257.21, 305324517122.73, 338328327379.94, 46876726648.57],
    [2037, 34538293305.07, 324512568188.70, 359050861493.77, 45473414656.54],
    [2038, 35901752528.66, 343763258604.75, 379665011133.40, 43952628031.55],
    [2039, 37092374291.88, 363027265191.59, 400119639483.47, 42340581560.58],
    [2040, 44715046624.56, 385620825463.26, 430335872087.82, 41625280943.60],
    [2041, 32392123175.17, 401397934160.52, 433790057335.69, 38354109131.00],
    [2042, 26122281172.29, 420405950184.05, 446528231356.34, 36088090737.59],
    [2043, 18684881335.09, 439229989661.24, 457914870996.33, 33828474195.33],
    [2044, 15424572287.54, 457820729412.82, 473245301700.35, 31957047716.80],
    [2045, 12230933599.22, 476128846259.49, 488359779858.71, 30144140641.27],
    [2046, 9090220293.95, 494105017021.97, 503195237315.93, 28391099908.67],
    [2047, 41907133633.22, 511699918520.99, 553607052154.21, 28551569574.97],
    [2048, -32631409259.37, 528864227577.26, 496232818317.89, 23393571733.32],
    [2049, -129569945.21, 545548621011.49, 545419051066.28, 23503039665.57],
    [2050, -7226584060.81, 549551111305.83, 542324527245.02, 21361692268.72],
    [2051, 0.00, 543235488178.90, 543235488178.90, 19559025803.46],
    [2052, 0.00, 522757037449.27, 522757037449.27, 17204484018.39],
    [2053, 0.00, 504360257463.92, 504360257463.92, 15172784859.71],
    [2054, 0.00, 488094471402.11, 488094471402.11, 13421807587.99],
    [2055, 0.00, 471309806581.86, 471309806581.86, 11846669547.52],
    [2056, 0.00, 447814220054.75, 447814220054.75, 10288933406.16],
    [2057, 0.00, 434300678007.26, 434300678007.26, 9121067326.91],
    [2058, 0.00, 418335771363.27, 418335771363.27, 8030874409.34],
    [2059, 0.00, 399968823302.07, 399968823302.07, 7018537916.45],
    [2060, 0.00, 381329612378.83, 381329612378.83, 6116510422.41],
    [2061, 0.00, 362467461772.85, 362467461772.85, 5314407994.35],
    [2062, 0.00, 343431694663.41, 343431694663.41, 4602660237.54],
    [2063, 0.00, 324271634229.78, 324271634229.78, 3972465941.46],
    [2064, 0.00, 305036603651.26, 305036603651.26, 3415748268.73],
    [2065, 0.00, 285775926107.11, 285775926107.11, 2925110110.54],
    [2066, 0.00, 264014754256.65, 264014754256.65, 2470173474.91],
    [2067, 0.00, 244435290108.02, 244435290108.02, 2090479153.53],
    [2068, 0.00, 220897273208.30, 220897273208.30, 1726851400.09],
    [2069, 0.00, 194999056237.04, 194999056237.04, 1393412812.57],
    [2070, 0.00, 168248043671.20, 168248043671.20, 1098955207.36],
    [2071, 0.00, 140742881869.35, 140742881869.35, 840309136.58],
    [2072, 0.00, 117870040186.27, 117870040186.27, 643278084.27],
    [2073, 0.00, 89152518988.09, 89152518988.09, 444745559.63],
    [2074, 0.00, 54688964633.38, 54688964633.38, 249379288.53],
    [2075, 0.00, 25153669473.13, 25153669473.13, 104844271.89],
    [2076, 0.00, 3604121986.12, 3604121986.12, 13731738.30],
    [2077, 0.00, 0.00, 0.00, 0.00], [2078, 0.00, 0.00, 0.00, 0.00],
    [2079, 0.00, 0.00, 0.00, 0.00], [2080, 0.00, 0.00, 0.00, 0.00],
    [2081, 0.00, 0.00, 0.00, 0.00], [2082, 0.00, 0.00, 0.00, 0.00],
    [2083, 0.00, 0.00, 0.00, 0.00], [2084, 0.00, 0.00, 0.00, 0.00],
    [2085, 0.00, 0.00, 0.00, 0.00], [2086, 0.00, 0.00, 0.00, 0.00],
    [2087, 0.00, 0.00, 0.00, 0.00], [2088, 0.00, 0.00, 0.00, 0.00],
    [2089, 0.00, 0.00, 0.00, 0.00], [2090, 0.00, 0.00, 0.00, 0.00],
    [2091, 0.00, 0.00, 0.00, 0.00], [2092, 0.00, 0.00, 0.00, 0.00],
    [2093, 0.00, 0.00, 0.00, 0.00], [2094, 0.00, 0.00, 0.00, 0.00],
    [2095, 0.00, 0.00, 0.00, 0.00], [2096, 0.00, 0.00, 0.00, 0.00],
    [2097, 0.00, 0.00, 0.00, 0.00], [2098, 0.00, 0.00, 0.00, 0.00],
    [2099, 0.00, 0.00, 0.00, 0.00], [2100, 0.00, 0.00, 0.00, 0.00],
    [2101, 0.00, 0.00, 0.00, 0.00], [2102, 0.00, 0.00, 0.00, 0.00],
    [2103, 0.00, 0.00, 0.00, 0.00], [2104, 0.00, 0.00, 0.00, 0.00],
    [2105, 0.00, 0.00, 0.00, 0.00], [2106, 0.00, 0.00, 0.00, 0.00],
    [2107, 0.00, 0.00, 0.00, 0.00], [2108, 0.00, 0.00, 0.00, 0.00],
    [2109, 0.00, 0.00, 0.00, 0.00], [2110, 0.00, 0.00, 0.00, 0.00],
    [2111, 0.00, 0.00, 0.00, 0.00], [2112, 0.00, 0.00, 0.00, 0.00],
    [2113, 0.00, 0.00, 0.00, 0.00], [2114, 0.00, 0.00, 0.00, 0.00],
    [2115, 0.00, 0.00, 0.00, 0.00], [2116, 0.00, 0.00, 0.00, 0.00],
    [2117, 0.00, 0.00, 0.00, 0.00], [2118, 0.00, 0.00, 0.00, 0.00],
    [2119, 0.00, 0.00, 0.00, 0.00], [2120, 0.00, 0.00, 0.00, 0.00],
    [2121, 0.00, 0.00, 0.00, 0.00], [2122, 0.00, 0.00, 0.00, 0.00],
    [2123, 0.00, 0.00, 0.00, 0.00], [2124, 0.00, 0.00, 0.00, 0.00],
    [2125, 0.00, 0.00, 0.00, 0.00], [2126, 0.00, 0.00, 0.00, 0.00],
    [2127, 0.00, 0.00, 0.00, 0.00], [2128, 0.00, 0.00, 0.00, 0.00],
    [2129, 0.00, 0.00, 0.00, 0.00], [2130, 0.00, 0.00, 0.00, 0.00],
    [2131, 0.00, 0.00, 0.00, 0.00], [2132, 0.00, 0.00, 0.00, 0.00],
    [2133, 0.00, 0.00, 0.00, 0.00], [2134, 0.00, 0.00, 0.00, 0.00],
    [2135, 0.00, 0.00, 0.00, 0.00], [2136, 0.00, 0.00, 0.00, 0.00],
    [2137, 0.00, 0.00, 0.00, 0.00], [2138, 0.00, 0.00, 0.00, 0.00],
    [2139, 0.00, 0.00, 0.00, 0.00]]

# "First Cost"!C37:C82
soln_pds_install_cost_per_iunit_nparray = np.array([
    [2015, 1444939544214.85], [2016, 1260211854559.48], [2017, 1131125771261.71],
    [2018, 1034176540754.27], [2019, 957914360042.17], [2020, 955853826404.52],
    [2021, 844363092072.89], [2022, 800615041745.80], [2023, 762954261503.24],
    [2024, 730136123170.93], [2025, 721678325520.19], [2026, 675595934758.92],
    [2027, 652654395751.15], [2028, 632005749879.43], [2029, 613318626692.05],
    [2030, 588974654797.70], [2031, 580807336513.56], [2032, 566583683816.19],
    [2033, 553503708701.86], [2034, 541440613073.64], [2035, 530286923303.66],
    [2036, 519950919467.44], [2037, 510353842407.28], [2038, 501427686348.92],
    [2039, 493113437720.23], [2040, 484074786193.61], [2041, 478121333143.78],
    [2042, 471358936327.06], [2043, 465037653845.78], [2044, 459126747449.31],
    [2045, 453599023283.05], [2046, 448430388622.18], [2047, 443599480377.26],
    [2048, 439087352857.46], [2049, 434877214846.06], [2050, 431361401332.87],
    [2051, 427305220575.04], [2052, 423918730328.15], [2053, 420784674297.91],
    [2054, 417894340462.60], [2055, 415240279798.58], [2056, 412816236436.15],
    [2057, 410617094526.91], [2058, 408638840847.23], [2059, 406878542591.41],
    [2060, 405334340227.07]])

# "First Cost"!O37:O82
conv_ref_install_cost_per_iunit_nparray = np.array([
    [2015, 2005749716919.21], [2016, 2003709559856.43], [2017, 2001740610594.36],
    [2018, 1999838071911.36], [2019, 1997997609222.97], [2020, 1996215293069.34],
    [2021, 1994487550260.54], [2022, 1992811122162.61], [2023, 1991183028908.37],
    [2024, 1989600538551.80], [2025, 1988061140369.17], [2026, 1986562521656.05],
    [2027, 1985102547485.31], [2028, 1983679242984.24], [2029, 1982290777764.18],
    [2030, 1980935452196.45], [2031, 1979611685278.25], [2032, 1978318003872.66],
    [2033, 1977053033140.28], [2034, 1975815488007.72], [2035, 1974604165541.04],
    [2036, 1973417938111.51], [2037, 1972255747256.95], [2038, 1971116598155.42],
    [2039, 1969999554639.64], [2040, 1968903734689.63], [2041, 1967828306349.86],
    [2042, 1966772484023.75], [2043, 1965735525104.47], [2044, 1964716726906.07],
    [2045, 1963715423863.49], [2046, 1962730984973.61], [2047, 1961762811452.90],
    [2048, 1960810334590.08], [2049, 1959873013774.63], [2050, 1958950334684.14],
    [2051, 1958041807615.42], [2052, 1957146965945.90], [2053, 1956265364713.38],
    [2054, 1955396579303.22], [2055, 1954540204233.54], [2056, 1953695852029.72],
    [2057, 1952863152180.40], [2058, 1952041750168.08], [2059, 1951231306567.92],
    [2060, 1950431496209.24]])

# "Operating Cost"!I126:I250
soln_vs_conv_single_iunit_cashflow_nparray = np.array([
    [2015, -469994891712], [2016, 130616812789], [2017, 130616812789],
    [2018, 130616812789], [2019, 130616812789], [2020, 130616812789],
    [2021, 130616812789], [2022, 130616812789], [2023, 130616812789],
    [2024, 130616812789], [2025, 130616812789], [2026, 130616812789],
    [2027, 130616812789], [2028, 130616812789], [2029, 130616812789],
    [2030, 130616812789], [2031, 130616812789], [2032, 130616812789],
    [2033, 130616812789], [2034, 130616812789], [2035, 130616812789],
    [2036, 130616812789], [2037, 130616812789], [2038, 130616812789],
    [2039, 130616812789], [2040, 130616812789], [2041, 32654203197],
    [2042, 0], [2043, 0], [2044, 0], [2045, 0], [2046, 0], [2047, 0], [2048, 0],
    [2049, 0], [2050, 0], [2051, 0], [2052, 0], [2053, 0], [2054, 0], [2055, 0],
    [2056, 0], [2057, 0], [2058, 0], [2059, 0], [2060, 0], [2061, 0], [2062, 0],
    [2063, 0], [2064, 0], [2065, 0], [2066, 0], [2067, 0], [2068, 0], [2069, 0],
    [2070, 0], [2071, 0], [2072, 0], [2073, 0], [2074, 0], [2075, 0], [2076, 0],
    [2077, 0], [2078, 0], [2079, 0], [2080, 0], [2081, 0], [2082, 0], [2083, 0],
    [2084, 0], [2085, 0], [2086, 0], [2087, 0], [2088, 0], [2089, 0], [2090, 0],
    [2091, 0], [2092, 0], [2093, 0], [2094, 0], [2095, 0], [2096, 0], [2097, 0],
    [2098, 0], [2099, 0], [2100, 0], [2101, 0], [2102, 0], [2103, 0], [2104, 0],
    [2105, 0], [2106, 0], [2107, 0], [2108, 0], [2109, 0], [2110, 0], [2111, 0],
    [2112, 0], [2113, 0], [2114, 0], [2115, 0], [2116, 0], [2117, 0], [2118, 0],
    [2119, 0], [2120, 0], [2121, 0], [2122, 0], [2123, 0], [2124, 0], [2125, 0],
    [2126, 0], [2127, 0], [2128, 0], [2129, 0], [2130, 0], [2131, 0], [2132, 0],
    [2133, 0], [2134, 0], [2135, 0], [2136, 0], [2137, 0], [2138, 0], [2139, 0]])

# "Operating Cost"!J126:J250
soln_vs_conv_single_iunit_npv_nparray = np.array([
    [2015, -358955962541.30], [2016, 91186342041.03], [2017, 83351318136.23],
    [2018, 76189504694.91], [2019, 69643057307.96], [2020, 63659101744.02],
    [2021, 58189306895.81], [2022, 53189494420.31], [2023, 48619281919.84],
    [2024, 44441756782.30], [2025, 40623178045.98], [2026, 37132703881.15],
    [2027, 33942142487.34], [2028, 31025724394.28], [2029, 28359894327.50],
    [2030, 25923120957.49], [2031, 23695722995.88], [2032, 21659710233.89],
    [2033, 19798638239.39], [2034, 18097475538.75], [2035, 16542482210.92],
    [2036, 15121098913.09], [2037, 13821845441.58], [2038, 12634228008.76],
    [2039, 11548654486.98], [2040, 10556356935.08], [2041, 2412330195.40],
    [2042, 0.0], [2043, 0.0], [2044, 0.0], [2045, 0.0], [2046, 0.0], [2047, 0.0],
    [2048, 0.0], [2049, 0.0], [2050, 0.0], [2051, 0.0], [2052, 0.0], [2053, 0.0],
    [2054, 0.0], [2055, 0.0], [2056, 0.0], [2057, 0.0], [2058, 0.0], [2059, 0.0],
    [2060, 0.0], [2061, 0.0], [2062, 0.0], [2063, 0.0], [2064, 0.0], [2065, 0.0],
    [2066, 0.0], [2067, 0.0], [2068, 0.0], [2069, 0.0], [2070, 0.0], [2071, 0.0],
    [2072, 0.0], [2073, 0.0], [2074, 0.0], [2075, 0.0], [2076, 0.0], [2077, 0.0],
    [2078, 0.0], [2079, 0.0], [2080, 0.0], [2081, 0.0], [2082, 0.0], [2083, 0.0],
    [2084, 0.0], [2085, 0.0], [2086, 0.0], [2087, 0.0], [2088, 0.0], [2089, 0.0],
    [2090, 0.0], [2091, 0.0], [2092, 0.0], [2093, 0.0], [2094, 0.0], [2095, 0.0],
    [2096, 0.0], [2097, 0.0], [2098, 0.0], [2099, 0.0], [2100, 0.0], [2101, 0.0],
    [2102, 0.0], [2103, 0.0], [2104, 0.0], [2105, 0.0], [2106, 0.0], [2107, 0.0],
    [2108, 0.0], [2109, 0.0], [2110, 0.0], [2111, 0.0], [2112, 0.0], [2113, 0.0],
    [2114, 0.0], [2115, 0.0], [2116, 0.0], [2117, 0.0], [2118, 0.0], [2119, 0.0],
    [2120, 0.0], [2121, 0.0], [2122, 0.0], [2123, 0.0], [2124, 0.0], [2125, 0.0],
    [2126, 0.0], [2127, 0.0], [2128, 0.0], [2129, 0.0], [2130, 0.0], [2131, 0.0],
    [2132, 0.0], [2133, 0.0], [2134, 0.0], [2135, 0.0], [2136, 0.0], [2137, 0.0],
    [2138, 0.0], [2139, 0.0]])

# "Operating Cost"!J126:J250 with purchase_year=2026, discount_rate=7.1, but
# holding I126:I250 unchanged
soln_vs_conv_single_iunit_npv_purchase_year_discount_rate_nparray = np.array([
    [2015, -221008490609.18], [2016, 57348944906.19], [2017, 53547100752.74],
    [2018, 49997292953.08], [2019, 46682813214.82], [2020, 43588060891.52],
    [2021, 40698469553.24], [2022, 38000438425.06], [2023, 35481268370.74],
    [2024, 33129102120.21], [2025, 30932868459.58], [2026, 28882230120.99],
    [2027, 26967535126.97], [2028, 25179771360.38], [2029, 23510524146.02],
    [2030, 21951936644.27], [2031, 20496672870.47], [2032, 19137883165.71],
    [2033, 17869171956.77], [2034, 16684567653.38], [2035, 15578494540.98],
    [2036, 14545746536.86], [2037, 13581462686.14], [2038, 12681104282.11],
    [2039, 11840433503.37], [2040, 11055493467.20], [2041, 2580647401.31],
    [2042, 0.0], [2043, 0.0], [2044, 0.0], [2045, 0.0], [2046, 0.0], [2047, 0.0],
    [2048, 0.0], [2049, 0.0], [2050, 0.0], [2051, 0.0], [2052, 0.0], [2053, 0.0],
    [2054, 0.0], [2055, 0.0], [2056, 0.0], [2057, 0.0], [2058, 0.0], [2059, 0.0],
    [2060, 0.0], [2061, 0.0], [2062, 0.0], [2063, 0.0], [2064, 0.0], [2065, 0.0],
    [2066, 0.0], [2067, 0.0], [2068, 0.0], [2069, 0.0], [2070, 0.0], [2071, 0.0],
    [2072, 0.0], [2073, 0.0], [2074, 0.0], [2075, 0.0], [2076, 0.0], [2077, 0.0],
    [2078, 0.0], [2079, 0.0], [2080, 0.0], [2081, 0.0], [2082, 0.0], [2083, 0.0],
    [2084, 0.0], [2085, 0.0], [2086, 0.0], [2087, 0.0], [2088, 0.0], [2089, 0.0],
    [2090, 0.0], [2091, 0.0], [2092, 0.0], [2093, 0.0], [2094, 0.0], [2095, 0.0],
    [2096, 0.0], [2097, 0.0], [2098, 0.0], [2099, 0.0], [2100, 0.0], [2101, 0.0],
    [2102, 0.0], [2103, 0.0], [2104, 0.0], [2105, 0.0], [2106, 0.0], [2107, 0.0],
    [2108, 0.0], [2109, 0.0], [2110, 0.0], [2111, 0.0], [2112, 0.0], [2113, 0.0],
    [2114, 0.0], [2115, 0.0], [2116, 0.0], [2117, 0.0], [2118, 0.0], [2119, 0.0],
    [2120, 0.0], [2121, 0.0], [2122, 0.0], [2123, 0.0], [2124, 0.0], [2125, 0.0],
    [2126, 0.0], [2127, 0.0], [2128, 0.0], [2129, 0.0], [2130, 0.0], [2131, 0.0],
    [2132, 0.0], [2133, 0.0], [2134, 0.0], [2135, 0.0], [2136, 0.0], [2137, 0.0],
    [2138, 0.0], [2139, 0.0]])

# "Operating Cost"!K126:K250
soln_vs_conv_single_iunit_payback_nparray = np.array([
    [2015, 0], [2016, 0], [2017, 0], [2018, 0], [2019, 1], [2020, 1], [2021, 1],
    [2022, 1], [2023, 1], [2024, 1], [2025, 1], [2026, 1], [2027, 1], [2028, 1],
    [2029, 1], [2030, 1], [2031, 1], [2032, 1], [2033, 1], [2034, 1], [2035, 1],
    [2036, 1], [2037, 1], [2038, 1], [2039, 1], [2040, 1], [2041, 1], [2042, 1],
    [2043, 1], [2044, 1], [2045, 1], [2046, 1], [2047, 1], [2048, 1], [2049, 1],
    [2050, 1], [2051, 1], [2052, 1], [2053, 1], [2054, 1], [2055, 1], [2056, 1],
    [2057, 1], [2058, 1], [2059, 1], [2060, 1], [2061, 1], [2062, 1], [2063, 1],
    [2064, 1], [2065, 1], [2066, 1], [2067, 1], [2068, 1], [2069, 1], [2070, 1],
    [2071, 1], [2072, 1], [2073, 1], [2074, 1], [2075, 1], [2076, 1], [2077, 1],
    [2078, 1], [2079, 1], [2080, 1], [2081, 1], [2082, 1], [2083, 1], [2084, 1],
    [2085, 1], [2086, 1], [2087, 1], [2088, 1], [2089, 1], [2090, 1], [2091, 1],
    [2092, 1], [2093, 1], [2094, 1], [2095, 1], [2096, 1], [2097, 1], [2098, 1],
    [2099, 1], [2100, 1], [2101, 1], [2102, 1], [2103, 1], [2104, 1], [2105, 1],
    [2106, 1], [2107, 1], [2108, 1], [2109, 1], [2110, 1], [2111, 1], [2112, 1],
    [2113, 1], [2114, 1], [2115, 1], [2116, 1], [2117, 1], [2118, 1], [2119, 1],
    [2120, 1], [2121, 1], [2122, 1], [2123, 1], [2124, 1], [2125, 1], [2126, 1],
    [2127, 1], [2128, 1], [2129, 1], [2130, 1], [2131, 1], [2132, 1], [2133, 1],
    [2134, 1], [2135, 1], [2136, 1], [2137, 1], [2138, 1], [2139, 1]])

# "Operating Cost"!L126:L250
soln_vs_conv_single_iunit_payback_discounted_nparray = np.array([
    [2015, 0], [2016, 0], [2017, 0], [2018, 0], [2019, 0], [2020, 1], [2021, 1],
    [2022, 1], [2023, 1], [2024, 1], [2025, 1], [2026, 1], [2027, 1], [2028, 1],
    [2029, 1], [2030, 1], [2031, 1], [2032, 1], [2033, 1], [2034, 1], [2035, 1],
    [2036, 1], [2037, 1], [2038, 1], [2039, 1], [2040, 1], [2041, 1], [2042, 1],
    [2043, 1], [2044, 1], [2045, 1], [2046, 1], [2047, 1], [2048, 1], [2049, 1],
    [2050, 1], [2051, 1], [2052, 1], [2053, 1], [2054, 1], [2055, 1], [2056, 1],
    [2057, 1], [2058, 1], [2059, 1], [2060, 1], [2061, 1], [2062, 1], [2063, 1],
    [2064, 1], [2065, 1], [2066, 1], [2067, 1], [2068, 1], [2069, 1], [2070, 1],
    [2071, 1], [2072, 1], [2073, 1], [2074, 1], [2075, 1], [2076, 1], [2077, 1],
    [2078, 1], [2079, 1], [2080, 1], [2081, 1], [2082, 1], [2083, 1], [2084, 1],
    [2085, 1], [2086, 1], [2087, 1], [2088, 1], [2089, 1], [2090, 1], [2091, 1],
    [2092, 1], [2093, 1], [2094, 1], [2095, 1], [2096, 1], [2097, 1], [2098, 1],
    [2099, 1], [2100, 1], [2101, 1], [2102, 1], [2103, 1], [2104, 1], [2105, 1],
    [2106, 1], [2107, 1], [2108, 1], [2109, 1], [2110, 1], [2111, 1], [2112, 1],
    [2113, 1], [2114, 1], [2115, 1], [2116, 1], [2117, 1], [2118, 1], [2119, 1],
    [2120, 1], [2121, 1], [2122, 1], [2123, 1], [2124, 1], [2125, 1], [2126, 1],
    [2127, 1], [2128, 1], [2129, 1], [2130, 1], [2131, 1], [2132, 1], [2133, 1],
    [2134, 1], [2135, 1], [2136, 1], [2137, 1], [2138, 1], [2139, 1]])

# "Operating Cost"!M126:M250
soln_only_single_iunit_cashflow_nparray = np.array([
    [2015, -1000508958473], [2016, 130616812789], [2017, 130616812789], [2018, 130616812789],
    [2019, 130616812789], [2020, 130616812789], [2021, 130616812789], [2022, 130616812789],
    [2023, 130616812789], [2024, 130616812789], [2025, 130616812789], [2026, 130616812789],
    [2027, 130616812789], [2028, 130616812789], [2029, 130616812789], [2030, 130616812789],
    [2031, 130616812789], [2032, 130616812789], [2033, 130616812789], [2034, 130616812789],
    [2035, 130616812789], [2036, 130616812789], [2037, 130616812789], [2038, 130616812789],
    [2039, 130616812789], [2040, 130616812789], [2041, 32654203197],
    [2042, 0.0], [2043, 0.0], [2044, 0.0], [2045, 0.0], [2046, 0.0], [2047, 0.0],
    [2048, 0.0], [2049, 0.0], [2050, 0.0], [2051, 0.0], [2052, 0.0], [2053, 0.0],
    [2054, 0.0], [2055, 0.0], [2056, 0.0], [2057, 0.0], [2058, 0.0], [2059, 0.0],
    [2060, 0.0], [2061, 0.0], [2062, 0.0], [2063, 0.0], [2064, 0.0], [2065, 0.0],
    [2066, 0.0], [2067, 0.0], [2068, 0.0], [2069, 0.0], [2070, 0.0], [2071, 0.0],
    [2072, 0.0], [2073, 0.0], [2074, 0.0], [2075, 0.0], [2076, 0.0], [2077, 0.0],
    [2078, 0.0], [2079, 0.0], [2080, 0.0], [2081, 0.0], [2082, 0.0], [2083, 0.0],
    [2084, 0.0], [2085, 0.0], [2086, 0.0], [2087, 0.0], [2088, 0.0], [2089, 0.0],
    [2090, 0.0], [2091, 0.0], [2092, 0.0], [2093, 0.0], [2094, 0.0], [2095, 0.0],
    [2096, 0.0], [2097, 0.0], [2098, 0.0], [2099, 0.0], [2100, 0.0], [2101, 0.0],
    [2102, 0.0], [2103, 0.0], [2104, 0.0], [2105, 0.0], [2106, 0.0], [2107, 0.0],
    [2108, 0.0], [2109, 0.0], [2110, 0.0], [2111, 0.0], [2112, 0.0], [2113, 0.0],
    [2114, 0.0], [2115, 0.0], [2116, 0.0], [2117, 0.0], [2118, 0.0], [2119, 0.0],
    [2120, 0.0], [2121, 0.0], [2122, 0.0], [2123, 0.0], [2124, 0.0], [2125, 0.0],
    [2126, 0.0], [2127, 0.0], [2128, 0.0], [2129, 0.0], [2130, 0.0], [2131, 0.0],
    [2132, 0.0], [2133, 0.0], [2134, 0.0], [2135, 0.0], [2136, 0.0], [2137, 0.0],
    [2138, 0.0], [2139, 0.0]])

# "Operating Cost"!N126:N250
soln_only_single_iunit_npv_nparray = np.array([
    [2015, -764133105599], [2016, 91186342041], [2017, 83351318136], [2018, 76189504695],
    [2019, 69643057308], [2020, 63659101744], [2021, 58189306896], [2022, 53189494420],
    [2023, 48619281920], [2024, 44441756782], [2025, 40623178046], [2026, 37132703881],
    [2027, 33942142487], [2028, 31025724394], [2029, 28359894327], [2030, 25923120957],
    [2031, 23695722996], [2032, 21659710234], [2033, 19798638239], [2034, 18097475539],
    [2035, 16542482211], [2036, 15121098913], [2037, 13821845442], [2038, 12634228009],
    [2039, 11548654487], [2040, 10556356935], [2041, 2412330195],
    [2042, 0.0], [2043, 0.0], [2044, 0.0], [2045, 0.0], [2046, 0.0], [2047, 0.0],
    [2048, 0.0], [2049, 0.0], [2050, 0.0], [2051, 0.0], [2052, 0.0], [2053, 0.0],
    [2054, 0.0], [2055, 0.0], [2056, 0.0], [2057, 0.0], [2058, 0.0], [2059, 0.0],
    [2060, 0.0], [2061, 0.0], [2062, 0.0], [2063, 0.0], [2064, 0.0], [2065, 0.0],
    [2066, 0.0], [2067, 0.0], [2068, 0.0], [2069, 0.0], [2070, 0.0], [2071, 0.0],
    [2072, 0.0], [2073, 0.0], [2074, 0.0], [2075, 0.0], [2076, 0.0], [2077, 0.0],
    [2078, 0.0], [2079, 0.0], [2080, 0.0], [2081, 0.0], [2082, 0.0], [2083, 0.0],
    [2084, 0.0], [2085, 0.0], [2086, 0.0], [2087, 0.0], [2088, 0.0], [2089, 0.0],
    [2090, 0.0], [2091, 0.0], [2092, 0.0], [2093, 0.0], [2094, 0.0], [2095, 0.0],
    [2096, 0.0], [2097, 0.0], [2098, 0.0], [2099, 0.0], [2100, 0.0], [2101, 0.0],
    [2102, 0.0], [2103, 0.0], [2104, 0.0], [2105, 0.0], [2106, 0.0], [2107, 0.0],
    [2108, 0.0], [2109, 0.0], [2110, 0.0], [2111, 0.0], [2112, 0.0], [2113, 0.0],
    [2114, 0.0], [2115, 0.0], [2116, 0.0], [2117, 0.0], [2118, 0.0], [2119, 0.0],
    [2120, 0.0], [2121, 0.0], [2122, 0.0], [2123, 0.0], [2124, 0.0], [2125, 0.0],
    [2126, 0.0], [2127, 0.0], [2128, 0.0], [2129, 0.0], [2130, 0.0], [2131, 0.0],
    [2132, 0.0], [2133, 0.0], [2134, 0.0], [2135, 0.0], [2136, 0.0], [2137, 0.0],
    [2138, 0.0], [2139, 0.0]])

# "Operating Cost"!O126:O250
soln_only_single_iunit_payback_nparray = np.array([
    [2015, 0], [2016, 0], [2017, 0], [2018, 0], [2019, 0], [2020, 0], [2021, 0],
    [2022, 0], [2023, 1], [2024, 1], [2025, 1], [2026, 1], [2027, 1], [2028, 1],
    [2029, 1], [2030, 1], [2031, 1], [2032, 1], [2033, 1], [2034, 1], [2035, 1],
    [2036, 1], [2037, 1], [2038, 1], [2039, 1], [2040, 1], [2041, 1], [2042, 1],
    [2043, 1], [2044, 1], [2045, 1], [2046, 1], [2047, 1], [2048, 1], [2049, 1],
    [2050, 1], [2051, 1], [2052, 1], [2053, 1], [2054, 1], [2055, 1], [2056, 1],
    [2057, 1], [2058, 1], [2059, 1], [2060, 1], [2061, 1], [2062, 1], [2063, 1],
    [2064, 1], [2065, 1], [2066, 1], [2067, 1], [2068, 1], [2069, 1], [2070, 1],
    [2071, 1], [2072, 1], [2073, 1], [2074, 1], [2075, 1], [2076, 1], [2077, 1],
    [2078, 1], [2079, 1], [2080, 1], [2081, 1], [2082, 1], [2083, 1], [2084, 1],
    [2085, 1], [2086, 1], [2087, 1], [2088, 1], [2089, 1], [2090, 1], [2091, 1],
    [2092, 1], [2093, 1], [2094, 1], [2095, 1], [2096, 1], [2097, 1], [2098, 1],
    [2099, 1], [2100, 1], [2101, 1], [2102, 1], [2103, 1], [2104, 1], [2105, 1],
    [2106, 1], [2107, 1], [2108, 1], [2109, 1], [2110, 1], [2111, 1], [2112, 1],
    [2113, 1], [2114, 1], [2115, 1], [2116, 1], [2117, 1], [2118, 1], [2119, 1],
    [2120, 1], [2121, 1], [2122, 1], [2123, 1], [2124, 1], [2125, 1], [2126, 1],
    [2127, 1], [2128, 1], [2129, 1], [2130, 1], [2131, 1], [2132, 1], [2133, 1],
    [2134, 1], [2135, 1], [2136, 1], [2137, 1], [2138, 1], [2139, 1]])

# "Operating Cost"!P126:P250
soln_only_single_iunit_payback_discounted_nparray = np.array([
    [2015, 0], [2016, 0], [2017, 0], [2018, 0], [2019, 0], [2020, 0], [2021, 0],
    [2022, 0], [2023, 0], [2024, 0], [2025, 0], [2026, 0], [2027, 0], [2028, 0],
    [2029, 0], [2030, 1], [2031, 1], [2032, 1], [2033, 1], [2034, 1], [2035, 1],
    [2036, 1], [2037, 1], [2038, 1], [2039, 1], [2040, 1], [2041, 1], [2042, 1],
    [2043, 1], [2044, 1], [2045, 1], [2046, 1], [2047, 1], [2048, 1], [2049, 1],
    [2050, 1], [2051, 1], [2052, 1], [2053, 1], [2054, 1], [2055, 1], [2056, 1],
    [2057, 1], [2058, 1], [2059, 1], [2060, 1], [2061, 1], [2062, 1], [2063, 1],
    [2064, 1], [2065, 1], [2066, 1], [2067, 1], [2068, 1], [2069, 1], [2070, 1],
    [2071, 1], [2072, 1], [2073, 1], [2074, 1], [2075, 1], [2076, 1], [2077, 1],
    [2078, 1], [2079, 1], [2080, 1], [2081, 1], [2082, 1], [2083, 1], [2084, 1],
    [2085, 1], [2086, 1], [2087, 1], [2088, 1], [2089, 1], [2090, 1], [2091, 1],
    [2092, 1], [2093, 1], [2094, 1], [2095, 1], [2096, 1], [2097, 1], [2098, 1],
    [2099, 1], [2100, 1], [2101, 1], [2102, 1], [2103, 1], [2104, 1], [2105, 1],
    [2106, 1], [2107, 1], [2108, 1], [2109, 1], [2110, 1], [2111, 1], [2112, 1],
    [2113, 1], [2114, 1], [2115, 1], [2116, 1], [2117, 1], [2118, 1], [2119, 1],
    [2120, 1], [2121, 1], [2122, 1], [2123, 1], [2124, 1], [2125, 1], [2126, 1],
    [2127, 1], [2128, 1], [2129, 1], [2130, 1], [2131, 1], [2132, 1], [2133, 1],
    [2134, 1], [2135, 1], [2136, 1], [2137, 1], [2138, 1], [2139, 1]])

