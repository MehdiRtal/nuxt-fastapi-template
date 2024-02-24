#!/bin/sh -e

pg_restore /backups/${1}.tar -Ft -U postgres -d postgres
