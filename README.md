# zz_scraper

This project consists of a scraping bot which scrapes zerozero.pt football league tables with the intent of building a linear regression model which forecasts,
based on the desired league table position and the number of teams in competition, the number of points needed for the desired outcome.

The scraper bot will work out of the box (as of November 2022 - just select the league IDs you want), but it will fail in some leagues if the league name is in a
different color than the default white (for instance, Belgian Leagues). To do that, you can comment out the part that creates the folder automatically.

There is a ready-made model in the model.pkl file. This was based in the datasets found in the "Clean Data" folder. (Other tables need cleaning to be properly used -
the 'cleaning' file only has a routine to clean playoffs out of English leagues, which are provided already clean)

This project was done in the context of the Ironhack Lisbon Full Time Data Analysis October 2022 bootcamp.
