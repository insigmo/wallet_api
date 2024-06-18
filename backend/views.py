from rest_framework import viewsets
from backend.models import Wallet, Transaction, session
from backend.serializers import WalletSerializer, TransactionSerializer
from rest_framework import filters


class WalletViewSet(viewsets.ModelViewSet):
    serializer_class = WalletSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['label', 'balance']
    search_fields = ['label']

    def get_queryset(self):
        return session.query(Wallet).all()

    def perform_create(self, serializer):
        new_wallet = Wallet(label=serializer.validated_data['label'], balance=serializer.validated_data['balance'])
        session.add(new_wallet)
        session.commit()
        return new_wallet


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['txid', 'amount']
    search_fields = ['txid', 'wallet__label']

    def get_queryset(self):
        return session.query(Transaction).all()
