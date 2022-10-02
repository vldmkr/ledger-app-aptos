import pytest
from hashlib import sha256
from sha3 import keccak_256

from ecdsa.curves import SECP256k1
from ecdsa.keys import VerifyingKey
from ecdsa.util import sigdecode_der

from aptos_client.transaction import Transaction

@pytest.mark.skip(reason="signing not implemented yet")
def test_sign_tx(cmd, button, model):
    bip32_path: str = "m/44'/0'/0'/0/0"

    pub_key, chain_code = cmd.get_public_key(
        bip32_path=bip32_path,
        display=False
    )  # type: bytes, bytes

    pk: VerifyingKey = VerifyingKey.from_string(
        pub_key,
        curve=SECP256k1,
        hashfunc=sha256
    )

    tx = Transaction(
        nonce=1,
        to="0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",
        value=666,
        memo="For u EthDev"
    )

    v, der_sig = cmd.sign_tx(bip32_path=bip32_path,
                             transaction=tx,
                             button=button,
                             model=model)

    assert pk.verify(signature=der_sig,
                     data=tx.serialize(),
                     hashfunc=keccak_256,
                     sigdecode=sigdecode_der) is True
