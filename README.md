# Universal Blue RPM specs

Packages for Universal Blue projects.

We use [this COPR](https://copr.fedorainfracloud.org/coprs/ublue-os/staging) as a way to get packages that either arent on Fedora/CentOS and maybe have patches for them.

You can build any package by running our custom builder container, it should fetch the sources and do everything for you.
It mounts `mock/` on the current directory so that you can get the resulting RPMs/SRPMs and check the resulting chroots 

```bash
# You can specify whatever chroot you want to use, usually those that are supported on COPR should work
just build $PATH_TO_SPEC $ARGUMENTS_FOR_MOCK
```

The COPR hosting our packages can be found [here].
