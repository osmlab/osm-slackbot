import json
import re

import defusedxml.ElementTree as et

from geowatchutil.broker.base import GeoWatchBroker
from geowatchutil.codec.geowatch_codec_slack import GeoWatchCodecSlack

from osmslackbot.enumerations import *  # noqa
from osmslackbot.mapping.base import *  # noqa
from osmslackbot.utils import load_patterns


class OSMSlackBotBroker(GeoWatchBroker):
    """
    Broker for OpenStreetMap Slack bot
    """
    _user_id = None  # Dervied from consumer authtoken
    _user_name = None  # Dervied from consumer authtoken
    patterns = None
    _ignore_errors = True

    def _make_request(self, url, params=None, data=None, cookie=None, contentType=None):
        """
        Prepares a request from a url, params, and optionally authentication.
        """

        import urllib
        import urllib2

        if params:
            url = url + '?' + urllib.urlencode(params)

        req = urllib2.Request(url, data=data)

        if cookie:
            req.add_header('Cookie', cookie)

        if contentType:
            req.add_header('Content-type', contentType)
        else:
            if data:
                req.add_header('Content-type', 'text/xml')

        return urllib2.urlopen(req)

    def _pre(self):
        pass

    def _post(self, messages=None):
        for m in messages:
            msgtype = m[u'type']
            if msgtype == u'hello':  # slack always open up connection with hello message
                pass
            elif msgtype == u'message':
                msgsubtype = m.get(u'subtype', None)
                if msgsubtype == u'bot_message':
                    # username = m[u'username']
                    # text = m[u'text']
                    pass
                elif msgsubtype == u'message_deleted':
                    pass
                else:
                    # user = m[u'user']
                    text = m[u'text']
                    channel = m[u'channel']

                    match_question = None
                    match_value = None
                    for question in self.patterns:
                        for pattern in self.patterns[question]:
                            match_value = re.search(pattern, text, re.M | re.I)
                            if match_value:
                                match_question = question
                                break
                        if match_value:
                            break

                    if match_value:
                        outgoing = None
                        print "Match Question: ", match_question
                        print "Match Value: ", match_value
                        try:
                            if match_question == "project":
                                ctx = self._request_project(match_value.group("project"), URL_PROJECT_TASKS)
                                t = self.templates.get('SLACK_MESSAGE_TEMPLATE_PROJECT', None)
                                if t:
                                    outgoing = self.codec_slack.render(ctx, t=t)
                            elif match_question == "changeset":
                                ctx = self._request_changeset(match_value.group("changeset"), URL_CHANGESET_API)
                                t = self.templates.get('SLACK_MESSAGE_TEMPLATE_CHANGESET', None)
                                if t:
                                    outgoing = self.codec_slack.render(ctx, t=t)
                            elif match_question == "node":
                                ctx = self._request_node(match_value.group("node"), URL_NODE_API)
                                t = self.templates.get('SLACK_MESSAGE_TEMPLATE_NODE', None)
                                if t:
                                    outgoing = self.codec_slack.render(ctx, t=t)
                            elif match_question == "way":
                                ctx = self._request_way(match_value.group("way"), URL_WAY_API)
                                t = self.templates.get('SLACK_MESSAGE_TEMPLATE_WAY', None)
                                if t:
                                    outgoing = self.codec_slack.render(ctx, t=t)
                            elif match_question == "relation":
                                ctx = self._request_relation(match_value.group("relation"), URL_RELATION_API)
                                t = self.templates.get('SLACK_MESSAGE_TEMPLATE_RELATION', None)
                                if t:
                                    outgoing = self.codec_slack.render(ctx, t=t)
                        except:
                            print "Error processing match for original text: ", text
                            if not self._ignore_errors:
                                raise

                        if outgoing:
                            print "Sending message ..."
                            print "+ Data = ", outgoing
                            self.duplex[0]._channel.send_message(outgoing, topic=channel)

    def _request_project(self, project, baseurl):

        url = baseurl.format(project=project)
        request = self._make_request(url, contentType="application/json")

        if request.getcode() != 200:
            raise Exception("Could not fetch json for project "+project+".")

        response = request.read()
        data = json.loads(response)

        counter = {
            "0": 0,
            "1": 0,
            "2": 0,
            "3": 0,
            "-1": 0
        }

        for f in data[u'features']:
            p = f[u'properties']
            state = str(p.get(u'state', None))
            counter[state] = counter[state] + 1

        return GeoWatchMappingProject().forward(project=int(project), counter=counter)

    def _request_changeset(self, changesetID, baseurl):

        url = baseurl.format(changeset=changesetID)
        request = self._make_request(url, contentType="text/xml")

        if request.getcode() != 200:
            raise Exception("Could not fetch xml for changeset "+changesetID+".")

        response = request.read()
        root = et.fromstring(response)

        kwargs = {
            'id': changesetID
        }
        for changeset in root.findall('changeset'):
            kwargs['user'] = changeset.get('user')
            kwargs['closed_at'] = changeset.get('closed_at')
            for tag in changeset.findall('tag'):
                kwargs[tag.get('k')] = tag.get('v', '')

        return GeoWatchMappingChangeset().forward(**kwargs)

    def _request_node(self, nodeID, baseurl):

        url = baseurl.format(node=nodeID)
        request = self._make_request(url, contentType="text/xml")

        if request.getcode() != 200:
            raise Exception("Could not fetch xml for node "+nodeID+".")

        response = request.read()
        root = et.fromstring(response)

        kwargs = {
            'id': nodeID
        }
        for node in root.findall('node'):
            kwargs['user'] = node.get('user')
            kwargs['timestamp'] = node.get('timestamp')
            kwargs['changeset'] = node.get('changeset')
            kwargs['lon'] = node.get('lon')
            kwargs['lat'] = node.get('lat')
            for tag in node.findall('tag'):
                kwargs[tag.get('k')] = tag.get('v', '')

        return GeoWatchMappingNode().forward(**kwargs)

    def _request_way(self, wayID, baseurl):

        url = baseurl.format(way=wayID)
        request = self._make_request(url, contentType="text/xml")

        if request.getcode() != 200:
            raise Exception("Could not fetch xml for way "+wayID+".")

        response = request.read()
        root = et.fromstring(response)

        kwargs = {
            'id': wayID
        }
        for way in root.findall('way'):
            kwargs['user'] = way.get('user')
            kwargs['timestamp'] = way.get('timestamp')
            kwargs['changeset'] = way.get('changeset')
            kwargs['visible'] = way.get('visible')
            for tag in way.findall('tag'):
                kwargs[tag.get('k')] = tag.get('v', '')
            kwargs['nodes'] = [node.get('ref', None) for node in way.findall('nd')]

        return GeoWatchMappingWay().forward(**kwargs)

    def _request_relation(self, relationID, baseurl):

        url = baseurl.format(relation=relationID)
        request = self._make_request(url, contentType="text/xml")

        if request.getcode() != 200:
            raise Exception("Could not fetch xml for way "+wayID+".")

        response = request.read()
        root = et.fromstring(response)

        kwargs = {
            'id': relationID
        }
        for relation in root.findall('relation'):
            kwargs['user'] = relation.get('user')
            kwargs['timestamp'] = relation.get('timestamp')
            kwargs['changeset'] = relation.get('changeset')
            for tag in relation.findall('tag'):
                kwargs[tag.get('k')] = tag.get('v', '')
            kwargs['ways'] = [member.get('ref', None) for member in relation.findall('member') if member.get('type', '') == 'way']

        return GeoWatchMappingRelation().forward(**kwargs)

    def _req_user(self, messages):
        pass

    def __init__(self, name, description, templates=None, duplex=None, consumers=None, producers=None, stores_out=None, filter_metadata=None, sleep_period=5, count=1, timeout=5, deduplicate=False, ignore_errors=True, verbose=False):  # noqa
        super(OSMSlackBotBroker, self).__init__(
            name,
            description,
            duplex=duplex,
            consumers=consumers,
            producers=producers,
            stores_out=stores_out,
            count=count,
            threads=1,
            sleep_period=sleep_period,
            timeout=timeout,
            deduplicate=deduplicate,
            filter_metadata=filter_metadata,
            verbose=verbose)

        self.templates = templates  # loaded from templates.yml
        self._ignore_errors = ignore_errors
        self._user_id = self.duplex[0]._client._user_id
        self._user_name = self.duplex[0]._client._user_name

        self.codec_slack = GeoWatchCodecSlack()

        self.patterns = load_patterns()
