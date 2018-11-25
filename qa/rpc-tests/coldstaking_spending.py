#!/usr/bin/env python3
# Copyright (c) 2018 The Navcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from test_framework.test_framework import NavCoinTestFramework
from test_framework.util import *

#import time

class ColdStakingSpending(NavCoinTestFramework):
    """Tests spending and staking to/from a spending wallet."""

    def __init__(self):
        super().__init__()
        self.setup_clean_chain = True
        self.num_nodes = 2

    def setup_network(self, split=False):
        self.nodes = self.setup_nodes()
        self.is_network_split = split

    def run_test(self):
        self.nodes[0].staking(False)

        slow_gen(self.nodes[0], 100)
        # Verify the Cold Staking is started
        assert(self.nodes[0].getblockchaininfo()["bip9_softforks"]["coldstaking"]["status"] == "started")

        slow_gen(self.nodes[0], 100)
        # Verify the Cold Staking is locked_in
        assert(self.nodes[0].getblockchaininfo()["bip9_softforks"]["coldstaking"]["status"] == "locked_in")

        slow_gen(self.nodes[0], 100)
        # Verify the Cold Staking is active
        assert(self.nodes[0].getblockchaininfo()["bip9_softforks"]["coldstaking"]["status"] == "active")

        # Generate our addresses

        SENDING_FEE= 0.00010000

        address_one_public_key = self.nodes[0].getnewaddress()
        address_one_private_key = self.nodes[0].dumpprivkey(address_one_public_key)
        address_two_public_key = self.nodes[1].getnewaddress()
        address_two_private_key = self.nodes[1].dumpprivkey(address_two_public_key)

        # Third party addresses and keys
        address_X_public_key = "mqyGZvLYfEH27Zk3z6JkwJgB1zpjaEHfiW"
        address_X_private_key = "cMuNajSALbixZvApkcYVE4KgJoeQY92umhEVdQwqX9wSJUzkmdvF"
        address_Y_public_key = "mrfjgazyerYxDQHJAPDdUcC3jpmi8WZ2uv"
        address_Y_private_key = "cST2mj1kXtiRyk8VSXU3F9pnTp7GrGpyqHRv4Gtap8jo4LGUMvqo"

        addr1_info = self.nodes[0].validateaddress(address_one_public_key)



        ## Our wallet holds the spending address key
        coldstaking_address_two = self.nodes[0].getcoldstakingaddress(address_X_public_key, address_one_public_key)
        
        # Sending to cold address:
            # Success case:
                # Available balance increase (or stay the same if sending wallet = spending wallet)
                # Staking weight decrease (if our wallet is the spending wallet)

        balance_before = self.nodes[0].getbalance()
        staking_weight_before = self.nodes[0].getstakinginfo()["weight"]

        # Check wallet weight roughly equals wallet balance
        assert(round(staking_weight_before / 100000000.0, -5) == round(balance_before, -5))

        # Send funds to the cold staking address (leave some NAV for fees)
        self.nodes[0].sendtoaddress(coldstaking_address_two, self.nodes[0].getbalance() - 1)

        balance_step_one = self.nodes[0].getbalance()
        staking_weight_one = self.nodes[0].getstakinginfo()["weight"]

        # We expect our balance to decrease by just the fees
        # We expect our staking weight to decrease
        print(staking_weight_before, staking_weight_one)

        assert(balance_step_one >= balance_before - 1)
        assert(staking_weight_one / 100000000.0 <= 1)



        # Test spending from a cold staking wallet with the spending key
            # Send half of funds to a third party address
        self.nodes[0].sendtoaddress(address_Y_public_key, float(balance_step_one) * 0.5)

        balance_step_two = self.nodes[0].getbalance()

        # We expect our balance to be half spent (less some fees)
        assert(balance_step_two <= balance_step_one - 1)



#        self.nodes[0].generate(1)
#        block_height = self.nodes[0].getblockcount()

