import hashlib
import json

from rest_framework_json_api import serializers
from backend.models import Wallet, Transaction, session


class WalletSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    label = serializers.CharField(max_length=255)
    balance = serializers.IntegerField()

    class Meta:
        model = Wallet
        fields = ['id', 'label', 'balance']
        resource_name = 'wallet'

    def create(self, validated_data):
        wallet = Wallet(**validated_data)
        session.add(wallet)
        session.commit()
        return wallet

    def update(self, instance, validated_data):
        instance.label = validated_data.get('label', instance.label)
        instance.balance = validated_data.get('balance', instance.balance)
        session.commit()
        return instance


class TransactionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    txid = serializers.CharField(max_length=255)
    amount = serializers.DecimalField(max_digits=36, decimal_places=18)
    wallet_id = serializers.IntegerField()

    class Meta:
        model = Transaction
        fields = ['id', 'txid', 'amount', 'wallet_id']
        resource_name = 'transaction'

    def create(self, validated_data):
        wallet_id = validated_data.pop('wallet_id')
        wallet = session.query(Wallet).get(wallet_id)
        if not wallet:
            raise serializers.ValidationError("Wallet not found")
        transaction = Transaction(wallet=wallet, **validated_data)
        transaction.save()
        return transaction
