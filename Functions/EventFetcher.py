from web3 import Web3
from web3._utils.events import get_event_data
from web3._utils.filters import construct_event_filter_params


class EventFetcher:
    def __init__(self, web3: Web3, event = None, argument_filters=None, from_block=None, to_block="latest", address=None, topics=None):
        if from_block is None:
            raise TypeError("Missing mandatory keyword argument to getLogs: from_Block")

        self.web3 = web3
        self.event = event
        self.argument_filters = dict()
        self.argument_filters.update(argument_filters or {})
        self.from_block = from_block
        self.to_block = to_block
        self.address = address
        self.topics = topics

    def fetch_events(self):
        abi = self.event._get_event_abi()
        abi_codec = self.event.web3.codec

        data_filter_set, event_filter_params = construct_event_filter_params(
            abi,
            abi_codec,
            contract_address=self.event.address,
            argument_filters=self.argument_filters,
            fromBlock=self.from_block,
            toBlock=self.to_block,
            address=self.address,
            topics=self.topics,
        )

        logs = self.event.web3.eth.getLogs(event_filter_params)

        for entry in logs:
            data = get_event_data(abi_codec, abi, entry)
            yield data
