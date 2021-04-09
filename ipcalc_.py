import ipaddress
import sys

class ip_tool:
        @staticmethod
        def ipstr_2_int(address: str):
                return int(ipaddress.IPv4Address(address))
        
        @staticmethod
        def int_2_ipstr(address: int):
                return str(ipaddress.IPv4Address(address))

        @staticmethod
        def ipstr_2_intarr(address: str)-> list:
                return list(map(int, address.split(".")))        

        @staticmethod
        def bin_format(ip_int_array:list)-> str:
                return '{0:08b}.{1:08b}.{2:08b}.{3:08b}'.format(*ip_int_array)

        @staticmethod
        def print_result(result:dict)-> None:
                print("===================== Subnet Results =====================")
                print(f"Subnet Representation : {result['Subnet Representation']}"       )
                print(f"# of Host             : {result['# of Host']}"                   ) 
                print(f"Network Address       : {result['Network Address']}"             )
                print(f"Broadcast Address     : {result['Broadcast Address']}"           )
                print(f"Availible Allocate IP : {result['Availible Allocate IP']}"       )
                print(f"Gateway               : {result['Gateway']}"                     )
                print(f"Host ID               : {result['Host ID']}"                     )
                print(f"so this IP is the {result['Host Number']} th IP in this network" )
                print("=========================================================="       )
        

if __name__ == "__main__":
        ip = sys.argv[1]        
        ip_arr = ip_tool.ipstr_2_intarr(ip)
        
        mask = sys.argv[2]
        mask_arr = ip_tool.ipstr_2_intarr(mask)
        total_host = ip_tool.bin_format(mask_arr).count('0')

        network_addr =  '.'.join([ str(i & j) for i, j in zip(ip_arr, mask_arr)])
        host_id      =  '.'.join([ str(i & ~j) for i, j in zip(ip_arr, mask_arr)])
        host_num     =  ip_tool.ipstr_2_int(host_id)
        broadcast_ip =  ip_tool.int_2_ipstr( ip_tool.ipstr_2_int(ip) | (2**total_host-1) )


        result = {}
        result["Subnet Representation"] = '{}.{}.{}.{} / {}'.format(*ip_arr, total_host)
        result["# of Host"] = 2 ** total_host - 2
        result["Network Address"] = network_addr
        result["Broadcast Address"] = broadcast_ip
        result["Availible Allocate IP"] = "{} ~ {}".format(ip_tool.int_2_ipstr( ip_tool.ipstr_2_int(network_addr)+1),
                                                           ip_tool.int_2_ipstr( ip_tool.ipstr_2_int(broadcast_ip)-1))
        result["Gateway"] = ip_tool.int_2_ipstr( ip_tool.ipstr_2_int(network_addr)+1)
        result["Host ID"] = host_id
        result["Host Number"] = host_num
        ip_tool.print_result(result)
        
        
        