# Run a one minute system benchmark
[group('System')]
benchmark:
    #!/usr/bin/env bash
    echo 'Running a 1 minute benchmark ...'
    trap popd EXIT
    pushd $(mktemp -d)
    stress-ng --matrix 0 -t 1m --times
