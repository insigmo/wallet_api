#!/bin/bash

set -eux

alembic upgrade head


echo_supervisord_conf > /etc/supervisor/supervisord.conf
printf "[include]\\nfiles = /etc/supervisor/supervisor.d/*.conf\\n" >> /etc/supervisor/supervisord.conf
exec supervisord --nodaemon
