from slackclient import SlackClient
import re


def oxfordize(strings):
    """Given a list of strings, formats them correctly given the length of the
    list. For example:
        oxfordize(['A'])  =>  'A'
        oxfordize(['A', 'B'])  =>  'A and B'
        oxfordize(['A', 'B', 'C'])  =>  'A, B, and C'
    """

    if len(strings) == 0:
        return ''
    elif len(strings) == 1:
        return strings[0]
    elif len(strings) == 2:
        return '%s and %s' % (strings[0], strings[1])
    else:
        return '%s, and %s' % (', '.join(strings[:-1]), strings[-1])


class SlackHelper(object):
    """A place to store all the Slack stuff"""

    def __init__(self, token):
        self.token = token
        self.client = SlackClient(token)

    # TODO do we need this? (maybe once we start storing data)
    def get_user_info(self, user_id):
        """Get info about the given user"""

        return self.client.api_call("users.info",
                                    user=user_id,
                                    token=self.token)

    def post_message(self, text):
        """ Convenience method to make it easier to post to slack. Might
            generalize even more e.g. pass in channel printing so we can see
            the output - this can be taken out once everything's working
        """

        import pprint
        pprint.pprint(self.client.api_call("chat.postMessage",
                                           channel="CC32SU9DE",
                                           text=text,
                                           username="cupcake"))

    def process_slash_command(self, requesting_user, command):
        """Process the incoming command, and either return an error message
           or the results of the command."""

        ERROR_RESPONSE_BODY = {
            "text": "Sorry, I didn't understand that. Please use the format `/cupcake to <@user(s)> for <doing something great>`.",
            "response_type": "ephemeral",
        }

        # check for the keyword "for" so we know it's safe to split on it
        if " for " not in command:
            return ERROR_RESPONSE_BODY
        users, reason = command.split(" for ")

        # make sure there are recipents
        recipients = re.findall(r"<@U\S*>", users)
        if not recipients:
            return ERROR_RESPONSE_BODY

        # if everything seems in order, return a valid response
        return {
            "text":
                "<@{user_id}> gave a cupcake to {users} for {reason}".format(
                    user_id=requesting_user,
                    users=oxfordize(recipients),
                    reason=reason),
            "response_type": "in_channel",
            "attachments": [{"text": "Thanks for giving cupcakes!"}],
        }


#############

# for reference, this is what comes through from getting user info:
# {u'headers': {u'Access-Control-Allow-Origin': u'*',
#               u'Cache-Control': u'private, no-cache, no-store, must-revalidate',
#               u'Connection': u'keep-alive',
#               u'Content-Encoding': u'gzip',
#               u'Content-Length': u'537',
#               u'Content-Type': u'application/json; charset=utf-8',
#               u'Date': u'Wed, 08 Aug 2018 22:04:35 GMT',
#               u'Expires': u'Mon, 26 Jul 1997 05:00:00 GMT',
#               u'Pragma': u'no-cache',
#               u'Referrer-Policy': u'no-referrer',
#               u'Server': u'Apache',
#               u'Strict-Transport-Security': u'max-age=31536000; includeSubDomains; preload',
#               u'Vary': u'Accept-Encoding',
#               u'Via': u'1.1 02400e961e7094d2c4fff83bc2205fc3.cloudfront.net (CloudFront)',
#               u'X-Accepted-OAuth-Scopes': u'users:read,read',
#               u'X-Amz-Cf-Id': u'gM-71-q7AInHmkzcRKsVS3fdzULBW-kUq-XWOzT2So9DPcaC2-Aq2A==',
#               u'X-Cache': u'Miss from cloudfront',
#               u'X-Content-Type-Options': u'nosniff',
#               u'X-OAuth-Scopes': u'identify,bot:basic',
#               u'X-Slack-Backend': u'h',
#               u'X-Slack-Req-Id': u'ebd012d6-929b-4b09-a0a0-5fe83817fdfa',
#               u'X-Via': u'haproxy-www-rb8i',
#               u'X-XSS-Protection': u'0'},
#  u'ok': True,
#  u'user': {u'color': u'9f69e7',
#            u'deleted': False,
#            u'id': u'UC37K8KUZ',
#            u'is_admin': True,
#            u'is_app_user': False,
#            u'is_bot': False,
#            u'is_owner': True,
#            u'is_primary_owner': True,
#            u'is_restricted': False,
#            u'is_ultra_restricted': False,
#            u'name': u'lobsterkatie',
#            u'profile': {u'avatar_hash': u'e0e5d770bb2d',
#                         u'display_name': u'Katie Byers',
#                         u'display_name_normalized': u'Katie Byers',
#                         u'email': u'lobsterkatie@gmail.com',
#                         u'first_name': u'Katie',
#                         u'image_1024': u'https://avatars.slack-edge.com/2018-08-07/412050892337_e0e5d770bb2d55aca2bd_1024.jpg',
#                         u'image_192': u'https://avatars.slack-edge.com/2018-08-07/412050892337_e0e5d770bb2d55aca2bd_192.jpg',
#                         u'image_24': u'https://avatars.slack-edge.com/2018-08-07/412050892337_e0e5d770bb2d55aca2bd_24.jpg',
#                         u'image_32': u'https://avatars.slack-edge.com/2018-08-07/412050892337_e0e5d770bb2d55aca2bd_32.jpg',
#                         u'image_48': u'https://avatars.slack-edge.com/2018-08-07/412050892337_e0e5d770bb2d55aca2bd_48.jpg',
#                         u'image_512': u'https://avatars.slack-edge.com/2018-08-07/412050892337_e0e5d770bb2d55aca2bd_512.jpg',
#                         u'image_72': u'https://avatars.slack-edge.com/2018-08-07/412050892337_e0e5d770bb2d55aca2bd_72.jpg',
#                         u'image_original': u'https://avatars.slack-edge.com/2018-08-07/412050892337_e0e5d770bb2d55aca2bd_original.jpg',
#                         u'is_custom_image': True,
#                         u'last_name': u'Byers',
#                         u'phone': u'',
#                         u'real_name': u'Katie Byers',
#                         u'real_name_normalized': u'Katie Byers',
#                         u'skype': u'',
#                         u'status_emoji': u'',
#                         u'status_expiration': 0,
#                         u'status_text': u'',
#                         u'status_text_canonical': u'',
#                         u'team': u'TC32SU5A4',
#                         u'title': u''},
#            u'real_name': u'Katie Byers',
#            u'team_id': u'TC32SU5A4',
#            u'tz': u'America/Los_Angeles',
#            u'tz_label': u'Pacific Daylight Time',
#            u'tz_offset': -25200,
#            u'updated': 1533686480}}
