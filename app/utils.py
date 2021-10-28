import logging

import requests
from requests.exceptions import Timeout, ConnectionError

from .settings import VALIDATOR_ADDR


def get_prometheus_info(name, url):
    try:
        response = requests.get(url=url)
        return response.text
    except (Timeout, ConnectionError):
        logging.error(f"[{name}] Timeout connection")
        return None


def get_additional_info():
    try:
        response = requests.get(url="http://127.0.0.1:11000/api/valopers?all=true")
    except (Timeout, ConnectionError):
        logging.error("[Node info] Timeout connection")
        return None

    content = response.json()

    info = f"# HELP active_validators Active validators in network.\n" \
           f"# TYPE active_validators gauge\n" \
           f"active_validators {content['status']['active_validators']}\n" \
           f"# HELP paused_validators Paused validators in network.\n" \
           f"# TYPE paused_validators gauge\n" \
           f"paused_validators {content['status']['paused_validators']}\n" \
           f"# HELP inactive_validators Inactive validators in network.\n" \
           f"# TYPE inactive_validators gauge\n" \
           f"inactive_validators {content['status']['inactive_validators']}\n" \
           f"# HELP jailed_validators Paused validators in network.\n" \
           f"# TYPE jailed_validators gauge\n" \
           f"jailed_validators {content['status']['jailed_validators']}\n" \
           f"# HELP total_validators Paused validators in network.\n" \
           f"# TYPE total_validators gauge\n" \
           f"total_validators {content['status']['total_validators']}\n" \
           f"# HELP waiting_validators Paused validators in network.\n" \
           f"# TYPE waiting_validators gauge\n" \
           f"waiting_validators {content['status']['waiting_validators']}\n"

    for validator in content['validators']:
        if validator['address'] == VALIDATOR_ADDR:
            validator_info = validator
            break
    else:
        return info

    additional_node_info = '{' + f'address="{validator_info.get("address", "None")}",valkey="{validator_info.get("valkey", "None")}",pubkey="{validator_info.get("pubkey", "None")}",proposer="{validator_info.get("proposer", "None")}",' \
                                 f'moniker="{validator_info.get("moniker", "None")}",website="{validator_info.get("website", "None")}",social="{validator_info.get("social", "None")}",identity="{validator_info.get("identity", "None")}",' \
                                 f'status="{validator_info["status"]}"' + '}'

    info = info + f"# HELP node_top_number Node number in the general top.\n" \
                  f"# TYPE node_top_number gauge\n" \
                  f"node_top_number{additional_node_info} {validator_info.get('top', -1)}\n" \
                  f"# HELP node_commission Node commission.\n" \
                  f"# TYPE node_commission gauge\n" \
                  f"node_commission{additional_node_info} {validator_info.get('commission', -1)}\n" \
                  f"# HELP node_rank Node rank.\n" \
                  f"# TYPE node_rank gauge\n" \
                  f"node_rank{additional_node_info} {validator_info.get('rank', -1)}\n" \
                  f"# HELP node_streak Node streak.\n" \
                  f"# TYPE node_streak gauge\n" \
                  f"node_streak{additional_node_info} {validator_info.get('streak', -1)}\n" \
                  f"# HELP node_mischance Node mischance.\n" \
                  f"# TYPE node_mischance gauge\n" \
                  f"node_mischance{additional_node_info} {validator_info.get('mischance', -1)}\n" \
                  f"# HELP node_mischance_confidence Node mischance confidence.\n" \
                  f"# TYPE node_mischance_confidence gauge\n" \
                  f"node_mischance_confidence{additional_node_info} {validator_info.get('mischance_confidence', -1)}\n" \
                  f"# HELP node_start_height Node start height.\n" \
                  f"# TYPE node_start_height gauge\n" \
                  f"node_start_height{additional_node_info} {validator_info.get('start_height', -1)}\n" \
                  f"# HELP node_last_present_block Node last present block.\n" \
                  f"# TYPE node_last_present_block gauge\n" \
                  f"node_last_present_block{additional_node_info} {validator_info.get('last_present_block', -1)}\n" \
                  f"# HELP node_missed_blocks_counter Node missed blocks counter.\n" \
                  f"# TYPE node_missed_blocks_counter gauge\n" \
                  f"node_missed_blocks_counter{additional_node_info} {validator_info.get('missed_blocks_counter', -1)}\n" \
                  f"# HELP node_produced_blocks_counter Node produced blocks counter.\n" \
                  f"# TYPE node_produced_blocks_counter gauge\n" \
                  f"node_produced_blocks_counter{additional_node_info} {validator_info.get('produced_blocks_counter', -1)}"

    return info
