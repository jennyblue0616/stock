import pandas as pd

from sort_price import csv2dict

p_t_all = pd.read_csv('000629.T.csv')
p_t_c = p_t_all.loc[(p_t_all['time'] >= 93000080) & (p_t_all['function_code'] == 'C')]
list1 = p_t_c[['trade_volume', 'ask_order',  'bid_order']]
list_c = []
list_b = []
dict1 = {}

for index, row in list1.iterrows():
    if row['ask_order']:
        list_b.append(row['ask_order'])
    elif row['bid_order']:
        list_b.append(row['bid_order'])

# print(list_b)
# [146066, 237015, 256676, 280450,
# 所有撤单的数据
for index, row in list1.iterrows():
    if row['ask_order']:
        dict1[str(row['ask_order'])] = row['trade_volume']
    elif row['bid_order']:
        dict1[str(row['bid_order'])] = row['trade_volume']

# print(dict1)
# {'146066': 100, '237015': 100, '256676': 100, '280450': 100, '146065': 100, '237046': 100,
result = csv2dict('o_continue.csv')
# print(result)
# 'volume': 10000,'order': '1757368', 'order_kind': '0', 'function_code': 'S'}
list_a = []
def chedan():
    for i in result:
        if int(i['order']) in list_b:
            if i['volume'] == dict1[i['order']]:
                # print(i)
                # print(dict1[i['order']])
                list_a.append(int(i['order']))
    return list_a

list_a = chedan()
# list_a是完全撤销的
# print(list_a)
list_123 = []
for i in list_b:
    if i not in list_a:
        list_123.append(i)
# list_123中的数据是没有完全撤销的
print(list_123)

