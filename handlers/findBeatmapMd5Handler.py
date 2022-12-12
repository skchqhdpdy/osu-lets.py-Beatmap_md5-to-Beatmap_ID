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


MODULE_NAME = "findBeatmapMd5Handler"
class handler(requestsManager.asyncRequestHandler):
	"""
	Handler for /find-beatmap-md5

	"""
	@tornado.web.asynchronous
	@tornado.gen.engine
	@sentry.captureTornado
	def asyncGet(self):
		statusCode = 400
		data = {"message": "unknown error"}
		try:
			# Check arguments
			if not requestsManager.checkArguments(self.request.arguments, ["md5"]):
				raise exceptions.invalidArgumentsException(MODULE_NAME)

			beatmapMD5 = self.get_argument("md5")
			getId = glob.db.fetch("SELECT beatmap_id FROM beatmaps WHERE beatmap_md5 = %s", [beatmapMD5])
			log.info("Requested md5 for beatmap {}, to {}".format(beatmapMD5, getId))
		
		except Exception as e:
			log.error(e)

		finally:
			self.write(getId)
