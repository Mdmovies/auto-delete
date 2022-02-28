if [ -z $BRANCH ]
then
  echo "Cloning main Repository"
  git clone https://github.com/Mdmovies/auto-delete /auto-delete
else
  echo "Cloning $UPSTREAM_REPO branch from Respository"
  git clone https://github.com/Mdmovies/auto-delete -b $BRANCH /auto-delete
fi
cd /auto-delete
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 main.py
