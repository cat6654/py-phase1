#### AQA Python (UI and API) Homeworks

[![CircleCI](https://circleci.com/gh/cat6654/py-phase1.svg?style=svg)](https://circleci.com/gh/cat6654/py-phase1)

This project was created for reviewing AQA Python (UI and API) Homeworks.
In a root folder you can find one configuration file and a resources directory that contain another configuration file: 
  * pytest.ini - for setting pytest test markers/tags
  * resources/test_config.ini - for setting base application url and test user credentials

To run tests you can use following commands:
	* pytest tests/<test_module_name> (for example pytest tests/test_phase_two.py)
	* pytest tests/<test_module_name> - n <number_of_concurrent_runs> (for example: pytest tests/test_phase_two.py -n 4)
	* pytest -v -m <test_marker_name>  (for example: pytest -v -m)
