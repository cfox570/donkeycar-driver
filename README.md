# donkeycar-driver
###A YAML driven driver script as an alternative to the standard manage.py script to run a Donkeycar.

The current implementation of DonkeyCar uses a very large and complex template manage.py to assemble parts. The python script uses the config.py and many ‘if statements’ to decide which parts are included into the vehicle. To add a new part, the developer must dig into this complex and add the new part with appropiate if statements.

Proposed alternative: YAML part configuration

Since parts have a standard structure, a YAML file can be used to identify to identify which parts to include. If the YAML file contains every part, a comment symbol # can be used to prevent the inclusion of the part.

Instantiating a part requires two sets of parameters. 1) Class Parameters are sent to the Class to configure the object. 2) Vehicle run parameters are used to control inputs, outputs, threading and the run condition.

Class Parameters: Since the values of these are typically setup in the config/myconfig files, I propose that the Class definition of parts be simplified to accept one parameter: cfg which holds all of the configuration parameters.

Vehicle Parameters: I would argue that these are really Part Parameters and should be set by the Part itself.

