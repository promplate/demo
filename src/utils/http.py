from typing import Mapping


def format_headers(headers: Mapping[str, str]):
    return {"-".join(map(str.title, k.split("-"))): v for k, v in headers.items()}


def forward_headers(headers: Mapping[str, str]):
    return format_headers({k: v for k, v in headers.items() if should_forward(k)})


def should_forward(key: str):
    key = key.lower()
    return key not in ("host", "connection", "content-length", "transfer-encoding", "upgrade") and not any(
        map(key.startswith, ("if", "accept", "proxy", "sec"))
    )
