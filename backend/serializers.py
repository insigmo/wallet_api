from rest_framework_json_api import serializers
from backend.models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'label', 'balance']
        resource_name = 'wallet'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'txid', 'amount', 'wallet_id']
        resource_name = 'transactions'
