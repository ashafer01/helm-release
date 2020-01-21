# helm-release

This is an attempt to create a simplified version of the
now-superseded [Ship](https://github.com/replicatedhq/ship).

It will not include a web GUI and is meant to be CI/CD-friendly.

It encourages repeatable Helm deployments by permanently storing
parameters and ensures the specific chart is unambiguously identified
for future use with the Helm CLI.

Requires the `jq` tool in addition to bash and coreutils.

*In Development*
