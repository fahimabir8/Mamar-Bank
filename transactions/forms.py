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
    
class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        return amount 
    


class TransferForm(forms.Form):
    recipient_account_no = forms.IntegerField(label="Recipient Account Number")
    amount = forms.DecimalField(max_digits=12, decimal_places=2, label="Amount")

    def __init__(self, *args, **kwargs):
        self.sender_account = kwargs.pop('sender_account')
        super().__init__(*args, **kwargs)

    def clean_recipient_account_no(self):
        recipient_account_no = self.cleaned_data.get('recipient_account_no')
        try:
            self.recipient_account = UserBankAccount.objects.get(account_no=recipient_account_no)
        except UserBankAccount.DoesNotExist:
            raise forms.ValidationError('Recipient account does not exist.')
        return recipient_account_no

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount < 2000:
            raise forms.ValidationError('The amount must be greater than 2000.')
        if amount > self.sender_account.balance:
            raise forms.ValidationError('You donot have enough balance in your account.')
        return amount