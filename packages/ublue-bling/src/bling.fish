#!/usr/bin/env fish

# FIXME: add no-source-twice fix

# ls aliases
if [ "$(command -v eza)" ]
    alias ll='eza -l --icons=auto --group-directories-first'
    alias l.='eza -d .*'
    alias ls='eza'
    alias l1='eza -1'
end

# ugrep for grep
if [ "$(command -v ug)" ]
    alias grep='ug'
    alias egrep='ug -E'
    alias fgrep='ug -F'
    alias xzgrep='ug -z'
    alias xzegrep='ug -zE'
    alias xzfgrep='ug -zF'
end

# bat for cat
alias cat='bat --style=plain --pager=never' 2>/dev/null

if status is-interactive
    # Initialize atuin before starship to ensure proper command history capture
    # Atuin allows these flags: "--disable-up-arrow" and/or "--disable-ctrl-r"
    # Use by setting a universal variable, e.g. set -U ATUIN_INIT_FLAGS "--disable-up-arrow"
    # Or set in config.fish before this file is sourced
    [ "$(command -v atuin)" ] && eval "$(atuin init fish $ATUIN_INIT_FLAGS)"

    [ "$(command -v starship)" ] && eval "$(starship init fish)"

    [ "$(command -v zoxide)" ] && eval "$(zoxide init fish)"
end
