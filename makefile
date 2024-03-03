install-retime:
	cp retime.py /usr/local/bin/retime

install-timer:
	mkdir -p ~/.config/systemd/user
	sudo cp retime.timer retime.service ~/.config/systemd/user/
	systemctl --user enable --now retime.timer

uninstall-timer:
	rm -rf ~/.config/systemd/user/retime.timer
	rm -rf ~/.config/systemd/user/retime.service

uninstall-retime:
	rm -rf /usr/local/bin/retime
