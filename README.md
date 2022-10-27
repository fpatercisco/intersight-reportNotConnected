# intersight-reportNotConnected
List all targets in your Intersight instance that don't have status=Connected, and the reason why.
This is useful as of October 2022, as Intersight itself has no mechanism for reporting to you when it loses connectivity to a target. So if you want to know when this happens, you need to poll Intersight for the info and react when it happens.

## TODO
* Make the API key info configurable
