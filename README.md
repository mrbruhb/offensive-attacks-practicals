# Ethical Hacking — Offensive Practicals

A collection of practical cybersecurity exercises covering network-layer attacks, web application exploitation, and malware mechanics. All work was completed in isolated lab environments.

---

## Contents

| Task | Topic | Techniques |
|------|-------|------------|
| [Q1 — ARP Spoofing](#q1--arp-spoofing) | Network Attack | ARP poisoning, MITM |
| [Q2 — XSS Cookie Theft](#q2--xss-cookie-theft) | Web Exploitation | Stored/Reflected XSS, session hijacking |
| [Q3 — Ransomware Simulation](#q3--ransomware-simulation) | Malware | AES encryption, RSA key wrapping |

---

## Q1 — ARP Spoofing

**Directory:** `Q1/`

### Overview

The goal of this task was to understand how ARP poisoning enables a Man-in-the-Middle (MITM) attack at the network layer. ARP has no authentication — any host can claim ownership of an IP address by broadcasting a forged reply. By exploiting this, an attacker can silently insert themselves between a victim and their router, intercepting all traffic passing between them.

The exercise also reinforces responsible penetration testing practice — the script restores both ARP tables to their legitimate state on exit, leaving the network unchanged after the attack concludes.

### Files

| File | Description |
|------|-------------|
| `arpspoof.py` | ARP spoofing script with MAC discovery and ARP restore |
| `Q1.pdf` | Full task write-up and screenshots |

### How It Works

1. **MAC Discovery** — Sends an ARP broadcast to resolve the MAC address of a given IP
2. **ARP Poisoning** — Sends crafted ARP replies to both the victim and the router, associating the attacker's MAC with each other's IP
3. **Continuous Spoofing** — Repeats every 2 seconds to keep ARP caches poisoned (entries expire)
4. **Restoration** — On `Ctrl+C`, sends legitimate ARP replies to both hosts to restore correct mappings

### Usage

```bash
sudo python3 arpspoof.py <Victim_IP> <Router_IP>

# Example
sudo python3 arpspoof.py 192.168.1.105 192.168.1.1
```

> Requires root (`sudo`) for raw packet injection via Scapy.

### Dependencies

```
scapy
```

---

## Q2 — XSS Cookie Theft

**Directory:** `Q2/`

### Overview

The goal of this task was to understand how XSS vulnerabilities allow an attacker to execute arbitrary JavaScript in a victim's browser, and how that can be leveraged to steal session cookies and hijack authenticated sessions.

Two variants are covered — reflected XSS (payload executes immediately via a malicious input) and stored XSS (payload is persisted to the database and executes for every subsequent user who loads the page), demonstrating why stored XSS is significantly more dangerous at scale.

### Files

| File | Description |
|------|-------------|
| `inject.html` | XSS payload that exfiltrates cookies via HTTP request |
| `makeserver.py` | Flask server that receives and logs stolen cookies |
| `Q2.pdf` | Full task write-up and screenshots |

### How It Works

1. **Attacker starts the listener** — Flask server runs on port 5000, logging any cookies it receives
2. **Payload injection** — The contents of `inject.html` are pasted into a vulnerable input field on the target web app
3. **Victim triggers the payload** — On page load/submit, the victim's browser executes the script
4. **Cookie exfiltration** — The script sends the victim's `document.cookie` to the attacker's server via an HTTP GET request
5. **Cookies logged** — The server appends the stolen cookie and a timestamp to `cookies.txt`

### Usage

```bash
# Step 1: Start the cookie-catching server
python3 makeserver.py

# Step 2: Inject the contents of inject.html into the XSS-vulnerable input field
# For reflected XSS: paste into the "What's your name?" field and submit
# For stored XSS: paste into the stored XSS comment/input field and submit
```

> Update the IP address in `inject.html` to match your attacker machine before running.

### Dependencies

```
flask
```

---

## Q3 — Ransomware Simulation

**Directory:** `Q3/`

### Overview

The goal of this task was to understand the cryptographic mechanisms that make modern ransomware effective and difficult to reverse without paying the ransom. The script implements the hybrid encryption scheme used by real-world ransomware families like WannaCry and REvil — AES for fast bulk file encryption, and RSA to protect the AES key so only the attacker can recover it.

Understanding this pattern is essential for defenders: it explains why backups are the primary mitigation, why decryption without the private key is computationally infeasible, and how ransomware operators maintain leverage over victims.

### Files

| File | Description |
|------|-------------|
| `ransomware.py` | Encryption script simulating ransomware behaviour |
| `Q3.pdf` | Full task write-up and screenshots |

### How It Works

1. **Key generation** — Generates a random 16-byte AES symmetric key and an RSA public/private key pair
2. **File encryption** — Encrypts `my_secrets.txt` using AES-CBC, writing ciphertext to `data_cipher.txt`
3. **Key wrapping** — Encrypts the AES key with the RSA public key, writing it to `key_cipher.txt`
4. **Cleanup** — Deletes the plaintext file (`my_secrets.txt`) and the unprotected AES key (`key.txt`)
5. **Ransom note** — Prints a ransom message instructing the victim to send `key_cipher.txt` to the attacker

### Encryption Scheme

```
my_secrets.txt  ──[AES-CBC]──►  data_cipher.txt
AES key         ──[RSA-OAEP]──► key_cipher.txt
```

### Usage

```bash
# Create a test target file first
echo "sensitive data" > my_secrets.txt

# Run the simulation
python3 ransomware.py
```

> No `sudo` required. Run only against files you own in an isolated environment.

### Dependencies

```
pycryptodome
openssl (system)
```

---

## Environment

All tasks were completed in an isolated virtual machine lab environment. No attacks were performed against live systems, real users, or infrastructure outside the controlled lab.

**Common tools and libraries used:**
- Python 3
- Scapy — packet crafting and raw socket access
- Flask — lightweight HTTP server for attack simulation
- PyCryptodome — AES/RSA cryptographic primitives
- OpenSSL — key generation

---

## Skills Demonstrated

- Network protocol exploitation (ARP, Layer 2 attacks)
- Web application security (XSS, session management weaknesses)
- Cryptography in a malware context (symmetric + asymmetric hybrid encryption)
- Offensive Python scripting
- Responsible disclosure practices (ARP table restoration, sandboxed execution)
