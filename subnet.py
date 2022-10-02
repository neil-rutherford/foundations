def bin2dec(binary):
    # Converts binary to decimal
    binary_string = str(binary)
    binary_list = [x for x in binary_string]
    listy = [128, 64, 32, 16, 8, 4, 2, 1]
    decimal = 0
    for x in range(0, len(binary_list)):
        if binary_list[x] == '1':
            decimal += listy[x]
    return decimal


def dec2bin(decimal):
    # Converts decimal to binary
    decimal_integer = int(decimal)
    listy = [128, 64, 32, 16, 8, 4, 2, 1]
    binary = ''
    for x in range(0, 8):
        if decimal_integer - listy[x] >= 0:
            decimal_integer -= int(listy[x])
            binary += '1'
        else:
            binary += '0'
    return binary


def ip2bin(ip_address):
    # Converts dotted decimal to dotted binary
    ip_string = str(ip_address)
    ip_list = ip_string.split('.')
    binary = ''
    for x in ip_list:
        binary += dec2bin(x)
        binary += '.'
    return binary[:-1]


def bin2ip(binary):
    # Converts dotted binary to dotted decimal
    binary_string = str(binary)
    binary_list = binary_string.split('.')
    ip_address = ''
    for x in binary_list:
        ip_address += str(bin2dec(x))
        ip_address += '.'
    return ip_address[:-1]


def cidr2bin(cidr):
    cidr_integer = int(cidr)
    binary_string = ''
    binary_string += (cidr_integer * '1')
    binary_string += ((32 - cidr_integer) * '0')
    binary_list = [x for x in binary_string]
    binary_list.insert(8, '.')
    binary_list.insert(17, '.')
    binary_list.insert(26, '.')
    binary = ''.join(binary_list)
    return binary


def find_network_id(ip_bin, sm_bin):
    ip_list = [x for x in str(ip_bin)]
    sm_list = [x for x in str(sm_bin)]
    network_id = ''
    for x in range(0, len(ip_list)):
        if ip_list[x] == '.':
            network_id += '.'
        elif ip_list[x] == '1' and sm_list[x] == '1':
            network_id += '1'
        else:
            network_id += '0'
    return network_id


def find_broadcast_id(network_id_bin, cidr):
    cidr_integer = int(cidr)
    remainder = 32 - cidr_integer
    network_id_list = [x for x in str(network_id_bin)]
    for x in range(0, remainder):
        network_id_list.pop()
    broadcast_id = ''.join(network_id_list)
    broadcast_id += ('1' * remainder)
    return broadcast_id


def find_host_range(network_id_bin, broadcast_id_bin):
    network_id = bin2ip(str(network_id_bin))
    broadcast_id = bin2ip(str(broadcast_id_bin))
    
    network_id_octets = network_id.split('.')
    for i in range(0, len(network_id_octets)):
        network_id_octets[i] = int(network_id_octets[i])
    network_id_octets[-1] += 1
    for i in range(0, len(network_id_octets)):
        network_id_octets[i] = str(network_id_octets[i])

    broadcast_id_octets = broadcast_id.split('.')
    for i in range(0, len(broadcast_id_octets)):
        broadcast_id_octets[i] = int(broadcast_id_octets[i])
    broadcast_id_octets[-1] -= 1
    for i in range(0, len(broadcast_id_octets)):
        broadcast_id_octets[i] = str(broadcast_id_octets[i])

    first = '.'.join(network_id_octets)
    last = '.'.join(broadcast_id_octets)
    return [first, last]


def do_the_thing(ip_address, cidr):

    # Step 1: Define IP address and CIDR
    ip_address = str(ip_address)
    cidr = int(cidr)

    # Step 2: Convert IP and CIDR to binary
    ip_bin = ip2bin(ip_address)
    sm_bin = cidr2bin(cidr)

    # Step 3: AND the binary IP and SM.
    network_id_bin = find_network_id(ip_bin, sm_bin)

    # Step 4 and 5: Find the broadcast ID.
    broadcast_id_bin = find_broadcast_id(network_id_bin, cidr)

    # Step 6: Find Host ID range.
    hr = find_host_range(network_id_bin, broadcast_id_bin)

    # Step 7: Find default gateway.

    # Step 8: Find increment and number of hosts
    remainder = 32 - cidr
    increment = pow(2, remainder)

    return {
        'ip_address': ip_address,
        'cidr': cidr,
        'network_id': bin2ip(network_id_bin),
        'broadcast_id': bin2ip(broadcast_id_bin),
        'host_range': [hr[0], hr[1]],
        'default_gateway': hr[0],
        'increment': increment,
        'hosts': increment - 2,
        'subnets': int(256/increment)
    }