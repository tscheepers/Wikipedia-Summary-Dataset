#!/bin/bash

LANG="en"
USER="wikiuser"
PASS="wikipass"
DATE="20180420"
DBNAME="${LANG}wiki"
XMLFILE="${LANG}wiki-${DATE}-pages-meta-current.xml.bz2"

# complle java jar if necessary
if [ ! -f ./mediawiki-tools-mwdumper/target/mwdumper-1.25.jar ]; then
    cd mediawiki-tools-mwdumper
    mvn install
    cd ..
fi

# create database
echo "DROP DATABASE IF EXISTS ${DBNAME}; CREATE DATABASE ${DBNAME};" | mysql -u ${USER} -p"${PASS}"

# create tables
cat mediawiki-1.25.sql | mysql -u ${USER} -p"${PASS}" ${DBNAME}

# import xml file
java -jar mediawiki-tools-mwdumper/target/mwdumper-1.25.jar --format=mysql:1.25 --filter=notalk --filter=latest data/${XMLFILE} | grep "INSERT INTO page " | sed -e 's/INSERT INTO page /INSERT IGNORE INTO page /g' | mysql -u ${USER} -p"${PASS}" ${DBNAME}
