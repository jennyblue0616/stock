import json

import pandas as pd

from sort_price import open_price_function


p_t_all = pd.read_csv('000629.T.csv')
p_t_c = p_t_all.loc[(p_t_all['time'] >= 93000080) & (p_t_all['function_code'] == 'C')]
# p_t_c_2 = p_t_all.loc[(p_t_all['time'] < 93000080) & (p_t_all['function_code'] == 'C')]
list1 = p_t_c[['ask_order',  'bid_order']]
list_c = []

# 所有撤单的数据
for index, row in list1.iterrows():
    if row['ask_order']:
        list_c.append(row['ask_order'])
    elif row['bid_order']:
        list_c.append(row['bid_order'])
# print(list_c)

buy_list, sell_list, open_price, amount = open_price_function()


def generate_list(list1):
    for i in list1[::-1]:
        if i['volume'] == 0:
            list1.remove(i)
        # if int(i['order']) in list_c:
        #     list1.remove(i)
    return list1


order_buy_list = generate_list(buy_list)
order_sell_list = generate_list(sell_list)
# print(order_sell_list)
# print(order_buy_list)
set1 = set()
for i in order_buy_list:
    set1.add(i['price'])
buy_10 = sorted(list(set1), reverse=True)[:10]
print(buy_10)
i = 0
dict1 = {}
while i < 10:
    amount = 0
    for item in buy_list:
        if item['price'] == buy_10[i]:
            amount += item['volume']
    dict1[buy_10[i]] = amount
    i += 1
print(dict1)

for i in order_sell_list:
    set1.add(i['price'])
sell_10 = sorted(list(set1))
# print(sell_10)

# 去除撤单
# with open('sell_list.json', 'w', encoding='utf-8') as f:
#     json.dump(order_sell_list, f)
# with open('buy_list.json', 'w', encoding='utf-8') as f:
#     json.dump(order_buy_list, f)

