---
applyTo: "**"
paths: "**"
globs: "**"
description: "SOLID design principles"
---

# SOLID Design Principles

## Single Responsibility Principle (SRP)
Each module/class/function should have one reason to change. The dispatcher reconciles and
routes; it does not itself implement research or issue-filing logic — that belongs to the
agent profiles it spawns.

## Open/Closed Principle (OCP)
Adding a new `idea_type` or agent profile should not require modifying the dispatcher's core
routing loop — profiles are data/config the dispatcher reads, not branches it hardcodes.

## Liskov Substitution Principle (LSP)
Any agent profile must be invocable through the same interface (inputs: idea record; outputs:
status update + events) so the dispatcher can treat all profiles interchangeably.

## Interface Segregation Principle (ISP)
Don't force an agent profile to depend on capabilities it doesn't use (e.g. a `docs` profile
shouldn't require code-edit tool access just because the interface offers it).

## Dependency Inversion Principle (DIP)
The dispatcher depends on the session creator's custom-agent contract, not on concrete per-type
implementations — agents are selected at session creation rather than imported by dispatcher code.
