# MIT License
#
# Copyright (c) 2019 Jettson Lim, jettson.lim@groundx.xyz
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


from blockchainetl.jobs.exporters.composite_item_exporter import CompositeItemExporter

BLOCK_FIELDS_TO_EXPORT = [
    'number',
    'hash',
    'parent_hash',
    'logs_bloom',
    'transactions_root',
    'state_root',
    'receipts_root',
    'size',
    'extra_data',
    'gas_limit',
    'gas_used',
    'timestamp',
    'unix_timestamp',
    'transaction_count',

    'block_score',
    'total_block_score',

    'governance_data',
    'vote_data',

    'committee',
    'proposer',
    'reward_address'

]

TRANSACTION_FIELDS_TO_EXPORT = [
    'hash',
    'nonce',
    'block_hash',
    'block_number',
    'block_timestamp',
    'block_unix_timestamp',

    'transaction_index',
    'from_address',
    'to_address',
    'value',
    'gas',
    'gas_price',
    'input',

    'receipt_gas_used',
    'receipt_contract_address',
    'receipt_status',

    'fee_payer',
    'fee_payer_signatures',
    'fee_ratio',
    'sender_tx_hash',
    'signatures',
    'tx_type',
    'tx_type_int'
]

LOG_FIELDS_TO_EXPORT = [
    'block_hash',
    'block_number',
    'block_timestamp',
    'block_unix_timestamp',
    'transaction_hash',
    'transaction_index',
    'transaction_receipt_status',
    'log_index',
    'address',
    'data',
    'topics'
]

TOKEN_TRANSFER_FIELDS_TO_EXPORT = [
    'token_address',
    'from_address',
    'to_address',
    'value',
    'block_hash',
    'block_number',
    'block_timestamp',
    'block_unix_timestamp',
    'transaction_hash',
    'transaction_index',
    'transaction_receipt_status',
    'log_index',
]


def enrich_block_group_item_exporter(blocks_output=None, transactions_output=None, logs_output=None, token_transfers_output=None):
    return CompositeItemExporter(
        filename_mapping={
            'block': blocks_output,
            'transaction': transactions_output,
            'log': logs_output,
            'token_transfer': token_transfers_output
        },
        field_mapping={
            'block': BLOCK_FIELDS_TO_EXPORT,
            'transaction': TRANSACTION_FIELDS_TO_EXPORT,
            'log': LOG_FIELDS_TO_EXPORT,
            'token_transfer': TOKEN_TRANSFER_FIELDS_TO_EXPORT
        }
    )
