#!/bin/sh -e

pg_dump -Ft -U postgres -f /backups/${1}.tar
