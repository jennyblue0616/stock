# 连续竞价阶段
import json

from sort_price import csv2dict, write_csv_content, write_csv_orderbook

import pandas as pd

p_t_all = pd.read_csv('000629.T.csv')
p_t_c = p_t_all.loc[(p_t_all['time'] >= 93000080) & (p_t_all['function_code'] == 'C')]
list1 = p_t_c[['trade_volume', 'ask_order',  'bid_order']]
list_c = []
list_b = []
dict1 = {}

#list_b 所有撤单
for index, row in list1.iterrows():
    if row['ask_order']:
        list_b.append(row['ask_order'])
    elif row['bid_order']:
        list_b.append(row['bid_order'])


for index, row in list1.iterrows():
    if row['ask_order']:
        dict1[str(row['ask_order'])] = row['trade_volume']
    elif row['bid_order']:
        dict1[str(row['bid_order'])] = row['trade_volume']


result = csv2dict('o_continue.csv')
list_a = []


def chedan():
    for i in result:
        if int(i['order']) in list_b:
            if i['volume'] == dict1[i['order']]:
                list_a.append(int(i['order']))
    return list_a

#list_a 完全撤单
list_a = chedan()


# 读取集合竞价剩余的交易
with open('sell_list.json', 'r', encoding='utf-8') as f:
    sell_list = json.load(f)

with open('buy_list.json', 'r', encoding='utf-8') as f:
    buy_list = json.load(f)


def sort_buy_list(item):
    buy_list.append(item)
    buy_list.sort(key=lambda x: (-int(x['price']), int(x['time'])))


def sort_sell_list(item):
    sell_list.append(item)
    sell_list.sort(key=lambda x: (x['price'], int(x['time'])))


