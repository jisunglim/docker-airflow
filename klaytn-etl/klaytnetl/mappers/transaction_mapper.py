# MIT License
#
# Copyright (c) 2019 Jettson Lim, jettson.lim@groundx.xyz
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from klaytnetl.mappers.receipt_log_mapper import EthReceiptLogMapper
from klaytnetl.mappers.receipt_log_mapper import KlaytnReceiptLogMapper

from klaytnetl.domain.transaction import EthTransaction
from klaytnetl.domain.transaction import KlaytnRawTransaction, KlaytnTransaction

from klaytnetl.utils import hex_to_dec, to_normalized_address

from typing import Union

class EthTransactionMapper(object):
    def json_dict_to_transaction(self, json_dict, **kwargs):
        transaction = EthTransaction()
        transaction.hash = json_dict.get('transactionHash')
        transaction.nonce = hex_to_dec(json_dict.get('nonce'))
        transaction.block_hash = json_dict.get('blockHash')
        transaction.block_number = hex_to_dec(json_dict.get('blockNumber'))
        transaction.block_timestamp = kwargs.get('block_timestamp')
        transaction.transaction_index = hex_to_dec(json_dict.get('transactionIndex'))
        transaction.from_address = to_normalized_address(json_dict.get('from'))
        transaction.to_address = to_normalized_address(json_dict.get('to'))
        transaction.value = hex_to_dec(json_dict.get('value'))
        transaction.gas = hex_to_dec(json_dict.get('gas'))
        transaction.gas_price = hex_to_dec(json_dict.get('gasPrice'))
        transaction.input = json_dict.get('input')

        # Klaytn additional properties
        transaction.fee_payer = json_dict.get('feePayer')
        transaction.fee_payer_signatures = json_dict.get('feePayerSignatures')
        # FIXME: deal with null input
        transaction.fee_ratio = hex_to_dec(json_dict.get('feeRatio'))

        transaction.sender_tx_hash = json_dict.get('senderTxHash')
        transaction.signatures = json_dict.get('signatures')

        transaction.tx_type = json_dict.get('type')
        transaction.tx_type_int = json_dict.get('typeInt')

        return transaction

    def transaction_to_dict(self, transaction):
        return {
            'type': 'transaction',
            'hash': transaction.hash,
            'nonce': transaction.nonce,
            'block_hash': transaction.block_hash,
            'block_number': transaction.block_number,
            'block_timestamp': transaction.block_timestamp,
            'transaction_index': transaction.transaction_index,
            'from_address': transaction.from_address,
            'to_address': transaction.to_address,
            'value': transaction.value,
            'gas': transaction.gas,
            'gas_price': transaction.gas_price,
            'input': transaction.input,

            # Klaytn additional properties
            'fee_payer': transaction.fee_payer,
            'fee_payer_signatures': transaction.fee_payer_signatures,
            'fee_ratio': transaction.fee_ratio,

            'sender_tx_hash': transaction.sender_tx_hash,
            'signatures': transaction.signatures,

            'tx_type': transaction.tx_type,
            'tx_type_int': transaction.tx_type_int
        }


class KlaytnTransactionMapper(object):
    def __init__(self, receipt_log_mapper=None, enrich=False):
        if receipt_log_mapper is None:
            self.receipt_log_mapper = KlaytnReceiptLogMapper(enrich=enrich)
        else:
            self.receipt_log_mapper = receipt_log_mapper

        self.enrich = enrich

    def json_dict_to_transaction(self, json_dict, **kwargs) -> Union[KlaytnTransaction, KlaytnRawTransaction]:
        _transaction = KlaytnRawTransaction()

        _transaction.hash = json_dict.get('transactionHash')
        _transaction.nonce = hex_to_dec(json_dict.get('nonce'))
        _transaction.block_hash = json_dict.get('blockHash')
        _transaction.block_number = hex_to_dec(json_dict.get('blockNumber'))
        _transaction.transaction_index = hex_to_dec(json_dict.get('transactionIndex'))
        _transaction.from_address = to_normalized_address(json_dict.get('from'))
        _transaction.to_address = to_normalized_address(json_dict.get('to'))
        _transaction.value = hex_to_dec(json_dict.get('value'))
        _transaction.gas = hex_to_dec(json_dict.get('gas'))
        _transaction.gas_price = hex_to_dec(json_dict.get('gasPrice'))
        _transaction.input = json_dict.get('input')

        # Klaytn additional properties
        _transaction.fee_payer = json_dict.get('feePayer')
        _transaction.fee_payer_signatures = json_dict.get('feePayerSignatures')
        # FIXME: deal with null input
        _transaction.fee_ratio = hex_to_dec(json_dict.get('feeRatio'))

        _transaction.sender_tx_hash = json_dict.get('senderTxHash')
        _transaction.signatures = json_dict.get('signatures')

        _transaction.tx_type = json_dict.get('type')
        _transaction.tx_type_int = json_dict.get('typeInt')

        if self.enrich and 'logs' in json_dict:
            _transaction.logs = [
                self.receipt_log_mapper.json_dict_to_receipt_log(log,
                    block_timestamp=kwargs.get('block_timestamp'),
                    block_timestamp_fos=kwargs.get('block_timestamp_fos'),
                    transaction_receipt_status=hex_to_dec(json_dict.get('status')),
                    enrich=self.enrich)
                for log in json_dict['logs']
            ]
        else:
            del _transaction.logs

        return _transaction if not self.enrich else KlaytnTransaction.enrich(_transaction,
            block_timestamp=kwargs.get('block_timestamp'),
            block_timestamp_fos=kwargs.get('block_timestamp_fos'),
            receipt_gas_used=hex_to_dec(json_dict.get('gasUsed')),
            receipt_status=hex_to_dec(json_dict.get('status')),
            receipt_contract_address=to_normalized_address(json_dict.get('contractAddress')))

    def transaction_to_dict(self, transaction: Union[KlaytnTransaction, KlaytnRawTransaction]) -> dict:
        # FIXME
        transaction_dict = {
            'type': 'transaction',
            'hash': transaction.hash,
            'nonce': transaction.nonce,
            'block_hash': transaction.block_hash,
            'block_number': transaction.block_number,
            'transaction_index': transaction.transaction_index,
            'from_address': transaction.from_address,
            'to_address': transaction.to_address,
            'value': transaction.value,
            'gas': transaction.gas,
            'gas_price': transaction.gas_price,
            'input': transaction.input,

            # Klaytn additional properties
            'fee_payer': transaction.fee_payer,
            'fee_payer_signatures': transaction.fee_payer_signatures,
            'fee_ratio': transaction.fee_ratio,

            'sender_tx_hash': transaction.sender_tx_hash,
            'signatures': transaction.signatures,

            'tx_type': transaction.tx_type,
            'tx_type_int': transaction.tx_type_int
        }

        if self.enrich and isinstance(transaction, KlaytnTransaction):
            transaction_dict['block_unix_timestamp'] = transaction.block_unix_timestamp
            transaction_dict['block_timestamp'] = transaction.block_timestamp
            transaction_dict['receipt_gas_used'] = transaction.receipt_gas_used
            transaction_dict['receipt_contract_address'] = transaction.receipt_contract_address
            transaction_dict['receipt_status'] = transaction.receipt_status

        return transaction_dict