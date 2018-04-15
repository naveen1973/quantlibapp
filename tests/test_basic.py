import pytest
from quantlibapp.core import ConsumerLoan

## Part I: Input Type Error Handler Test --------------------------------------------------
def test_negative_notional_amountErrorHandling():
    with pytest.raises(ValueError) as excinfo:
        ConsumerLoanClass = ConsumerLoan(notional_amount=-1)
        ConsumerLoanClass._checkDataType()
    assert str(excinfo.value) == "'notional_amount' must be an float larger than 0"
    
def test_float_termErrorHandling():
    with pytest.raises(ValueError) as excinfo:
        ConsumerLoanClass = ConsumerLoan(term_in_tenor=2.5)
        ConsumerLoanClass._checkDataType()
    assert str(excinfo.value) == "'term_in_tenor' must be an integer between 1 and 240"

def test_long_termErrorHandling():
    with pytest.raises(ValueError) as excinfo:
        ConsumerLoanClass = ConsumerLoan(term_in_tenor=1000)
        ConsumerLoanClass._checkDataType()
    assert str(excinfo.value) == "'term_in_tenor' must be an integer between 1 and 240"

def test_large_APRErrorHandling():
    with pytest.raises(ValueError) as excinfo:
        ConsumerLoanClass = ConsumerLoan(annual_percentage_rate=2)
        ConsumerLoanClass._checkDataType()
    assert str(excinfo.value) == "'annual_percentage_rate' must be an float between 0 and 1"

def test_negative_APRErrorHandling():
    with pytest.raises(ValueError) as excinfo:
        ConsumerLoanClass = ConsumerLoan(annual_percentage_rate=-1)
        ConsumerLoanClass._checkDataType()
    assert str(excinfo.value) == "'annual_percentage_rate' must be an float between 0 and 1"
    
def test_negative_repayment_dayErrorHandling():
    with pytest.raises(ValueError) as excinfo:
        ConsumerLoanClass = ConsumerLoan(repayment_day=-1)
        ConsumerLoanClass._checkDataType()
    assert str(excinfo.value) == "'repayment_day' must be an integer between 1 and 31"

def test_large_repayment_dayErrorHandling():
    with pytest.raises(ValueError) as excinfo:
        ConsumerLoanClass = ConsumerLoan(repayment_day=32)
        ConsumerLoanClass._checkDataType()
    assert str(excinfo.value) == "'repayment_day' must be an integer between 1 and 31"

def test_float_repayment_dayErrorHandling():
    with pytest.raises(ValueError) as excinfo:
        ConsumerLoanClass = ConsumerLoan(repayment_day=1.5)
        ConsumerLoanClass._checkDataType()
    assert str(excinfo.value) == "'repayment_day' must be an integer between 1 and 31"

## Part II: Schedule Calender --------------------------------------------------

## Regular Sample
def test_sample1():
    import datetime
    import numpy as np
    ConsumerLoanClass = ConsumerLoan(notional_amount=100000.0, 
                                     term_in_tenor=24, 
                                     annual_percentage_rate=0.05,
                                     effective_date=datetime.datetime.today(),
                                     repayment_day=10)
    ## duration test
    ConsumerLoanClass.process()
    durationOutput = ConsumerLoanClass.output.End_Date.values[-1] - ConsumerLoanClass.output.Start_Date.values[0]
    expectedSDuration = ConsumerLoanClass.term_in_tenor * 28
    expectedLDuration = (ConsumerLoanClass.term_in_tenor+1) * 31
    
    ## total payment
    totalpaymentOutput = np.round(np.sum(ConsumerLoanClass.output.Payment.values), 2)
    borrowedAmount = ConsumerLoanClass.notional_amount
    
    ## interest+principal=payment
    totalInterest = np.sum(ConsumerLoanClass.output.Interest.values)
    totalPrincipal = np.sum(ConsumerLoanClass.output.Principal.values)
    totalIPlusP = np.round(totalInterest + totalPrincipal, 2)
    
    ## duration test
    assert durationOutput <= expectedLDuration and durationOutput >= expectedSDuration
    ## total payment
    assert totalpaymentOutput >= borrowedAmount
    ## interest+principal=payment
    assert totalpaymentOutput == totalIPlusP
    ## principal=borrowed
    assert totalPrincipal == borrowedAmount
    
    
