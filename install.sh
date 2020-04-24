#! /bin/bash

installSoftware() {
    apt -qq -y install python3-flask python3-click python3-pycryptodome uwsgi-plugin-python3 python3-pip nginx git
}

installSimpleTextEncryption() {
    mkdir -p /var/log/uwsgi
    pip3 install -e git+https://github.com/sunshineplan/SimpleTextEncryption.git#egg=ste --src /var/www
}

setupsystemd() {
    cp -s /var/www/ste/ste.service /etc/systemd/system
    systemctl enable ste
    service ste start
}

writeLogrotateScrip() {
    if [ ! -f '/etc/logrotate.d/uwsgi' ]; then
        cat >/etc/logrotate.d/uwsgi <<-EOF
		/var/log/uwsgi/*.log {
		    copytruncate
		    rotate 12
		    compress
		    delaycompress
		    missingok
		    notifempty
		}
		EOF
    fi
}

setupNGINX() {
    cp -s /var/www/ste/SimpleTextEncryption.conf /etc/nginx/conf.d
    sed -i "s/\$domain/$domain/" /var/www/ste/SimpleTextEncryption.conf
    service nginx reload
}

main() {
    read -p 'Please enter domain:' domain
    installSoftware
    installSimpleTextEncryption
    setupsystemd
    writeLogrotateScrip
    setupNGINX
}

main
