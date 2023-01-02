import platform
import sys
from datetime import datetime, timedelta

import asyncio
import aiohttp


def json_formate(json, currency_list):

    final_dict = {json["date"]: {}}
    for_append = final_dict[json["date"]]
    json_exchange_rate_list = json["exchangeRate"]
    for currency in json_exchange_rate_list:
        if currency["currency"] in currency_list:
            for_append[currency["currency"]] = {
                "sale": currency["saleRateNB"],
                "purchase": currency["purchaseRateNB"],
            }
    return final_dict


async def index(session):

    try:
        days, *extra_currency = sys.argv[1:]
    except ValueError:
        days = sys.argv[1]
        extra_currency = ()

    if extra_currency:
        currency_list = ["EUR", "USD", *extra_currency]
    else:
        currency_list = ["EUR", "USD"]
    json_list = []

    if int(days) > 10:
        return "Can't make more than 10 days"

    for i in range(int(days)):

        raw_date = datetime.now()
        if i:
            raw_date = raw_date - timedelta(days=i)
        date = raw_date.strftime("%d.%m.%Y")
        url = f"https://api.privatbank.ua/p24api/exchange_rates?date={date}"
        async with session.get(url) as response:
            print("Status:", response.status)
            if response.status == 200:
                json_full = await response.json()
                json_list.append(json_formate(json_full, currency_list))
            else:
                return f"Error status: {response.status} for {url}"

    return f"json: {json_list}"


async def main():
    async with aiohttp.ClientSession() as session:
        result = await index(session)
        return result


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        r = asyncio.run(main())
    print(r)
