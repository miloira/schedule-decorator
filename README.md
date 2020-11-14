# schedule-decorator

## 例子
### 执行任务
```python
from schedule_decorator import Timer

t = Timer()

@t.every("1","day","08:00:00")
def task():
    print("起床啦！")

t.run()
```
### 支持异步执行
```python
#-*-coding:utf-8-*-
from schedule_decorator import Timer
import time

t = Timer()

n = 1
m = 1
@t.every("1", "s")
def _():
    global n
    print("t1---", n)
    time.sleep(5)
    n += 1

@t.every("1", "s")
def _():
    global m
    print("t2---", m)
    m += 1

t.run()

```

## 参数说明
```python
# 具体时间执行
# @t.every('1','second')              # 每1秒钟执行一次
# @t.every('2','minute')              # 每2分钟执行一次
# @t.every('2','minute',':05')        # 每2分钟的第5秒执行一次
# @t.every('5','hour')                # 每5小时执行一次
# @t.every('5','hour','25:30')        # 每5小时的第25分钟30秒执行一次
# @t.every('2','day')                 # 每2天执行一次
# @t.every('2','day','00:00:00')      # 每2天的00:00:00执行一次

# @t.every('1','week')                # 每周执行
# @t.every('1','monday')              # 每个星期一执行一次
# @t.every('1','tuesday')             # 每个星期二执行一次
# @t.every('1','wednesday')           # 每个星期三执行一次
# @t.every('1','thursday')            # 每个星期四执行一次
# @t.every('1','friday')              # 每个星期五执行一次
# @t.every('1','saturday')            # 每个星期六执行一次
# @t.every('1','sunday')              # 每个星期天执行一次
# @t.every('1','monday','12:00:00')   # 每个星期一的12:00:00执行一次

# 随机时间范围执行
# @t.every('1-5','second')             # 随机每1到5秒执行一次
# @t.every('1-5','minute')             # 随机每1到5分钟执行一次
# @t.every('1-5','minute',':05')       # 随机每1到5分钟的第5秒执行执行一次
# @t.every('1-5','hour')               # 随机每1到5小时执行一次
# @t.every('1-5','hour','20:10')       # 随机每1到5小时第20分钟的第10秒执行一次
# @t.every('1-5','day')                # 随机每1到5天执行一次
# @t.every('1-5','day','00:00:20')     # 随机每1到5天00:00:20执行一次
# t.every('1-2','week')                # 随机每1到5周执行一次

# @t.every('1-2','monday')              # 随机每1到2个星期一执行一次
# @t.every('1-2','tuesday')             # 随机每1到2个星期二执行一次
# @t.every('1-2','wednesday')           # 随机每1到2个星期三执行一次
# @t.every('1-2','thursday')            # 随机每1到2个星期四执行一次
# @t.every('1-2','friday')              # 随机每1到2个星期五执行一次
# @t.every('1-2','saturday')            # 随机每1到2个星期六执行一次
# @t.every('1-2','sunday')              # 随机每1到2个星期天执行一次
# @t.every('1-2','monday','00:00:05')   # 随机每1到2个星期一的00:00:05执行一次

# 时间类型参数可使用简写
# second       s
# minute       m
# hour         h
# day          d
# week         w
# 
# monday       mon
# tuesday      tue
# wednesday    wed
# thursday     thu
# friday       fri
# saturday     sat
# sunday       sun
```
