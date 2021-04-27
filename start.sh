#!/usr/bin/env bash
script_dir=$(dirname "${BASH_SOURCE[0]}")

exec python3 -m dripping_reinvest --verbose "$@" |& tee ${script_dir}/dripping_reinvest.log
