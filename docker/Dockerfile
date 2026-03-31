FROM rust:1.86-slim-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip ca-certificates pkg-config libdbus-1-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN python3 -m pip install --break-system-packages -e '.[dev]'

CMD cargo test --manifest-path skills/desktop-window-fixture-ocr/helpers/accessibility-probe/Cargo.toml && \
    python3 -m pytest -q
