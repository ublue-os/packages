FROM registry.fedoraproject.org/fedora:latest AS builder
ARG TARGET_SPEC="${TARGET_SPEC:-staging/devpod/devpod.spec}"

COPY . /app

RUN dnf update -y && dnf upgrade -y && dnf install rpkg spectool -y && dnf clean all

WORKDIR /app
RUN rpkg --path $(dirname $TARGET_SPEC) spec --outdir /tmp --spec $(basename $TARGET_SPEC)
WORKDIR /tmp
RUN export SPEC=$(basename $TARGET_SPEC) && \
    dnf -y builddep $SPEC && \
    spectool -ag $SPEC -C /tmp && \
    rpkg local --spec $SPEC

FROM scratch AS artifacts

COPY --from=builder /tmp/rpkg/*/*/*.rpm /
