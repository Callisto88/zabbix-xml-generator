import subprocess
import xml.etree.cElementTree as ET
from datetime import date

root = ET.Element("zabbix_export")

ET.SubElement(root, "version").text = "3.4"
ET.SubElement(root, "date").text = "2018-05-15T12:41:12Z"

# First step, lists vhosts on plesk
# https://support.plesk.com/hc/en-us/articles/213368629-How-to-get-a-list-of-Plesk-domains-and-their-IP-addresses
command = "MYSQL_PWD=`sudo cat /etc/psa/.psa.shadow` mysql -u admin -Dpsa -s -r -e\"SELECT dom.name FROM domains " \
          "dom LEFT JOIN DomainServices d ON (dom.id = d.dom_id AND d.type = 'web')\""
s = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True).stdout
vhostsList = s.read().splitlines()

groupArr = ['Vhost KreativMedia', 'Vhosts', 'Wordpress']
groups = ET.SubElement(root, "groups")

for groupName in groupArr:
    group = ET.SubElement(groups, "group")
    ET.SubElement(group, "name").text = groupName

hosts = ET.SubElement(root, "hosts")

for host in vhostsList:
    hostName = "www."+host
    hostTag = ET.SubElement(groups, "host")
    ET.SubElement(hostTag, "host").text = hostName
    ET.SubElement(hostTag, "name").text = hostName
    ET.SubElement(hostTag, "description")
    ET.SubElement(hostTag, "proxy")
    ET.SubElement(hostTag, "status")
    ET.SubElement(hostTag, "status").text = '0'
    ET.SubElement(hostTag, "ipmi_authtype").text = '-1'
    ET.SubElement(hostTag, "ipmi_privilege").text = '2'
    ET.SubElement(hostTag, "ipmi_username")
    ET.SubElement(hostTag, "ipmi_password")
    ET.SubElement(hostTag, "tls_connect").text = '1'
    ET.SubElement(hostTag, "tls_accept").text = '1'
    ET.SubElement(hostTag, "tls_issuer")
    ET.SubElement(hostTag, "tls_subject")
    ET.SubElement(hostTag, "tls_psk_identity")
    ET.SubElement(hostTag, "tls_psk")

    templates = ET.SubElement(hostTag, "templates")
    template = ET.SubElement(templates, "template")
    ET.SubElement(template, "name").text = "Template Web App"

    groups = ET.SubElement(hostTag, "groups")
    for groupName in groupArr:
        group = ET.SubElement(groups, "group")
        ET.SubElement(group, "name").text = groupName

    interfaces = ET.SubElement(hostTag, "interfaces")
    interface = ET.SubElement(interfaces, "interface")
    ET.SubElement(interface, "default").text = '1'
    ET.SubElement(interface, "type").text = '1'
    ET.SubElement(interface, "useip").text = '0'
    ET.SubElement(interface, "ip")
    ET.SubElement(interface, "dns").text = hostName
    ET.SubElement(interface, "port").text = '10050'
    ET.SubElement(interface, "bulk").text = '1'
    ET.SubElement(interface, "interface_ref").text = 'if1'

    apps = ET.SubElement(hostTag, "applications")
    app = ET.SubElement(apps, "application")
    ET.SubElement(app, "name").text = 'Agent'

    ET.SubElement(hostTag, "items")
    ET.SubElement(hostTag, "discovery_rules")
    ET.SubElement(hostTag, "httptests")
    ET.SubElement(hostTag, "macros")
    ET.SubElement(hostTag, "inventory")

tree = ET.ElementTree(root)


# write(file, encoding="us-ascii", xml_declaration=None, default_namespace=None, method="xml", *,
# short_empty_elements=True)
tree.write("filename.xml", "utf-8", xml_declaration=True, method="xml")