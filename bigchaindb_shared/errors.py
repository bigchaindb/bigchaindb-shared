
class BDBSharedError(Exception):
    pass

class InvalidMethod(BDBSharedError):
    pass

class InvalidProtocol(BDBSharedError):
    pass

class InvalidJson(BDBSharedError):
    pass

class TxInvalid(BDBSharedError):
    pass

class TxInvalidFulfillment(BDBSharedError):
    pass

class TxCreateError(BDBSharedError):
    pass

class TxTransferError(BDBSharedError):
    pass

class TxConditionParseError(BDBSharedError):
    pass

class TxSignMissingPrivateKeys(BDBSharedError):
    pass

class TxWrongId(BDBSharedError):
    pass