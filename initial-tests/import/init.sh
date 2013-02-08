#!/bin/sh
PLUGIN_HOME='/usr/lib/openvas/plugins/nvt'
PLUGIN_DIR='/home/gnorton/Source/Butters/initial-tests/import/plugins'
EXT='*.nasl'

# backup the original plugins
tar zcvf /tmp/plugin-bak.tar.gz $PLUGIN_HOME > /dev/null 2>&1

# remove the old files
echo "Removing old files..."
rm -f $PLUGIN_DIR/$EXT

# copy the fresh files
echo "Copying new files..."
perl -pi -e 's/openvas/Finnean-SSC/gi' $PLUGIN_HOME/$EXT
cp $PLUGIN_HOME/$EXT $PLUGIN_DIR

# use perl to do a little file cleanup
echo "Cleaning files..."
perl -pi -e "s/^\n+//" $PLUGIN_DIR/$EXT

echo "Running CSV creation."
perl parse-bugtraq.pl > bugtraq.csv
perl parse-category.pl > category.csv
perl parse-cve.pl > cve.csv
perl parse-description.pl > description.csv
perl parse-family.pl > family.csv
perl parse-filename.pl > filename.csv
perl parse-name.pl > name.csv
perl parse-risk.pl > risk.csv
perl parse-solution.pl > solution.csv
perl parse-version.pl > version.csv


echo "Loading into MySQL."
mysql -h localhost -u plugin -p < load-all.mysql

echo "Completed."
