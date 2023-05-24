# IE 692: Advanced Process Mining Project

## General information

### University of Mannheim

### Chair of Process Analytics

**Lecturer:** Prof. Dr. Han van der Aa

**Tutors:** Alexander Kraus and Adrian Rebmann

**Topic:** Decision mining with time series data based on automatic feature generation

**Team:**
   * Adrian Augustin
   * Abderrahmane Charrade
   * Alexander Dietrich
   * Fatma Koumi
   * Sergen Keskincelik

**Goal:** Replication of the results by Beate Scheibel and Stefanie Rinderle-Ma

**Origin:** This repository is based on the original work by the [decision mining paper](https://link.springer.com/chapter/10.1007/978-3-031-07472-1_1) authors, which can be found here: https://github.com/bscheibel/edt-ts.
We applied additional code, which helped us to successfully replicate the original results and to perform additional investigation, i.e. examining the quality of the data and the classifier in detail.

## Step-by-step instruction

### Requirements

* Python version 3.9.6 or better
* Python packages: 
    * pandas version 1.2.0
    * numpy 1.20.1
    * scikit_learn 0.24.0
    * tsfresh 0.18.0

Packages can be installed using pip.


### Execution of Code

* Navigate to the python file you want to run, i.e. time_series_replication.py in the replication folder
* Type in terminal: python time_series_replication.py USE_CASE
   * replace USE_CASE with running, manufacturing or BPI (supported datasets)
   * associated datasets can be found in the data folder
   * BPI dataset is too large, which has to be downloaded here: http://icpmconference.org/2019/wp-content/uploads/sites/6/2019/02/BPIChallenge2019CSV.zip
* Alternatively make use of a virtual environment with pipenv
   * pipenv has to be installed via pip<br>
      `pip install pipenv`
   * type in terminal:<br>
      `pipenv install`
   * then execute: <br>
   `pipenv run python time_series_replication.py USE_CASE` from root of the project directory
   * Note that in case you use pipenv, you have to comment out the line 350 in file __time_series_application.py__ which changes directory to access the csv files:
      ```
      os.chdir("..")
      ``` 

**Note:** Jupyter notebook is not suitable for this code.

### Parameters

Three parameters exist to manually influence the classification process:

* use_case: enter the name of the existing use case
* variable_interest: enter the variable of interest, which should be included in the rule extraction process, otherwise it will discover all possible time series variables in the data (OPTIONAL)
* interval: choose your own intervals, in which the time series data should be split to (OPTIONAL)

### New dataset

You can include a new dataset. However, several tasks have to be performed:

* Preprocessing: Dataset itself has to be transformed into a suitable format in order to work with it as time-series data
* Variable values: several variable values have to be provided to use the classification pipeline
   * df: dataset has to be loaded into a suitable dataframe
   * id: case identifier of the event log
   * result_column: column of the classification results
   * variable_result: choosing the category of interest
   * results: all possible result classes
* Parameter selection: default parameters as for the running & manufacturing case may perform well but not necessarily for the new dataset. It is useful to test out other parameter values to find the optimal solution

## System Information

In the following table, you can view the system information for each machine, that ran the code.

<!-- TABLE_GENERATE_START -->

| Setting number  | CPU | RAM | OS |
| -------- | --- | --- | --- |
|  1  | Intel i5-8265U | 8 GB | Windows 10 |
|  2  | Intel i7-8550U | 8 GB | Windows 10 |
|  3  | Intel i7-85650U | 8 GB | Windows 10 |
|  4  | Intel i5 Quad-Core | 8 GB | MacOS Ventura 13.3.1 |
|  5  | Intel i7 Quad-Core | 16 GB | MacOS BigSur 11.7.5 |

<!-- TABLE_GENERATE_END -->