## Small Amount Sample
def test_sample2():
    import datetime
    import numpy as np
    ConsumerLoanClass = ConsumerLoan(notional_amount=1, 
                                     term_in_tenor=24, 
                                     annual_percentage_rate=0.05,
                                     effective_date=datetime.datetime.today(),
                                     repayment_day=10)
    ## duration test
    ConsumerLoanClass.process()
    durationOutput = ConsumerLoanClass.output.End_Date.values[-1] - ConsumerLoanClass.output.Start_Date.values[0]
    expectedSDuration = ConsumerLoanClass.term_in_tenor * 28
    expectedLDuration = (ConsumerLoanClass.term_in_tenor+1) * 31
    
    ## total payment
    totalpaymentOutput = np.round(np.sum(ConsumerLoanClass.output.Payment.values), 2)
    borrowedAmount = ConsumerLoanClass.notional_amount
    
    ## interest+principal=payment
    totalInterest = np.sum(ConsumerLoanClass.output.Interest.values)
    totalPrincipal = np.sum(ConsumerLoanClass.output.Principal.values)
    totalIPlusP = np.round(totalInterest + totalPrincipal, 2)
    
    ## duration test
    assert durationOutput <= expectedLDuration and durationOutput >= expectedSDuration
    ## total payment
    assert totalpaymentOutput >= borrowedAmount
    ## interest+principal=payment
    assert totalpaymentOutput == totalIPlusP
    ## principal=borrowed
    assert totalPrincipal == borrowedAmount
    

## Short Duration
def test_sample3():
    import datetime
    import numpy as np
    ConsumerLoanClass = ConsumerLoan(notional_amount=100000.0, 
                                     term_in_tenor=1, 
                                     annual_percentage_rate=0.05,
                                     effective_date=datetime.datetime.today(),
                                     repayment_day=10)
    ## duration test
    ConsumerLoanClass.process()
    durationOutput = ConsumerLoanClass.output.End_Date.values[-1] - ConsumerLoanClass.output.Start_Date.values[0]
    expectedSDuration = ConsumerLoanClass.term_in_tenor * 28
    expectedLDuration = (ConsumerLoanClass.term_in_tenor+1) * 31
    
    ## total payment
    totalpaymentOutput = np.round(np.sum(ConsumerLoanClass.output.Payment.values), 2)
    borrowedAmount = ConsumerLoanClass.notional_amount
    
    ## interest+principal=payment
    totalInterest = np.sum(ConsumerLoanClass.output.Interest.values)
    totalPrincipal = np.sum(ConsumerLoanClass.output.Principal.values)
    totalIPlusP = np.round(totalInterest + totalPrincipal, 2)
    
    ## duration test
    assert durationOutput <= expectedLDuration and durationOutput >= expectedSDuration
    ## total payment
    assert totalpaymentOutput >= borrowedAmount
    ## interest+principal=payment
    assert totalpaymentOutput == totalIPlusP
    ## principal=borrowed
    assert totalPrincipal == borrowedAmount
    
