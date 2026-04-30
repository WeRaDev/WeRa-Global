try:  # pragma: no cover - optional dependency
    from poly_eip712_structs import make_domain
    from eth_utils import keccak
    from py_order_utils.utils import prepend_zx
    _HAS_EIP712 = True
except ModuleNotFoundError:
    _HAS_EIP712 = False
    def make_domain(*args, **kwargs):
        raise ModuleNotFoundError(
            "poly_eip712_structs is required for signing. "
            "Install it with `pip install poly-eip712-structs`."
        )
    def keccak(*args, **kwargs):
        raise ModuleNotFoundError(
            "eth-utils is required for signing."
        )
    def prepend_zx(*args, **kwargs):
        raise ModuleNotFoundError(
            "py_order_utils is required for signing."
        )

from .model import ClobAuth
from ..signer import Signer

CLOB_DOMAIN_NAME = "ClobAuthDomain"
CLOB_VERSION = "1"
MSG_TO_SIGN = "This message attests that I control the given wallet"


def get_clob_auth_domain(chain_id: int):
    return make_domain(name=CLOB_DOMAIN_NAME, version=CLOB_VERSION, chainId=chain_id)


def sign_clob_auth_message(signer: Signer, timestamp: int, nonce: int) -> str:
    if not _HAS_EIP712:
        raise ModuleNotFoundError(
            "poly_eip712_structs, eth-utils, and py_order_utils are required for "
            "auth message signing."
        )
    clob_auth_msg = ClobAuth(
        address=signer.address(),
        timestamp=str(timestamp),
        nonce=nonce,
        message=MSG_TO_SIGN,
    )
    chain_id = signer.get_chain_id()
    auth_struct_hash = prepend_zx(
        keccak(clob_auth_msg.signable_bytes(get_clob_auth_domain(chain_id))).hex()
    )
    return prepend_zx(signer.sign(auth_struct_hash))