def continue_trade():
    for i in range(9520):
        volume_totall = 0
        # 先看有没有撤单
        # if result[i]['order'] == '5093143':
        #     print('123')
        if int(result[i]['order']) not in list_a:
            # 0为限价
            if result[i]['order_kind'] == '0':
                if result[i]['function_code'] == 'B':
                    # 与sell_list第一个值的价格A进行比较
                    while int(result[i]['price']) >= int(sell_list[0]['price']):
                        # 以A价格成交, 成交量以两者中最小量为准
                        trade_price = sell_list[0]['price']
                        trade_volume = min(result[i]['volume'], sell_list[0]['volume'])
                        # write_csv_content(result[i]['time'], trade_price, trade_volume, sell_list[0]['order'],
                        #                   result[i]['order'])
                        volume_totall += trade_volume
                        # 写入orderbook
                        write_csv_orderbook(result[i]['time'], trade_price, volume_totall)
                        if trade_volume == sell_list[0]['volume']:
                            # result v 还有剩余
                            result[i]['volume'] = result[i]['volume'] - trade_volume
                            sell_list[0]['volume'] = 0
                            if sell_list[0]['volume'] == 0:
                                # 去除sell_list第一个值
                                del sell_list[0]
                            if result[i]['volume'] == 0:
                                break
                        elif trade_volume == result[i]['volume']:
                            # sell v 还有剩余
                            sell_list[0]['volume'] = sell_list[0]['volume'] - trade_volume
                            break

                    else:
                        # 插入买方队列合适的位置中
                        sort_buy_list(result[i])

                elif result[i]['function_code'] == 'S':
                    #与buy_list第一个值的价格B进行比较
                    while int(result[i]['price']) <= int(buy_list[0]['price']):
                        # 以B价格成交
                        trade_price = buy_list[0]['price']
                        trade_volume = min(result[i]['volume'], buy_list[0]['volume'])
                        # write_csv_content(result[i]['time'], trade_price, trade_volume, result[i]['order'],
                        #                   buy_list[0]['order'])
                        volume_totall += trade_volume
                        # 写入orderbook
                        write_csv_orderbook(result[i]['time'], trade_price, volume_totall)
                        if trade_volume == buy_list[0]['volume']:
                            # result v 还有剩余
                            result[i]['volume'] -= trade_volume
                            buy_list[0]['volume'] = 0
                            if buy_list[0]['volume'] == 0:
                                # 去除buy_list第一个值
                                del buy_list[0]
                            if result[i]['volume'] == 0:
                                break
                        elif trade_volume == result[i]['volume']:
                            buy_list[0]['volume'] = buy_list[0]['volume'] - trade_volume
                            break
                    else:
                        # 插入卖方队列合适的位置中
                        sort_sell_list(result[i])


            if result[i]['order_kind'] == '1':
                if result[i]['function_code'] == 'B':
                    # 一直到数量成交完为止
                    while result[i]['volume'] != 0:
                        if result[i]['volume'] < sell_list[0]['volume']:
                            # write_csv_content(result[i]['time'], sell_list[0]['price'], result[i]['volume'],
                            #                   sell_list[0]['order'], result[i]['order'])
                            volume_totall += result[i]['volume']
                            sell_list[0]['volume'] = sell_list[0]['volume'] - result[i]['volume']
                            result[i]['volume'] = 0
                        elif result[i]['volume'] > sell_list[0]['volume']:
                            # write_csv_content(result[i]['time'], sell_list[0]['price'], sell_list[0]['volume'],
                            #                   sell_list[0]['order'], result[i]['order'])
                            volume_totall += sell_list[0]['volume']
                            result[i]['volume'] = result[i]['volume'] - sell_list[0]['volume']
                            sell_list[0]['volume'] = 0
                            if sell_list[0]['volume'] == 0:
                                del sell_list[0]
                        elif result[i]['volume'] == sell_list[0]['volume']:
                            # write_csv_content(result[i]['time'], sell_list[0]['price'], sell_list[0]['volume'],
                            #                   sell_list[0]['order'], result[i]['order'])
                            volume_totall += sell_list[0]['volume']
                            result[i]['volume'] = 0
                            sell_list[0]['volume'] = 0
                            if sell_list[0]['volume'] == 0:
                                del sell_list[0]
                    write_csv_orderbook(result[i]['time'], sell_list[0]['price'], volume_totall)
                elif result[i]['function_code'] == 'S':
                    # 一直到数量成交完为止
                    while result[i]['volume'] != 0:
                        if result[i]['volume'] < buy_list[0]['volume']:
                            # write_csv_content(result[i]['time'], buy_list[0]['price'], result[i]['volume'],
                            #                   result[i]['order'],
                            #                   buy_list[0]['order'])
                            volume_totall += result[i]['volume']
                            buy_list[0]['volume'] = buy_list[0]['volume'] - result[i]['volume']
                            result[i]['volume'] = 0
                        elif result[i]['volume'] > buy_list[0]['volume']:
                            # write_csv_content(result[i]['time'], buy_list[0]['price'], buy_list[0]['volume'], result[i]['order'], buy_list[0]['order'])
                            volume_totall += buy_list[0]['volume']
                            result[i]['volume'] = result[i]['volume'] - buy_list[0]['volume']
                            buy_list[0]['volume'] = 0
                            if buy_list[0]['volume'] == 0:
                                del buy_list[0]
                        elif result[i]['volume'] == buy_list[0]['volume']:
                            # write_csv_content(result[i]['time'], buy_list[0]['price'], buy_list[0]['volume'],
                            #                    result[i]['order'], buy_list[0]['order'])
                            volume_totall += buy_list[0]['volume']
                            result[i]['volume'] = 0
                            buy_list[0]['volume'] = 0
                            if buy_list[0]['volume'] == 0:
                                del buy_list[0]
                    write_csv_orderbook(result[i]['time'], buy_list[0]['price'], volume_totall)
            if result[i]['order_kind'] == 'U':
                if result[i]['function_code'] == 'B':
                    result[i]['price'] = buy_list[0]['price']
                    # 与sell_list第一个值的价格A进行比较
                    while int(result[i]['price']) >= int(sell_list[0]['price']):
                        # 以A价格成交, 成交量以两者中最小量为准
                        trade_price = sell_list[0]['price']
                        trade_volume = min(result[i]['volume'], sell_list[0]['volume'])
                        # write_csv_content(result[i]['time'], trade_price, trade_volume, sell_list[0]['order'],
                        #                   result[i]['order'])
                        volume_totall += trade_volume
                        write_csv_orderbook(result[i]['time'], trade_price, volume_totall)
                        if trade_volume == sell_list[0]['volume']:
                            # result v 还有剩余
                            result[i]['volume'] = result[i]['volume'] - trade_volume
                            sell_list[0]['volume'] = 0
                            if sell_list[0]['volume'] == 0:
                                # 去除sell_list第一个值
                                del sell_list[0]
                            if result[i]['volume'] == 0:
                                break
                        elif trade_volume == result[i]['volume']:
                            # sell v 还有剩余
                            sell_list[0]['volume'] = sell_list[0]['volume'] - trade_volume
                            break
                    else:
                        # 插入买方队列合适的位置中
                        sort_buy_list(result[i])

                elif result[i]['function_code'] == 'S':
                    result[i]['price'] = sell_list[0]['price']
                    # 与buy_list第一个值的价格B进行比较
                    while int(result[i]['price']) <= int(buy_list[0]['price']):
                        # 以B价格成交
                        trade_price = buy_list[0]['price']
                        trade_volume = min(result[i]['volume'], buy_list[0]['volume'])
                        # write_csv_content(result[i]['time'], trade_price, trade_volume, result[i]['order'],
                        #                   buy_list[0]['order'])
                        volume_totall += trade_volume
                        write_csv_orderbook(result[i]['time'], trade_price, volume_totall)
                        if trade_volume == buy_list[0]['volume']:
                            # result v 还有剩余
                            result[i]['volume'] -= trade_volume
                            buy_list[0]['volume'] = 0
                            if buy_list[0]['volume'] == 0:
                                # 去除buy_list第一个值
                                del buy_list[0]
                            if result[i]['volume'] == 0:
                                break
                        elif trade_volume == result[i]['volume']:
                            buy_list[0]['volume'] = buy_list[0]['volume'] - trade_volume
                            break
                    else:
                        # 插入卖方队列合适的位置中
                        sort_sell_list(result[i])

        else:
            continue


