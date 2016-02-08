Slack Bot for OpenStreetMap (osm-slackbot)
==========

.. image:: https://travis-ci.org/osmlab/osm-slackbot.png
    :target: https://travis-ci.org/osmlab/osm-slackbot

.. image:: https://img.shields.io/pypi/v/osm-slackbot.svg
    :target: https://pypi.python.org/pypi/osm-slackbot

.. image:: https://readthedocs.org/projects/osm-slackbot/badge/?version=master
        :target: http://osm-slackbot.readthedocs.org/en/latest/
        :alt: Master Documentation Status

Description
-----------

Slack bot for OpenStreetMap (http://www.openstreetmap.org/).  The bot queries
the Humanitarian OpenStreetMap Team Tasking Manager
(https://github.com/hotosm/osm-tasking-manager2) and the OSM API
(https://api.openStreetMap.org/api/0.6/). The bot handles the message
types specified below in the coverage section.

**Coverage**

- [X] HOT Projects: `@osm project 34`
- [X] OSM Changesets: `@osm changeset 1`
- [X] OSM Nodes: `@osm node 1`
- [X] OSM Ways: `@osm way 19754176`
- [X] OSM Relations: `@osm relation 70000`
- [-] OSM Users: `@osm user Steve`

For a full list of text that this bot detects read the patterns.yml file at https://github.com/osmlab/osm-slackbot/blob/master/osmslackbot/patterns.yml.

For a full list of responses / templates read the responses.yml file at https://github.com/osmlab/osm-slackbot/blob/master/osmslackbot/responses.yml.

Installation
------------

The osm-slackbot-ansible_ repo uses Ansible_ to make installation easy.

.. _osm-slackbot-ansible: https://github.com/osmlab/osm-slackbot-ansible
.. _Ansible: http://ansible.com

Usage
-----

First, you'll need to create a bot in your Slack team.  The easiest way is to
just call your bot `osm` (so its referenced as @osm).  Navigate to the
integrations customization page (https://<teamname>.slack.com/apps/manage/custom-integrations).

Once you've created your Slack bot, be sure to invite it to the channels you
want it to watch.

Then, follow the instructions on the osm-slackbot-ansible_ repo
to provision a virtual machine within minutes.

Contributing
------------

We are currently accepting pull requests for this repository. Please provide a human-readable description with a pull request and update the README.rst file as needed.

If you'd like to add coverage for a new message type, the key files are:

- patterns.yml - https://github.com/osmlab/osm-slackbot/blob/master/osmslackbot/patterns.yml - Specifies the text to look for.

- responses.yml -  https://github.com/osmlab/osm-slackbot/blob/master/osmslackbot/responses.yml - Templates for the bot's reponse.

- broker/base.py - https://github.com/osmlab/osm-slackbot/blob/master/osmslackbot/broker/base.py - Contains logic for detecting and responding to pattern matches.

- mapping/base.py - https://github.com/osmlab/osm-slackbot/blob/master/osmslackbot/mapping/base.py - Flattens and transforms raw Slack RTM JSON dicts for rendering the templates.

- enumerations.py - https://github.com/osmlab/osm-slackbot/blob/master/osmslackbot/enumerations.py - URL templates referenced in broker/base.py and mapping/base.py.
