import scrapy
import json
from USTA_2021_Ranking_Optimized.items import Usta2021RankingOptimizedItem

class UstaRankingSpider(scrapy.Spider):
    name = 'usta_ranking'
    allowed_domains = []
    start_urls = ['https://www.usta.com']
    file_name = "ranking"
    folder = "data/"

    def parse(self, response):
        data ={}
        auth_url = "https://www.usta.com/etc/usta/nologinjwt.nljwt.json"
        headers = {
            "Origin": "https://www.usta.com",
            "Referer": "https://www.usta.com/en/home/play/rankings/juniors-combined.html",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        yield scrapy.Request(auth_url, method="POST", headers=headers,body=json.dumps(data),callback=self.parse_cookies)

    def parse_cookies(self, response):
        json_data = json.loads(response.text)
        authorization_token = json_data["access_token"]
        li = [
            "JUNIOR_NULL_M_STANDING_Y18_UNDER_NULL_NULL_NULL",
            "JUNIOR_NULL_M_STANDING_Y14_UNDER_NULL_NULL_NULL"
            "JUNIOR_NULL_M_STANDING_Y12_UNDER_NULL_NULL_NULL",
            "JUNIOR_NULL_M_STANDING_Y16_UNDER_NULL_NULL_NULL",
            "JUNIOR_NULL_F_STANDING_Y14_UNDER_NULL_NULL_NULL",
            "JUNIOR_NULL_F_STANDING_Y16_UNDER_NULL_NULL_NULL",
            "JUNIOR_NULL_F_STANDING_Y18_UNDER_NULL_NULL_NULL",
            "JUNIOR_NULL_F_STANDING_Y12_UNDER_NULL_NULL_NULL",
            "JUNIOR_NULL_M_SEEDING_Y12_UNDER_DOUBLES_INDIVIDUAL_NULL",
            "JUNIOR_NULL_M_SEEDING_Y14_UNDER_DOUBLES_INDIVIDUAL_NULL",
            "JUNIOR_NULL_M_SEEDING_Y16_UNDER_DOUBLES_INDIVIDUAL_NULL",
            "JUNIOR_NULL_M_SEEDING_Y18_UNDER_DOUBLES_INDIVIDUAL_NULL",
            "JUNIOR_NULL_F_SEEDING_Y16_UNDER_DOUBLES_INDIVIDUAL_NULL",
            "JUNIOR_NULL_F_SEEDING_Y12_UNDER_DOUBLES_INDIVIDUAL_NULL",
            "JUNIOR_NULL_F_SEEDING_Y14_UNDER_DOUBLES_INDIVIDUAL_NULL",
            "JUNIOR_NULL_F_SEEDING_Y18_UNDER_DOUBLES_INDIVIDUAL_NULL"
        ]
        for j in li[:2]:
            for i in range(1, 101):
                headers = {
                    "Accept": "*/*",
                    "Authorization": "Bearer " + authorization_token,
                    "Content-Type": "application/json; charset=UTF-8",
                }
                data = {
                    "pagination": {"pageSize": 100, "currentPage": i},
                    "selection": {"catalogId": j},
                }
                url = "https://services.usta.com/v1/dataexchange/rankings/search/public"
                yield scrapy.Request(
                    url,
                    method="POST",
                    headers=headers,
                    body=json.dumps(data),
                    callback=self.parse_tournament,
                )
                break

    def parse_tournament(self, response):
        details = json.loads(response.text)
        if details.get("data"):
            for i in range(len(details)):
                list = details.get("displayLabel")
                bonusPoint = details["data"][i]["pointsRecord"]["bonusPoints"]
                doublesPoints = details["data"][i]["pointsRecord"]["doublesPoints"]
                singlesPoints = details["data"][i]["pointsRecord"]["singlesPoints"]
                district = details["data"][i]["district"]["name"]
                playerName = details["data"][i]["name"]
                points = details["data"][i]["points"]
                rank = details["data"][i]["rank"]
                section = details["data"][i]["section"]["name"]
                state = details["data"][i]["state"]
                uaid = details["data"][i]["uaid"]
                city = details["data"][i]["city"]
                rank_list = list.replace("'", "")
                rank_list1 = rank_list.split(" ")
                p = rank_list1[0] + " " + rank_list1[1]
                div = list.replace("(", "").replace(")", "")
                key = div.split(" ")
                
                if "Doubles" in key:
                    nametype = "Doubles"
                elif "combined" in key:
                    nametype = "Singles"

                data = {
                    "bonusPoints": bonusPoint,
                    "division": p,
                    "type": nametype,
                    "doublesPoints": doublesPoints,
                    "singlesPoints": singlesPoints,
                    "district": district,
                    "name": playerName,
                    "combinedPoints": points,
                    "defaultSection": "National",
                    "rank": rank,
                    "section": section,
                    "state": state,
                    "list": list,
                    "uaid": uaid,
                    "city": city,
                }
                yield Usta2021RankingOptimizedItem(**data)
