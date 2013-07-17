#/bin/bash
eval python manage.py test
r1=$?
eval cd js_sandbox && npm install . && npm test
r2=$?
exit $(($r1 + $r2))
