#!/bin/bash

echo "Build execute"
cd ./execute
npm install
pipenv run pip install pip==18.0.0
npm run build
cd ..

echo "Build onerror"
cd ./onerror
npm install
pipenv run pip install pip==18.0.0
npm run build
cd ..

echo "Build onsuccess"
cd ./onsuccess
npm install
pipenv run pip install pip==18.0.0
npm run build
cd ..

echo "Build orchestrator"
cd ./orchestrator
npm install
pipenv run pip install pip==18.0.0
npm run build
cd ..