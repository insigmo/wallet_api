from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, validates
from django.conf import settings

Base = declarative_base()

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
session = sessionmaker(bind=engine)()


class Wallet(Base):
    __tablename__ = 'wallet'

    id = Column(Integer, primary_key=True)
    label = Column(String(255))
    balance = Column(Integer, default=0)

    transactions = relationship("Transaction", back_populates="wallet")

    @validates('balance')
    def validate_balance(self, balance):
        if balance < 0:
            raise ValueError("Wallet balance cannot be negative")
        return balance

    class Meta:
        ordering = ['label']


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    wallet_id = Column(Integer, ForeignKey('wallets.id'))
    txid = Column(String(255), unique=True)
    amount = Column(Numeric(36, 18))

    wallet = relationship("Wallet", back_populates="transactions")

    class Meta:
        ordering = ['wallet_id']

    def save(self):
        self.wallet.balance += self.amount
        if self.wallet.balance < 0:
            raise ValueError("Wallet balance cannot be negative")

        session.add(self)
        session.add(self.wallet)
        session.commit()

    def delete(self):
        self.wallet.balance -= self.amount
        if self.wallet.balance < 0:
            raise ValueError("Wallet balance cannot be negative")

        session.delete(self)
        session.add(self.wallet)
        session.commit()
