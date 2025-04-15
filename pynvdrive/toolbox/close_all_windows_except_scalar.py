from pynvdrive import NVDriveCommandError
import pynvdrive

from ..client import Client
from .get_layouts_list import get_layouts_list
from .get_windows_list import get_windows_list
from pynvdrive.commands.marker import GetWindowTraces
from pynvdrive.commands.graphics import SetLayout, CloseWindow

from pynvdrive.formats.process import processes_scalar


def close_all_windows_except_scalar(client: pynvdrive.Client = None):
	"""
	Close all windows except scalar ones
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	list_layouts = get_layouts_list(client=client)

	for layout in list_layouts:
		# Select layout
		try:
			cmd = SetLayout(layout_name=layout)
			client.send_command(cmd)
		except NVDriveCommandError as e:
			print('error SetLayout ', e)

		list_windows = get_windows_list(layout, client=client)
		for window in list_windows:
			# print('Layout : {}, window : {}'.format(layout, window))
			list_traces = []
			try:
				cmd = GetWindowTraces(window_name=window)
				client.send_command(cmd)
				list_traces = cmd.value
			except NVDriveCommandError as e:
				print('error GetWindowTraces ', e)

			is_scalar = False
			for trace in list_traces:
				if trace.process_id in processes_scalar:
					# print('{} is a scalar process'.format(trace.process_id))
					is_scalar = True
					break

			if not is_scalar:
				try:
					cmd = CloseWindow(layout_name=layout, window_name=window)
					client.send_command(cmd)
				except NVDriveCommandError as e:
					print('error CloseWindow ', e)
