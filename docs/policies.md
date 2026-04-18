# Policies

The policy layer separates route discovery from permission decisions.

Route classes in the demo:

- informational actions such as `gym_info`, `pool_info`, `policy_info`
- approval-required actions such as `booking_request`
- billing-sensitive actions such as `billing_exception`
- unknown or out-of-domain actions

The active policy config is stored in:

- [data/default_policy.json](../data/default_policy.json)

This keeps routing logic measurable and inspectable instead of burying workflow assumptions in prompt text alone.
