from django import forms
from .models import Transaction
from accounts.models import UserBankAccount

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type']
    
    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True
        self.fields['transaction_type'].widget = forms.HiddenInput()
        
    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()
    
class DepositForm(TransactionForm):
    def clean_amount(self):
        min_deposit_amount = 500
        amount = self.cleaned_data.get('amount')
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount}$'
            )
            
        return amount 
    
    
class WithdrawForm(TransactionForm):
    def clean_amount(self):
        account = self.account 
        min_withdraw_amount = 400
        max_withdraw_amount = 2000000
        balance = account.balance 
        amount = self.cleaned_data.get('amount')
        if self.account.bank.bankruptcy:
            raise forms.ValidationError(
                f'Sorry. You cannot withdraw as the bank is bankrupt.'
            )
        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at least {min_withdraw_amount} $'
            )
        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw most {max_withdraw_amount}'
            )
        if amount > balance:
            raise forms.ValidationError(
                f'You have {balance} $ in your account.'
                'You can not withdraw more than your account balance'            
            )
                
        return amount 
    
    
class TransferForm(forms.ModelForm):
    
    class Meta:
        model = Transaction
        fields = ['account_number', 'amount', 'transaction_type']
    
    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True
        self.fields['transaction_type'].widget = forms.HiddenInput()
        
    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()
    
    def clean_amount(self):
        account = self.account 
        balance = account.balance 
        min_transfer = 3000
        max_transfer = balance - 2000
        amount = self.cleaned_data.get('amount')
        if self.account.bank.bankruptcy:
            raise forms.ValidationError(
                f'Sorry. You cannot transfer as the bank is bankrupt.'
            )
        if amount < min_transfer:
            raise forms.ValidationError(
                f'You have to transfer at least {min_transfer} $'
            )
        if amount > max_transfer:
            raise forms.ValidationError(
                f'You can transfer most {max_transfer} $'
            )
        if amount > balance:
            raise forms.ValidationError(
                f'You have {balance} $ in your account.'
                'You can not transfer more than your account balance'            
            )
                
        return amount
    
    def clean_account_number(self):
        account_no = self.cleaned_data.get('account_number')
                
        return account_no


class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        return amount 
    