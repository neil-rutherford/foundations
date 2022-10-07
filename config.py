from subnet import do_the_thing, find_wildcard

def configure_router(hostname, password, bridge_ip, bridge_cidr, node_ip, node_cidr):
    bridge_data = do_the_thing(str(bridge_ip), int(bridge_cidr))
    node_data = do_the_thing(str(node_ip), int(node_cidr))

    node_dgw_ip = node_data['default_gateway']
    node_subnet_mask = node_data['subnet_mask']

    if hostname[-1] == '1':
        bridge_dgw_ip = bridge_data['default_gateway']
    else:
        bridge_dgw_ip = bridge_data['host_range'][1]
    bridge_subnet_mask = bridge_data['subnet_mask']

    bridge_network_id = bridge_data['network_id']
    bridge_wildcard = find_wildcard(bridge_data['subnet_mask'])

    node_network_id = node_data['network_id']
    node_wildcard = find_wildcard(node_data['subnet_mask'])

    with open("{}_pyconfig.txt".format(str(hostname)), 'a') as f:
        f.write("!\nversion 15.1\nno service timestamps log datetime msec\nno service timestamps debug datetime msec\nno service password-encryption\n!\n")
        f.write("hostname {}\n!\n!\n!\n".format(str(hostname)))
        f.write("enable password {}\n!\n!\n!\n!\n!\n!\n".format(str(password)))
        f.write("ip cef\nno ipv6 cef\n!\n!\n!\n!\n")
        f.write("license udi pid CISCO2911/K9 sn FTX1524XQ8J-\n!\n!\n!\n!\n!\n!\n!\n!\n!\n")
        f.write("no ip domain-lookup\n!\n!\n")
        f.write("spanning-tree mode pvst\n!\n!\n!\n!\n!\n!\n")
        
        f.write("interface GigabitEthernet0/0\n ip address {} {}\n duplex auto\n speed auto\n!\n".format(node_dgw_ip, node_subnet_mask))
        f.write("interface GigabitEthernet0/1\n ip address {} {}\n duplex auto\n speed auth\n!\n".format(bridge_dgw_ip, bridge_subnet_mask))
        f.write("interface GigabitEthernet0/2\n no ip address\n duplex auto\n speed auto\n shutdown\n!\n")
        f.write("interface Vlan1\n no ip address\n shutdown\n!\n")
        f.write("router ospf 100\n log-adjacency-changes\n network {} {} area 0\n network {} {} area 0\n!\n".format(bridge_network_id, bridge_wildcard, node_network_id, node_wildcard))
        
        f.write("ip classless\n!\n")
        f.write("ip flow-export version 9\n!\n!\n!\n")
        f.write("banner login *Unauthorized access prohibited.*\nbanner motd *This router was configured by me.*\n!\n!\n!\n!\n")
        f.write("line con 0\n exec-timeout 0 0\n password {}\n logging synchronous\n login\n!\n".format(str(password)))
        f.write("line aux 0\n!\n")
        f.write("line vty 0 4\n password {}\nlogin\n!\n!\n!\nend\n".format(str(password)))
    print("Router configuration file generated.")