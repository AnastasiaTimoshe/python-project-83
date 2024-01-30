#!/usr/bin/env bash

make install && psql -U admin -a --dbname=$DATABASE_URL --file=database.sql