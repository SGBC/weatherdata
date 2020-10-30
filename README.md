# weatherdata
This project will integrate data from SLU Lantmet and SMHI for data analysis

**Evaluating locally measured weather and weathers services**
The purpose of the project is to compare predicted, reported and measured weather data from the Swedish Meterological and Hydrological Institute (SMHI) with data collected from weather stations within SLU Lantmet. This project is the first step towards enabling researchers to integrate farm-level data from herd management systems and genome analysis collected by SLU Gigacow with weather data to conduct long term studies on how weather conditions affect animal health and milk production.
Objectives for the project are to:
•	Conduct a literature study on currently available methods to study animal-environment effects caused by weather.
•	Compare data collected from weather stations with measurements and interpolations provided by SMHI.
•	Provide summary statistics of available data and the distribution of measurement errors for different parameters caused by using interpolated values from a weather service versus installing weather stations at each farm or pasture. 
The expected outcome of the project is that animal scientists will be provided with scripts and knowledge to better interpret and handle meteorological data for research purposes. Depending on the outcome of the project the SLU Gigacow infrastructure will collect and store data from SMHI and/or weather stations installed on the 17 farms participating in the research network to support animal-environment research in dairy farms.
All scripts and visualizations produced in the project will be published as open source code via a Github repository. The aim is also to produce one scientific article on the topic describing the process and the measurement errors estimated by the project. We encourage the student to participate in this writing either as the main (first) author with support from the main supervisor.
Requirements: Python is the preferred programming language and to complete the project you must be comfortable working with API:s such as the ones provided by SMIH (http://opendata.smhi.se/apidocs/) and SLU Lantmet (clickable link). An interest in in meteorological data and animal science is beneficial but not required.
During the project you will be working as a part of the SLU Gigacow team working at the Department of Animal Breeding and Genetics at SLU campus Ultuna (see https://www.slu.se/gigacow for more information) with Dr Tomas Klingström (tomas.klingstrom@slu.se, https://www.slu.se/cv/tomas-klingstrom/) as your main supervisor. Most work can be conducted remotely but a working space will also be provided as necessary.  

**Appendix 1, instructions SMHI**
The base URL and a link to the docs:
https://opendata.smhi.se/
http://opendata.smhi.se/apidocs/ 
Basically we know the locations where we can get observations (start out with some Lantmet weather station locations). Using that list of locations the weather prediction API will give you predictions for the closest grid points (the actual locations of predictions). The annoying part is that they post predictions and later remove them. So if you collect predictions for 1 hour before observation, 6, 12, 24, 48 etc you cannot do it just 1 hour before the observation I think.
SMHI Open Data Meteorological Forecasts, PMP, contains forecast data for the following 10 days. It is based on a number of forecast models statistical adjustments and manual edits. Applications that want to benefit from SMHI Open Data Meteorological Forecasts can use this service to retrieve data. The Entry point is located at https://opendata-download-metfcst.smhi.se/. The data is returned as mediatype application/json(JSON). All times are in UTC (Coordinated Universal Time). To get a forecast, eg. https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/16.158/lat/58.5812/data.json, can be used to get a meteorological forecast at a point near SMHI, Norrköping. To get started with the API, see Examples and Point Demo in the API documentation.
SMHI is currently adding older data to collections (pre 1961) but it is mostly complete from 1961 and they switched from manual measurements recording to automated with digital instruments in 1995 so data back to 1996 from SMHI is useful for the project but not before that. 

**Appendix 2, instructions Lantmet**
Note: The name of a station includes the final year of collection (Delsbo -1995 stopped collecting in 1995) but the start year varies depending on station.
De väderdata vi har i Lantmet finns tillgängligt på följande länkar:
https://www.slu.se/fakulteter/nj/om-fakulteten/centrumbildningar-och-storre-forskningsplattformar/faltforsk/vader/ (gå till väderstationer för att söka data)
 
eller i separat fönster https://www.ffe.slu.se/lm (klicka på klimatdata för att söka data)
 
Lantmet är ett samarbete mellan Jordbruksverket, Hushållningssällskapen och SLU Fältforsk. Systemet drivs med begränsade resurser som inte medger tillgängliget 24/7. 
Driftsavbrott kan förekomma kortare tider speciellt över helger. Notera också att en hel del lokala stationer endast är sommarstationer (normalt igång från april-oktober).
 
Vi har SMHI Synop-stationer (3 timmarsvärden, knappt 90 stationer), lokala stationer (egna, fruitweb m.m. knappt 100 st.) samt dessutom griddata från SMHI (timvärden ca 12700 punkter, utökades 2018-05-01).
 
När man söker på data väljer man station, tidsperiod och typ av utdata. Då sökresultatet visas finns i tabellhuvudet en länk för att ta hem data på csv-fil.
 
Jag ska också nämna att stationer i Lantmet också kan ingå som stationer för olika prognoser (för bl.a. potatissjukdomar) från t.ex. VIPS (Norge vid Nibio) eller Dacom (Nederländerna, Grimme/Danmark).
 
Fältforsk/Lantmet har en JSON-tjänst med vilken man kan hämta indata till egna webbsidor eller appar.
Dokumentation finns på länk: https://www.ffe.slu.se/lm/json/JSON-Specifikation.pdf
Länken till JSON-tjänsten (utan parametrar visas stationslistor resp. lista på gridpunkter):
https://www.ffe.slu.se/lm/json/downloadjs.cfm (visar lista på valbara stationer)
https://www.ffe.slu.se/lm/json/downloadjs.cfm?inputType=GRID (visar lista på gridpunkter)
Man kan hämta timvärden eller dygnsvärden genom att ange en rad parametrar (se dokumentationen)
Som utdata kan man få en JSON-fil eller en CSV-fil (då anger man outputType=CSV)
 
Vi kommer antagligen att komplettera JSON-tjänsten så att man även kan hämta rådata med ned till 1 minuts upplösning. 
Rådata samlar vi normalt in per 15 minuter (Lantmet standard för egna stationer). Vanligaste stationstyp är Adcon.
För Fruitweb-stationerna är det oftast 30-minutersvärden och där är det Davis-stationer. 
Vi har även 4 st Campbell-stationer där två samlar 15-minutersvärden, 1 samlar timvärden och Ultuna väderstation samlar 1-minutervärden.
Lantmet kan inte lagra rådata med mindre tidsintervall än 1 minut.
 
Vill ni skaffa nya stationer, och om de ska ingå i Lantmet (det kan vi diskutera i så fall, sådan data blir öppna för alla andra också), så bör det vara Adcon eller Davis-stationer (eller ev. Campbell)
En dokumentation om Lantmet-stationer finns på länk: https://www.ffe.slu.se/lm/ManualLantmet.pdf
Se också kontaktinfo på sidan: https://www.slu.se/fakulteter/nj/om-fakulteten/centrumbildningar-och-storre-forskningsplattformar/faltforsk/vader/lantmet/
Det kan ev. finnas ett par begagnade Adcon-stationer till salu f.n..
 
När man utnyttjar Lantmet data i egna applikationer ska man som källa ange Lantmet/SLU Fältforsk (om SMHI-data används - även SMHI Synop och Mesan-R).
SLU Fältforsk och Lantmet tar inte på sig något ansvar för ev.  ekonomisk skada som fel i data eller driftsavbrott kan orsaka.
Med dessa begränsningar är Lantmet data öppet tillgängliga utan kostnad.
 
