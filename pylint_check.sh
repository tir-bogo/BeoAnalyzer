find . -name '*.py' -not -path '*/\*' | xargs ls -hat | xargs pylint || pylint-exit $?
if [ $? -ne 0 ]; then
  echo "An error occurred while running pylint." >&2
  exit 1
fi