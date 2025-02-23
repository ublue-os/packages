#!/usr/bin/env bash
if [[ -d "/home/linuxbrew/.linuxbrew/opt/uutils-coreutils/libexec/uubin" && $- == *i* ]] ; then
  PATH="/home/linuxbrew/.linuxbrew/opt/uutils-coreutils/libexec/uubin:$PATH" 
  PATH="/home/linuxbrew/.linuxbrew/opt/uutils-diffutils/libexec/uubin:$PATH"
  PATH="/home/linuxbrew/.linuxbrew/opt/uutils-findutils/libexec/uubin:$PATH"
  export PATH
fi
