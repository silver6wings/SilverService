import datetime
import time
import asyncio


async def task(name):
    print(datetime.datetime.now())
    print(f"Started: {name}")

    print("Do something")


async def start_ticker(interval, times):
    print(f">>>>>> {time.strftime('%X')} Starting Tasks")
    tasks = []
    task_error_count = 0

    for i in range(times):
        tasks.append(asyncio.create_task(task("Task:" + str(i))))
        await asyncio.sleep(interval)

    for i in range(times):
        try:
            await tasks[i]
        except:
            task_error_count += 1
            continue

    if task_error_count > 0:
        raise Exception(print(f">>>>>>Job error: there are {task_error_count} tasks error in this job"))

    print(f"<<<<<< {time.strftime('%X')} Finished Tasks")


def trigger():
    print('start')
    start_seconds = 20
    cron_interval = 10
    total_period = 60  # also execute every 1 minutes
    ignore = 0
    now = datetime.datetime.now()
    late_seconds = now.second - start_seconds

    print(now)

    if late_seconds > 0:
        ignore += int(late_seconds / cron_interval) + 1

    try_times = int(total_period / cron_interval) - ignore
    print(str(try_times) + ' jobs will schedule.')

    # wait for first start time
    time.sleep(start_seconds - time.time() % start_seconds)

    # start ticker
    asyncio.run(start_ticker(cron_interval, try_times))
    print('end')


if __name__ == '__main__':
    trigger()