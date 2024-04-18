echo "Creating virtual enviorment"
python3 -m venv .venv
echo "Installing packages"
source ".venv/bin/activate"
pip3 install -r requirements.txt
echo "Done"
echo "Testing"
python3 test/test.py