# Fail Travis build if Pylint returns fatal (1) | error (2)
if [ $(($rc & 3)) -ne 0 ]; then
    echo "Pylint failed"
    exit 1
else
    echo "Pylint passed"
    exit 0
fi