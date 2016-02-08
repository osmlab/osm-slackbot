import yaml

from geowatchutil.runtime import build_broker_kwargs

from osmslackbot import settings
from osmslackbot.broker.base import OSMSlackBotBroker
from osmslackbot.utils import load_templates

verbose = False

broker_config = None
with open("osmslackbot/bot.yml", 'r') as f:
    broker_config = yaml.load(f)
#print "Broker Config: ", broker_config

templates = load_templates()
#print "##############"
#print "Templates: ", templates

broker_kwargs = build_broker_kwargs(
    broker_config,
    settings.GEOWATCH_CONFIG,
    verbose=verbose)
broker_kwargs["templates"] = templates
broker_kwargs["ignore_errors"] = True  # Set to False to raise errors and break execution
#print "##############"
#print "KWARGS: ", broker_kwargs

broker = OSMSlackBotBroker(
    broker_config.get('name', None),
    broker_config.get('description', None),
    **broker_kwargs)
broker.run(run_cycle_out=False)  # run_cycle_out=False prevents default producer behavior
