# Universal Blue RPM specs

Packages for Universal Blue projects.

We use this repository as the base for [multiple Universal Blue COPRs](https://copr.fedorainfracloud.org/coprs/ublue-os)
each one with their own purpose defined on their [READMEs](./packages/README.md).

You can build any package by running our custom builder container, it should fetch the sources and do everything for you.
It mounts `mock/` on the current directory so that you can get the resulting RPMs/SRPMs and check the resulting chroots

```bash
# You can specify whatever chroot you want to use, usually those that are supported on COPR should work
just build $PATH_TO_SPEC $ARGUMENTS_FOR_MOCK

# This builds devpod on the Fedora version that the builder container is on (F41)
just build ./staging/devpod/devpod.spec

# This builds devpod on the CentOS Stream + EPEL 10 chroot
just build ./staging/devpod/devpod.spec -r epel-10-$(arch)

# You can also compile for other architectures by passing --forcearch if you have qemu-user-static on your host system
just build ./staging/devpod/devpod.spec --forcearch=aarch64
```

## Contributing

### New package

When adding a new package certain guidelines should be followed, usually try to stick to the [Fedora Packaging Guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/)
for all packages (with case-by-case exceptions). `rpmlint` should always pass ([rpkg](https://docs.pagure.org/rpkg-util/v3/quick_start.html)-based packages are an exception),
they should always be buildable offline once all sources are fetched (so that they can be built on GitHub actions/[mock](https://rpm-software-management.github.io/mock/)),
and always make sure that [Renovate](https://github.com/renovatebot/renovate) can automatically update your package, we have [macros on this repo](./.github/renovate.json5).

Once merged, your new package will need to be manually added to its corresponding COPR ([file in an issue](https://github.com/ublue-os/packages/issues) if it hasn't
been added in a week or so) and then it should be automatically rebuilt over time.

### Existing package

Make sure your contribution passes linting and the guidelines required by [the New Package section](#new-package). Bump the package accordingly: 
- If the package has sources on this repo, bump the `Version:` field;
- If it has external sources, bump the spec `Release:` field (you can/should do it via `rpmdev-bumpspec` ideally).

### For maintainers/approvers

Make sure all the PRs are safe, as in they don't have [RCE](https://www.cloudflare.com/learning/security/what-is-remote-code-execution/)
exploits or any abuse of GitHub actions (or similar). When you are sure of that, put the `safe-to-run` tag on the target
pull request and let it run. Sometimes some packages will require the runner to have an online connection and that isn't
implemented yet so you might want to review the commits on your local machine and make sure they build correctly with a network connection.

You can create a testing distrobox by running `distrobox create --name testingbox --image ghcr.io/ublue-os/ublue-builder`
or by running `just build` from the locally cloned fork, it should be exactly the same environment as the GitHub actions use for building.

## Metrics

![Alt](https://repobeats.axiom.co/api/embed/8bde34be4a2fcd7f506672742563f330d0b6b240.svg "Repobeats analytics image")
