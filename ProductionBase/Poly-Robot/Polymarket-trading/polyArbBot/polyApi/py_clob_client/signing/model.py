try:
    from poly_eip712_structs import EIP712Struct, Address, String, Uint
    _HAS_POLY_EIP = True
except ModuleNotFoundError:  # pragma: no cover
    _HAS_POLY_EIP = False

if _HAS_POLY_EIP:

    class ClobAuth(EIP712Struct):
        address = Address()
        timestamp = String()
        nonce = Uint()
        message = String()

else:

    class ClobAuth:  # type: ignore
        def __init__(self, *args, **kwargs):
            raise ModuleNotFoundError(
                "poly_eip712_structs is required for signing. "
                "Install it with `pip install poly-eip712-structs`."
            )

        def signable_bytes(self, *args, **kwargs):
            raise ModuleNotFoundError(
                "poly_eip712_structs is required for signing. "
                "Install it with `pip install poly-eip712-structs`."
            )
