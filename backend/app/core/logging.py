import logging
import re
from contextvars import ContextVar
from typing import Optional

request_id_ctx: ContextVar[Optional[str]] = ContextVar("request_id", default=None)

SENSITIVE_REPLACEMENTS = [
    (
        re.compile(r'(password|secret|api_key|token|auth|admin_api_key|jwt_secret)\s*[:=]\s*["\']?([^"\'\s]+)["\']?', re.IGNORECASE),
        r'\1=***REDACTED***'
    ),
    (
        re.compile(r'Bearer\s+[A-Za-z0-9\-\._~\+\/]+=*', re.IGNORECASE),
        'Bearer ***REDACTED***'
    ),
]


class SensitiveFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = self.mask_sensitive(record.msg)
        if record.args:
            if isinstance(record.args, dict):
                record.args = {k: self.mask_value(k, v) for k, v in record.args.items()}
            elif isinstance(record.args, tuple):
                record.args = tuple(
                    self.mask_sensitive(arg) if isinstance(arg, str) else arg
                    for arg in record.args
                )
        return True

    @staticmethod
    def mask_sensitive(text: str) -> str:
        masked = text
        for pattern, replacement in SENSITIVE_REPLACEMENTS:
            masked = pattern.sub(replacement, masked)
        return masked

    @staticmethod
    def mask_value(key: str, value: any) -> any:
        if any(sens in key.lower() for sens in ["password", "secret", "token", "api_key", "resume"]):
            return "***REDACTED***"
        if isinstance(value, str):
            return SensitiveFilter.mask_sensitive(value)
        return value


class StructuredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        req_id = request_id_ctx.get()
        req_prefix = f"[{req_id}] " if req_id else ""
        record.msg = f"{req_prefix}{record.msg}"
        return super().format(record)


def setup_logging(log_level: str = "INFO") -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level.upper())

    # Clear existing handlers
    root_logger.handlers = []

    handler = logging.StreamHandler()
    formatter = StructuredFormatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    handler.addFilter(SensitiveFilter())
    root_logger.addHandler(handler)
