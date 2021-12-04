# -*-coding:utf-8-*-
import time
from itertools import chain
from schedule import Scheduler


# 具体时间执行
# @cron.every('1','seconds')              # 每1秒钟执行一次
# @cron.every('2','minutes')              # 每2分钟执行一次
# @cron.every('2','minutes',':05')        # 每2分钟的第5秒执行一次
# @cron.every('5','hours')                # 每5小时执行一次
# @cron.every('5','hours','25:30')        # 每5小时的第25分钟30秒执行一次
# @cron.every('2','days')                 # 每2天执行一次
# @cron.every('2','days','00:00:00')      # 每2天的00:00:00执行一次

# @cron.every('1','weeks')                # 每周执行
# @cron.every('1','monday')               # 每个星期一执行一次
# @cron.every('1','tuesday')              # 每个星期二执行一次
# @cron.every('1','wednesday')            # 每个星期三执行一次
# @cron.every('1','thursday')             # 每个星期四执行一次
# @cron.every('1','friday')               # 每个星期五执行一次
# @cron.every('1','saturday')             # 每个星期六执行一次
# @cron.every('1','sunday')               # 每个星期天执行一次
# @cron.every('1','monday','12:00:00')    # 每个星期一的12:00:00执行一次

# 随机时间范围执行
# @cron.every('1-5','seconds')             # 随机每1到5秒执行一次
# @cron.every('1-5','minutes')             # 随机每1到5分钟执行一次
# @cron.every('1-5','minutes',':05')       # 随机每1到5分钟的第5秒执行执行一次
# @cron.every('1-5','hours')               # 随机每1到5小时执行一次
# @cron.every('1-5','hours','20:10')       # 随机每1到5小时第20分钟的第10秒执行一次
# @cron.every('1-5','days')                # 随机每1到5天执行一次
# @cron.every('1-5','days','00:00:20')     # 随机每1到5天00:00:20执行一次
# t.every('1-2','weeks')                   # 随机每1到5周执行一次

# @cron.every('1-2','monday')              # 随机每1到2个星期一执行一次
# @cron.every('1-2','tuesday')             # 随机每1到2个星期二执行一次
# @cron.every('1-2','wednesday')           # 随机每1到2个星期三执行一次
# @cron.every('1-2','thursday')            # 随机每1到2个星期四执行一次
# @cron.every('1-2','friday')              # 随机每1到2个星期五执行一次
# @cron.every('1-2','saturday')            # 随机每1到2个星期六执行一次
# @cron.every('1-2','sunday')              # 随机每1到2个星期天执行一次
# @cron.every('1-2','monday','00:00:05')   # 随机每1到2个星期一的00:00:05执行一次

# 时间类型参数可使用简写
# seconds       s
# minutes       m
# hours         h
# days          d
# weeks         w
#
# monday       mon
# tuesday      tue
# wednesday    wed
# thursday     thu
# friday       fri
# saturday     sat
# sunday       sun


