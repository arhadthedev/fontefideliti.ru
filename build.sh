#!/usr/bin/env bash

# build.py - builds the whole site into a public/ directory
#
# Copyright (c) 2020 Oleg Iarygin <oleg@arhadthedev.net>
#
# Distributed under the MIT software license; see the accompanying
# file LICENSE.txt or <https://www.opensource.org/licenses/mit-license.php>.

# exit when any command fails
set -e

./photo_generation.py public
scripts/generate_shows.py public
