import zsh
import json
from powerline.shell import ShellPowerline


def get_var_config(var):
	try:
		return dict(((k, json.loads(v)) for k, v in zsh.getvalue(var).items()))
	except:
		return None


class Args(object):
	ext = ['shell']
	renderer_module = 'zsh_prompt'

	@property
	def last_exit_code(self):
		return zsh.last_exit_code()

	@property
	def last_pipe_status(self):
		return zsh.pipestatus()

	@property
	def config(self):
		return get_var_config('POWERLINE_CONFIG')

	@property
	def theme_option(self):
		return get_var_config('POWERLINE_THEME_CONFIG')


class Prompt(object):
	__slots__ = ('render', 'side', 'savedpsvar', 'savedps')

	def __init__(self, powerline, side, savedpsvar=None, savedps=None):
		self.render = powerline.renderer.render
		self.side = side
		self.savedpsvar = savedpsvar
		self.savedps = savedps

	def __str__(self):
		return self.render(width=zsh.columns(), side=self.side).encode('utf-8')

	def __del__(self):
		if self.savedps:
			zsh.setvalue(self.savedpsvar, self.savedps)


def set_prompt(powerline, psvar, side):
	savedps = zsh.getvalue(psvar)
	zpyvar = 'ZPYTHON_POWERLINE_' + psvar
	prompt = Prompt(powerline, side, psvar, savedps)
	zsh.set_special_string(zpyvar, prompt)
	zsh.setvalue(psvar, '${' + zpyvar + '}')


def setup():
	powerline = ShellPowerline(Args())
	set_prompt(powerline, 'PS1', 'left')
	set_prompt(powerline, 'RPS1', 'right')
