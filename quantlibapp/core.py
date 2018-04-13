"""
Contains the core building blocks of the framework.
"""
import QuantLib as ql
import pandas as pd
import numpy as np
import datetime
import calendar
from scipy.optimize import root
import qgrid
import ipywidgets as widgets

class ConsumerLoan(object):
    
    """
    The ConsumerLoan is the main building block.
    Args:
        * notional_amount (double): The amount of the loan
        * term_in_tenor (integer): The duration of the loan (in tenor unit)
        * annual_percentage_rate (double): The rate of the loan p.a.
        * effective_date (date): The effective date of the loan
        * repayment_day (integer): The loan repayment day each month
        * calendar (QuantLib Object): Calendar of a country
        * tenor (QuantLib Object): Tenor of the term
        
    Attributes:
        
    """        
        
    def __init__(self):
        self._inputScreen()
    
    def _inputScreen(self, dfInput=None):
        if dfInput==None:
            self.dfInput = pd.DataFrame({'Notional Amount': [100000], 
                                     'Term in Months': [24], 
                                     'APR': [0.05], 
                                     'Repayment Day': [10], 
                                     'Effective Date': [datetime.datetime.today()]})
        else:
            self.dfInput = dfInput
        
        self.dfInputQG = qgrid.QgridWidget(df=self.dfInput, 
                                           show_toolbar=False)
        tab_content = ['Loan Details']
        children = [self.dfInputQG]
        tab = widgets.Tab()
        tab.children = children
        for i in range(len(children)):
            tab.set_title(i, str(tab_content[i]))
        self.input = tab
    
    def _setup(self):
        self.dfInput = self.dfInputQG.get_changed_df()
        self.notional_amount = self.dfInput.loc[0, 'Notional Amount']
        self.term_in_tenor = self.dfInput.loc[0, 'Term in Months']
        self.annual_percentage_rate = self.dfInput.loc[0, 'APR']
        self.effective_date = self.dfInput.loc[0, 'Effective Date']
        self.repayment_day = self.dfInput.loc[0, 'Repayment Day']
        self.calendar = ql.UnitedKingdom()
        self.tenor = ql.Period(ql.Monthly)

        self.effective_date = ql.DateParser.parseFormatted(
            self.effective_date.strftime('%Y-%m-%d'), 
            '%Y-%m-%d')
        _lastDate = calendar.monthrange(self.effective_date.year(), 
                                        self.effective_date.month())[1]
        _lastDate = np.minimum(_lastDate, 
                               self.repayment_day)
        self.first_date = ql.Date(int(_lastDate),
                                  self.effective_date.month(), 
                                  self.effective_date.year())
        if self.first_date < self.effective_date:
            self.first_date = self.first_date + ql.Period(1, ql.Months)
            
        self.termination_date = self.first_date + ql.Period(int(self.term_in_tenor), 
                                                            ql.Months)
        self.business_convention = ql.Following
        self.termination_business_convention = ql.Following
        self.date_generation = ql.DateGeneration.Backward
        self.end_of_month = False
         
        self.schedule = ql.Schedule(self.effective_date,
                                    self.termination_date,
                                    self.tenor,
                                    self.calendar,
                                    self.business_convention,
                                    self.termination_business_convention,
                                    self.date_generation,
                                    self.end_of_month, 
                                    self.first_date)
        
        d = {'Start_Date': list(self.schedule)[:-1], 
             'End_Date': list(self.schedule)[1:]}
        df = pd.DataFrame(data=d)
        dc = ql.Thirty360(ql.Thirty360.USA)
        df['Day_Count'] = df.apply(lambda x: dc.yearFraction(x['Start_Date'], 
                                                             x['End_Date']), 
                                   axis=1)
        df['Balance_Start'] = self.notional_amount
        df['Balance_End'] = self.notional_amount
        df.loc[df.shape[0]-1, 'Balance_End'] = 0
        df['Interest'] = 0
        df['Principal'] = 0
        df['Payment'] = 0
        self.schedule = df
    
    def _solve_annuity(self, y):
        df = self.schedule
        df['Payment'] = np.round(y[0], 2)
        for i in range(df.shape[0]):
            if i != 0:
                df.loc[i, 'Balance_Start'] = df.Balance_End[i-1]
            df.loc[i, 'Interest'] = np.round(df.Balance_Start[i] * df.Day_Count[i] * self.annual_percentage_rate, 2)
            df.loc[i, 'Principal'] = np.round(y[0] - df.Interest[i], 2)
            df.loc[i, 'Balance_End'] = np.round(df.Balance_Start[i] - df.Principal[i], 2)
    
        self.schedule = df
        
        return df.loc[df.shape[0]-1, 'Balance_End']
    
    def process(self):
        self._setup()
        solv = root(self._solve_annuity,
                    -np.pmt(self.annual_percentage_rate/12,
                            self.term_in_tenor, 
                            self.notional_amount),
                    method='hybr')
        self.annuity = solv.x
        self.output = self.schedule
        lastIndex = self.output.shape[0] - 1
        self.output.loc[lastIndex, 'Payment'] = self.output.Payment[lastIndex]  + self.output.Balance_End[lastIndex]
        self.output.loc[lastIndex, 'Principal'] = self.output.Principal[lastIndex]  + self.output.Balance_End[lastIndex]
        self.output.loc[lastIndex, 'Balance_End'] = 0