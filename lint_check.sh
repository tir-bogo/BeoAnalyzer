echo "Running pylint validation"
find . -iname "*.py" | xargs pylint -d R0801 || pylint-exit $?
if [ $? -ne 0 ]; then
  echo "An error occurred while running pylint." >&2
  exit 1
fi

echo "Running pycodestyle validation"
pycodestyle .
if [ $? -ne 0 ]; then
  echo "An error occured wile running pycodestyle" >&2
  exit 1
fi