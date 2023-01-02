import platform
import sys
from datetime import datetime, timedelta

import asyncio
import aiohttp



async def index(session, days, extra_currency=None):

    currence_list = ["EUR", "USD", *extra_currency]
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
                def json_formate(json):
                
                    final_dict = {json["date"]:{}}
                    for_append = final_dict[json["date"]]
                    json_exchange_rate_list = json["exchangeRate"]
                    for currency in json_exchange_rate_list:
                        if currency["currency"] in currence_list:
                            for_append[currency["currency"]] = {"sale": currency["saleRateNB"], "purchase": currency["purchaseRateNB"]}
                    return final_dict
                
                json_full = await response.json()
                json_list.append(json_formate(json_full))
            else:
                return f"Error status: {response.status} for {url}"
        
    return f"json: {json_list}"

async def main(days, extra_currency=None):
    async with aiohttp.ClientSession() as session:
        result = await index(session, days, extra_currency)
        return result

if __name__ == "__main__":
    try:
        days, *extra_currency = sys.argv[1:]
        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            r = asyncio.run(main(days, extra_currency))
    except ValueError:
        days = sys.argv[1]
        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            r = asyncio.run(main(days))
    print(r)
