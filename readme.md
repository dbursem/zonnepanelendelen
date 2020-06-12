Simple script to fetch production data from a zonnepanelendelen javascript applet into an influx database.

Unfortunately, the zonnepanelendelen applet does not return real production, but rather an extrapolation/estimation
based on the last two real measurements it has. It does this to artificially increase the resolution. Of course these
extrapolated points have no historical value so I made an effort to filter them out. By running this script every minute
and calculating the rate and jerk of the production graph, only the first call after a real measurement is tagged with
`isRealValue=True`. Which I think is close enough. 

If zonnepanelendelen is watching: It would be very nice to have an API endpoint to fetch actual production stats, or 
maybe a webhook called when a measurement is updated?
