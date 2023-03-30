![Header](https://github.com/michaperki/Nomi-Financial-Dashboard/blob/main/header.PNG)
# Nomi Financial Dashboard
This project is a part of [Nomi Health](https://nomihealth.com/g).

#### -- Project Status: [Active]

# Table of Contents
- [Project Intro](#project-intro)
- [Project Description](#project-description)
- [Process](#process)
  1. [Initialize](#initialize)
  2. [Monthly Calculation](#monthly-calculation)
  3. [Headcount Calculation](#headcount-calculation)
  4. [Delta Calculation](#delta-calculation)
  5. [Quarterly Calculation](#quarterly-calculation)
  6. [QM_Diff Calculation](#qm_diff-calculation)
- [Needs of this Project](#needs-of-this-project)


## Project Intro
[(Back to top)](#table-of-contents)

The purpose of this project is to clean and compile several Excel models and output a dataset powering a BI Dashboard. This repository stores the scripts for data import, transform, and export. The project is designed to run modularly in VSCode and then compile into a single text file for injection into Domo, using the "compile_scripts.py" helper tool.

### Methods Used
* Data Science Techniques (group by, pivot, melt, etc.)
* Key Creation and Mapping (joining)
* Data Visualization
* GitHub CoPilot and ChatGPT for code improvement

### Technologies
* Python (libraries listed below)
  * Pandas
  * Numpy
  * Logging
* Domo BI Tool

## Project Description
[(Back to top)](#table-of-contents)

Data is provided by the Nomi Financial team and sent straight to Domo via Domo's automated 'upload via email' connector. This codebase replaces a time and labor intensive process created by a consulting team and maintained in Excel models. The data consists of Projected and Actual spend (Monthly and Quarterly spend files are supplied separately), allocation files for each Expense Bucket, and a name map for cross-referencing between the actuals and projections. The specific visualizations required necessitate several different operations (see below).

## Process
[(Back to top)](#table-of-contents)

At the highest level, the process is as follows:
```mermaid
graph LR;
    A(<b>Initialize</b> <ol><li>detect environment</li><li>declare constants</li><li>create output list</li>) --> B;
    B(<b>Monthly Calculation</b></b> <ol><li>import data</li><li>transform</li><li>add to output list</li>) --> C(Headcount Calculation);
    C(<b>Other Calculations</b> <ol><li>Headcount</li><li>Delta</li><li>Quarterly</li><li>QM Diff</li><li>Dashboard Health</li>) --> D;
    D(<b>Output Data</b> <ol><li>concatenate output list</li><li>write to Domo</li>);
```

### Initialize
[(Back to top)](#table-of-contents)

The script runs in both VSCode and Domo. The [detect_environment](https://github.com/michaperki/Nomi-Financial-Dashboard/blob/main/scripts/detect_environment.py) function uses the ```os``` library to detect whether it is being run locally or in Domo. It returns a boolean constant ```RUNNING_IN_DOMO```.
All constants and the empty output list are declared in [constants](https://github.com/michaperki/Nomi-Financial-Dashboard/blob/main/scripts/constants.py).

### Monthly Calculation
[(Back to top)](#table-of-contents)

The monthly calculation is the main transform of this ETL. It involves reformatting and cleaning the data, joining the allocations, and merging the Actuals and Projections.
The [main script](https://github.com/michaperki/Nomi-Financial-Dashboard/blob/main/scripts/_main_.py) runs the monthly calculations. 

#### Data Import
First, the main script retrieves the data using [get_data](https://github.com/michaperki/Nomi-Financial-Dashboard/blob/main/scripts/get_data.py). Each file has a dictionary declared in [constants](https://github.com/michaperki/Nomi-Financial-Dashboard/blob/main/scripts/constants.py) with the relevant file path in Domo and locally. The get_data function accepts this dictionary (and the ```RUNNING_IN_DOMO``` boolean) to retrieve the data in either environment.

##### Actual File Date
The ```ACTUAL_FILE_DATE``` is an integer representing the month of Actuals data available. Per the [Upload Checklist](https://nomihealth.atlassian.net/wiki/spaces/~6268326934b9b700687acfc6/pages/1906639311/Upload+Checklist), the Actuals must include a month name in the file (three-letter abbreviation also accepted). This month is extracted as an integer using [get_actuals_date](https://github.com/michaperki/Nomi-Financial-Dashboard/blob/main/scripts/get_actuals_date.py) and the ```ACTUAL_FILE_DATE``` stores that value.

**_NOTE:_**  During the first few months of the year, there is no Actuals data available. During this time, the boolean ```FIRST_RUN_OF_YEAR``` should be switched to ```True```. This will set ```ACTUAL_FILE_DATE``` to zero and allow the script to run. The ```DELTA_CONTROLLER``` should also be switched off at this time.

#### Data Validation
Before cleaning the data, we take stock of our input numbers to compare with our final output using [setup_data_validation](https://github.com/michaperki/Nomi-Financial-Dashboard/blob/main/scripts/setup_data_validation.py)

#### Data Cleaning
Next, the main script cleans the allocations using [clean_allocation_sheet](https://github.com/michaperki/Nomi-Financial-Dashboard/blob/main/scripts/clean_allocation_sheet.py) and the Actuals using [clean_actuals](https://github.com/michaperki/Nomi-Financial-Dashboard/blob/main/scripts/clean_actuals.py). 
Each projections model has its own cleaning function ([clean_fte](https://github.com/michaperki/Nomi-Financial-Dashboard/blob/main/scripts/clean_fte.py), [clean_orm](https://github.com/michaperki/Nomi-Financial-Dashboard/blob/main/scripts/clean_orm.py), [clean_ftc](https://github.com/michaperki/Nomi-Financial-Dashboard/blob/main/scripts/clean_ftc.py), etc).

#### Join Allocations to the Projections and Actuals
Concatenate the cleaned allocations into a single dataframe.
Then use [join_allocation_to_df](https://github.com/michaperki/Nomi-Financial-Dashboard/blob/main/scripts/join_allocation_to_df.py) to add the allocations to the Actuals and Projections.

<details>
  <summary>Detailed Explanation of Allocation Process</summary>
  <br>
  At this point, we have our Actuals, Projections, and Allocations cleaned and formatted. We created an <code>ALLOCATION_KEY</code> column in each of our Allocation dataframes. Here's an example of an ALLOCATION_KEY: <p><strong>Q1|CARE|SHARED SERVICES|ATLASSIAN|2023|SOFTWARE</strong>.</p>
  The data that needs to be allocated in the Projections and Actuals is labelled as <strong>SHARED SERVICES</strong> and not assigned to a specific BU. The exception here is FTE Actuals. The FTE Actuals are allocated by the Finance team. They are assigned "NOT SHARED SERVICES" in [clean_actuals_fte](https://github.com/michaperki/Nomi-Financial-Dashboard/blob/main/scripts/clean_actuals_fte.py), so they will never reach the allocation stage.

  [Duplicate_df_for_shared_services](https://github.com/michaperki/Nomi-Financial-Dashboard/blob/main/scripts/duplicate_df_for_shared_services.py) creates duplicate data for each BU. It also creates the <code>ALLOCATION_KEY</code> for the Projections / Actuals. The duplicate spend is resolved by bringing in the allocations.

  If the allocation fails for some reason (for example, a shared spend line item without a vendor name), assign .5 to Care and .5 to Connect for that spend. Assign 0 to both Network and Trust.

  At the beginning and end of the allocation process, check the sum of the spend in the dataframe and confirm that the pre/post numbers are within .01%. Log the results of this validation test using the Python logging library.
  </details>


#### Final Formatting
Concatenate the Projections and Actuals and feed the final dataframe to [format_final_df](https://github.com/michaperki/Nomi-Financial-Dashboard/blob/main/scripts/format_final_df.py).

#### Complete the Validation
Confirm that the allocated numbers match the numbers we stored earlier in our validation setup using [validation_complete](https://github.com/michaperki/Nomi-Financial-Dashboard/blob/main/scripts/validation_complete.py).

### Headcount Calculation
[(Back to top)](#table-of-contents)

Import the data fresh and use [calculate_headcount](https://github.com/michaperki/Nomi-Financial-Dashboard/blob/main/scripts/hc_calculate_headcount.py) to obtain the headcount calculations.

### Delta Calculation
[(Back to top)](#table-of-contents)

Import the data fresh and use [dt_calculate_deltas](https://github.com/michaperki/Nomi-Financial-Dashboard/blob/main/scripts/dt_calculate_deltas.py) to obtain the Delta calculations.

### Quarterly Calculation
[(Back to top)](#table-of-contents)

Import the Quarterly data and use [format_quarterly_data](https://github.com/michaperki/Nomi-Financial-Dashboard/blob/main/scripts/format_quarterly_data.py) to obtain the Quarterly calculations.

### QM_Diff Calculation
[(Back to top)](#table-of-contents)

Use [calculate_qm_diff](https://github.com/michaperki/Nomi-Financial-Dashboard/blob/main/scripts/calculate_qm_diff.py) to obtain the QM_Diff calculations.



## Needs of this project
[(Back to top)](#table-of-contents)

- data scientist(s) with intermediate Python
- data processing/cleaning
- code clean up
- increased data validation
- analysis view
- writeup/reporting

## Getting Started
[(Back to top)](#table-of-contents)

1. Clone this repo (for help see this [tutorial](https://help.github.com/articles/cloning-a-repository/)).
2. Raw Data can be provided by the Nomi Financial team to authorized parties.    
3. Data processing/transformation scripts are being kept [here](https://github.com/michaperki/Nomi-Financial-Dashboard/tree/main/scripts)

## Pending Sections
[(Back to top)](#table-of-contents)

1. Console Output (validation and bug testing)

## Featured Notebooks/Analysis/Deliverables
* [Notebook/Markdown/Slide Deck Title](link)
* [Notebook/Markdown/Slide DeckTitle](link)
* [Blog Post](link)


## Contributing DSWG Members

**Team Leads (Contacts) : [Michael Perkins](https://github.com/michaperki)(@mperkins1995)**

#### Other Members:

|Name     |  Slack Handle   | 
|---------|-----------------|
|[Full Name](https://github.com/[github handle])| @johnDoe        |
|[Full Name](https://github.com/[github handle]) |     @janeDoe    |

## Contact
* If you haven't joined the SF Brigade Slack, [you can do that here](http://c4sf.me/slack).  
* Our slack channel is `#datasci-projectname`
* Feel free to contact team leads with any questions or if you are interested in contributing!
