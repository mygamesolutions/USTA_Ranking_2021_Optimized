# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import os 
import csv
from pathlib import Path
from USTA_2021_Ranking_Optimized.items import Usta2021RankingOptimizedItem
data_fields = Usta2021RankingOptimizedItem.fields.keys()

class Usta2021RankingOptimizedPipeline:
    def process_item(self,item,spider):
        filename = spider.file_name
        folder = spider.folder
        
        if not os.path.exists(folder):
            os.makedirs(folder)
        else:
            pass

        myfile = os.path.join(folder, filename)
        myfil = Path(myfile)
        headers = list(data_fields)

        if myfil.exists():
            with open(myfil, "a") as csvfile:                
                writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n',fieldnames=headers,quoting=csv.QUOTE_ALL)
                # writer = csv.DictWriter(csvfile,lineterminator='\n',fieldnames=headers)#,quoting=csv.QUOTE_ALL)
                writer.writerow(item)
        else:
            with open(myfil, "w") as csvfile:
                writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n',fieldnames=headers,quoting=csv.QUOTE_ALL)
                #   writer = csv.DictWriter(csvfile, lineterminator='\n',fieldnames=headers)#,quoting=csv.QUOTE_ALL)
                writer.writeheader()  # file doesn't exist yet, write a header
                writer.writerow(item)
        return item
