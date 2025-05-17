The packages in this sub-dir are built in COPR.

Only add packages patched/added for ublue but which we believe to be somewhat temporary as we expect the chagenges to be upstreamed.

See: https://copr.fedorainfracloud.org/coprs/ublue-os/staging/

## Reasons

In order to actually know what to remove in the future, please write why each package is here, so we can drop this at some point whenever they dont need the patches or upstream packaged them.

### Readymade / Taidan

Needed for new Titanoboa Bluefin and Aurora installers.

We've had to add quite a few packages to make it so we could compile Readymade here

- `dart`
- `sass`
- `xcursorgen` (needs an [EPEL request](https://docs.fedoraproject.org/en-US/epel/epel-package-request/))
- `hydrogen-icon-theme`
- `helium-gtk-theme`
- `libhelium`
- `readymade`
- `taidan`

### Bazaar

New GNOME-software alternative, being used for Bluefin{,-LTS}

- `bazaar`
- `glycin-libs` on EPEL10 specifically we dont have it on EPEL
