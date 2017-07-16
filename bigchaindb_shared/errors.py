
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

class HttpError(BDBSharedError):
    pass

class HttpConnectionError(BDBSharedError):
    pass

class HttpJsonError(BDBSharedError):
    pass

class Http404NotFound(BDBSharedError):
    pass