#        block_hash = self.nodes[0].getblockhash(block_height)
#        spending_tx_block = self.nodes[0].getblock(block_hash)
        
#        try:
#            tx = self.nodes[0].getrawtransaction(spending_tx_block["tx"][1])
            
#            print('PRINTING DECODED RAW TX FROM BLOCK')
#            print(self.nodes[0].decoderawtransaction(tx))
#            print('****')

#            raw_tx = self.nodes[0].createrawtransaction(
#                [{
#                    "txid": tx,
#                    "vout": 1
#                }],
#                {address_two_public_key: 9.9999}
#            )

#            print('PRINTING OUR NEW RAW TX')
#            print(self.nodes[0].decoderawtransaction(raw_tx))
#            print('****')

#            signed_raw_tx = self.nodes[0].signrawtransaction(raw_tx)

#            print('PRINTING OUR SIGNED RAW TX')
#            print(signed_raw_tx)
#            print('****')

#            print('PRINTING OUR DECODED RAW TX')
#            print(self.nodes[0].decoderawtransaction(str(signed_raw_tx)))
#            print('****')

#            self.nodes[0].sendrawtransaction(str(signed_raw_tx))
            
#            print("sending worked")
#        except JSONRPCException as e:
#            print('hey look error')
#            print(e.error['message'])
#            assert(1==2)


        
    #     spending_tx_block = self.nodes[0].getblock(self.nodes[0].getblockhash(block_height))


    #     # Sending from spending address:
    #         # From wallet that controls staking address only :
        

    #         # Sending coins (should fail) 
    #         # Sending coins rawtx w/signing (should fail) 
    #         # Sending to original staking address (not combined cold address) (should fail) 
    #         # Sending to original spending address (not combined cold address) (should fail) 
    #         # when staking a cold staking output coins should not be able to move to a different cold staking address (should fail)


    #     # Try and spend from the cold staking address, 
    #     # The only utxo big enough for this tx belongs to the coldstaking address, we can't access that so this should fail
    #     try:
    #         self.nodes[0].sendtoaddress(address_one_public_key, 10) 
    #     except JSONRPCException as e:   
    #         assert("Insufficient funds" in e.error['message'])
        
    #     # Staking
    #         # Try staking with zero balance in immature staking address, balance in spending
    #         # Try staking with balance in immature staking address, balance in spending (should fail)
    #         # Try staking with zero balance in staking wallet, balance in spending
    #         # Try staking with balance in staking wallet, balance in spending, 
    #         # Try staking with balance in staking wallet, zero balance in spending
    #         # Try staking with balance in staking wallet, zero balance in immature address for spending (should fail?
    #         # Try staking with rawtx w/signing

    #     # From wallet that controls spending address only:
    #         # Sending coins 
    #         # Sending coins rawtx w/signing
    #         # Sending to original staking address (not combined cold address)
    #         # Sending to original spending address (not combined cold address)
    #         # Staking rawtx (should fail)
    #         # Staking rawtx w/signing (should fail)



    # def send_raw_transaction(self, destination_address, amount, time, description):

    #     amount = amount * 100000000

    #     # Create a raw proposal tx
    #     raw_proposal_tx = self.nodes[0].createrawtransaction(
    #         [],
    #         {"6ac1": 1},
    #         json.dumps({"v": 2, "n": amount, "a": destination_address,  "d": time, "s": description})
    #     )

    #     # Modify version
    #     raw_proposal_tx = "04" + raw_proposal_tx[2:]

    #     # Fund raw transaction
    #     raw_proposal_tx = self.nodes[0].fundrawtransaction(raw_proposal_tx)['hex']

    #     # Sign raw transaction
    #     raw_proposal_tx = self.nodes[0].signrawtransaction(raw_proposal_tx)['hex']

    #     # Send raw transaction
    #     return self.nodes[0].sendrawtransaction(raw_proposal_tx)
        

if __name__ == '__main__':
    ColdStakingSpending().main()