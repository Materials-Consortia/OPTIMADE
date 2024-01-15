#! /bin/sh

sudo apt-get install -y \
    ant \
    default-jdk \
    make \
    patch \
    python3-mdx-math \
    unzip \
;

# Required by the 'optimade-property-tools' submodule
sudo apt-get install -y \
    python3-jsonschema \
    python3-markdown \
    python3-mdx-math \
    python3-pygments \
    python3-yaml \
;
