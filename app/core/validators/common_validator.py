def validate_page_size(input_params, error_class):
    if "size" not in input_params.keys():
        return error_class.bad_request_response("Page size is missing")
    try:
        page_size = int(input_params["size"])
    except ValueError:
        return error_class.bad_request_response("Page size is not a number")
    return page_size


def validate_page(input_params, error_class):
    if "page" not in input_params.keys():
        return error_class.bad_request_response("Page is missing")
    try:
        page = int(input_params["page"])
    except ValueError:
        return error_class.bad_request_response("Page is not a number")
    return page
