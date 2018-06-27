#!/bin/bash
curl -s ftp://ftp.unidata.ucar.edu/pub/idv/nightly_idv_5.5/idv_5_5_linux64_installer.sh>idv.sh
chmod +x idv.sh
wrkdir=`pwd`
printf 'o\n\n1\n'`pwd`'/IDV\n'|./idv.sh
wkdir=`pwd`
export IDV_HOME=${wrkdir}/IDV
mkdir -p ${wrkdir}/.java/.systemPrefs
mkdir ${wrkdir}/.java/.userPrefs
chmod -R 755 ${wrkdir}/.java
export JAVA_OPTS="-Dawt.useSystemAAFontSettings=on -Dswing.aatext=true -Dsun.java2d.xrender=true -Djava.util.prefs.systemRoot="${wrkdir}"/.java -Djava.util.prefs.userRoot="${wrkdir}"/.java/.userPrefs"
#export JAVA_OPTS="-Djava.util.prefs.systemRoot="`pwd`"/.java -Djava.util.prefs.userRoot="`pwd`"/.java/.userPrefs"
cd test
echo $HOME
idv_teleport -b NOAA_sst.xidv -t 2011-01-01 -td 1days -nohead True
cp *.gif ../sphinx/_build/html/_static/
cp *.png ../sphinx/_build/html/_static/
