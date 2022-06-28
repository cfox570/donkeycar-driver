# donkeycar-driver
#### A YAML driven driver script as an alternative to the standard manage.py script to run a Donkeycar.

This repository is intended to extend the functionality of the standard [Donkeycar framework](https://github.com/autorope/donkeycar).

The DonkeyCar framework uses a very large and complex template script installed as manage.py to assemble car parts and run the vehicle. The python script uses the config.py/myconfig.py and many ‘if statements’ to decide which parts are included into the vehicle. This comprehensive file is difficult to modify. Debugging and adding custom parts is cumbersome. To add a new part, the developer must dig into this complex script and add the new part with appropiate "if statements". The ideal solution for the manage.py would only include parts that are in use by the car or simulated car.  

#### Setup
* Step 1 - Install yaml module - _pip install pyyaml_
* Step 2 - Add the following lines to the myconfig.py file:
```
import os
CAR_PATH = PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))
PARTSYAML_PATH         = os.path.join(CAR_PATH, 'parts.yml')
```
* Step 3 - Copy **driver.py** to your **mycar** folder
* Step 4 - Create a **parts** folder in your **mycar** folder
* Step 5 - Copy **helpers.py** to the **parts** folder
* Step 6 - Copy one of the example yaml parts files as **parts.yml** to your **mycar** folder
* Step 7 - Edit the **parts.yml** to match your vehicle configuration
* Step 8 - Run your vehicle as specifed below


#### Command Line
The driver script works like the standard manage.py script with similar command line parameters. The default name for the yaml parts file is included in the myconfig.py file. The new optional parameter allows specification of filename for the yaml file on the fly. 

```
Usage:
    driver.py [--yaml=<yamlfile>] [--myconfig=<filename>] [--model=<model>] 
      [--type=(linear|categorical|tflite_linear|tensorrt_linear)] [--meta=<key:value> ...]

Options:
    -h --help               Show this screen.
    --yaml=yamlfile         Specify yaml file to use. Default is PARTSYAML_PATH in the config.py or myconfig.py.
    --myconfig=filename     Specify myconfig file to use. [default: myconfig.py]
    --model=model           Path to model. Default is MODEL_PATH in the config.py or myconfig.py.
    --type=type             Type of model. Default is DEFAULT_MODEL_TYPE in the config.py or myconfig.py.
    --meta=<key:value>      Key/Value strings describing describing a piece of meta data that will be
                            stored as metada into the manifest.json file when storing tub data.
                            Option may be used more than once.

Examples:
    driver.py
    driver.py --yaml parts-simple.py
    driver.py --meta 

```

### driver.py and helpers.py

There are three steps to including a part into the vehicle in the manage.py. 1) Import the module/calls 2) Instantiate the part with initilization parameters 3) Add the part to the vehicle. The driver.py script performs these three steps in a generic way. The parameters for each of the steps is specified in a YAML file.

In addition to the code to add parts from module files, the standard manage.py script contains embedded parts; DriveMode, RecordTracker. There is also some "glue" code to create the parameters for the parts. This code was moved to helpers.py. The part AI_Pilot was added since instantiating the Keras AI part does not follow the standard pattern. The goal at this time is to produce a working car without a lots of "bells and whistles." There is a other functionality included in manage.py that is not part of helper.py or drivers.py. This could be added as required by the developer to either the helpers.py or drivers.py or to a new parts file. 


### Structure of the YAML Parts File
The YAML parts file specifies all the parts to be included into the vehicle. Each part contains an enable parameter that is used to disable the part for debugging.  Like python, indented lines are required to associated the parameters of a definition.  Indents shown below are required for each type of parameter. Colons are required. Do not include hyphens when filling in the values. String values DO NOT require quotes.  *All the parameters below can be found in manage.py.*  Comments can be embedded with the pound/sharp sign #. All characters to the right are ignored. Insert the pound # in front of any of the optional arguments to have them ignored. 

```
parts:
    -partname-:
        class:          -classname-
        module:         -modulename-
        enable:         -Boolean-
        args:
            -argument1-:    -value-
            -argument2-:    -value-
        inputs:         -[value1,value2]-
        outputs:        -[value1,value2]-
        threaded:       -Boolean-
        run_condition:  -value-
```
* **parts:** The first required token in the file starting in the first column.
* **-partname-**: Give each part an arbitrary unique part name. You can specify multiple parts with the same classname as long as the partname is unique.
* **class:**  -classname- Specify the class name of the part.
* **module:** -modulename- Specify the module/file name where the part is defined.
* **wenable:** -Boolean- Specify **True** to include the part or **False** to ignore the definition
* **args:**  Specifies the arguments for initializing the part. List each -argument- and -value- or a separate line. if no arguments are needed, use {} on                  the same line. Values can be specified explicitly (ex. 0.0, 27, PICAM) or referencing the config parameters. The special keyword **cfg** is used to specify the object created from config.py/myconfig.py. When specifying arguments, use cfg refers to the whole object or use cfg.NAME (ex. cfg.DRIVE_LOOP_HZ) to specify a specific value.
* **inputs:** Specifies the inputs the part requires at runtime. Provide the list of inputs separated by commas. The list may be empty specified by [].
* **outputs:** Specifies the outputs the part generates at runtime. Provide the list of outputs separated by commas. The list may be empty specified by [].
* **threaded:** -Boolean- This is an optional parameter.  Specify **True** to indicate the part is threaded or **False** to indicate the part is NOT threaded.
* **run_condition:**  -value-  This is an optional parameter. Include this parameter when another boolean parameter is required to control running the part. *Replace the value with True to force the part to run.*

### YAML Example Files
