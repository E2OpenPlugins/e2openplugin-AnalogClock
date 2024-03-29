from distutils.core import setup
import setup_translate

pkg = 'Extensions.AnalogClock'
setup(name='enigma2-plugin-extensions-analogclock',
	version='1.23',
	description='permanent analog clock on TV screen',
	packages=[pkg],
	package_dir={pkg: 'plugin'},
	package_data={pkg: ['png/*.png', 'locale/*/LC_MESSAGES/*.mo']},
	cmdclass=setup_translate.cmdclass, # for translation
	)
