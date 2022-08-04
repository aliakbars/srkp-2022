from pathlib import Path

import pandas as pd


# tickers = pd.read_csv(Path('srkp-2022') / 'tickers.txt', header=None)[0].tolist()
# df = []
# for ticker in tickers:
#     try:
#         df.append(pd.DataFrame(read_financials(ticker).rename(ticker)))
#         print(ticker)
#     except FileNotFoundError:
#         print(f'----{ticker}')
# df = pd.concat(df, axis=1).T


def read_financials(ticker, year=2018, dirpath=Path('data') / 'financials'):
    fpath = dirpath / str(year) / f'FinancialStatement-{year}-Tahunan-{ticker}.xlsx'

    df_general = pd.read_excel(fpath, sheet_name='1000000', skiprows=3, header=None)
    x_general = df_general.set_index(2)[1]

    df_bsheet = pd.read_excel(fpath, sheet_name='4220000', skiprows=3, header=None)
    x_bsheet = df_bsheet.set_index(3)[1]
    
    try:
        df_income = pd.read_excel(fpath, sheet_name='4312000', skiprows=3, header=None)
    except ValueError as err:
        assert str(err).startswith("Worksheet named '") and str(err).endswith("' not found")
        df_income = pd.read_excel(fpath, sheet_name='4322000', skiprows=3, header=None)
        
    x_income = df_income.set_index(3)[1]

    df_cash_flows = pd.read_excel(fpath, sheet_name='4510000', skiprows=3, header=None)
    x_cash_flows = df_cash_flows.set_index(3)[1]

    multiplier = x_general['Level of rounding used in financial statements']
    multiplier = multiplier.split()[0]
    multiplier = {
        'Satuan': 1,
        'Ribuan': 1000,
        'Jutaan': 1000_000,
        }[multiplier]

    x = pd.Series({
        'assets': x_bsheet['Total assets'],
        'cash_and_current_accounts_in_bi': x_bsheet['Cash'] + x_bsheet['Current accounts with bank Indonesia'],
        'earning_assets': x_bsheet[list_earning_assets].sum() - x_bsheet[list_earning_assets_contra].sum(),

        'liabilities': x_bsheet['Total liabilities'],

        'interest_income': x_income['Interest income'],
        'noninterest_income': x_income[list_noninterest_income].sum(),
        'other_operating_income': x_income[list_other_operating_income].sum(),

        'interest_expenses': x_income['Interest expenses'],
        'noninterest_expenses': x_income[list_noninterest_expenses].sum(),
        'other_operating_expenses': x_income[list_other_operating_expenses].sum(),

        'net_income': x_income['Total comprehensive income'],
    })

    x *= multiplier
    
    x['leverage'] = x['liabilities'] / x['assets']
    x['operating_income'] = x[['interest_income', 'noninterest_income', 'other_operating_income']].sum()
    x['operating_expenses'] = x[['interest_expenses', 'noninterest_expenses', 'other_operating_expenses']].sum()
    x['net_operating_income'] = x['operating_income'] - x['operating_expenses']
    x['nim'] = (x['interest_income'] - x['interest_expenses']) / x['earning_assets']
    x['bopo'] = x['operating_expenses'] / x['operating_income']
    x['eps'] = x_income['Basic earnings (loss) per share from continuing operations']
    
    return x


list_earning_assets = [
    'Placements with bank Indonesia and other banks third parties',
    'Placements with bank Indonesia and other banks related parties',
    
    'Derivative receivables third parties',
    'Derivative receivables related parties',
    
    'Marketable securities third parties',
    'Marketable securities related parties',
    'Investments of policyholder in unit-linked contracts',
    'Securities purchased under agreement to resale',
    'Government bonds',
    
    'Acceptance receivables third parties',
    'Acceptance receivables related parties',
    
    #'Loans',
    'Loans third parties',
    'Loans related parties',
    'Receivables from clearing and settlement guarantee institution',
    #'Receivables from customers',
    'Receivables from customers third parties',
    'Receivables from customers related parties',
    #'Murabahah receivables',
    'Murabahah receivables third parties',
    'Murabahah receivables related parties',
    #'Istishna receivables',
    'Istishna receivables third parties',
    'Istishna receivables related parties',
    #'Ijarah receivables',
    'Ijarah receivables third parties',
    'Ijarah receivables related parties',
    #'Consumer financing receivables',
    'Consumer financing receivables third parties',
    'Consumer financing receivables related parties',
    #'Qardh funds',
    'Qardh funds third parties',
    'Qardh funds related parties',
    #'Mudharabah financing',
    'Mudharabah financing third parties',
    'Mudharabah financing related parties',
    #'Musyarakah financing',
    'Musyarakah financing third parties',
    'Musyarakah financing related parties',
    'Factoring receivables third parties',
    'Factoring receivables related parties',
    'Factoring receivables on deferred factoring income',
    
    'Investments accounted for using equity method',
    'Investments in subsidiaries',
    'Investments in joint ventures',
    'Investments in associates',
    ]

