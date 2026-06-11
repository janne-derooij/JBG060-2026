# JBG060-2026
Repository for the course JBG060 in 2026, investigating flood dynamics in South Sudan

The data that we have prepared as a starting position can be downloaded from
https://surfdrive.surf.nl/s/45yFwCAWmXb63Ec with password 3F7rq7kEET

Please follow the following steps:
1) Clone this repository:
```
// git clone https://github.com/janne-derooij/JBG060-2026
```

2) Download the data from surfdrive, and place it in a sub-folder of JBG060-2026, called 'raw_data'.

3) Set up the environment: 

If you are using venv:
```
// py -m venv myenv
// myenv\Scripts\activate
// pip install -r requirements.txt
```

If you are using conda:
```
// conda create -n myenv python=3.14
// conda activate myenv
// pip install -r requirements.txt
```

4) Run the project:<br>
loading.py loads the hydrological/meteorological data<br>
loading_impact.py loads the exposure/impact data that we provide.




