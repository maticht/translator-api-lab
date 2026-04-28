# ru-en-translation-service

Standalone self-hosted `Russian <-> English` translation API based on [LibreTranslate](https://github.com/LibreTranslate/LibreTranslate).

This repository keeps the upstream LibreTranslate codebase and adds a thin service adapter for the following goals:

- support only `en` and `ru`
- run as an independent HTTP API
- stay easy to deploy as its own project
- work with `Vercel` as a separate deployable service

## What This Service Supports

- `POST /translate`
- `POST /detect`
- `GET /languages`
- `GET /health`
- `source=auto`
- short text translation for `en -> ru` and `ru -> en`

## What Is Restricted

- only `en` and `ru` language models are loaded
- file translation is disabled by default
- web UI is disabled by default

The language restriction is enforced by the service adapter with the equivalent of:

```bash
libretranslate --load-only en,ru
```

## Local Run

### 1. Install dependencies

```bash
pip install -e .
```

### 2. Download only the required models

```bash
python scripts/prepare_runtime.py
```

### 3. Start the service

```bash
python main.py
```

By default the service starts on `0.0.0.0:5000`.

## Runtime Storage

Translation models and Argos runtime data are stored inside the project under:

```text
.runtime/argos/
```

This keeps the deployment self-contained and makes it easier to prepare the runtime during a Vercel build.

## Important Environment Variables

### Service defaults

- `PORT`: runtime port override
- `LT_SERVICE_HOST`: host override. Default: `0.0.0.0`
- `LT_SERVICE_LOAD_ONLY`: comma-separated languages. Default: `en,ru`

### LibreTranslate / service behavior

- `LT_DISABLE_WEB_UI`: default `true`
- `LT_DISABLE_FILES_TRANSLATION`: default `true`
- `LT_UPDATE_MODELS`: optional `true` to refresh models on startup
- `LT_API_KEYS`: optional LibreTranslate API key mode
- `LT_REQ_LIMIT`: optional per-minute rate limit
- `LT_CHAR_LIMIT`: optional request character limit

### Argos runtime paths

- `LT_RUNTIME_ROOT`: overrides the local runtime directory used by this adapter

## API Examples

### `GET /languages`

Expected response shape:

```json
[
  {
    "code": "en",
    "name": "English",
    "targets": ["ru"]
  },
  {
    "code": "ru",
    "name": "Russian",
    "targets": ["en"]
  }
]
```

### `POST /translate`

```json
{
  "q": "books",
  "source": "en",
  "target": "ru",
  "format": "text",
  "alternatives": 2
}
```

## Faster Client Requests

For the fastest requests from a client application:

- send `source: "ru"` or `source: "en"` whenever the client can infer it
- avoid `alternatives` unless you really need them
- keep `format: "text"` for normal text input

This repository includes a tiny client-side helper at:

```text
examples/optimized_translate.js
```

It detects Cyrillic vs Latin text before calling `/translate`, so the client can often avoid server-side `source=auto` detection.

### `POST /detect`

```json
{
  "q": "The article was written by our editor."
}
```

### `GET /health`

Upstream LibreTranslate already exposes:

```json
{
  "status": "ok"
}
```

## Deploying To Vercel

This repository includes:

- root `app.py` Flask entrypoint for Vercel
- `vercel.json` with a build step
- `scripts/prepare_runtime.py` to preinstall only `en` and `ru` models into project-local storage

### Recommended deploy flow

1. Push this repository to your own GitHub repo, for example `ru-en-translation-service`.
2. Import that repo into Vercel.
3. Let Vercel run the configured build step.
4. Deploy.

### Notes about Vercel

- This service runs as a Python function on Vercel.
- Cold starts are possible.
- Translation models are relatively large, so bundle size and startup time matter.
- Vercel is acceptable for this MVP, but it is not the best fit for high-load, low-latency production translation workloads.

## Repository Shape

Key files added for the standalone service:

```text
app.py
service_config.py
scripts/prepare_runtime.py
vercel.json
```

The upstream LibreTranslate application code remains in:

```text
libretranslate/
```

## Upstream Base

- Upstream repository: https://github.com/LibreTranslate/LibreTranslate
- LibreTranslate docs: https://docs.libretranslate.com/
- Installation guide: https://docs.libretranslate.com/guides/installation/
- API usage: https://docs.libretranslate.com/guides/api_usage/

## License

This repository remains based on LibreTranslate and therefore keeps its upstream licensing obligations. Review [LICENSE](LICENSE) before publishing or deploying.
