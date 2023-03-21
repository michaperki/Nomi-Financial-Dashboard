# Nomi Financial Dashboard
This project is a part of [Nomi Health](https://nomihealth.com/g).

#### -- Project Status: [Active]

## Project Intro/Objective
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
Data is provided by the Nomi Financial team and sent straight to Domo via Domo's automated 'upload via email' connector. This codebase replaces a time and labor intensive process created by a consulting team and maintained in Excel models. The data consists of Projected and Actual spend (Monthly and Quarterly spend files are supplied separately), allocation files for each Expense Bucket, and a name map for cross-referencing between the actuals and projections. The specific visualizations required necessitate several different operations (see below).

## Process
At the highest level, the process is as follows:
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

## Needs of this project

- data scientist(s) with intermediate Python
- data processing/cleaning
- code clean up
- increased data validation
- analysis view
- writeup/reporting

## Getting Started

1. Clone this repo (for help see this [tutorial](https://help.github.com/articles/cloning-a-repository/)).
2. Raw Data can be provided by the Nomi Financial team to authorized parties.    
3. Data processing/transformation scripts are being kept [here](https://github.com/michaperki/Nomi-Financial-Dashboard/tree/main/scripts)

#  sections pending below
5. Follow setup [instructions](Link to file)

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
