# With API key:
1. Create a virtual environment, activate it and install required packages
```
python3 -m venv .venv
```
```
source ./.venv/bin/activate
```
```
pip install -r requirements_poc_nvd.txt
```

2. Create a .env file and insert your api key
```
cp .env.example.nvd .env
```
3. Run
```
python nvd_poc.py
```

# Without API key:
1. Create a virtual environment, activate it and install required packages
```
python3 -m venv .venv
```
```
source ./.venv/bin/activate
```
```
pip install -r requirements_poc_nvd.txt
```

2. Do not create a .env file, or leave NVD_API_KEY empty
```
NVD_API_KEY=
```

3. Run
```
python nvd_poc.py
```
