# vim: set ft=make :

alias setup-luks-hwkey-unlock := setup-luks-fido-unlock
alias remove-luks-hwkey-unlock := setup-luks-fido-unlock

# Enable automatic LUKS unlock via TPM
setup-luks-tpm-unlock:
    #!/usr/bin/bash
    sudo /usr/libexec/luks-enable-tpm2-autounlock

# Disable automatic LUKS unlock via TPM
remove-luks-tpm-unlock:
    #!/usr/bin/bash
    sudo /usr/libexec/luks-disable-tpm2-autounlock

# Enable hardware key LUKS unlock via FIDO2
setup-luks-fido-unlock:
    #!/usr/bin/bash
    sudo /usr/libexec/luks-enable-fido2-autounlock

# Disable hardware key LUKS unlock via FIDO2
remove-luks-fido-unlock:
    #!/usr/bin/bash
    sudo /usr/libexec/luks-disable-fido2-autounlock
