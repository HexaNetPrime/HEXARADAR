#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Nmap Commands - Complete Collection
सभी Nmap कमांड्स एक ही फाइल में
Based on nmap.html - Complete Guide
"""

class NmapCommands:
    """All Nmap commands in one place"""
    
    def __init__(self):
        self.commands = self._get_all_commands()
    
    def _get_all_commands(self):
        """Return all Nmap commands organized by category"""
        
        return {
            # ========== TARGET SPECIFICATION ==========
            "target": {
                "--exclude": {
                    "desc": "Exclude specified hosts (comma-separated)",
                    "syntax": "--exclude <host1,host2>",
                    "example": "nmap 192.168.1.1/24 --exclude 192.168.1.5,192.168.1.10",
                    "what": "स्कैन से कुछ specific hosts को बाहर कर देता है।"
                },
                "--excludefile": {
                    "desc": "Exclude hosts from file (one host per line)",
                    "syntax": "--excludefile <file>",
                    "example": "nmap 192.168.1.1/24 --excludefile exclude.txt",
                    "what": "एक फ़ाइल से hosts को पढ़कर उन्हें स्कैन से बाहर करता है।"
                },
                "-iL": {
                    "desc": "Input from list of hosts file",
                    "syntax": "-iL <inputfile>",
                    "example": "nmap -iL targets.txt",
                    "what": "किसी फ़ाइल से target hosts की list पढ़ता है।"
                }
            },
            
            # ========== HOST DISCOVERY ==========
            "host_discovery": {
                "-sL": {
                    "desc": "List Scan - list targets without sending packets",
                    "syntax": "-sL <target>",
                    "example": "nmap -sL 192.168.1.1/24",
                    "what": "बिना कोई packet भेजे सिर्फ targets की लिस्ट बनाता है।"
                },
                "-sn": {
                    "desc": "Ping Scan - host discovery only, no port scan",
                    "syntax": "-sn <target>",
                    "example": "nmap -sn 192.168.1.1/24",
                    "what": "केवल यह पता करता है कि कौन से hosts alive हैं (port scan नहीं करता)।"
                },
                "-Pn": {
                    "desc": "Skip host discovery (treat all hosts as online)",
                    "syntax": "-Pn <target>",
                    "example": "nmap -Pn 192.168.1.1",
                    "what": "मानता है कि सभी hosts alive हैं – ping को skip करता है (firewall वाले hosts के लिए)।"
                },
                "-PS": {
                    "desc": "TCP SYN ping to specified ports",
                    "syntax": "-PS <portlist>",
                    "example": "nmap -PS22,80,443 192.168.1.1",
                    "what": "TCP SYN ping – specified ports पर SYN packet भेजता है।"
                },
                "-PA": {
                    "desc": "TCP ACK ping to specified ports",
                    "syntax": "-PA <portlist>",
                    "example": "nmap -PA22,80 192.168.1.1",
                    "what": "TCP ACK ping – ACK packet भेजता है।"
                },
                "-PU": {
                    "desc": "UDP ping to specified ports",
                    "syntax": "-PU <portlist>",
                    "example": "nmap -PU53 192.168.1.1",
                    "what": "UDP ping – UDP packet भेजता है।"
                },
                "-PY": {
                    "desc": "SCTP INIT ping",
                    "syntax": "-PY <portlist>",
                    "example": "nmap -PY22 192.168.1.1",
                    "what": "SCTP ping – SCTP INIT packet भेजता है।"
                },
                "-PO": {
                    "desc": "IP Protocol ping",
                    "syntax": "-PO <protocol list>",
                    "example": "nmap -PO1,2,4 192.168.1.1",
                    "what": "IP Protocol ping – specified IP प्रोटोकॉल के packets भेजता है।"
                },
                "--traceroute": {
                    "desc": "Trace hop path to each host",
                    "syntax": "--traceroute <target>",
                    "example": "nmap --traceroute 8.8.8.8",
                    "what": "Target तक पहुँचने के लिए network path (hops) दिखाता है।"
                },
                "--system-dns": {
                    "desc": "Use system DNS resolver",
                    "syntax": "--system-dns <target>",
                    "example": "nmap --system-dns google.com",
                    "what": "DNS resolution के लिए system के DNS resolver का उपयोग करता है।"
                }
            },
            
            # ========== SCAN TECHNIQUES ==========
            "scan_techniques": {
                "-sS": {
                    "desc": "TCP SYN Stealth Scan (half-open)",
                    "syntax": "-sS <target>",
                    "example": "nmap -sS 192.168.1.1",
                    "what": "TCP SYN Stealth Scan – आधा कनेक्शन बनाता है, तेज़ और कम दिखता है।"
                },
                "-sT": {
                    "desc": "TCP Connect Scan (full handshake)",
                    "syntax": "-sT <target>",
                    "example": "nmap -sT 192.168.1.1",
                    "what": "TCP Connect Scan – पूरा TCP handshake करता है।"
                },
                "-sA": {
                    "desc": "TCP ACK Scan (for firewall rules)",
                    "syntax": "-sA <target>",
                    "example": "nmap -sA 192.168.1.1",
                    "what": "TCP ACK Scan – firewall rules का पता लगाने के लिए ACK packets भेजता है।"
                },
                "-sW": {
                    "desc": "TCP Window Scan",
                    "syntax": "-sW <target>",
                    "example": "nmap -sW 192.168.1.1",
                    "what": "TCP Window Scan – window size के आधार पर port status बताता है।"
                },
                "-sM": {
                    "desc": "TCP Maimon Scan (FIN/ACK)",
                    "syntax": "-sM <target>",
                    "example": "nmap -sM 192.168.1.1",
                    "what": "TCP Maimon Scan – FIN/ACK packets भेजता है।"
                },
                "-sU": {
                    "desc": "UDP Scan (can be slow)",
                    "syntax": "-sU <target>",
                    "example": "nmap -sU 192.168.1.1",
                    "what": "UDP Scan – UDP ports के लिए स्कैन करता है (धीमा हो सकता है)।"
                },
                "-sN": {
                    "desc": "TCP Null Scan (no flags)",
                    "syntax": "-sN <target>",
                    "example": "nmap -sN 192.168.1.1",
                    "what": "TCP Null Scan – बिना किसी flag के packet भेजता है।"
                },
                "-sF": {
                    "desc": "TCP FIN Scan (FIN flag only)",
                    "syntax": "-sF <target>",
                    "example": "nmap -sF 192.168.1.1",
                    "what": "TCP FIN Scan – सिर्फ FIN flag से packet भेजता है।"
                },
                "-sX": {
                    "desc": "TCP Xmas Scan (FIN, PSH, URG)",
                    "syntax": "-sX <target>",
                    "example": "nmap -sX 192.168.1.1",
                    "what": "TCP Xmas Scan – FIN, PSH, URG flags सभी set होते हैं।"
                },
                "--scanflags": {
                    "desc": "Custom TCP scan flags",
                    "syntax": "--scanflags <flags>",
                    "example": "nmap --scanflags SYN,ACK 192.168.1.1",
                    "what": "कस्टम TCP flags के साथ स्कैन करता है।"
                },
                "-sZ": {
                    "desc": "SCTP Cookie Echo Scan",
                    "syntax": "-sZ <target>",
                    "example": "nmap -sZ 192.168.1.1",
                    "what": "SCTP Cookie Echo Scan (SCTP protocol के लिए)।"
                },
                "-sI": {
                    "desc": "Idle Scan (zombie host)",
                    "syntax": "-sI <zombie>",
                    "example": "nmap -sI 192.168.1.50:80 192.168.1.1",
                    "what": "Idle Scan – zombie host का उपयोग करके बिना पहचाने स्कैन करना।"
                },
                "-sO": {
                    "desc": "IP Protocol Scan",
                    "syntax": "-sO <target>",
                    "example": "nmap -sO 192.168.1.1",
                    "what": "IP Protocol Scan – कौन से IP प्रोटोकॉल (TCP, UDP, ICMP etc.) support हैं।"
                },
                "-b": {
                    "desc": "FTP Bounce Scan",
                    "syntax": "-b <ftp relay>",
                    "example": "nmap -b ftp://user:pass@server:21",
                    "what": "FTP Bounce Scan – FTP server के माध्यम से स्कैन करता है (पुरानी तकनीक)।"
                }
            },
            
            # ========== PORT SPECIFICATION ==========
            "port_spec": {
                "-p": {
                    "desc": "Specify ports (single, range, multiple)",
                    "syntax": "-p <port ranges>",
                    "example": "nmap -p22,80,443 192.168.1.1",
                    "what": "Specified ports को ही scan करता है। UDP/TCP अलग-अलग specify कर सकते हैं।"
                },
                "--exclude-ports": {
                    "desc": "Exclude ports from scan",
                    "syntax": "--exclude-ports <port ranges>",
                    "example": "nmap -p 1-1000 --exclude-ports 22,80",
                    "what": "कुछ ports को scan से बाहर कर देता है।"
                },
                "-F": {
                    "desc": "Fast scan (top 100 ports)",
                    "syntax": "-F <target>",
                    "example": "nmap -F 192.168.1.1",
                    "what": "Fast scan – सिर्फ 100 सबसे common ports scan करता है।"
                },
                "-r": {
                    "desc": "Scan ports sequentially (no randomize)",
                    "syntax": "-r <target>",
                    "example": "nmap -r 192.168.1.1",
                    "what": "Ports को random क्रम में नहीं, बल्कि sequential order में scan करता है।"
                },
                "--top-ports": {
                    "desc": "Scan most common N ports",
                    "syntax": "--top-ports <number>",
                    "example": "nmap --top-ports 10 192.168.1.1",
                    "what": "सबसे popular ‘number’ ports को scan करता है।"
                }
            },
            
            # ========== SERVICE/VERSION DETECTION ==========
            "service_version": {
                "-sV": {
                    "desc": "Service/Version detection",
                    "syntax": "-sV <target>",
                    "example": "nmap -sV 192.168.1.1",
                    "what": "Open ports पर चल रहे service और उनके version का पता लगाता है।"
                },
                "--version-intensity": {
                    "desc": "Set version detection intensity (0-9)",
                    "syntax": "--version-intensity <0-9>",
                    "example": "nmap -sV --version-intensity 5 192.168.1.1",
                    "what": "Version detection की गहराई (intensity) set करता है। 9 = सबसे गहरा।"
                },
                "--version-all": {
                    "desc": "Use every probe (intensity 9)",
                    "syntax": "--version-all <target>",
                    "example": "nmap -sV --version-all 192.168.1.1",
                    "what": "हर port पर हर probe भेजता है (intensity 9 के बराबर)।"
                },
                "--version-trace": {
                    "desc": "Show detailed version scan events",
                    "syntax": "--version-trace <target>",
                    "example": "nmap -sV --version-trace 192.168.1.1",
                    "what": "Version detection के दौरान भेजे गए packets का detailed log दिखाता है।"
                }
            },
            
            # ========== SCRIPT SCAN (NSE) ==========
            "script_scan": {
                "-sC": {
                    "desc": "Run default scripts (--script=default)",
                    "syntax": "-sC <target>",
                    "example": "nmap -sC 192.168.1.1",
                    "what": "Default scripts चलाता है (equivalent to --script=default)।"
                },
                "--script": {
                    "desc": "Run specified Lua scripts",
                    "syntax": "--script=<lua scripts>",
                    "example": "nmap --script=http-title,ssh-auth-methods 192.168.1.1",
                    "what": "Specified Lua scripts को चलाता है (category या नाम से)।"
                },
                "--script-args": {
                    "desc": "Pass arguments to scripts",
                    "syntax": "--script-args=<args>",
                    "example": "nmap --script=http-title --script-args http.useragent='Mozilla'",
                    "what": "Scripts को arguments pass करता है।"
                },
                "--script-args-file": {
                    "desc": "Load script arguments from file",
                    "syntax": "--script-args-file <filename>",
                    "example": "nmap --script-args-file args.txt",
                    "what": "किसी फ़ाइल से script arguments पढ़ता है।"
                },
                "--script-trace": {
                    "desc": "Show packets sent/received by scripts",
                    "syntax": "--script-trace <target>",
                    "example": "nmap --script-trace 192.168.1.1",
                    "what": "Script द्वारा भेजे/प्राप्त packets को दिखाता है।"
                },
                "--script-updatedb": {
                    "desc": "Update Nmap script database",
                    "syntax": "--script-updatedb",
                    "example": "nmap --script-updatedb",
                    "what": "Nmap script database को update करता है।"
                }
            },
            
            # ========== OS DETECTION ==========
            "os_detection": {
                "-O": {
                    "desc": "Enable OS detection",
                    "syntax": "-O <target>",
                    "example": "nmap -O 192.168.1.1",
                    "what": "Target के operating system का पता लगाने की कोशिश करता है।"
                },
                "--osscan-limit": {
                    "desc": "Limit OS detection to promising targets",
                    "syntax": "--osscan-limit <target>",
                    "example": "nmap -O --osscan-limit 192.168.1.1",
                    "what": "OS detection सिर्फ उन hosts पर करता है जो कम से कम एक open और एक closed port दिखाते हैं।"
                },
                "--osscan-guess": {
                    "desc": "Guess OS more aggressively",
                    "syntax": "--osscan-guess <target>",
                    "example": "nmap -O --osscan-guess 192.168.1.1",
                    "what": "अगर exact match न मिले तो भी ज़्यादा से ज़्यादा guess करता है।"
                }
            },
            
            # ========== TIMING AND PERFORMANCE ==========
            "timing_performance": {
                "-T0": {
                    "desc": "Paranoid (extremely slow, IDS evasion)",
                    "syntax": "-T0 <target>",
                    "example": "nmap -T0 192.168.1.1",
                    "what": "Paranoid – बहुत धीमा, IDS evasion के लिए।"
                },
                "-T1": {
                    "desc": "Sneaky (quite slow)",
                    "syntax": "-T1 <target>",
                    "example": "nmap -T1 192.168.1.1",
                    "what": "Sneaky – काफी धीमा, IDS evasion के लिए।"
                },
                "-T2": {
                    "desc": "Polite (slower, less bandwidth)",
                    "syntax": "-T2 <target>",
                    "example": "nmap -T2 192.168.1.1",
                    "what": "Polite – धीमा, कम bandwidth use करता है।"
                },
                "-T3": {
                    "desc": "Normal (default timing)",
                    "syntax": "-T3 <target>",
                    "example": "nmap -T3 192.168.1.1",
                    "what": "Normal – default timing template।"
                },
                "-T4": {
                    "desc": "Aggressive (fast, assumes good network)",
                    "syntax": "-T4 <target>",
                    "example": "nmap -T4 192.168.1.1",
                    "what": "Aggressive – तेज़, अच्छे network के लिए।"
                },
                "-T5": {
                    "desc": "Insane (very fast, may miss ports)",
                    "syntax": "-T5 <target>",
                    "example": "nmap -T5 192.168.1.1",
                    "what": "Insane – बहुत तेज़, कुछ ports miss हो सकते हैं।"
                },
                "--min-hostgroup": {
                    "desc": "Minimum parallel host group size",
                    "syntax": "--min-hostgroup <size>",
                    "example": "nmap --min-hostgroup 10 192.168.1.1/24",
                    "what": "Parallel में scan किए जाने वाले hosts के समूह का minimum size।"
                },
                "--max-hostgroup": {
                    "desc": "Maximum parallel host group size",
                    "syntax": "--max-hostgroup <size>",
                    "example": "nmap --max-hostgroup 50 192.168.1.1/24",
                    "what": "Parallel में scan किए जाने वाले hosts के समूह का maximum size।"
                },
                "--max-retries": {
                    "desc": "Maximum port scan retransmissions",
                    "syntax": "--max-retries <tries>",
                    "example": "nmap --max-retries 3 192.168.1.1",
                    "what": "Port scan के दौरान retries की अधिकतम संख्या।"
                },
                "--min-rtt-timeout": {
                    "desc": "Minimum RTT timeout value",
                    "syntax": "--min-rtt-timeout <time>",
                    "example": "nmap --min-rtt-timeout 100ms",
                    "what": "Round-trip time timeout को manually set करता है।"
                },
                "--max-rtt-timeout": {
                    "desc": "Maximum RTT timeout value",
                    "syntax": "--max-rtt-timeout <time>",
                    "example": "nmap --max-rtt-timeout 300ms",
                    "what": "Round-trip time timeout को manually set करता है।"
                },
                "--initial-rtt-timeout": {
                    "desc": "Initial RTT timeout value",
                    "syntax": "--initial-rtt-timeout <time>",
                    "example": "nmap --initial-rtt-timeout 100ms",
                    "what": "Initial round-trip time timeout set करता है।"
                },
                "--host-timeout": {
                    "desc": "Maximum time per host (then skip)",
                    "syntax": "--host-timeout <time>",
                    "example": "nmap --host-timeout 5m 192.168.1.1",
                    "what": "एक host पर scan करने का maximum समय, उसके बाद छोड़ देता है।"
                },
                "--scan-delay": {
                    "desc": "Delay between probes (IDS evasion)",
                    "syntax": "--scan-delay <time>",
                    "example": "nmap --scan-delay 1s 192.168.1.1",
                    "what": "दो probes के बीच delay डालता है (IDS evasion के लिए)।"
                },
                "--max-scan-delay": {
                    "desc": "Maximum delay between probes",
                    "syntax": "--max-scan-delay <time>",
                    "example": "nmap --max-scan-delay 1s 192.168.1.1",
                    "what": "Probes के बीच maximum delay।"
                },
                "--min-rate": {
                    "desc": "Minimum packet sending rate",
                    "syntax": "--min-rate <number>",
                    "example": "nmap --min-rate 100 192.168.1.1",
                    "what": "प्रति सेकंड packets की minimum दर।"
                },
                "--max-rate": {
                    "desc": "Maximum packet sending rate",
                    "syntax": "--max-rate <number>",
                    "example": "nmap --max-rate 500 192.168.1.1",
                    "what": "प्रति सेकंड packets की maximum दर।"
                }
            },
            
            # ========== FIREWALL/IDS EVASION ==========
            "firewall_evasion": {
                "-f": {
                    "desc": "Fragment packets (IDS bypass)",
                    "syntax": "-f <target>",
                    "example": "nmap -f 192.168.1.1",
                    "what": "Packet fragmentation – packets को छोटे fragments में तोड़ता है (IDS बाईपास)।"
                },
                "--mtu": {
                    "desc": "Set MTU for fragmentation",
                    "syntax": "--mtu <val>",
                    "example": "nmap --mtu 8 192.168.1.1",
                    "what": "MTU (Maximum Transmission Unit) को specified value पर set करता है।"
                },
                "-D": {
                    "desc": "Decoy scan (hide real IP)",
                    "syntax": "-D <decoy1,decoy2,ME>",
                    "example": "nmap -D 10.0.0.1,10.0.0.2,ME 192.168.1.1",
                    "what": "Decoy hosts – असली IP को छुपाने के लिए झूठे IPs भेजता है।"
                },
                "-S": {
                    "desc": "Spoof source IP address",
                    "syntax": "-S <IP_Address>",
                    "example": "nmap -S 10.0.0.5 192.168.1.1",
                    "what": "Source IP address spoof करता है।"
                },
                "-e": {
                    "desc": "Use specified network interface",
                    "syntax": "-e <iface>",
                    "example": "nmap -e eth0 192.168.1.1",
                    "what": "Specified network interface का उपयोग करता है।"
                },
                "-g": {
                    "desc": "Spoof source port number",
                    "syntax": "-g <portnum>",
                    "example": "nmap -g 53 192.168.1.1",
                    "what": "Source port number को fake करता है (e.g., port 53 DNS जैसा दिखाने के लिए)।"
                },
                "--source-port": {
                    "desc": "Spoof source port (alias for -g)",
                    "syntax": "--source-port <portnum>",
                    "example": "nmap --source-port 53 192.168.1.1",
                    "what": "Source port number को fake करता है।"
                },
                "--proxies": {
                    "desc": "Scan via proxy chain",
                    "syntax": "--proxies <url1,url2>",
                    "example": "nmap --proxies http://proxy1:8080,http://proxy2:8080 192.168.1.1",
                    "what": "HTTP/SOCKS4 proxy chain के माध्यम से स्कैन करता है।"
                },
                "--data": {
                    "desc": "Append raw binary data (hex) to packets",
                    "syntax": "--data <hex string>",
                    "example": "nmap --data 0xDEADBEEF 192.168.1.1",
                    "what": "Raw binary data (hex) को packets में जोड़ता है।"
                },
                "--data-string": {
                    "desc": "Append text string to packets",
                    "syntax": "--data-string <string>",
                    "example": "nmap --data-string 'HELLO' 192.168.1.1",
                    "what": "Text string को packets में शामिल करता है।"
                },
                "--data-length": {
                    "desc": "Append random data of given length",
                    "syntax": "--data-length <num>",
                    "example": "nmap --data-length 200 192.168.1.1",
                    "what": "Random data of given length को packets में जोड़ता है।"
                },
                "--ip-options": {
                    "desc": "Add IP header options",
                    "syntax": "--ip-options <options>",
                    "example": "nmap --ip-options 'L 10.0.0.1' 192.168.1.1",
                    "what": "IP header में options जोड़ता है (जैसे Loose Source Routing)।"
                },
                "--ttl": {
                    "desc": "Set IP Time To Live value",
                    "syntax": "--ttl <val>",
                    "example": "nmap --ttl 50 192.168.1.1",
                    "what": "IP TTL (Time To Live) value को set करता है।"
                },
                "--spoof-mac": {
                    "desc": "Spoof MAC address",
                    "syntax": "--spoof-mac <mac/prefix/vendor>",
                    "example": "nmap --spoof-mac 00:11:22:33:44:55",
                    "what": "MAC address को spoof करता है (vendor name भी दे सकते हैं जैसे Apple, Cisco)।"
                },
                "--badsum": {
                    "desc": "Send packets with bad checksum",
                    "syntax": "--badsum <target>",
                    "example": "nmap --badsum 192.168.1.1",
                    "what": "गलत TCP/UDP checksum वाले packets भेजता है (कुछ firewalls को पहचानने के लिए)।"
                }
            },
            
            # ========== OUTPUT OPTIONS ==========
            "output_options": {
                "-oN": {
                    "desc": "Normal output to file",
                    "syntax": "-oN <file>",
                    "example": "nmap -oN result.txt 192.168.1.1",
                    "what": "Normal output को फ़ाइल में save करता है।"
                },
                "-oX": {
                    "desc": "XML output to file",
                    "syntax": "-oX <file>",
                    "example": "nmap -oX result.xml 192.168.1.1",
                    "what": "XML format में output save करता है।"
                },
                "-oS": {
                    "desc": "Script Kiddie output (1337 speak)",
                    "syntax": "-oS <file>",
                    "example": "nmap -oS result.script 192.168.1.1",
                    "what": "ScRipT KIddIe style output (1337 speak में)।"
                },
                "-oG": {
                    "desc": "Grepable output",
                    "syntax": "-oG <file>",
                    "example": "nmap -oG result.gnmap 192.168.1.1",
                    "what": "Grepable output – tools के साथ parse करने के लिए।"
                },
                "-oA": {
                    "desc": "All major formats (.nmap, .xml, .gnmap)",
                    "syntax": "-oA <basename>",
                    "example": "nmap -oA scan 192.168.1.1",
                    "what": "तीनों formats (.nmap, .xml, .gnmap) एक साथ generate करता है।"
                },
                "-v": {
                    "desc": "Verbose output (more details)",
                    "syntax": "-v <target>",
                    "example": "nmap -v 192.168.1.1",
                    "what": "Verbose output – ज़्यादा जानकारी दिखाता है।"
                },
                "-vv": {
                    "desc": "Verbose level 2 (even more details)",
                    "syntax": "-vv <target>",
                    "example": "nmap -vv 192.168.1.1",
                    "what": "Verbose level 2 – और ज़्यादा जानकारी।"
                },
                "-vvv": {
                    "desc": "Verbose level 3 (maximum details)",
                    "syntax": "-vvv <target>",
                    "example": "nmap -vvv 192.168.1.1",
                    "what": "Verbose level 3 – सबसे ज़्यादा जानकारी।"
                },
                "-d": {
                    "desc": "Debugging output (detailed)",
                    "syntax": "-d <target>",
                    "example": "nmap -d 192.168.1.1",
                    "what": "Debugging output (बहुत detailed)।"
                },
                "--reason": {
                    "desc": "Show reason for each port state",
                    "syntax": "--reason <target>",
                    "example": "nmap --reason 192.168.1.1",
                    "what": "बताता है कि port open/closed क्यों है (जैसे SYN-ACK मिला, RST मिला आदि)।"
                },
                "--open": {
                    "desc": "Only show open ports",
                    "syntax": "--open <target>",
                    "example": "nmap --open 192.168.1.1",
                    "what": "सिर्फ open (या open|filtered) ports दिखाता है, closed नहीं।"
                },
                "--packet-trace": {
                    "desc": "Show all packets sent and received",
                    "syntax": "--packet-trace <target>",
                    "example": "nmap --packet-trace 192.168.1.1",
                    "what": "हर भेजा और प्राप्त packet को दिखाता है।"
                },
                "--iflist": {
                    "desc": "List network interfaces and routes",
                    "syntax": "--iflist",
                    "example": "nmap --iflist",
                    "what": "Available network interfaces और routes की list दिखाता है।"
                },
                "--append-output": {
                    "desc": "Append to output file (don't overwrite)",
                    "syntax": "--append-output <file>",
                    "example": "nmap -oN result.txt --append-output 192.168.1.1",
                    "what": "मौजूदा फ़ाइल में output जोड़ता है (overwrite नहीं करता)।"
                },
                "--stylesheet": {
                    "desc": "Set XSLT stylesheet for XML output",
                    "syntax": "--stylesheet <path/URL>",
                    "example": "nmap -oX result.xml --stylesheet https://nmap.org/data/nmap.xsl",
                    "what": "XML output के लिए custom XSLT stylesheet सेट करता है।"
                }
            },
            
            # ========== MISC OPTIONS ==========
            "misc": {
                "-6": {
                    "desc": "Enable IPv6 scanning",
                    "syntax": "-6 <target>",
                    "example": "nmap -6 2001:db8::1",
                    "what": "IPv6 scanning enable करता है।"
                },
                "-A": {
                    "desc": "Aggressive scan (OS, version, scripts, traceroute)",
                    "syntax": "-A <target>",
                    "example": "nmap -A 192.168.1.1",
                    "what": "Aggressive scan – OS, version, script, traceroute सब एक साथ (-O -sV -sC --traceroute)।"
                },
                "-n": {
                    "desc": "No DNS resolution (faster)",
                    "syntax": "-n <target>",
                    "example": "nmap -n 192.168.1.1",
                    "what": "DNS resolution बंद करता है (तेज़)।"
                },
                "-R": {
                    "desc": "Always do DNS resolution",
                    "syntax": "-R <target>",
                    "example": "nmap -R 192.168.1.1",
                    "what": "हमेशा DNS resolution करता है।"
                }
            }
        }
    
    # ========== HELPER METHODS ==========
    
    def get_all_commands(self):
        """Get all commands as flat dictionary"""
        all_cmds = {}
        for category, cmds in self.commands.items():
            for cmd, info in cmds.items():
                all_cmds[cmd] = {
                    'category': category,
                    'desc': info['desc'],
                    'syntax': info['syntax'],
                    'example': info['example'],
                    'what': info['what']
                }
        return all_cmds
    
    def get_command(self, cmd):
        """Get single command info"""
        all_cmds = self.get_all_commands()
        return all_cmds.get(cmd, None)
    
    def get_category(self, category):
        """Get all commands in a category"""
        return self.commands.get(category, {})
    
    def get_categories(self):
        """Get all category names"""
        return list(self.commands.keys())
    
    def search(self, keyword):
        """Search commands by keyword"""
        results = []
        keyword = keyword.lower()
        all_cmds = self.get_all_commands()
        
        for cmd, info in all_cmds.items():
            if (keyword in cmd.lower() or 
                keyword in info['desc'].lower() or 
                keyword in info['what'].lower()):
                results.append({
                    'cmd': cmd,
                    'info': info
                })
        return results
    
    def format_command(self, cmd):
        """Format a single command for display"""
        info = self.get_command(cmd)
        if not info:
            return f"❌ Command '{cmd}' not found"
        
        return f"""
