#!/usr/bin/env bash

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
pushd $SCRIPT_DIR

version=`git describe --tags`

# v0.0.7-11-g4364885 --> v0.0.7-11
version=$(echo $version | cut -d'-' -f1-2)

if [[ $? -ne 0 ]]; then
  echo "Error: git describe failed, cannot continue!"
  exit 1
fi

echo "Replacing with version: $version"

if [[ ! -f "$SCRIPT_DIR/../pyproject.toml" ]]; then
  echo "Error: did not find pyproject.toml file, cannot continue"
  exit 1
fi


# execute replacement
sed -i "s/^version = .*/version = \"${version}\"/" "$SCRIPT_DIR/../pyproject.toml"

if [[ $? -eq 0 ]];then
  echo "Replacement successful!"
  head "$SCRIPT_DIR/../pyproject.toml"
fi
