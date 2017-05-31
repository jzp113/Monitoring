#! /bin/sh
### BEGIN INIT INFO
# Provides:          rtc_ds1307
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: DS1307 real-time clock usage script
# Description:       This file should be used to construct scripts to be
#                    placed in /etc/init.d.
### END INIT INFO

# Author: Alexander Golenshin <shooreg@gmail.com>

# PATH should only include /usr/* if it runs after the mountnfs.sh script
PATH=/sbin:/usr/sbin:/bin:/usr/bin
DESC="ds1307_rtc maintenance service"

do_start()
{
        echo "Selecting correct  RTC instance "
        echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-0/new_device
        sudo ln -f -s /dev/rtc1 /dev/rtc
        echo "Syncing system time to RTC"
        sudo hwclock -s
}

do_stop()
{
        echo "Syncing RTC to system time"
        sudo hwclock -w
}

case "$1" in
  start)
        do_start
        ;;
  stop)
        do_stop
        ;;
  status)
        echo "RTC time:"
        hwclock -r
        echo "System time:"
        date
        ;;
  restart|force-reload)
        do_stop
        ;;
  *)
        echo "Usage: rtc_ds1307 {start|stop|status|restart}" >&2
        exit 3
        ;;
esac

:
