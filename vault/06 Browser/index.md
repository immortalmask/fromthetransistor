---
id: "06"
title: "Section 06: Browser"
section: "06"
tags: ["moc", "networking", "browser"]
---

# Section 06: Browser

This section carries bytes from a process to a terminal document while preserving the boundaries between transport, service, loading, parsing, layout, and rendering.

1. [[06.01 TCP Stack]] — a deterministic, deliberately limited reliable byte stream.
2. [[06.02 Telnet Server]] — concurrent remote sessions over the socket interface.
3. [[06.03 Dynamic Linking]] — map reusable code and resolve symbols at runtime.
4. [[06.04 Text Web Browser]] — fetch, parse, lay out, and render a constrained page.

The core remains offline-capable: protocol tests use packet simulation and applications use localhost fixture servers. Production Internet compatibility is outside the acceptance path.
