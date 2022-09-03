# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import asyncio
from bleak import BleakScanner
import flask





class MajigfirealarmPlugin(
		octoprint.plugin.StartupPlugin,
		octoprint.plugin.TemplatePlugin,
		octoprint.plugin.SimpleApiPlugin,
		octoprint.plugin.AssetPlugin
):
		def detection_callback(self, device, advertisement_data):
			#print(device.address, "RSSI:", device.rssi, advertisement_data)
			if advertisement_data.local_name == "MAJIG":
				print(advertisement_data.manufacturer_data.get(741))
				self.status = advertisement_data.manufacturer_data.get(741)
				if self.status == "FIRE":
					self._logger.info("Attempting to emergency stop printer")
					#self._printer.commands(self.emergencyGCODE, force=True)
					self._printer.commands("M112", force=True)
				#print(advertisement_data.local_name)

		async def main(self):
			scanner = BleakScanner(self.detection_callback)
			#await scanner.start()
			#await asyncio.sleep(5.0)
			#await scanner.stop()
			await scanner.start()
			await asyncio.sleep(2.0)

		def on_after_startup(self):
				self._logger.info("Hello from Majig Firealarm Plugin!")
				self.searching = False
				self.status = 'empty'
				# Thank you too: https://github.com/Sebclem/OctoPrint-SimpleEmergencyStop
				self.emergencyGCODE = "M112"

		def get_template_configs(self):
				return [
						dict(type="sidebar", icon="fire", custom_bindings=True, template="majigfirealarm_sidebar.jinja2")
				]
						
		def on_api_get(self, request):
				try:
					loop = asyncio.get_running_loop()
				except RuntimeError:  # 'RuntimeError: There is no current event loop...'
					loop = None

				if loop and loop.is_running() and not self.searching:
					print('Async event loop already running. Adding coroutine to the event loop.')
					tsk = loop.create_task(self.main())
					self.searching=True
					# ^-- https://docs.python.org/3/library/asyncio-task.html#task-object
					# Optionally, a callback function can be executed when the coroutine completes
					tsk.add_done_callback(
						lambda t: print(f'Task done with result={t.result()}  << return val of main()'))

				return flask.jsonify(status=self.status)


		def get_assets(self):
				return dict(
						js=['js/majigfirealarm.js']
				)


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Majigfirealarm Plugin"


# Set the Python version your plugin is compatible with below. Recommended is Python 3 only for all new plugins.
# OctoPrint 1.4.0 - 1.7.x run under both Python 3 and the end-of-life Python 2.
# OctoPrint 1.8.0 onwards only supports Python 3.
__plugin_pythoncompat__ = ">=3,<4"	# Only Python 3
__plugin_implementation__ = MajigfirealarmPlugin()
