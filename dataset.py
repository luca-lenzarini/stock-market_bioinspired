import pandas as pd 
import numpy as np

lines_per_day = 10
start_time = 9


# current_date = pd.to_datetime({'year': 2020, 'month': 1, 'day': 1})
day = 2
month = 1
year = 2020

# pd.date_range(start='1/1/2020', periods=10)

datas = []

for i in range(20):

    start_datetime = '01/' + str(day) + '/2020 09:00:00'

    hours_day = pd.date_range(start=start_datetime, periods=10, freq='1H')
    a = hours_day.to_pydatetime()

    # print(a)
    if len(datas) == 0:
        datas = hours_day.to_pydatetime()
    else:
        datas = np.concatenate((datas, hours_day.to_pydatetime()))

    day += 1


novas_datas = [date_obj.strftime('%d/%m/%Y %H:%M') for date_obj in datas]

value = 5
final_value = 10

step = (final_value - value) / 200

## sobe
values = [(str(np.random.uniform(i - (5 * step) , i + (5 * step))).replace('.',',')) for i in np.arange(value, final_value, step)]

## desce
# values = [(str(np.random.uniform(i - (5 * step) , i + (5 * step))).replace('.',',')) for i in np.arange(final_value, value, step)]

## sobe desce
# values = []
# a = 0
# count = 0
# for i in np.arange(value, final_value, step):

#     count += 1

#     j = ''
#     if count > 129:
#         a -= step
#         j = str(np.random.uniform(a - (5 * step) , a + (5 * step))).replace('.',',')
#     else:
#         a = i
#         j = str(np.random.uniform(a - (5 * step) , a + (5 * step))).replace('.',',')

#     values.append(j)

## desce sobe
# values = []
# a = 0
# count = 0
# for i in np.arange(final_value, value, step):

#     count += 1

#     j = ''
#     if count > 129:
#         a -= step
#         j = str(np.random.uniform(a - (5 * step) , a + (5 * step))).replace('.',',')
#     else:
#         a = i
#         j = str(np.random.uniform(a - (5 * step) , a + (5 * step))).replace('.',',')

#     values.append(j)


d = {'Data': novas_datas, 'Values': values}

df = pd.DataFrame(data=d)

df[::-1].to_csv('tab_1.csv', index = False, header=True)


    
