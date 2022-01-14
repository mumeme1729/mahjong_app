#!/bin/bash

#postgresqlの起動設定を変更する

set -e

#sed -i -e"s///" /var/lib/postgresql/data/postgresql.conf

sed -i -e"s/#log_destination = 'stderr'/log_destination = 'stderr'/" /var/lib/postgresql/data/postgresql.conf
sed -i -e"s/#logging_collector = off/logging_collector = on/" /var/lib/postgresql/data/postgresql.conf
sed -i -e"s!#log_directory = 'log'!log_directory = '../../../log/postgresql'!" /var/lib/postgresql/data/postgresql.conf
sed -i -e"s/#log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'/log_filename = 'postgresql_%Y%m%d.log'/" /var/lib/postgresql/data/postgresql.conf
sed -i -e"s/#log_file_mode = 0600/log_file_mode = 0640/" /var/lib/postgresql/data/postgresql.conf
sed -i -e"s/#log_rotation_age = 1d/log_rotation_age = 1d/" /var/lib/postgresql/data/postgresql.conf
sed -i -e"s/#log_rotation_size = 10MB/log_rotation_size = 2048kB/" /var/lib/postgresql/data/postgresql.conf
sed -i -e"s/#log_min_error_statement = error/log_min_error_statement = error/" /var/lib/postgresql/data/postgresql.conf
sed -i -e"s/#log_min_duration_statement = -1/log_min_duration_statement = 5000/" /var/lib/postgresql/data/postgresql.conf
sed -i -e"s/#log_line_prefix.*$/log_line_prefix = '[%t]%u %d %p[%l]'/" /var/lib/postgresql/data/postgresql.conf
