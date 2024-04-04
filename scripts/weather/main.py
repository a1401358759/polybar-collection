import argparse
import os

import requests

API_KEY = os.environ.get("OPENWEATHER_API_KEY", "eooplgqeodcxoy9c")
HEADER = {"User-agent": "Mozilla/5.0"}


def unit_suffix(unit: str) -> str:
    match unit:
        case "c":
            unit = "ºC"
        case "f":
            unit = "ºF"
        case _:
            unit = " K"

    return unit


def get_weather(
    city: str = "beijing",
    lang: str = "zh-Hans",
    unit: str = "c",
    api_key: str = API_KEY,
) -> dict[str, str] | None:
    try:
        r = requests.get(
            f"https://api.seniverse.com/v3/weather/now.json?key={api_key}&location={city}&language={lang}&unit={unit}"
        )
        data = r.json()["results"][0]
        temp = data["now"]["temperature"]
        desc = data["now"]["text"]
        unit = unit_suffix(unit)

        return {
            "temp": f"{int(temp)}{unit}",
            "desc": desc.title(),
        }

    except requests.exceptions.ConnectionError:
        print("E: failed to establish connection with the API")
        raise


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Display information about the weather.",
    )
    parser.add_argument(
        "-c",
        metavar="CITY",
        dest="city",
        type=str,
        nargs="+",
        help="city name",
    )
    parser.add_argument(
        "-l",
        metavar="LANG",
        dest="lang",
        type=str,
        nargs=1,
        help="language (en, es, fr, ja, pt, pt_br, ru, zh-Hans)",
    )
    parser.add_argument(
        "-u",
        metavar="metric/imperial",
        choices=("c", "f"),
        dest="unit",
        type=str,
        nargs=1,
        help="unit of temperature (default: kelvin)",
    )
    parser.add_argument(
        "-a",
        metavar="API_KEY",
        dest="api_key",
        nargs=1,
        help="API Key",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
        help="verbose mode",
    )

    args = parser.parse_args()

    api_key = args.api_key[0] if args.api_key else API_KEY
    city = "beijing"
    lang = args.lang[0] if args.lang else "zh-Hans"
    unit = args.unit[0] if args.unit else "c"

    weather = get_weather(city, lang, unit, api_key)
    if weather:
        temp, desc = weather.values()
        if args.verbose:
            print(f"{temp}, {desc}")
        else:
            print(f"{temp}")


if __name__ == "__main__":
    main()
