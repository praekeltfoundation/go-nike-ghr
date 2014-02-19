manage="${VENV}/bin/python ${INSTALLDIR}/go-nike-ghr/manage.py"

$manage syncdb --noinput --no-initial-data --migrate
$manage collectstatic --noinput
