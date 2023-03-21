# Nomi Financial Dashboard

## Introduction
This repository stores the scripts for compiling Nomi Health financials. The script is run in the Business Intelligence tool Domo using their Magic ETL interface. 
The data output powers a BI dashboard in Domo.

compile_scripts.py gathers the needed libraries, constants, and functions and concatenates them into a single script for injection into Domo. 
The output script is saved in the compiled_scripts folder.

## Process
At ahe highest level, the process is as follows:
```mermaid
graph TD;
    A(<b>Initialize</b> <ol><li>detect environment</li><li>declare constants</li><li>create output list</li>) --> B;
    B(<b>Monthly Calculation</b></b> <ol><li>import data</li><li>transform</li><li>add to output list</li>) --> C(Headcount Calculation);
    C(<b>Headcount Calculation</b> <ol><li>import/transform/output</li>) --> D;
    D(<b>Delta Calculation</b> <ol><li>import/transform/output</li>) --> E;
    E(<b>Quarterly Calculation</b> <ol><li>import/transform/output</li>) --> F;
    F(<b>QM Diff Calculation</b> <ol><li>use monthly and quarterly ouputs</li><li>add to output list</li>) --> G;
    G(<b>Analysis Calculation</b> <ol><li>import/transform/output</li>) --> H;
    H(<b>Dashboard Health</b> <ol><li>complete data validation</li><li>add to output list</li>) --> I(<b>Output Data</b> <ol><li>concatenate output list</li><li>write to Domo</li>);

```


