#!/bin/bash
set -e
shopt -s extglob

# owner    project    namespace_dir
namespaces="\
            ublue-os    packages    ./packages"

src=".packit.yaml"
__usage="$0: Script to include any namespace to $src"

case "$*" in
  help|--help|-h)
    echo "$__usage"
    exit
  ;;
esac

# Check we have the required deps
hash yq sed

mkyaml() {
  mkdir -p .tmp
  mktemp .tmp/packit.XXXXXXX.yaml
}

trap 'rm -r .tmp' EXIT

#for namespace in "${namespaces[@]}"; do
while read -r _owner _project namespace_dir; do
  echo >&2 "=== Processing namespace_dir: $namespace_dir ==="

  for pkg in "$namespace_dir"/*/; do
    pkg=$(basename "$pkg")
    if [[ ! -f ./$namespace_dir/$pkg/$pkg.spec ]]; then
      printf >&2 'No matching spec file with %s.\nPossible values:\n' "$pkg"
      printf >&2 '  - %s\n' ./"$namespace_dir"/"$pkg"/*.spec
      continue
    fi

    cat <<EOF >>"$(mkyaml)"
packages:
  $pkg:
    paths: [ "$namespace_dir/$pkg" ]
    specfile_path: "$pkg.spec"

EOF

  done

done <<<"$namespaces"

# See https://stackoverflow.com/a/67036496
# shellcheck disable=SC2016
yq ea -i '. as $item ireduce ({}; . * $item )' "$src" ./.tmp/packit.*.yaml
sed -E -i 's|!!merge\s+||g' "$src"