## Long Duration
def test_sample4():
    import datetime
    import numpy as np
    ConsumerLoanClass = ConsumerLoan(notional_amount=100000.0, 
                                     term_in_tenor=240, 
                                     annual_percentage_rate=0.05,
                                     effective_date=datetime.datetime.today(),
                                     repayment_day=10)
    ## duration test
    ConsumerLoanClass.process()
    durationOutput = ConsumerLoanClass.output.End_Date.values[-1] - ConsumerLoanClass.output.Start_Date.values[0]
    expectedSDuration = ConsumerLoanClass.term_in_tenor * 28
    expectedLDuration = (ConsumerLoanClass.term_in_tenor+1) * 31
    
    ## total payment
    totalpaymentOutput = np.round(np.sum(ConsumerLoanClass.output.Payment.values), 2)
    borrowedAmount = ConsumerLoanClass.notional_amount
    
    ## interest+principal=payment
    totalInterest = np.sum(ConsumerLoanClass.output.Interest.values)
    totalPrincipal = np.sum(ConsumerLoanClass.output.Principal.values)
    totalIPlusP = np.round(totalInterest + totalPrincipal, 2)
    
    ## duration test
    assert durationOutput <= expectedLDuration and durationOutput >= expectedSDuration
    ## total payment
    assert totalpaymentOutput >= borrowedAmount
    ## interest+principal=payment
    assert totalpaymentOutput == totalIPlusP
    ## principal=borrowed
    assert totalPrincipal == borrowedAmount
    
## High Interest
def test_sample5():
    import datetime
    import numpy as np
    ConsumerLoanClass = ConsumerLoan(notional_amount=100000.0, 
                                     term_in_tenor=24, 
                                     annual_percentage_rate=0.99,
                                     effective_date=datetime.datetime.today(),
                                     repayment_day=10)
    ## duration test
    ConsumerLoanClass.process()
    durationOutput = ConsumerLoanClass.output.End_Date.values[-1] - ConsumerLoanClass.output.Start_Date.values[0]
    expectedSDuration = ConsumerLoanClass.term_in_tenor * 28
    expectedLDuration = (ConsumerLoanClass.term_in_tenor+1) * 31
    
    ## total payment
    totalpaymentOutput = np.round(np.sum(ConsumerLoanClass.output.Payment.values), 2)
    borrowedAmount = ConsumerLoanClass.notional_amount
    
    ## interest+principal=payment
    totalInterest = np.sum(ConsumerLoanClass.output.Interest.values)
    totalPrincipal = np.sum(ConsumerLoanClass.output.Principal.values)
    totalIPlusP = np.round(totalInterest + totalPrincipal, 2)
    
    ## duration test
    assert durationOutput <= expectedLDuration and durationOutput >= expectedSDuration
    ## total payment
    assert totalpaymentOutput >= borrowedAmount
    ## interest+principal=payment
    assert totalpaymentOutput == totalIPlusP
    ## principal=borrowed
    assert totalPrincipal == borrowedAmount
    
## Low Interest
def test_sample5():
    import datetime
    import numpy as np
    ConsumerLoanClass = ConsumerLoan(notional_amount=100000.0, 
                                     term_in_tenor=24, 
                                     annual_percentage_rate=0.0001,
                                     effective_date=datetime.datetime.today(),
                                     repayment_day=10)
    ## duration test
    ConsumerLoanClass.process()
    durationOutput = ConsumerLoanClass.output.End_Date.values[-1] - ConsumerLoanClass.output.Start_Date.values[0]
    expectedSDuration = ConsumerLoanClass.term_in_tenor * 28
    expectedLDuration = (ConsumerLoanClass.term_in_tenor+1) * 31
    
    ## total payment
    totalpaymentOutput = np.round(np.sum(ConsumerLoanClass.output.Payment.values), 2)
    borrowedAmount = ConsumerLoanClass.notional_amount
    
    ## interest+principal=payment
    totalInterest = np.sum(ConsumerLoanClass.output.Interest.values)
    totalPrincipal = np.sum(ConsumerLoanClass.output.Principal.values)
    totalIPlusP = np.round(totalInterest + totalPrincipal, 2)
    
    ## duration test
    assert durationOutput <= expectedLDuration and durationOutput >= expectedSDuration
    ## total payment
    assert totalpaymentOutput >= borrowedAmount
    ## interest+principal=payment
    assert totalpaymentOutput == totalIPlusP
    ## principal=borrowed
    assert totalPrincipal == borrowedAmount