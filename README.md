# pySolid

Solid server built with Python and RDFLib.

Following documentation has been tested on Ubuntu 18.

## Install pre requisites

```
cd /home/{user}/
git clone http://github.com/assemblee-virtuelle/pySolid
```

### Data persistance with Berkeley DB

Download Berkeley zip from this repository : db-5.3.28.tar.gz
```
cd ~/
tar -zxvf db-5.3.28.tar.gz
cd db-5.3.28
sed -i 's/\(__atomic_compare_exchange\)/\1_db/' src/dbinc/atomic.h
cd build_unix
../dist/configure --prefix=/usr --enable-compat185 --enable-dbm --disable-static --enable-cxx*
make
make docdir=/usr/share/doc/db-5.3.28 install
```

References :
- https://www.oracle.com/technetwork/database/database-technologies/berkeleydb/downloads/index.html
- http://www.linuxfromscratch.org/blfs/view/svn/server/db.html

### Python dependencies
```
cd /home/{user}/pySolid
pip install pew
pew new --python=python3 pysolid
pew workon pysolid # if venv is not started
pip install -r requierements.txt
```
### Python lib for Berkeley DB : bsddb3

Download source zip from this repository : bsddb3-6.2.6.tar.gz
```
tar -zxvf bsddb3-6.2.6.tar.gz
python setup.py --berkeley-db-incdir=/usr/include --berkeley-db-libdir=/usr/lib/ install
```
References :
- https://pypi.org/project/bsddb3/

# Start server
```
cd /home/{user}/pySolid
pew workon pysolid
python dev.py
```
You can test all is running by going on http://127.0.0.1:5000/test_sparql