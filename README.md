Setup


Run vagrant


vagrant plugin install vagrant-scp

vagrant up offerdown

vagrant scp item-price-service offerdown:.

vagrant scp redis-3.0.6 offerdown:.

vagrant scp ouchallenge.jmx offerdown:.

vagrant ssh

sudo scp ouchallenge.jmx /usr/share/jmeter/bin



Install requirements for postgres


sudo apt-get update

sudo apt-get install python-dev

sudo apt-get install python-psycopg2 

sudo apt-get install -y postgresql postgresql-contrib

sudo apt-get install libpq-dev

sudo apt-get install python-pip



Run Redis


cd redis-3.0.6

make

cd src

./redis-server



Install other requirements and run item-price-service


cd item-price-service

sudo pip install -r requirements.txt

python item-price-service.py



curl --request GET "http://127.0.0.1:5000/item-price-service/?item=ps4&city=Seattle"

cd /usr/share/jmeter/bin

sudo ./jmeter -n -t ouchallenge.jmx -l run1.jtl

