# The impact of weather factors on the productivity of dairy cows

This project aims to explore the impact caused by weather on the milk yields of dairy cows. For this goal, we create a data set by combining weather data from the Swedish Meteorological and Hydrological Institute and milking data from the Gigacow project at SLU. With the combined data set, we explore the correlations and regression between a number of weather factors and milk yield. The results show that there appears to be some negative correlation between temperature/THI and the milk yield of dairy cows.


## milkStatsandMSNO.ipynb
Plots the missingness for each farm in AllMilkings.csv and prints some basic statistics.


## weatherPreProcessing.ipynb 
1. Reads all mesan csv files created by Grib2CSV.ipynb within the date range specified below and puts them in a pandas dataframe
2. Acceses the SMHI STRÅNG API once for each radiation parameter and adds the data to the data frame.
3. Calculates 2 different temperature humidity index (THI) values for each hour.
4. Calculates the daily mean and max for every parameter
5. Saves 2 csv files. Hourly and daily.

It is assumed that you have alredy run Grib2CSV.ipynb for the points in question.
It is also assumed that you run this script from the same location as Grib2CSV.ipynb, meaning a folder named "MESAN_CSV" should exist in the same folder.
To run this script for all the data created by Grib2CSV.ipynb, you can use the exact same function call as you uesed for Grib2CSV.
It is also possible to run it for a subset of the locations and/or a sub range of the time.
If you choose to run this script on non existing data you will have a bad time.

## weathersStats.ipynb
Calculates a few statistics for the weather data and generates a few plots.

## THIplots.ipynb
Generates plots that compare temperature and THI

## milkAndWeather.ipynb 
1. Removes all events with no total yield
2. removes cows named "Unknown"
3. Sums all milkings for each cow in a single day and calculates number of milking events
4. Adds the specified weather data
5. Outputs one or multiple csv files with the combined data

Note that the file "AllMilkings.csv" is required to run this, as well as the relevant daily weather data output by weatherPreProcessing.ipynb

## categorical.ipynb
Plots the mean daily milk yield for a number of temperature and THI-ranges

## simpRegs.ipynb
Generates regression plots and calculates slopes for a number of weather parameters

## autocorrelation.ipynb
plots the autoregression for weather factors and milk yield

## fftXcorrs.ipynb
1. Does some basic imputation of the milking data
2. separates the high and low frequency components of the milk yield
3. Outputs "AllMilkingsDaily_Weather_Filtered.csv", containing the high and low frequency components.
4. Calculates and prints some correlation and regression stuff.

## fftpres.ipynb
Loads "AllMilkingsDaily_Weather_Filtered.csv" and show the filtered curves for one random cow

## Records_Distribution.ipynb 
Explore the distribution of records for each farm.

## Special_Index.ipynb
Explore the special cows with special indexes, which were born in one farm but live in another farm.

## Curve_Fitting_farm.ipynb
Curve cleaning, curve fitting and the exploration about the corrrelations between deviations and weather factors for each farm.

## Curve_Fitting_cow.ipynb
Curve cleaning, curve fitting and the exploration about the corrrelations between deviations and weather factors for each cow.


