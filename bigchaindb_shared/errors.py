
class BDBSharedError(Exception):
    pass

class InvalidJson(BDBSharedError):
    pass

class InvalidMethod(BDBSharedError):
    pass

class InvalidProtocol(BDBSharedError):
    pass

class InvalidParams(BDBSharedError):
    pass

class TxInvalid(BDBSharedError):
    pass

class TxInvalidFulfillment(BDBSharedError):
    pass

class TxConditionParseError(BDBSharedError):
    pass

class TxSignMissingPrivateKeys(BDBSharedError):
    pass

class TxWrongId(BDBSharedError):
    pass