#!/usr/bin/env bash
docker-compose -f ./docker-compose.test.yml up -d
docker-compose exec app pylint -r n --rcfile /opt/webapp/scripts/pylintrc /opt/webapp
docker-compose exec app pytest ./ --cov ./  --verbose --cov-fail-under 1
docker-compose stop