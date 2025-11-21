#!/usr/bin/env sh

# Check if bling has already been sourced so that we dont break atuin. https://github.com/atuinsh/atuin/issues/380#issuecomment-1594014644
[ "${BLING_SOURCED:-0}" -eq 1 ] && return 
BLING_SOURCED=1

# ls aliases
if [ "$(command -v eza)" ]; then
    alias ll='eza -l --icons=auto --group-directories-first'
    alias l.='eza -d .*'
    alias ls='eza'
    alias l1='eza -1'
fi

# ugrep for grep
if [ "$(command -v ug)" ]; then
    alias grep='ug'
    alias egrep='ug -E'
    alias fgrep='ug -F'
    alias xzgrep='ug -z'
    alias xzegrep='ug -zE'
    alias xzfgrep='ug -zF'
fi

# bat for cat
alias cat='bat --style=plain --pager=never' 2>/dev/null

HOMEBREW_PREFIX="${HOMEBREW_PREFIX:-/home/linuxbrew/.linuxbrew}"

# set ATUIN_INIT_FLAGS in your ~/.bashrc before ublue-bling is sourced.
# Atuin allows these flags: "--disable-up-arrow" and/or "--disable-ctrl-r"
ATUIN_INIT_FLAGS=${ATUIN_INIT_FLAGS:-""}

if [ "$(basename $(readlink /proc/$$/exe))" = "bash" ]; then
    # Initialize direnv before bash-preexec to avoid PROMPT_COMMAND conflicts
    # See: https://github.com/rcaloras/bash-preexec/pull/143
    [ "$(command -v direnv)" ] && eval "$(direnv hook bash)"
    [ -f "/etc/profile.d/bash-preexec.sh" ] && . "/etc/profile.d/bash-preexec.sh"
    [ -f "/usr/share/bash-prexec" ] && . "/usr/share/bash-prexec"
    [ -f "/usr/share/bash-prexec.sh" ] && . "/usr/share/bash-prexec.sh"
    [ -f "${HOMEBREW_PREFIX}/etc/profile.d/bash-preexec.sh" ] && . "${HOMEBREW_PREFIX}/etc/profile.d/bash-preexec.sh"
    # Initialize atuin before starship to ensure proper command history capture
    # See: https://github.com/atuinsh/atuin/issues/2804
    [ "$(command -v atuin)" ] && eval "$(atuin init bash ${ATUIN_INIT_FLAGS})"
    [ "$(command -v starship)" ] && eval "$(starship init bash)"
    [ "$(command -v zoxide)" ] && eval "$(zoxide init bash)"
elif [ "$(basename $(readlink /proc/$$/exe))" = "zsh" ]; then
    # Initialize direnv before atuin to avoid PROMPT_COMMAND conflicts
    [ "$(command -v direnv)" ] && eval "$(direnv hook zsh)"
    # Initialize atuin before starship to ensure proper command history capture
    [ "$(command -v atuin)" ] && eval "$(atuin init zsh ${ATUIN_INIT_FLAGS})"
    [ "$(command -v starship)" ] && eval "$(starship init zsh)"
    [ "$(command -v zoxide)" ] && eval "$(zoxide init zsh)"
fi
