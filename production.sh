cp -rf ../Incu2019_gitlab ../Incu2019_github
rm  ../Incu2019_github/student_info.json
rm ../Incu2019_github/nxapi/src/config_test.py
rm  ../Incu2019_github/production.sh

cd ../Incu2019_github

git add -A
git commit -m $1
git push github master

cd ../Incu2019_gitlab

rm -rf ../Incu2019_github
