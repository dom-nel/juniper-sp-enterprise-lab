# LAB-FW-01 Change Checkpoint

## Objective

Prepare the Phase 1 firewall for a controlled policy test while keeping transit traffic unauthorized until the deliberate ICMP policy is added.

## Candidate Changes Reviewed

- Assigned `ge-0/0/0.0` to `trust`.
- Enabled host-inbound ping on `ge-0/0/0.0`.
- Assigned `ge-0/0/1.0` to `untrust`.
- Enabled host-inbound ping on `ge-0/0/1.0`.
- Removed the broad `trust -> untrust` default permit.
- Added `10.20.20.0/24 -> 10.255.0.2`.

## Validation

The candidate was inspected with:

```text
show | compare
```

It was validated without activation using:

```text
commit check
```

Observed result:

```text
configuration check succeeds
```

It was then activated with the commit comment:

```text
Phase 1 firewall zones and static route baseline
```

## Result

The firewall can classify the planned path as `trust -> untrust` and has an active route toward the WAN endpoint network. It intentionally has no transit permit at this checkpoint.

## Why This Matters

Leaving policy absent creates a controlled failure condition. After the router and endpoints are complete, an unsuccessful ping establishes the denied baseline. Adding one narrow ICMP policy should then be the only meaningful change between failure and success.
