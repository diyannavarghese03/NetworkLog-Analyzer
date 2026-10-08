# CyberGuard API Reference

This document describes the lightweight REST API and live event stream used by the CyberGuard Network Log Analyzer.

## Base URL

- Local development: http://localhost:8080

## Endpoints

### GET /api/status
Returns the server health and operating mode.

Example response:

```json
{
  "status": "ONLINE",
  "mode": "SIMULATION_FALLBACK",
  "suricataLogPath": "/var/log/suricata/eve.json",
  "suricataFound": false,
  "activeClients": 1
}
```

### GET /api/config
Returns the current server configuration.

Example response:

```json
{
  "serverIp": "10.0.2.50",
  "domain": "",
  "logPath": "/var/log/suricata/eve.json",
  "interface": "eth0",
  "apiEndpoint": ""
}
```

### POST /api/config
Updates the server configuration object.

Request body example:

```json
{
  "serverIp": "10.0.2.50",
  "interface": "eth0",
  "logPath": "/var/log/suricata/eve.json"
}
```

### GET /api/stream
Opens a Server-Sent Events (SSE) stream used for real-time dashboard updates.

Example event payload:

```json
{
  "timestamp": "14:32:10.123",
  "src": "198.51.100.89",
  "dst": "10.0.2.50",
  "proto": "ALERT",
  "length": 128,
  "status": "SECURITY ALERT: Nmap Stealth Scan (Sid: 1000002)",
  "isThreat": true,
  "rule": "alert tcp $EXTERNAL_NET any -> $HOME_NET any (msg:\"SECURITY ALERT: Nmap Stealth Scan\"; flags:S; sid:1000002;)",
  "threatType": "NMAP"
}
```

### GET /api/simulate?type=TEST
Generates a simulated security packet or attack event from the backend for testing the dashboard stream.

Supported examples:

- NMAP
- SQLI
- DDOS
- TEST

## Event Stream Notes

- The dashboard subscribes to /api/stream.
- Each event is pushed as a standard SSE `data:` payload.
- Clients can react to incoming packets in real time without reloading the page.

## Concepts

### Traffic Mirroring
Traffic mirroring copies packet traffic from a source interface to a monitoring appliance without interrupting the original data flow.

### Suricata
Suricata is an intrusion detection and prevention engine that inspects network traffic and reads alerts from logs such as eve.json.

### VXLAN
VXLAN encapsulates mirrored traffic in UDP port 4789 so AWS traffic can be forwarded across the network to a security appliance.

### Simulation Mode
When no live Suricata log is available, the app runs in simulation fallback mode and generates realistic packet events locally for demonstrations.

## Troubleshooting

- If no Suricata log is present, the server automatically uses simulation mode.
- Check the console output for the active server mode.
- Ensure the configured log path exists before expecting live traffic.

## Quick Example

```bash
curl http://localhost:8080/api/status
curl http://localhost:8080/api/simulate?type=NMAP
```
