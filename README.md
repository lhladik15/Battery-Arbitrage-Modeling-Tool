# Blueprint-Power-Modeling-Tool

Please note that the final system design is included in the file "FinalSystem.py".
Inputs:
  1. Battery Storage Design 
  Max power capacity (both charge and discharge in kW)
  Discharge energy capacity (in kWh)
  AC-AC Roundtrip efficiency 
  Max daily discharged throughput (in kWh) 
  2. Market Price inputs:
  Hourly LMBPS (write the beginning names of the csv files, i.e., the year for the variable named 'filenames'
  Zone 
 Outputs:
  CSV file with power output (kW) & State of Energy (kWh)
  CSV file with total annual revenue generation, total annual charging cost, and total annual throughput 
  
 NOTE:
 I've added an extra file called 'dayAheadPrediction.' I've created a neural network to assist the project with energy price projections, but is in its early stages and requires more development, tuning and data to become effective. I figured it couldn't hurt to attempt to solve the problem of next-day forecasts, so I included it here! 


  