class Crontab:

    def __init__(self):
        self.scheduler = Scheduler()
        self.funcs_time_attrs = []
        self.timer_type_map = {
            's': 'seconds',
            'm': 'minutes',
            'h': 'hours',
            'd': 'days',
            'w': 'weeks',
            'mon': 'monday',
            'tue': 'tuesday',
            'wed': 'wednesday',
            'thu': 'thursday',
            'fri': 'friday',
            'sat': 'saturday',
            'sun': 'sunday'
        }

    def every(self, timer_value, timer_type, timer_concrete=None):
        """
        Decorate function change to time function.
        """

        def decorator(func):
            nonlocal timer_value
            nonlocal timer_type

            if isinstance(timer_value, str):
                if '-' not in timer_value:
                    timer_value = int(timer_value)
                else:
                    timer_value = timer_value
            else:
                raise Exception("timer_value should be str!")

            timer_type_list = list(chain(*self.timer_type_map.items()))

            if timer_type in timer_type_list:
                if isinstance(timer_value, int) and timer_concrete is None:
                    func_time_dict = {func: timer_value}
                    if self.timer_type_map.get(timer_type):
                        attr_name = 'funcs_%s_timer' % self.timer_type_map[timer_type]
                    else:
                        attr_name = 'funcs_%s_timer' % timer_type
                elif isinstance(timer_value, int) and timer_concrete is not None:
                    func_time_dict = {func: [timer_value, timer_concrete]}
                    if self.timer_type_map.get(timer_type):
                        attr_name = 'funcs_%s_concrete_timer' % self.timer_type_map[timer_type]
                    else:
                        attr_name = 'funcs_%s_concrete_timer' % timer_type
                elif isinstance(timer_value, str) and timer_concrete is None:
                    func_time_dict = {func: timer_value}
                    if self.timer_type_map.get(timer_type):
                        attr_name = 'funcs_%s_random_timer' % self.timer_type_map[timer_type]
                    else:
                        attr_name = 'funcs_%s_random_timer' % timer_type
                elif isinstance(timer_value, str) and timer_concrete is not None:
                    func_time_dict = {func: [timer_value, timer_concrete]}
                    if self.timer_type_map.get(timer_type):
                        attr_name = 'funcs_%s_random_concrete_timer' % self.timer_type_map[timer_type]
                    else:
                        attr_name = 'funcs_%s_random_concrete_timer' % timer_type
                else:
                    raise Exception('parameter error!')

                if hasattr(self, attr_name):
                    attr_name_func_dict = getattr(self, attr_name)
                    attr_name_func_dict.update(func_time_dict)
                    setattr(self, attr_name, attr_name_func_dict)
                else:
                    setattr(self, attr_name, func_time_dict)
                self.funcs_time_attrs.append(attr_name)
            else:
                raise Exception('timer_type error!')

        return decorator

    def load_time_funcs(self, attr_name):
        """
        Load the time type but not specific exact time function.
        """
        for k, v in zip(getattr(self, attr_name).keys(), getattr(self, attr_name).values()):
            time_type = attr_name.split('_')[1]
            getattr(self.scheduler.every(v), time_type).do(job_func=k)

    def load_concrete_time_funcs(self, attr_name):
        """
        Load the time type and specific exact time function.
        """
        for k, v in zip(getattr(self, attr_name).keys(), getattr(self, attr_name).values()):
            time_type = attr_name.split('_')[1]
            getattr(self.scheduler.every(v[0]), time_type).at(v[1]).do(job_func=k)

    def load_random_time_funcs(self, attr_name):
        """
        Load the time range but not specific exact time function.
        """
        for k, v in zip(getattr(self, attr_name).keys(), getattr(self, attr_name).values()):
            v_list = v.split('-')
            left_value = int(v_list[0])
            right_value = int(v_list[-1])
            time_type = attr_name.split('_')[1]
            getattr(self.scheduler.every(left_value), time_type).to(right_value).do(job_func=k)

    def load_random_concrete_time_funcs(self, attr_name):
        """
        Load the time range and specific exact time function.
        """
        for k, v in zip(getattr(self, attr_name).keys(), getattr(self, attr_name).values()):
            v_list = v.split('-')
            left_value = int(v_list[0])
            right_value = int(v_list[-1])
            time_type = attr_name.split('_')[1]
            getattr(self.scheduler.every(left_value), time_type).to(right_value).at(v[1]).do(job_func=k)

    def load_scheduler_funcs(self):
        """
        Load all function decorated.
        """
        for attr_name in self.funcs_time_attrs:
            if attr_name.endswith('_random_concrete_timer'):
                self.load_random_concrete_time_funcs(attr_name)
            elif attr_name.endswith('_random_timer'):
                self.load_random_time_funcs(attr_name)
            elif attr_name.endswith('_concrete_timer'):
                self.load_concrete_time_funcs(attr_name)
            elif attr_name.endswith('_timer'):
                self.load_time_funcs(attr_name)

    def run_all_jobs(self):
        """
        Run all function once immediately.
        """
        self.load_scheduler_funcs()
        self.scheduler.run_all()

    def job_start(self):
        """
        Scheduler into pending.
        """
        while True:
            self.scheduler.run_pending()
            time.sleep(self.interval)

    def run(self, interval=0):
        """
        Run all tasks.
        """
        if not isinstance(interval, (int, float)):
            raise TypeError('interval should be int or float.')
        self.interval = interval
        self.load_scheduler_funcs()
        self.job_start()


cron = Crontab()