continue_trade()
# print(sell_list)
# print(buy_list)

close = csv2dict('close.csv')
# print(close)
for i in close:
    if i['function_code'] == 'B':
        buy_list.append(i)
    elif i['function_code'] == 'S':
        sell_list.append(i)
buy_list.sort(key=lambda x: (-int(x['price']), int(x['time'])))
sell_list.sort(key=lambda x: (x['price'], int(x['time'])))


def close_price_function():

    # buy_list = csv2dict('b2.csv')
    # sell_list = csv2dict('s2.csv')
    # i控制sell
    i = 0
    # j控制buy
    j = 0
    amount = 0

    result_volume = min(buy_list[j]['volume'], sell_list[j]['volume'])
    while buy_list[j]['price'] >= sell_list[i]['price']:
        # if buy_list[j]['order'] == '18481560':
        #     print('111')
        result_volume = min(buy_list[j]['volume'], sell_list[i]['volume'])
        if result_volume == buy_list[j]['volume'] and buy_list[j]['volume'] != sell_list[i]['volume']:
            buy_list[j]['volume'] = 0
            sell_list[i]['volume'] = sell_list[i]['volume'] - result_volume
            # write_csv_content('150000000', '22500', result_volume, sell_list[i]['order'], buy_list[j]['order'])
            j += 1
            amount += result_volume
        elif result_volume == sell_list[i]['volume'] and buy_list[j]['volume'] != sell_list[i]['volume']:
            sell_list[i]['volume'] = 0
            buy_list[j]['volume'] = buy_list[j]['volume'] - result_volume
            # write_csv_content('150000000', '22500', result_volume, sell_list[i]['order'], buy_list[j]['order'])
            i += 1
            amount += result_volume
        elif buy_list[j]['volume'] == sell_list[i]['volume']:
            buy_list[j]['volume'] = 0
            sell_list[i]['volume'] = 0
            # write_csv_content('150000000', '22500', result_volume, sell_list[i]['order'], buy_list[j]['order'])
            i += 1
            j += 1
            amount += result_volume
    write_csv_orderbook('150003000', buy_list[j]['price'], amount)
    return buy_list, sell_list, buy_list[j]['price'], amount


buy_list, sell_list, close_price, close_amount = close_price_function()