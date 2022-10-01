"""
TODO: adjust delay interval after long cron times
"""

import datetime
import time
import asyncio

task_pool = {}
delay = 0.01

async def task(id):
    print(datetime.datetime.now())
    print(f"Started: {id}")
    print("Do something")
    del task_pool[id]


async def start_limited_ticker(interval, times):
    task_error_count = 0

    for i in range(times):
        task_pool[i] = asyncio.create_task(task(i))
        await asyncio.sleep(interval - delay)

    # wait for all task finished
    for id in task_pool:
        try:
            await task_pool[id]
        except:
            task_error_count += 1
            continue

    if task_error_count > 0:
        raise Exception(print(f">>>>>>Job error: there are {task_error_count} tasks error in this job"))


async def start_endless_ticker(interval):
    i = 0
    while True:
        i += 1
        task_pool[i] = asyncio.create_task(task(i))
        await asyncio.sleep(interval - delay)


def start_ticker(interval, times=0):
    print(f">>>>>> {time.strftime('%X')} Starting Tasks")
    if times > 0:
        asyncio.run(start_limited_ticker(interval, times))
    else:
        asyncio.run(start_endless_ticker(interval))
    print(f"<<<<<< {time.strftime('%X')} Finished Tasks")


def trigger():
    print('Ticker started')
    start_seconds = 20
    cron_seconds = 5

    # wait for first start time
    time.sleep(start_seconds - time.time() % start_seconds - delay)

    # start ticker
    start_ticker(cron_seconds, 0)
    print('Ticker ended')


if __name__ == '__main__':
    trigger()