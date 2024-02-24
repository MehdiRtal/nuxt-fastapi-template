#!/bin/sh -e

redis-cli SAVE

cp /data/dump.rdb /backups/${1}.rdb
