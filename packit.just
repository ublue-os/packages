# Recipes meant to be inside a packit build environment

_sh_utils := '''
    die() {
        echo "$*" >&2
        exit 1
    }
'''

_default:
    @just --list --justfile packit.just

# Fetch remote sources
[no-cd]
_fetch_sources package_dir='.':
    #!/usr/bin/env bash
    {{ _sh_utils }}
    set -x
    cd "{{ package_dir }}" || exit 1
    # For each spec file, fetch its sources
    for spec in ./*.spec; do
        [[ ! -f $spec ]] && continue
        rpmspec -P $spec | grep -P '^Source[0-9]*:\s+https?://' >./.sources
        # Download the files from their urls
        while read -r source url; do
            file_name="${url##*/}"
            wget --no-clobber -O "$file_name" "$url" || die "Couldnt download file $url"
            sed -E -i "s|($source)\s+(.*)|\1 ${file_name}|" $spec
        done <./.sources
    done
    rm -f ./.sources
