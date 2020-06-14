from blinker import Namespace
from flask import current_app

signals = Namespace()

cache_signals = signals.signal('cache_signals')
email_signals = signals.signal('email_signals')

login_signal_sender = 'login_signal_sender'
