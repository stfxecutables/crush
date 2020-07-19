#SOURCE: https://stackoverflow.com/questions/64786/error-handling-in-bash

lib_name='trap'
lib_version=20121026

stderr_log="/dev/shm/stderr.log"

#
# TO BE SOURCED ONLY ONCE:
#
###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

if test "${g_libs[$lib_name]+_}"; then
    return 0
else
    if test ${#g_libs[@]} == 0; then
        declare -A g_libs
    fi
    g_libs[$lib_name]=$lib_version
fi


#
# MAIN CODE:
#
###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

set -o pipefail  # trace ERR through pipes
set -o errtrace  # trace ERR through 'time command' and other functions
set -o nounset   ## set -u : exit the script if you try to use an uninitialised variable
set -o errexit   ## set -e : exit the script if any statement returns a non-true return value

exec 2>"$stderr_log"
