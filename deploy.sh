#!/bin/bash
# deploy.sh

project_dir=`pwd`
frontend_dir="$project_dir/frontend/sql2nl-demo"
frontend_templates_dir="$frontend_dir/dist"
frontend_assets_dir="$frontend_dir/dist/static"

backend_dir="$project_dir/backend"
backend_templates_dir="$backend_dir/flaskr/templates"
backend_assets_dir="$backend_dir/flaskr/static"

# step0: build frontend project
echo "[$0] enter frontend directory: '$frontend_dir'"
cd $frontend_dir
echo "[$0] build vue project..."
npm run build
echo "[$0] build finished!"

# step1: clean target directory
echo "[$0] start cleaning '$backend_templates_dir' ..."
rm -rv $backend_templates_dir/*
ls -l $backend_templates_dir
echo "[$0] start cleaning '$backend_assets_dir' ..."
rm -rv $backend_assets_dir/*
ls -l $backend_assets_dir
echo "[$0] rm finished!"

# step2: move generated content to backend directory
echo "[$0] cp all .html files under '$frontend_templates_dir' to '$backend_templates_dir'"
cp -rv $frontend_templates_dir/*.html $backend_templates_dir
echo "[$0] cp all files under '$frontend_assets_dir' to '$backend_assets_dir'"
cp -rv $frontend_assets_dir/* $backend_assets_dir
echo "[$0] cp finished!"

# step3: activate conda env
. "$2" # your 'conda/etc/profile.d/conda.sh' here
conda activate $1 # your conda env
conda env list

# step4: goto backend directory and run server
echo "[$0] enter backend directory: '$backend_dir'"
cd $backend_dir
export FLASK_APP=flaskr
export FLASK_ENV=development
echo "[$0] run flask server..."
flask run --host=0.0.0.0

# step5: return project directory
# cd $project_dir
