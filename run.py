# import datetime as dt
import time
import schedule
from octranspo.models import next_trips as nt

if __name__ == '__main__':
    schedule.every(1).minutes.do(
        nt.NextTrips().run,
        [(4808, 14)]
    )

    while True:
        schedule.run_pending()
        time.sleep(1)
# nt.NextTrips().run([(4808, 14)])
