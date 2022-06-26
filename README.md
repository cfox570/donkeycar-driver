# donkeycar-driver
#### A YAML driven driver script as an alternative to the standard manage.py script to run a Donkeycar.

This repository is intended to extend the functionality of the standard [Donkeycar framework](https://github.com/autorope/donkeycar).

The DonkeyCar framework uses a very large and complex template script installed as manage.py to assemble car parts and run the vehicle. The python script uses the config.py/myconfig.py and many ‘if statements’ to decide which parts are included into the vehicle. This comprehensive file is difficult to modify. Debugging and adding custom parts is cumbersome. To add a new part, the developer must dig into this complex script and add the new part with appropiate "if statements". The ideal solution for the manage.py would only include parts that are in use by the car or simulated car.  

## Setup
* Step 1 - Install yaml module - _pip install pyyaml_
* Step 2 - Copy **driver.py** to your **mycar** folder
* Step 3 - Create a **parts** folder in your **mycar** folder
* Step 4 - Copy **helpers.py** to the **parts** folder
* Step 5 - Copy the **parts.yml** to your **mycar** folder
* Step 6 - Edit the **parts.yml** to match your vehicle configuration
* Step 7 - Run your vehicle as specifed below


## driver.py

The driver script works like the standard manage.py script with similar command line parameters. The new optional parameter allows specification of filename for the yaml file. 

### Command Line
```
Usage:
    driver.py [--yaml=<yamlfile>] [--myconfig=<filename>] [--model=<model>] 
      [--type=(linear|categorical|tflite_linear|tensorrt_linear)] [--meta=<key:value> ...]

Options:
    -h --help               Show this screen.
    --yaml=yamlfile         Specify yaml file to use. Default is PARTS_PATH in the config file.
    --myconfig=filename     Specify myconfig file to use. [default: myconfig.py]
    --model=model           Path to model. Default is MODEL_PATH in the config file.
    --type=type             Type of model. Default is DEFAULT_MODEL_TYPE in the config file.
    --meta=<key:value>      Key/Value strings describing describing a piece of meta data that will be
                            stored as metada into the manifest.json file when storing tub data.
                            Option may be used more than once.

Examples:
    driver.py
    driver.py --yaml parts-simple.py
    driver.py --meta 

```

There are three steps to including a part into the vehicle. 1) Import the module/calls 2) Instantiate the part with initilization parameters 3) Add the part to the vehicle. The driver.py script performs these three steps. The parameters for each of the steps is specified in a YAML file.


## YAML Parts File
