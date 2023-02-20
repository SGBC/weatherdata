# The impact of weather factors on the productivity of dairy cows

This project aims to explore the impact caused by weather on the milk yields of dairy cows. For this goal, we create a data set by combining weather data from the Swedish Meteorological and Hydrological Institute and milking data from the Gigacow project at SLU. With the combined data set, we explore the correlations and regression between a number of weather factors and milk yield. The results show that there appears to be some negative correlation between temperature/THI and the milk yield of dairy cows.


# Code explanation...

## milkAndWeather.ipynb 
1. Removes all events with no total yield
2. removes cows named "Unknown"
3. Sums all milkings for each cow in a single day and calculates number of milking events
4. Adds the specified weather data
5. Outputs one or multiple csv files with the combined data

Note that the file "AllMilkings.csv" is required to run this, as well as the relevant daily weather data output by weatherPreProcessing.ipynb
