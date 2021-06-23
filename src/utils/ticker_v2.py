import datetime
import time
import asyncio

task_pool = {}


async def task(id):
    print(datetime.datetime.now())
    print(f"Started: {id}")
    print("Do something")
    del task_pool[id]


async def start_ticker(interval, times):
    print(f">>>>>> {time.strftime('%X')} Starting Tasks")
    task_error_count = 0

    for i in range(times):
        task_pool[i] = asyncio.create_task(task(i))
        await asyncio.sleep(interval)

    # wait for all task finished
    for id in task_pool:
        try:
            await task_pool[id]
        except:
            task_error_count += 1
            continue

    if task_error_count > 0:
        raise Exception(print(f">>>>>>Job error: there are {task_error_count} tasks error in this job"))

    print(f"<<<<<< {time.strftime('%X')} Finished Tasks")


def trigger():
    print('Ticker started')
    start_seconds = 20
    cron_interval = 2

    # wait for first start time
    time.sleep(start_seconds - time.time() % start_seconds)

    # start ticker
    asyncio.run(start_ticker(cron_interval, 5))
    print('Ticker ended')


if __name__ == '__main__':
    trigger()