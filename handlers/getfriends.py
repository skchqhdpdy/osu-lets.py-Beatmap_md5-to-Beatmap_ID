import json
import sys
import traceback

import tornado.gen
import tornado.web
from raven.contrib.tornado import SentryMixin

from objects import beatmap
from common.constants import gameModes
from common.log import logUtils as log
from common.web import requestsManager
from constants import exceptions
from helpers import osuapiHelper
from objects import glob
from common.sentry import sentry

from common.ripple import userUtils


MODULE_NAME = "findBeatmapMd5Handler"
class handler(requestsManager.asyncRequestHandler):
	"""
	Handler for /web/osu-getfriends.php

	"""
	@tornado.web.asynchronous
	@tornado.gen.engine
	@sentry.captureTornado
	def asyncGet(self):
		statusCode = 400
		data = {"message": "unknown error"}
		try:
			# Check arguments
			if not requestsManager.checkArguments(self.request.arguments, ["u", "h"]):
				raise exceptions.invalidArgumentsException(MODULE_NAME)

			# Get user ID
			username = self.get_argument("u")
			userID = userUtils.getID(username)
			password = self.get_arguments("h")

			getFriends = []
			getFriends = glob.db.fetchAll("SELECT user2 FROM users_relationships WHERE user1 = %s", [userID])
			log.info("Requested getFriends by {}, id = {}".format(username, userID))
            
			result = []
			result = json.dumps(getFriends)
			log.info(result)

		except Exception as e:
			log.error(e)

		finally:
			self.write(result)
