#!/bin/bash --login
echo "--------------------------------------------"
echo "Checkout to latest tag"
echo "--------------------------------------------"
git checkout v4.15.4 -f
echo "--------------------------------------------"
echo "Describing Head"
echo "--------------------------------------------"
git describe > HEAD
echo "____________________________________________"
echo "Removing Gemfile.lock"
echo "____________________________________________"
rm Gemfile.lock
echo "____________________________________________"
echo "Installing Local Gems"
echo "____________________________________________"
bundle install --local
echo "--------------------------------------------"
#echo "killing sync_worker cron job"
#pkill -f bin/lab/sync_worker.rb
echo "____________________________________________"
echo "running bin_update art"
echo "____________________________________________"
./bin/update_art_metadata.sh development
echo "--------------------------------------------"
#echo "replace port 5000 in application.yml to 8050"
#sed -i 's/5000/8050/g' config/application.yml
