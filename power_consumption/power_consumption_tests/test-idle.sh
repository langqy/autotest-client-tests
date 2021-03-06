#!/bin/bash
#
#  Simple power measurement test, idle system
#

. ${SCRIPT_PATH}/test-common.sh

#
# Gather samples
#
echo "DEBUG: Starting logmeter $LOGMETER" > /dev/stderr

rm -f $SAMPLES_LOG
$LOGMETER --addr=$METER_ADDR --port=$METER_PORT --tagport=$METER_TAGPORT \
          --measure=c --acdc=AC \
	  --interval=$SAMPLE_INTERVAL --samples=$SAMPLES \
	  --out=$SAMPLES_LOG > /dev/null

echo "DEBUG: Logging completed" > /dev/stderr

echo "DEBUG: idle test completed." > /dev/stderr
echo "DEBUG: samples gathered in $SAMPLES_LOG :" > /dev/stderr
echo "DEBUG: -------------------------" > /dev/stderr
cat $SAMPLES_LOG > /dev/stderr
echo "DEBUG: -------------------------" > /dev/stderr

#
# Compute stats, scale by 100 because we are using a power clamp
#
$STATSTOOL -S -T -X 100 -a $SAMPLES_LOG | grep metric: | sed 's/metric:/metric:idle_system_/'

echo "DEBUG: statstool output:" > /dev/stderr
echo "DEBUG: -------------------------" > /dev/stderr
$STATSTOOL -S -T -X 100 -a $SAMPLES_LOG | grep metric: | sed 's/metric:/metric:idle_system_/' > /dev/stderr
echo "DEBUG: -------------------------" > /dev/stderr
echo "DEBUG: test-idle.sh now complete" > /dev/stderr
