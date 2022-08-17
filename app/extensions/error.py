class Error:
    def __init__(self, request_id, exc_value, exc_traceback=None):
        self.req_id = request_id
        self.exc_value = exc_value
        self.exc_traceback = exc_traceback

    def __str__(self):
        short_desc = f"[Error][{self.req_id}] {self.exc_value}"

        if self.exc_traceback is None:
            return short_desc

        return f"{short_desc}\n{self.exc_traceback}"

    def to_slack_msg(self):
        short_dec = f"*Exception:* {self.exc_value}\n" f"*RequestID:* {self.req_id}"

        if self.exc_traceback is None:
            return short_dec

        return f"{short_dec}\n" f"*Traceback*:\n" f">>>{self.exc_traceback}"
