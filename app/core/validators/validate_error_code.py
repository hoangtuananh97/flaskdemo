class ValidateErrorCode:
    """
    Message codes and descriptions
    """

    MAX_LENGTH = "too_long"  # 'The input length is longer than maximum length'
    MIN_LENGTH = "too_short"  # 'The input length is shorter than maximum length'
    INVALID_FORMAT = "invalid_format"  # 'The input format is invalid'
    INVALID_TYPE = "invalid_type"  # The input type is not valid
    INVALID_LOCALE = "invalid_locale"  # The input type is not valid
    INVALID_DATE = "invalid_date"  # The input date is in the future
    IS_REQUIRED = "is_required"  # The input is required
    IS_UNIQUE = "is_unique"  # The input is existed in database
    NOT_EXIST = "not_exist"  # the input value is not exist
    EXISTED = "existed"  # the input value is not exist
    UNKNOWN_FIELD = "unknown_field"  # the input field is not exist
    INVALID = "invalid"  # the input field is not exist
