full_path=$(realpath $0) 
dir_path=$(dirname $full_path)

cd $dir_path/rssbots
source venv/bin/activate
python rssbots.py
deactivate
cd -