╔══════════════════════════════════════════════════════════════╗
║  📌 {cmd}
╠══════════════════════════════════════════════════════════════╣
║  📝 {info['desc']}
║  
║  📖 Syntax: {info['syntax']}
║  
║  📋 Example: {info['example']}
║  
║  💡 {info['what']}
╚══════════════════════════════════════════════════════════════╝
"""
    
    def format_category(self, category):
        """Format a whole category for display"""
        cmds = self.get_category(category)
        if not cmds:
            return f"❌ Category '{category}' not found"
        
        output = []
        output.append("\n" + "="*70)
        output.append(f"📂 {category.upper().replace('_', ' ')}")
        output.append("="*70)
        
        for cmd, info in cmds.items():
            output.append(f"\n  {cmd}")
            output.append(f"    📝 {info['desc']}")
            output.append(f"    📖 {info['syntax']}")
        
        return "\n".join(output)
    
    def format_all(self):
        """Format all commands for display"""
        output = []
        output.append("\n" + "█"*70)
        output.append("█" + " " * 68 + "█")
        output.append("█" + " " * 20 + "NMAP COMPLETE COMMANDS" + " " * 28 + "█")
        output.append("█" + " " * 68 + "█")
        output.append("█"*70)
        
        for category, cmds in self.commands.items():
            output.append(f"\n📂 {category.upper().replace('_', ' ')} ({len(cmds)} commands)")
            output.append("-"*50)
            for cmd, info in cmds.items():
                output.append(f"  • {cmd:<15} - {info['desc'][:50]}")
        
        output.append("\n" + "█"*70)
        output.append(f"📊 Total Commands: {len(self.get_all_commands())}")
        output.append(f"📂 Total Categories: {len(self.commands)}")
        output.append("█"*70)
        
        return "\n".join(output)


# ========== USAGE EXAMPLE ==========
if __name__ == "__main__":
    nmap = NmapCommands()
    
    # Print all commands
    print(nmap.format_all())
    
    # Get a specific command
    print("\n" + nmap.format_command("-sS"))
    
    # Get a category
    print(nmap.format_category("host_discovery"))
    
    # Search
    print("\n🔍 Searching for 'stealth':")
    results = nmap.search("stealth")
    for r in results:
        print(f"  • {r['cmd']}: {r['info']['desc']}")
    
    # Get all commands as dict
    all_cmds = nmap.get_all_commands()
    print(f"\n📊 Total commands: {len(all_cmds)}")
