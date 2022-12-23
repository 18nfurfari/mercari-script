import mercari
import time
import discord_notify as dn
from datetime import datetime
import numpy as np


def main():
    # def search(keywords, sort="created_time", order="desc", status="on_sale", limit=120):
    search_query = "のカービィ ときめきクレーン"

    # send that invite link again
    notifier = dn.Notifier(
        "https://discord.com/api/webhooks/1055628680082239618/Dq8aDfJLyPo5B3m2QH8awMZn_qN7IxRHLqNuVSh-kw-mkDfktJPMKZFs2gvD3TBdLuYj")

    # forming initial "old" list
    print("-----Old list formed-----", datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
    old_List, old_count = perform_search(search_query)
    print("Old list count: ", old_count)

    # sleep for 10 seconds to slow down next call
    time.sleep(10)


    while True:
        # forming new list of items
        print("-----Checking for new items-----", datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        new_List, new_count = perform_search(search_query)
        print("New list count: ", new_count)

        # resetting old list because an item sold
        if old_count - new_count > 0:
            print("Item sold, reformatting old list")
            old_List, old_count = perform_search(search_query)

            print("-----Old list formed-----", datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            print("Old list count: ", old_count)

        # sending discord notifications if new listings
        elif old_count - new_count < 0:
            notifier.send("----------New Items!----------", print_message=True)

            # finding items in new_List NOT in old_List (broken)
            listings = [item for item in new_List if item not in old_List]

            # sending discord notification for each new listing
            for item in listings:
                discord_message = item.productName + " " + item.productURL \
                                  + "               " + item.imageURL + " "
                notifier.send(discord_message, print_message=True)
                time.sleep(1)

            # reset old list
            print("New item listed, reformatting old list")
            old_List, old_count = perform_search(search_query)
            print("-----Old list formed-----", datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            print("Old list count: ", old_count)


        # refreshing search every 10 minutes
        time.sleep(600)


def perform_search(search_query):
    item_list = []
    item_count = 0
    search_success = False

    while not search_success:
        try:
            for item in mercari.search(search_query):
                item_list.append(item)
                item_count += 1
            search_success = True
        except:
            print("API error, searching again...")
            item_list = []
            item_count = 0
            time.sleep(10)

    return item_list, item_count


if __name__ == '__main__':
    main()
