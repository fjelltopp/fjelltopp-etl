# Fjelltopp ETL Framework

## Structure of fjelltopp ETL batch projects

Define a function called `run_pipeline()` that will run the ETL pipeline

This function can then be called in a __name__ == "__main__" block or by in a lambda function.

Extract functions should get the needed data and return a pandas dataframe.

Transform functions should be pure functions that take a pandas dataframe as an argument and returns a data frame. Ideal functions would allow the use of pandas [https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.pipe.html](pipe).

Load functions should take data frames and write them to their indent destinations


## Secrets

We support two ways of including secrets in ETL pipelines. The first is through environment variables. The second using AWS Secret manager. 


## Logging:

It is important to log the execution of our data pipelines. To log directly to cloudwatch get a logger from the get_logger function in etl.logging. This supports normal python logging.


## Scheduling

   Scheduling by crontab or other means should be clearly documented in the etl_pipeline