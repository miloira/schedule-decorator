# schedule-decorator


```python
from schedule_decorator import Timer

t = Timer()

@t.every("1","day","08:00:00")
def task():
    print("起床啦！")

t.run()
```
