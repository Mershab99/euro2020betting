#!/bin/bash
cd ..
docker build --tag=euro2020betting ./service/
docker tag euro2020betting mershab99/euro2020betting
docker push mershab99/euro2020betting
