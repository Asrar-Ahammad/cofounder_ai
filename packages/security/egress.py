"""SSRF filter and safe network egress URL validator."""

import ipaddress
import socket
from urllib.parse import urlparse

from packages.core.errors import PolicyViolation

_BLOCKED_NETWORKS = [
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("100.64.0.0/10"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),  # AWS/Cloud metadata
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10"),
]


def validate_egress_url(url: str) -> None:
    """Validate that target URL does not resolve to private, loopback, or metadata addresses.

    Args:
        url: The external URL to validate before HTTP fetching.

    Raises:
        PolicyViolation: If URL scheme is invalid or resolves to a blocked network.
    """
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise PolicyViolation(f"Unsupported URL scheme: {parsed.scheme}")

    hostname = parsed.hostname
    if not hostname:
        raise PolicyViolation("URL must contain a valid hostname")

    try:
        addr_info = socket.getaddrinfo(hostname, None)
    except socket.gaierror as e:
        raise PolicyViolation(f"Unable to resolve hostname '{hostname}': {e}") from e

    for item in addr_info:
        ip_str = item[4][0]
        ip_obj = ipaddress.ip_address(ip_str)
        if isinstance(ip_obj, ipaddress.IPv6Address) and ip_obj.ipv4_mapped:
            ip_obj = ip_obj.ipv4_mapped

        for blocked in _BLOCKED_NETWORKS:
            if ip_obj in blocked:
                raise PolicyViolation(
                    f"Egress blocked: hostname '{hostname}' resolves to private/metadata IP {ip_str}"
                )
