import csv
import pandas as pd


def csv2dict(filename):
    new_list = []
    with open(filename, 'r') as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
            new_dict = {}
            new_dict['time'] = row['time']
            new_dict['price'] = row['order_price']
            new_dict['volume'] = int(row['order_volume'])
            new_dict['order'] = row['order']
            if row.get('order_kind') and row.get('function_code'):
                new_dict['order_kind'] = row['order_kind']
                new_dict['function_code'] = row['function_code']
            new_list.append(new_dict)
        return new_list


def write_csv_content(time, trade_price, trade_volume, ask, bid):
    f = open('trade.csv', 'a', encoding='utf-8', newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow([time, trade_price, trade_volume, ask, bid])
    f.close()


def write_csv_order():
    f = open('order_book.csv', 'w', encoding='utf-8')
    csv_writer = csv.writer(f)
    csv_writer.writerow(['time', 'trade_price', 'volume'])
    f.close()


# write_csv_order()


def write_csv_orderbook(time, trade_price, volume):
    f = open('order_book.csv', 'a', encoding='utf-8', newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow([time, trade_price, volume])
    f.close()


def write_csv():
    f = open('trade.csv', 'w', encoding='utf-8')
    csv_writer = csv.writer(f)
    csv_writer.writerow(['time', 'trade_price', 'trade_volume', 'ask', 'bid'])
    f.close()


# write_csv()


def open_price_function():

    buy_list = csv2dict('b2.csv')
    sell_list = csv2dict('s2.csv')
    # i控制sell
    i = 0
    # j控制buy
    j = 0
    amount = 0
    result_volume = min(buy_list[j]['volume'], sell_list[j]['volume'])

    while buy_list[j]['price'] >= sell_list[i]['price']:
        result_volume = min(buy_list[j]['volume'], sell_list[i]['volume'])
        if result_volume == buy_list[j]['volume'] and buy_list[j]['volume'] != sell_list[i]['volume']:
            buy_list[j]['volume'] = 0
            sell_list[i]['volume'] = sell_list[i]['volume'] - result_volume
            # write_csv_content('92500000', '22600', result_volume, sell_list[i]['order'], buy_list[j]['order'])
            j += 1
            amount += result_volume
        elif result_volume == sell_list[i]['volume'] and buy_list[j]['volume'] != sell_list[i]['volume']:
            sell_list[i]['volume'] = 0
            buy_list[j]['volume'] = buy_list[j]['volume'] - result_volume
            # write_csv_content('92500000', '22600', result_volume, sell_list[i]['order'], buy_list[j]['order'])
            i += 1
            amount += result_volume
        elif buy_list[j]['volume'] == sell_list[i]['volume']:
            buy_list[j]['volume'] = 0
            sell_list[i]['volume'] = 0
            # write_csv_content('92500000', '22600', result_volume, sell_list[i]['order'], buy_list[j]['order'])
            i += 1
            j += 1
            amount += result_volume

    write_csv_orderbook('92500000', buy_list[j]['price'], amount)
    return buy_list, sell_list, buy_list[j]['price'], amount


buy_list, sell_list, open_price, amount = open_price_function()


order_book = pd.read_csv('order_book.csv')
order_book = order_book.groupby(['time'])['volume'].sum()
order_book = pd.DataFrame(order_book)
order_book.to_csv('test.csv')
# print(order_book)



