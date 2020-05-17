#!/bin/sh

PIDFILE="/var/run/echo_server.pid"

start() {
	echo -n "Starting echo_server ..."
	start-stop-daemon -b -m -S -p "$PIDFILE" -x /bin/echo_server
	status=$?
	if [ "$status" -eq 0 ]; then
		echo "OK"
	else
		echo "FAIL"
	fi
	return "$status"
}

stop() {
	echo -n "Stopping echo_server ..."
	start-stop-daemon -K -p "$PIDFILE"
	status=$?
	if [ "$status" -eq 0 ]; then
		rm -f "$PIDFILE"
		echo "OK"
	else
		echo "FAIL"
	fi
	return "$status"
}

case "$1" in
	start) start;;
	stop) stop;;
esac
