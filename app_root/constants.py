"""
    the app custom configs names, the regular expression patterns, the status codes and other constants;
    should be defined once and used in the entire App, welcome to the Constants module :)
"""

from datetime import datetime, UTC


class DTFormats:
    LONG = '%Y-%m-%d %H:%M:%S'
    SHORT = '%a %d, %b %Y %H:%M'


class StringNames:
    # > app config
    REQUIRED_PASSWORD_STRENGTH = 'REQUIRED_PASSWORD_STRENGTH'  # this is a config name, see `configs` module
    LOGOUT_TOKEN_EXPIRE_SECONDS = 'LOGOUT_TOKEN_EXPIRE_SECONDS'
    # > other parts
    LOGOUT_TOKEN_NAME = 'logout'


class Regex:
    USERNAME_REGEX = r'^[a-zA-Z]+[a-zA-Z0-9_\-]+\w$'
    NOTE_TITLE_REGEX = r'^[a-zA-Z]+[\w &"_@:)(+-]*$'


class SCodes:
    """ Status Codes for easy access, because we all forget them """
    CONTINUE_100 = 100
    SWITCHING_PROTOCOLS_101 = 101
    PROCESSING_102 = 102
    EARLY_HINTS_103 = 103
    #
    OK_200 = SUCCESS_200 = 200
    CREATED_201 = 201
    ACCEPTED_202 = 202
    NON_AUTHORITATIVE_INFORMATION_203 = 203
    NO_CONTENT_204 = 204
    RESET_CONTENT_205 = 205
    PARTIAL_CONTENT_206 = 206
    MULTI_STATUS_207 = 207
    ALREADY_REPORTED_208 = 208
    IM_USED_226 = 226
    #
    MULTIPLE_CHOICES_300 = 300
    MOVED_PERMANENTLY_301 = 301
    FOUND_302 = 302
    SEE_OTHER_303 = 303
    NOT_MODIFIED_304 = 304
    USE_PROXY_305 = 305
    UNUSED_306 = 306
    TEMPORARY_REDIRECT_307 = 307
    PERMANENT_REDIRECT_308 = 308
    #
    BAD_REQUEST_400 = 400
    UNAUTHORIZED_401 = 401
    PAYMENT_REQUIRED_402 = 402
    FORBIDDEN_403 = 403
    NOT_FOUND_404 = 404
    METHOD_NOT_ALLOWED_405 = 405
    NOT_ACCEPTABLE_406 = 406
    PROXY_AUTHENTICATION_REQUIRED_407 = 407
    REQUEST_TIMEOUT_408 = 408
    CONFLICT_409 = 409
    GONE_410 = 410
    LENGTH_REQUIRED_411 = 411
    PRECONDITION_FAILED_412 = 412
    PAYLOAD_TOO_LARGE_413 = 413
    URI_TOO_LONG_414 = 414
    UNSUPPORTED_MEDIA_TYPE_415 = 415
    RANGE_NOT_SATISFIABLE_416 = 416
    EXPECTATION_FAILED_417 = 417
    IM_A_TEAPOT_418 = 418
    MISDIRECTED_REQUEST_421 = 421
    UNPROCESSABLE_ENTITY_422 = 422
    LOCKED_423 = 423
    FAILED_DEPENDENCY_424 = 424
    TOO_EARLY_425 = 425
    UPGRADE_REQUIRED_426 = 426
    PRECONDITION_REQUIRED_428 = 428
    TOO_MANY_REQUESTS_429 = 429
    REQUEST_HEADER_FIELDS_TOO_LARGE_431 = 431
    UNAVAILABLE_FOR_LEGAL_REASONS_451 = 451
    #
    INTERNAL_SERVER_ERROR_500 = 500
    NOT_IMPLEMENTED_501 = 501
    BAD_GATEWAY_502 = 502
    SERVICE_UNAVAILABLE_503 = 503
    GATEWAY_TIMEOUT_504 = 504
    HTTP_VERSION_NOT_SUPPORTED_505 = 505
    VARIANT_ALSO_NEGOTIATES_506 = 506
    INSUFFICIENT_STORAGE_507 = 507
    LOOP_DETECTED_508 = 508
    NOT_EXTENDED_510 = 510
    NETWORK_AUTHENTICATION_REQUIRED_511 = 511


# logger
LOG_FILE = f'logs/log-{datetime.now(UTC).strftime("%y-%m-%d")}.log'  # used by app.logger to log to
LOGGER_FILE_FORMATTER = "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"  # logger formatter for file
LOGGER_STREAM_FORMATTER = "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"  # logger formatter for stdout
