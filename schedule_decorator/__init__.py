#-*-coding:utf-8-*-
from schedule import Scheduler
import threading
import time
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

timer_instance = []
class Timer(object):
    def __init__(self, buffer_time=0, multithreading=False):
        super().__init__()
        # schedule 所有任务轮询间隔时间
        self.buffer_time = buffer_time
        # 多线程开关
        self.multithreading = multithreading
        # 具体时间 未指定精确时间
        self.funcs_second_timer = {}
        self.funcs_minute_timer = {}
        self.funcs_hour_timer = {}
        self.funcs_day_timer = {}

        self.funcs_monday_timer = {}
        self.funcs_tuesday_timer = {}
        self.funcs_wednesday_timer = {}
        self.funcs_thursday_timer = {}
        self.funcs_friday_timer = {}
        self.funcs_saturday_timer = {}
        self.funcs_sunday_timer = {}
        self.funcs_week_timer = {}

        # 具体时间 指定精确时间
        self.funcs_minute_concrete_timer = {}
        self.funcs_hour_concrete_timer = {}

        self.funcs_day_concrete_timer = {}
        self.funcs_monday_concrete_timer = {}
        self.funcs_tuesday_concrete_timer = {}
        self.funcs_wednesday_concrete_timer = {}
        self.funcs_thursday_concrete_timer = {}
        self.funcs_friday_concrete_timer = {}
        self.funcs_saturday_concrete_timer = {}
        self.funcs_sunday_concrete_timer = {}

        # 时间范围 未指定精确时间
        self.funcs_second_random_timer = {}
        self.funcs_minute_random_timer = {}
        self.funcs_hour_random_timer = {}

        self.funcs_day_random_timer = {}
        self.funcs_week_random_timer = {}
        self.funcs_monday_random_timer = {}
        self.funcs_tuesday_random_timer = {}
        self.funcs_wednesday_random_timer = {}
        self.funcs_thursday_random_timer = {}
        self.funcs_friday_random_timer = {}
        self.funcs_saturday_random_timer = {}
        self.funcs_sunday_random_timer = {}

        # 时间范围 指定精确时间
        self.funcs_minute_random_concrete_timer = {}
        self.funcs_hour_random_concrete_timer = {}

        self.funcs_day_random_concrete_timer = {}
        self.funcs_monday_random_concrete_timer = {}
        self.funcs_tuesday_random_concrete_timer = {}
        self.funcs_wednesday_random_concrete_timer = {}
        self.funcs_thursday_random_concrete_timer = {}
        self.funcs_friday_random_concrete_timer = {}
        self.funcs_saturday_random_concrete_timer = {}
        self.funcs_sunday_random_concrete_timer = {}

    def every(self, timer_sum, timer_type, timer_concrete=None):
        def decorator(func):
            nonlocal timer_sum
            nonlocal timer_type
            # 判断传入的参数类型
            if isinstance(timer_sum, str):
                # 处理传入的字符串
                if '-' not in timer_sum:
                    # 如果是具体时间 整型处理
                    timer_sum = int(timer_sum)
                else:
                    # 如果是时间范围 字符串处理
                    timer_sum = timer_sum
            else:
                # 不是字符类型直接抛出错误
                raise Exception("timer_sum error!")

            # 具体时间 未指定精确时间时
            if isinstance(timer_sum, int) and timer_concrete == None:
                # 每小时/分钟/秒钟计时类型单参数选择
                if timer_type in ('s', 'second'):
                    self.funcs_second_timer[func] = timer_sum
                elif timer_type in ('m', 'minute'):
                    self.funcs_minute_timer[func] = timer_sum
                elif timer_type in ('h', 'hour'):
                    self.funcs_hour_timer[func] = timer_sum

                elif timer_type in ('d', 'day'):
                    self.funcs_day_timer[func] = timer_sum
                elif timer_type in ('mon', 'monday'):
                    self.funcs_monday_timer[func] = timer_sum
                elif timer_type in ('tue', 'tuesday'):
                    self.funcs_tuesday_timer[func] = timer_sum
                elif timer_type in ('wed', 'wednesday'):
                    self.funcs_wednesday_timer[func] = timer_sum
                elif timer_type in ('thu', 'thursday'):
                    self.funcs_thursday_timer[func] = timer_sum
                elif timer_type in ('fri', 'friday'):
                    self.funcs_friday_timer[func] = timer_sum
                elif timer_type in ('sat', 'saturday'):
                    self.funcs_saturday_timer[func] = timer_sum
                elif timer_type in ('sun', 'sunday'):
                    self.funcs_sunday_timer[func] = timer_sum
                elif timer_type in ('w', 'week'):
                    self.funcs_week_timer[func] = timer_sum

            # 具体时间 指定了精确时间时
            elif isinstance(timer_sum, int) and timer_concrete != None:
                # 每小时/分钟/秒钟计时类型 传入具体时间
                if timer_type in ('m', 'minute'):
                    self.funcs_minute_concrete_timer[func] = [timer_sum, timer_concrete]
                elif timer_type in ('h', 'hour'):
                    self.funcs_hour_concrete_timer[func] = [timer_sum, timer_concrete]
                elif timer_type in ('d', 'day'):
                    self.funcs_day_concrete_timer[func] = [timer_sum, timer_concrete]
                elif timer_type in ('mon', 'monday'):
                    self.funcs_monday_concrete_timer[func] = [timer_sum, timer_concrete]
                elif timer_type in ('tue', 'tuesday'):
                    self.funcs_tuesday_concrete_timer[func] = [timer_sum, timer_concrete]
                elif timer_type in ('wed', 'wednesday'):
                    self.funcs_wednesday_concrete_timer[func] = [timer_sum, timer_concrete]
                elif timer_type in ('thu', 'thursday'):
                    self.funcs_thursday_concrete_timer[func] = [timer_sum, timer_concrete]
                elif timer_type in ('fri', 'friday'):
                    self.funcs_friday_concrete_timer[func] = [timer_sum, timer_concrete]
                elif timer_type in ('sat', 'saturday'):
                    self.funcs_saturday_concrete_timer[func] = [timer_sum, timer_concrete]
                elif timer_type in ('sun', 'sunday'):
                    self.funcs_sunday_concrete_timer[func] = [timer_sum, timer_concrete]
                else:
                    raise Exception('timer_type error!')

            # 时间范围 未指定精确时间时
            elif timer_concrete == None and isinstance(timer_sum, str):
                if timer_type in ('s', 'second'):
                    self.funcs_second_random_timer[func] = timer_sum
                elif timer_type in ('m', 'minute'):
                    self.funcs_minute_random_timer[func] = timer_sum
                elif timer_type in ('h', 'hour'):
                    self.funcs_hour_random_timer[func] = timer_sum
                elif timer_type in ('d', 'day'):
                    self.funcs_day_random_timer[func] = timer_sum
                elif timer_type in ('w', 'week'):
                    self.funcs_week_random_timer[func] = timer_sum

                elif timer_type in ('mon', 'monday'):
                    self.funcs_sunday_random_timer[func] = timer_sum
                elif timer_type in ('tue', 'tuesday'):
                    self.funcs_tuesday_random_timer[func] = timer_sum
                elif timer_type in ('wed', 'wednesday'):
                    self.funcs_wednesday_random_timer[func] = timer_sum
                elif timer_type in ('thu', 'thursday'):
                    self.funcs_thursday_random_timer[func] = timer_sum
                elif timer_type in ('fri', 'friday'):
                    self.funcs_friday_random_timer[func] = timer_sum
                elif timer_type in ('sat', 'saturday'):
                    self.funcs_saturday_random_timer[func] = timer_sum
                elif timer_type in ('sun', 'sunday'):
                    self.funcs_sunday_random_timer[func] = timer_sum
                else:
                    raise Exception('timer_type error!')

            # 时间范围 指定了精确时间时
            elif timer_concrete != None and isinstance(timer_sum, str):
                # 每小时/分钟/秒钟计时类型多参数选择
                if timer_type in ('m', 'minute'):
                    self.funcs_minute_random_concrete_timer[func] = [timer_sum, timer_concrete]
                elif timer_type in ('h', 'hour'):
                    self.funcs_hour_random_concrete_timer[func] = [timer_sum, timer_concrete]
                elif timer_type in ('d', 'day'):
                    self.funcs_hour_random_concrete_timer[func] = [timer_sum, timer_concrete]

                elif timer_type in ('sun', 'sunday'):
                    self.funcs_sunday_random_concrete_timer[func] = [timer_sum, timer_concrete]
                elif timer_type in ('tue', 'tuesday'):
                    self.funcs_tuesday_random_concrete_timer[func] = [timer_sum, timer_concrete]
                elif timer_type in ('wed', 'wednesday'):
                    self.funcs_wednesday_random_concrete_timer[func] = [timer_sum, timer_concrete]
                elif timer_type in ('thu', 'thursday'):
                    self.funcs_thursday_random_concrete_timer[func] = [timer_sum, timer_concrete]
                elif timer_type in ('fri', 'friday'):
                    self.funcs_friday_random_concrete_timer[func] = [timer_sum, timer_concrete]
                elif timer_type in ('sat', 'saturday'):
                    self.funcs_saturday_random_concrete_timer[func] = [timer_sum, timer_concrete]
                elif timer_type in ('sun', 'sunday'):
                    self.funcs_sunday_random_concrete_timer[func] = [timer_sum, timer_concrete]

            else:
                pass

        return decorator

    # 将所有被every装饰的函数放入schedule中
    def load_schedule(self):
        global timer_instance


        """具体时间 未指定精确时间"""
        # 加载秒计时
        if self.funcs_second_timer:
            for k, v in zip(self.funcs_second_timer.keys(), self.funcs_second_timer.values()):
                t = Scheduler()
                t.every(v).seconds.do(job_func=k)
                timer_instance.append(t)

        # 加载分钟计时
        if self.funcs_minute_timer:
            for k, v in zip(self.funcs_minute_timer.keys(), self.funcs_minute_timer.values()):
                t = Scheduler()
                t.every(v).minutes.do(job_func=k)
                timer_instance.append(t)
        # 加载小时计时
        if self.funcs_hour_timer:
            for k, v in zip(self.funcs_hour_timer.keys(), self.funcs_hour_timer.values()):
                t = Scheduler()
                t.every(v).hours.do(job_func=k)
                timer_instance.append(t)
        # 加载天计时
        if self.funcs_day_timer:
            for k, v in zip(self.funcs_day_timer.keys(), self.funcs_day_timer.values()):
                t = Scheduler()
                t.every(v).days.do(job_func=k)
                timer_instance.append(t)
        # 加载星期一计时
        if self.funcs_monday_timer:
            for k, v in zip(self.funcs_monday_timer.keys(), self.funcs_monday_timer.values()):
                t = Scheduler()
                t.every(v).monday.do(job_func=k)
                timer_instance.append(t)
        # 加载星期二计时
        if self.funcs_tuesday_timer:
            for k, v in zip(self.funcs_tuesday_timer.keys(), self.funcs_tuesday_timer.values()):
                t = Scheduler()
                t.every(v).tuesday.do(job_func=k)
                timer_instance.append(t)
        # 加载星期三计时
        if self.funcs_wednesday_timer:
            for k, v in zip(self.funcs_wednesday_timer.keys(), self.funcs_wednesday_timer.values()):
                t = Scheduler()
                t.every(v).wednesday.do(job_func=k)
                timer_instance.append(t)
        # 加载星期四计时
        if self.funcs_thursday_timer:
            for k, v in zip(self.funcs_thursday_timer.keys(), self.funcs_thursday_timer.values()):
                t = Scheduler()
                t.every(v).thursday.do(job_func=k)
                timer_instance.append(t)
        # 加载星期五计时
        if self.funcs_friday_timer:
            for k, v in zip(self.funcs_friday_timer.keys(), self.funcs_friday_timer.values()):
                t = Scheduler()
                t.every(v).friday.do(job_func=k)
                timer_instance.append(t)
        # 加载星期六计时
        if self.funcs_saturday_timer:
            for k, v in zip(self.funcs_saturday_timer.keys(), self.funcs_saturday_timer.values()):
                t = Scheduler()
                t.every(v).saturday.do(job_func=k)
                timer_instance.append(t)
        # 加载星期天计时
        if self.funcs_sunday_timer:
            for k, v in zip(self.funcs_sunday_timer.keys(), self.funcs_sunday_timer.values()):
                t = Scheduler()
                t.every(v).sunday.do(job_func=k)
                timer_instance.append(t)
        # 加载周计时
        if self.funcs_week_timer:
            for k, v in zip(self.funcs_week_timer.keys(), self.funcs_week_timer.values()):
                t = Scheduler()
                t.every(v).weeks.do(job_func=k)
                timer_instance.append(t)

        """具体时间 指定了精确时间"""
        # 加载分钟计时
        if self.funcs_minute_concrete_timer:
            for k, v in zip(self.funcs_minute_concrete_timer.keys(), self.funcs_minute_concrete_timer.values()):
                t = Scheduler()
                t.every(v[0]).minutes.at(v[1]).do(job_func=k)
                timer_instance.append(t)
        # 加载小时计时
        if self.funcs_hour_concrete_timer:
            for k, v in zip(self.funcs_hour_concrete_timer.keys(), self.funcs_hour_concrete_timer.values()):
                t = Scheduler()
                t.every(v[0]).hours.at(v[1]).do(job_func=k)
                timer_instance.append(t)
        # 加载天计时
        if self.funcs_day_concrete_timer:
            for k, v in zip(self.funcs_day_concrete_timer.keys(), self.funcs_day_concrete_timer.values()):
                t = Scheduler()
                t.every(v[0]).days.at(v[1]).do(job_func=k)
                timer_instance.append(t)
        # 加载星期一计时
        if self.funcs_monday_concrete_timer:
            for k, v in zip(self.funcs_monday_concrete_timer.keys(), self.funcs_monday_concrete_timer.values()):
                t = Scheduler()
                t.every(v[0]).monday.at(v[1]).do(job_func=k)
                timer_instance.append(t)
        # 加载星期二计时
        if self.funcs_tuesday_concrete_timer:
            for k, v in zip(self.funcs_tuesday_concrete_timer.keys(), self.funcs_tuesday_concrete_timer.values()):
                t = Scheduler()
                t.every(v[0]).tuesday.at(v[1]).do(job_func=k)
                timer_instance.append(t)
        # 加载星期三计时
        if self.funcs_wednesday_concrete_timer:
            for k, v in zip(self.funcs_wednesday_concrete_timer.keys(),
                            self.funcs_wednesday_concrete_timer.values()):
                t = Scheduler()
                t.every(v[0]).wednesday.at(v[1]).do(job_func=k)
                timer_instance.append(t)
        # 加载星期四计时
        if self.funcs_thursday_concrete_timer:
            for k, v in zip(self.funcs_thursday_concrete_timer.keys(), self.funcs_thursday_concrete_timer.values()):
                t = Scheduler()
                t.every(v[0]).thursday.at(v[1]).do(job_func=k)
                timer_instance.append(t)
        # 加载星期五计时
        if self.funcs_friday_concrete_timer:
            for k, v in zip(self.funcs_friday_concrete_timer.keys(), self.funcs_friday_concrete_timer.values()):
                t = Scheduler()
                t.every(v[0]).friday.at(v[1]).do(job_func=k)
                timer_instance.append(t)
        # 加载星期六计时
        if self.funcs_saturday_concrete_timer:
            for k, v in zip(self.funcs_saturday_concrete_timer.keys(), self.funcs_saturday_concrete_timer.values()):
                t = Scheduler()
                t.every(v[0]).saturday.at(v[1]).do(job_func=k)
                timer_instance.append(t)
        # 加载星期天计时
        if self.funcs_sunday_concrete_timer:
            for k, v in zip(self.funcs_sunday_concrete_timer.keys(), self.funcs_sunday_concrete_timer.values()):
                t = Scheduler()
                t.every(v[0]).sunday.at(v[1]).do(job_func=k)
                timer_instance.append(t)
        """时间范围 未指定时间"""
        # 加载秒计时
        if self.funcs_second_random_timer:
            for k, v in zip(self.funcs_second_random_timer.keys(), self.funcs_second_random_timer.values()):
                left_value = int(v.split('-')[0])
                right_value = int(v.split('-')[-1])
                t = Scheduler()
                t.every(left_value).seconds.to(right_value).do(job_func=k)
                timer_instance.append(t)
        # 加载分计时
        if self.funcs_minute_random_timer:
            for k, v in zip(self.funcs_minute_random_timer.keys(), self.funcs_minute_random_timer.values()):
                left_value = int(v.split('-')[0])
                right_value = int(v.split('-')[-1])
                t = Scheduler()
                t.every(left_value).minutes.to(right_value).do(job_func=k)
                timer_instance.append(t)
        # 加载小时计时
        if self.funcs_hour_random_timer:
            for k, v in zip(self.funcs_hour_random_timer.keys(), self.funcs_hour_random_timer.values()):
                left_value = int(v.split('-')[0])
                right_value = int(v.split('-')[-1])
                t = Scheduler()
                t.every(left_value).hours.to(right_value).do(job_func=k)
                timer_instance.append(t)
        # 加载天计时
        if self.funcs_day_random_timer:
            for k, v in zip(self.funcs_day_random_timer.keys(), self.funcs_day_random_timer.values()):
                left_value = int(v.split('-')[0])
                right_value = int(v.split('-')[-1])
                t = Scheduler()
                t.every(left_value).days.to(right_value).do(job_func=k)
                timer_instance.append(t)
        # 加载周计时
        if self.funcs_week_random_timer:
            for k, v in zip(self.funcs_week_random_timer.keys(), self.funcs_week_random_timer.values()):
                left_value = int(v.split('-')[0])
                right_value = int(v.split('-')[-1])
                t = Scheduler()
                t.every(left_value).week.to(right_value).do(job_func=k)
                timer_instance.append(t)
        # 加载星期一计时
        if self.funcs_monday_random_timer:
            for k, v in zip(self.funcs_monday_random_timer.keys(), self.funcs_monday_random_timer.values()):
                left_value = int(v.split('-')[0])
                right_value = int(v.split('-')[-1])
                t = Scheduler()
                t.every(left_value).monday.to(right_value).do(job_func=k)
                timer_instance.append(t)
        # 加载星期二计时
        if self.funcs_tuesday_random_timer:
            for k, v in zip(self.funcs_tuesday_random_timer.keys(), self.funcs_tuesday_random_timer.values()):
                left_value = int(v.split('-')[0])
                right_value = int(v.split('-')[-1])
                t = Scheduler()
                t.every(left_value).tuesday.to(right_value).do(job_func=k)
                timer_instance.append(t)
        # 加载星期三计时
        if self.funcs_wednesday_random_timer:
            for k, v in zip(self.funcs_wednesday_random_timer.keys(), self.funcs_wednesday_random_timer.values()):
                left_value = int(v.split('-')[0])
                right_value = int(v.split('-')[-1])
                t = Scheduler()
                t.every(left_value).wednesday.to(right_value).do(job_func=k)
                timer_instance.append(t)
        # 加载星期四计时
        if self.funcs_thursday_random_timer:
            for k, v in zip(self.funcs_thursday_random_timer.keys(), self.funcs_thursday_random_timer.values()):
                left_value = int(v.split('-')[0])
                right_value = int(v.split('-')[-1])
                t = Scheduler()
                t.every(left_value).thursday.to(right_value).do(job_func=k)
                timer_instance.append(t)
        # 加载星期五计时
        if self.funcs_friday_random_timer:
            for k, v in zip(self.funcs_friday_random_timer.keys(), self.funcs_friday_random_timer.values()):
                left_value = int(v.split('-')[0])
                right_value = int(v.split('-')[-1])
                t = Scheduler()
                t.every(left_value).friday.to(right_value).do(job_func=k)
                timer_instance.append(t)
        # 加载星期六计时
        if self.funcs_saturday_random_timer:
            for k, v in zip(self.funcs_saturday_random_timer.keys(), self.funcs_saturday_random_timer.values()):
                left_value = int(v.split('-')[0])
                right_value = int(v.split('-')[-1])
                t = Scheduler()
                t.every(left_value).saturday.to(right_value).do(job_func=k)
                timer_instance.append(t)
        # 加载星期天计时
        if self.funcs_sunday_random_timer:
            for k, v in zip(self.funcs_sunday_random_timer.keys(), self.funcs_sunday_random_timer.values()):
                left_value = int(v.split('-')[0])
                right_value = int(v.split('-')[-1])
                t = Scheduler()
                t.every(left_value).sunday.to(right_value).do(job_func=k)
                timer_instance.append(t)
        """时间范围 指定了精确时间"""
        # 加载分计时
        if self.funcs_minute_random_concrete_timer:
            for k, v in zip(self.funcs_minute_random_concrete_timer.keys(),
                            self.funcs_minute_random_concrete_timer.values()):
                left_value = int(v[0].split('-')[0])
                right_value = int(v[0].split('-')[-1])
                t = Scheduler()
                t.every(left_value).minutes.to(right_value).at(v[1]).do(job_func=k)
                timer_instance.append(t)
        # 加载小时计时
        if self.funcs_hour_random_concrete_timer:
            for k, v in zip(self.funcs_hour_random_concrete_timer.keys(),
                            self.funcs_hour_random_concrete_timer.values()):
                left_value = int(v[0].split('-')[0])
                right_value = int(v[0].split('-')[-1])
                t = Scheduler()
                t.every(left_value).hours.to(right_value).at(v[1]).do(job_func=k)
                timer_instance.append(t)
        # 加载天计时
        if self.funcs_day_random_concrete_timer:
            for k, v in zip(self.funcs_day_random_concrete_timer.keys(),
                            self.funcs_day_random_concrete_timer.values()):
                left_value = int(v[0].split('-')[0])
                right_value = int(v[0].split('-')[-1])
                t = Scheduler()
                t.every(left_value).days.to(right_value).at(v[1]).do(job_func=k)
                timer_instance.append(t)
        # 加载星期一计时
        if self.funcs_monday_random_concrete_timer:
            for k, v in zip(self.funcs_monday_random_concrete_timer.keys(),
                            self.funcs_monday_random_concrete_timer.values()):
                left_value = int(v[0].split('-')[0])
                right_value = int(v[0].split('-')[-1])
                t = Scheduler()
                t.every(left_value).monday.to(right_value).at(v[1]).do(job_func=k)
                timer_instance.append(t)
        # 加载星期二计时
        if self.funcs_tuesday_random_concrete_timer:
            for k, v in zip(self.funcs_tuesday_random_concrete_timer.keys(),
                            self.funcs_tuesday_random_concrete_timer.values()):
                left_value = int(v[0].split('-')[0])
                right_value = int(v[0].split('-')[-1])
                t = Scheduler()
                t.every(left_value).tuesday.to(right_value).at(v[1]).do(job_func=k)
                timer_instance.append(t)
        # 加载星期三计时
        if self.funcs_wednesday_random_concrete_timer:
            for k, v in zip(self.funcs_wednesday_random_concrete_timer.keys(),
                            self.funcs_wednesday_random_concrete_timer.values()):
                left_value = int(v[0].split('-')[0])
                right_value = int(v[0].split('-')[-1])
                t = Scheduler()
                t.every(left_value).wednesday.to(right_value).at(v[1]).do(job_func=k)
                timer_instance.append(t)
        # 加载星期四计时
        if self.funcs_thursday_random_concrete_timer:
            for k, v in zip(self.funcs_thursday_random_concrete_timer.keys(),
                            self.funcs_thursday_random_concrete_timer.values()):
                left_value = int(v[0].split('-')[0])
                right_value = int(v[0].split('-')[-1])
                t = Scheduler()
                t.every(left_value).thursday.to(right_value).at(v[1]).do(job_func=k)
                timer_instance.append(t)
        # 加载星期五计时
        if self.funcs_friday_random_concrete_timer:
            for k, v in zip(self.funcs_friday_random_concrete_timer.keys(),
                            self.funcs_friday_random_concrete_timer.values()):
                left_value = int(v[0].split('-')[0])
                right_value = int(v[0].split('-')[-1])
                t = Scheduler()
                t.every(left_value).friday.to(right_value).at(v[1]).do(job_func=k)
                timer_instance.append(t)
        # 加载星期六计时
        if self.funcs_saturday_random_concrete_timer:
            for k, v in zip(self.funcs_saturday_random_concrete_timer.keys(),
                            self.funcs_saturday_random_concrete_timer.values()):
                left_value = int(v[0].split('-')[0])
                right_value = int(v[0].split('-')[-1])
                t = Scheduler()
                t.every(left_value).saturday.to(right_value).at(v[1]).do(job_func=k)
                timer_instance.append(t)
        # 加载星期天计时
        if self.funcs_sunday_random_concrete_timer:
            for k, v in zip(self.funcs_sunday_random_concrete_timer.keys(),
                            self.funcs_sunday_random_concrete_timer.values()):
                left_value = int(v[0].split('-')[0])
                right_value = int(v[0].split('-')[-1])
                t = Scheduler()
                t.every(left_value).sunday.to(right_value).at(v[1]).do(job_func=k)
                timer_instance.append(t)

    # 直接运行一遍所有函数 用于测试
    def run_all_jobs(self):
        self.load_schedule()
        for t in timer_instance:
            t.run_all()

    # schedule 任务总调度
    def job_start(self,t):
        while True:
            t.run_pending()

    # 启动多线程
    def manage_schedule(self):
        for t in timer_instance:
            threading.Thread(target=self.job_start,args=(t,)).start()

    # 运行程序
    def run(self):
        self.load_schedule()
        print(timer_instance)
        self.manage_schedule()


if __name__ == '__main__':
    t = Timer()
    n = 1
    m = 1

    @t.every("1","s")
    def _():
        global n
        print("t1---",n)
        time.sleep(5)
        n+=1

    @t.every("1","s")
    def _():
        global m
        print("t2---",m)
        m+=1
        
    t.run()