from sys import argv


def make_ip_str(ip_str):
	subsets = []
	for i in ip_str.split('.'):
		subsets.append(int(i))
	return (subsets[0] << 24) + (subsets[1] << 16) + (subsets[2] << 8) + (subsets[3])
	

def make_str_ip(int_ip):
	return f"{(int_ip >> 24) % 256}.{(int_ip >> 16) % 256}.{(int_ip >> 8) % 256}.{(int_ip) % 256}"


def get_network_id(packed_ip, cidr):
	"""Implements a bitwise AND with the integer IP agaisnt the hostbits (CIDR)"""
	hostbits = 32 - cidr
	return ((packed_ip >> hostbits) << hostbits)


def get_broadcast(network_id, cidr):
	"""To get the broadcast we need to bitwise OR the network_id with the network mask"""
	hostbits = 32 - cidr
	net_mask = int(('1' * hostbits), 2)
	return ((network_id | net_mask), int('1' * 32, 2) - net_mask)


def pretty_print(values):
	net_id, first_host, last_host, broadcast, subnet_mask, host_addresses = values
	print(f"""NetworkID: {net_id}\nFirst Host: {first_host}\nLast Host: {last_host}\nBroadcast: {broadcast}\nSubnet Mask: {subnet_mask}\nHost Addresses: {host_addresses}""")


def check_params(ip_cidr):
	if type(ip_cidr) == str and len(ip_cidr) != 2:
		if len(ip_cidr.split()) != 2:
			return False

	elif type(ip_cidr) == list and len(ip_cidr) != 2:
		return False

	
	elif ip_cidr[1].isdigit() == False:
		return False
	
	# Will check each value in our ip address to see if it fits in a valid range
	for i in ip_cidr[0].split('.'):
		if int(i) > 255:
			return False
	return True


if __name__ == "__main__":
	ip_cidr_input = argv[1:] # Allows us to take multiple values from the user
	if "/" in ip_cidr_input[0]:
		ip = ip_cidr_input[0].split('/')[0]
		cidr = int(ip_cidr_input[0].split('/')[1])
		ip_cidr_input = ip + " " + str(cidr)
	elif check_params(ip_cidr=ip_cidr_input) == False:
		print("Correct format:\nx.x.x.x/17 (OR) x.x.x.x 17")
		exit(f"Please pass only an IPv4 Address and your CIDR: python {__file__}")

	else:
		ip = ip_cidr_input[0]
		cidr = int(ip_cidr_input[1])


	print(f"The ip being subnetted is: {ip}/{cidr}\n")
	
	int_ip = make_ip_str(ip_str=ip) # Convert the string ip to an integer
	network_id = get_network_id(int_ip, cidr) # Pass our PACKEDIP (integer ip) & CIDR to get our network id
	broadcast_address, network_mask = get_broadcast(network_id, cidr)
	first_host = network_id + 1 # Add one to the integer to get the first host in a network
	last_host = broadcast_address - 1 # Subtract one from the broadcast to get the last_host (generally last host will be 254)
	host_addresses = last_host - first_host # Gets the available host addresses

	values = make_str_ip(network_id), make_str_ip(first_host), make_str_ip(last_host), make_str_ip(broadcast_address), make_str_ip(network_mask), host_addresses
	pretty_print(values)
