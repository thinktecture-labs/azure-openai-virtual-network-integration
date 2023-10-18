#!/bin/bash

set -e

cd infra/workload
terraform output -raw app_url
