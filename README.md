# helm-release

This is an attempt to create a simplified version of the
now-superseded [Ship](https://github.com/replicatedhq/ship).

It will not include a web GUI and is meant to be CI/CD-friendly.

It encourages repeatable Helm deployments by permanently storing
parameters and ensures the specific chart is unambiguously identified
for future use with the Helm CLI.

Requires the `jq` tool in addition to bash and coreutils.

*In Development*

## Usage

First I suggest adding `helm-release` to your PATH. This can be
accomplished by a variety of means.

Also note that the tool makes use of the `$EDITOR` variable. Be
sure to set it to a text editor you are comfortable with before
continuing.

After your environment is prepped, set up a new Helm release
directory. We will deploy Gitlab for this example:

```bash
mkdir my_gitlab
cd my_gitlab
helm-release init
```

This will first open a new `release-info` template file in your
editor. Suggested values for our Gitlab release are shown below:

```bash
# Metadata for a single release of a Helm chart

# Required. Name for this individual release of the chart
# If you use multiple environments for example it may be desirable to
# add the environment name to the release name
RELEASE_NAME="gitlab"

# Required. The local canonical name for the helm repository hosting
# this chart. First argument to `helm repo add`
REPO_NAME="gitlab"

# Required. The base URL for the helm repository hosting this chart
# Second argument to `helm repo add`
REPO="https://charts.gitlab.io/"

# Required. The chart name within the above repo
CHART="gitlab"

# Required. The namespace to use for K8s resources for this release
NAMESPACE="default"

# Optional. Pin the chart version
# **Leave empty for unpinned/latest**
VERSION=""
```

After you save this file and close your editor, the repo will be set
up if necessary and the chart will be pulled.

The `values.yaml` from the chart will be copied and opened in your
editor. Consult the chart's documentation for details on this file.

Once you close the editor, the tool will render all of the chart's
templates together into one `rendered.yaml`. You can then use
`kubectl` to apply the file.

**All files created or modified by either the tool or you should be
committed to git**

## Updating values.yaml

Edit values.yaml with your preferred editor. Then:

```bash
helm-release refresh
```

This will take in the updated values and re-render the chart.

Technically this will render local modifications to the chart copy in
`.release` as well, but this is *not recommended* at this time.

## Upstream Chart Updates

When you want to bring in the current version of the chart from
upstream:

```bash
helm-release upgrade
```