list_earning_assets_contra = [
    'Allowance for impairment losses for placements with other banks',
    'Allowance for impairment losses for marketable securities',
    'Allowance for impairment losses for acceptance receivables',
    'Allowance for impairment losses for loans',
    'Allowance for impairment losses for receivables from customers',
    'Allowance for impairment losses for murabahah receivables',
    'Allowance for impairment losses for istishna receivables',
    'Allowance for impairment losses for ijarah receivables',
    'Allowance for impairment losses for consumer financing receivables',
    'Allowance for impairment losses for qardh funds',
    'Allowance for impairment losses for mudharabah financing',
    'Allowance for impairment losses for musyarakah financing',
    'Allowance for impairment losses for factoring receivables',
    ]

list_noninterest_income = [
    'Revenue from fund management as mudharib',
    'Third parties share on return of temporary syirkah funds',
    #'Insurance income',
    'Revenue from insurance premiums',
    'Decrease (increase) in unearned premiums',
    'Insurance commission income',
    'Net investment income',
    'Ujrah received',
    'Other insurance income',
    'Reinsurance claims',
    'Retrocession claims',
    'Increase (decrease) in insurance liabilities ceded to reinsurers',
    #'Financing income',
    'Revenue from consumer financing',
    'Revenue from finance lease',
    'Revenue from operating lease',
    'Revenue from factoring',
    #'Securities income',
    'Revenue from underwriting activities and selling fees',
    'Revenue from financing transactions',
    'Revenue from securities administration service',
    'Revenue from investment management services',
    'Revenue from financial advisory services',
    'Realised gains (losses) on trading of marketable securities',
    'Gains (losses) on changes in fair value of marketable securities',
    #'Recovery of impairment loss',
    'Recovery of impairment loss of financial assets',
    'Recovery of impairment loss of financial assets finance lease',
    'Recovery of impairment loss of financial assets consumer financing receivables',
    'Recovery of impairment loss of non-financial assets',
    'Recovery of impairment loss of non-financial assets repossessed collaterals',
    'Recovery of estimated loss of commitments and contingency',
    'Reversal (expense) of estimated losses on commitments and contingencies',
    ]

list_noninterest_expenses = [
    'Reinsurance premiums',
    'Retrocession premiums',
    'Decrease (increase) in premium income ceded to reinsurancer',
    #'Insurance expenses',
    'Claim expenses',
    'Increase (decrease) in estimated claims liability',
    'Increase (decrease) in liability for future policy benefit',
    'Increase (decrease) in provision for losses arising from liability adequacy test',
    'Increase (decrease) in liabilities to policyholder in unit-linked contracts',
    'Insurance commission expenses',
    'Ujrah paid',
    'Acquisition costs of insurance contracts',
    'Other insurance expenses',
    #'Allowances for impairment losses',
    'Allowances for impairment losses on earnings assets',
    'Allowances for impairment losses on non-earnings assets',
    ]

list_other_operating_income = [
    'Investments income',
    'Provisions and commissions income from transactions other than loan',
    'Revenue from trading transactions',
    'Dividends income',
    'Realised gains (losses) from derivative instruments',
    'Revenue from recovery of written-off assets',
    'Gains (losses) on changes in foreign exchange rates',
    'Gains (losses) on disposal of property and equipment',
    'Gains (losses) on disposal of foreclosed assets',
    'Other operating income',
    ]

list_other_operating_expenses = [
    'General and administrative expenses',
    'Selling expenses',
    'Rent, maintenance and improvement expenses',
    'Other fees and commissions expenses',
    'Other operating expenses',
    ]
