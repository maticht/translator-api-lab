from __future__ import annotations

from waitress import serve
from werkzeug.serving import run_simple

from service_config import build_service_args, create_service_app


service_args = build_service_args()
app = create_service_app(service_args)


def main() -> None:
    host = service_args.host
    if service_args.debug and host == "*":
        host = "::"

    if service_args.debug:
        run_simple(host, service_args.port, app)
        return

    url_scheme = "https" if service_args.ssl else "http"
    print(
        "Running ru-en-translation-service on "
        f"{url_scheme}://{service_args.host}:{service_args.port}"
    )
    serve(
        app,
        host=service_args.host,
        port=service_args.port,
        url_scheme=url_scheme,
        threads=service_args.threads,
    )


if __name__ == "__main__":
    main()
