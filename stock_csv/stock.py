import pandas as pd

p_o_all = pd.read_csv('000629.O.csv')
p_o_simple = p_o_all[['time', 'order', 'order_kind', 'function_code', 'order_price', 'order_volume']]
p_o_1 = p_o_all.loc[(p_o_all['time'] >= 91500020) & (p_o_all['time'] <= 92455820)]
p_t_all = pd.read_csv('000629.T.csv')
p_t_c = p_t_all.loc[(p_t_all['time'] >= 91503450) & (p_t_all['time'] <= 91957750)]
list1 = p_t_c[['ask_order',  'bid_order']]
list2 = list1.ask_order[list1['ask_order'] != 0].tolist()
list3 = list1.bid_order[list1['bid_order'] != 0].tolist()
list4 = list2 + list3
test = list(p_o_1.order)
for i in list4:
    test.remove(i)
df_data = p_o_1[p_o_1.order.isin(test)]
list_s = df_data[df_data['function_code'] == 'S']
list_b = df_data[df_data['function_code'] == 'B']
b_sort = list_b.sort_values(by=['order_price', 'time'], ascending=(False, True))
s_sort = list_s.sort_values(by=['order_price', 'time'], ascending=(True, True))
# s_sum = s_sort['order_volume'].groupby(s_sort['order_price']).sum()
# b_sum = b_sort['order_volume'].groupby(b_sort['order_price']).sum()
# sum_all = pd.DataFrame([s_sum, b_sum])
b_sort[['time', 'order', 'order_price', 'order_volume']].to_csv('b2.csv')
s_sort[['time', 'order', 'order_price', 'order_volume']].to_csv('s2.csv')

print(b_sort)
