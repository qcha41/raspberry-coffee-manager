SCRIPT=`realpath $0`
SCRIPTFOLDER=`dirname $SCRIPT`
MAINFOLDER=`dirname $SCRIPTFOLDER`

mkdir -p data

cp -n $SCRIPTFOLDER/data_template/config.ini $MAINFOLDER/data
cp -n $SCRIPTFOLDER/data_template/database.db $MAINFOLDER/data

echo "Installation complete! Now edit the config.ini file with your configuration."

