SCRIPT=`realpath $0`
SCRIPTFOLDERPATH=`dirname $SCRIPT`
MAINFOLDERPATH=`dirname $SCRIPTFOLDERPATH`

cd $MAINFOLDERPATH
mkdir -p data

cp -n $SCRIPTFOLDERPATH/data_template/config.ini $MAINFOLDERPATH/data/config.ini
cp -n $SCRIPTFOLDERPATH/data_template/database.db $MAINFOLDERPATH/data/database.db

echo "Installation completed! Now, update the config.ini file in the data folder."