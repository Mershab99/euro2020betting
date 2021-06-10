#!/bin/bash
cd ..
sudo docker build --tag=euro2020betting ./service/
sudo docker tag euro2020betting mershab99/euro2020betting
sudo docker push mershab99/euro2020betting
