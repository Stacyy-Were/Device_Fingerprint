
# Device Fingerprint
Device Fingerprint Lab - A local research project demonstrating browser fingerprint collection, signal normalization, SHA-256 fingerprinting, persistent storage and weighted device-correlation analysis.

Inspiration from the AliExpress' device detection "fraud" tool with a similarity engine that gives points when device/browser/network similarities are identified, otherwise no similarities = 0 Points.

## Browser & Network Correlation

A cybersecurity home-lab experiment exploring how browser fingerprinting and network metadata can be combined to correlate sessions.

The main concept tested was:

**Browser fingerprint ≠ Device identity ≠ Network identity**

## What it does

The Flask application:

* Collects browser-visible signals
* Generates a SHA-256 fingerprint
* Stores captures in SQLite
* Records basic network metadata
* Compares two captures
* Calculates browser, network and overall similarity

## Browser signals

The fingerprint currently uses:

| Signal        | Weight |
| ------------- |:------:|
| Platform      |10      |
| Screen Width  | 8      |
| Screen Height | 7      |
| Color Depth   | 5      |
| Pixel Ratio   | 5      |
| Timezone      |15      |
| CPU Cores     |10      |
| Touch Points  | 5      |
| Language      |10      |
| User-Agent    |20      |
| Do Not Track  | 5      |

Total browser score: **100**

## Network signals

The application also compares:

| Signal            | Weight |
| ----------------- |:------:|
| IP Address        |15      |
| X-Forwarded-For   | 5      |
| Connection Scheme | 2      |


## Test Results

### Test 1: Same browser

```json
// Fingerprint A
{
  "label": "Fingerprint A",
  "fingerprint": "21e3cb3605e312cfa8f4f0338e40faebd23ac182717ef8a049775ced3d42af37",
  "signals": {
    "colorDepth": 24,
    "cookiesEnabled": true,
    "cpuCores": 8,
    "doNotTrack": "1",
    "language": "en-US",
    "languages": [
      "en-US",
      "en"
    ],
    "pixelRatio": 2,
    "platform": "Linux x86_64",
    "screenHeight": 960,
    "screenWidth": 1440,
    "timezone": "Africa/Nairobi",
    "touchPoints": 0,
    "userAgent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0"
  }
}
```

### Fingerprint B

```json
// Fingerprint B
{
  "label": "Fingerprint B",
  "fingerprint": "21e3cb3605e312cfa8f4f0338e40faebd23ac182717ef8a049775ced3d42af37",
  "signals": {
    "colorDepth": 24,
    "cookiesEnabled": true,
    "cpuCores": 8,
    "doNotTrack": "1",
    "language": "en-US",
    "languages": [
      "en-US",
      "en"
    ],
    "pixelRatio": 2,
    "platform": "Linux x86_64",
    "screenHeight": 960,
    "screenWidth": 1440,
    "timezone": "Africa/Nairobi",
    "touchPoints": 0,
    "userAgent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0"
  }
}
```

### Comparison between Fingerprints A and B

```json
// Comparison between A and B
{
  "colorDepth": {
    "match": true,
    "value_a": 24,
    "value_b": 24,
    "weight": 5
  },
  "cpuCores": {
    "match": true,
    "value_a": 8,
    "value_b": 8,
    "weight": 10
  },
  "doNotTrack": {
    "match": true,
    "value_a": "1",
    "value_b": "1",
    "weight": 5
  },
  "language": {
    "match": true,
    "value_a": "en-US",
    "value_b": "en-US",
    "weight": 10
  },
  "pixelRatio": {
    "match": true,
    "value_a": 2,
    "value_b": 2,
    "weight": 5
  },
  "platform": {
    "match": true,
    "value_a": "Linux x86_64",
    "value_b": "Linux x86_64",
    "weight": 10
  },
  "screenHeight": {
    "match": true,
    "value_a": 960,
    "value_b": 960,
    "weight": 7
  },
  "screenWidth": {
    "match": true,
    "value_a": 1440,
    "value_b": 1440,
    "weight": 8
  },
  "timezone": {
    "match": true,
    "value_a": "Africa/Nairobi",
    "value_b": "Africa/Nairobi",
    "weight": 15
  },
  "touchPoints": {
    "match": true,
    "value_a": 0,
    "value_b": 0,
    "weight": 5
  },
  "userAgent": {
    "match": true,
    "value_a": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0",
    "value_b": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0",
    "weight": 20
  }
}
```

| Signal        |  Weight |
| ------------- |:------: |
| Platform      |10       |
| Screen Width  | 8       |
| Screen Height | 7       |
| Color Depth   | 5       |
| Pixel Ratio   | 5       |
| Timezone      |15       |
| CPU Cores     |10       |
| Touch Points  | 5       |
| Language      |10       |
| User-Agent    |20       |
| DNT           | 5       |
| **Total**     | **100** |

**Result: 100% similarity**

All tested signals matched.

## Experiment 2: Firefox vs Opera


```json
// Comparison between Fingerprints A and B
{
  "colorDepth": {
    "match": true,
    "value_a": 24,
    "value_b": 24,
    "weight": 5
  },
  "cpuCores": {
    "match": true,
    "value_a": 8,
    "value_b": 8,
    "weight": 10
  },
  "doNotTrack": {
    "match": false,
    "value_a": "1",
    "value_b": null,
    "weight": 5
  },
  "language": {
    "match": true,
    "value_a": "en-US",
    "value_b": "en-US",
    "weight": 10
  },
  "pixelRatio": {
    "match": true,
    "value_a": 2,
    "value_b": 2,
    "weight": 5
  },
  "platform": {
    "match": true,
    "value_a": "Linux x86_64",
    "value_b": "Linux x86_64",
    "weight": 10
  },
  "screenHeight": {
    "match": true,
    "value_a": 960,
    "value_b": 960,
    "weight": 7
  },
  "screenWidth": {
    "match": true,
    "value_a": 1440,
    "value_b": 1440,
    "weight": 8
  },
  "timezone": {
    "match": true,
    "value_a": "Africa/Nairobi",
    "value_b": "Africa/Nairobi",
    "weight": 15
  },
  "touchPoints": {
    "match": true,
    "value_a": 0,
    "value_b": 0,
    "weight": 5
  },
  "userAgent": {
    "match": false,
    "value_a": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 OPR/135.0.0.0",
    "value_b": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0",
    "weight": 20
  }
}
```

| Signal        |  Weight |
| ------------- |:-------:|
| Platform      |10       |
| Screen Width  | 8       |
| Screen Height | 7       |
| Color Depth   | 5       |
| Pixel Ratio   | 5       |
| Timezone      |15       |
| CPU Cores     |10       |
| Touch Points  | 5       |
| Language      |10       |
| User-Agent    |20       |
| DNT           | 5       |
| **Total**     | **100** |

Matching signals:

```text
10 + 8 + 7 + 5 + 5 + 15 + 10 + 5 + 10 = 75
```

**Result: 75% similarity**

The browsers shared most system-level characteristics, but the User-Agent and Do Not Track values were different.

## Experiment 3: Kali VM vs Ubuntu Host

```json
//Comparison between Fingerprints A and B
{
  "colorDepth": {
    "match": true,
    "value_a": 24,
    "value_b": 24,
    "weight": 5
  },
  "cpuCores": {
    "match": false,
    "value_a": 2,
    "value_b": 8,
    "weight": 10
  },
  "doNotTrack": {
    "match": false,
    "value_a": "unspecified",
    "value_b": "1",
    "weight": 5
  },
  "language": {
    "match": true,
    "value_a": "en-US",
    "value_b": "en-US",
    "weight": 10
  },
  "pixelRatio": {
    "match": false,
    "value_a": 1,
    "value_b": 1.5789473684210527,
    "weight": 5
  },
  "platform": {
    "match": true,
    "value_a": "Linux x86_64",
    "value_b": "Linux x86_64",
    "weight": 10
  },
  "screenHeight": {
    "match": false,
    "value_a": 800,
    "value_b": 1216,
    "weight": 7
  },
  "screenWidth": {
    "match": false,
    "value_a": 1280,
    "value_b": 1824,
    "weight": 8
  },
  "timezone": {
    "match": false,
    "value_a": "America/New_York",
    "value_b": "Africa/Nairobi",
    "weight": 15
  },
  "touchPoints": {
    "match": true,
    "value_a": 0,
    "value_b": 0,
    "weight": 5
  },
  "userAgent": {
    "match": false,
    "value_a": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "value_b": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0",
    "weight": 20
  }
}
```

| Signal        |  Weight |
| ------------- |:-------:|
| Platform      |10       |
| Screen Width  | 8       |
| Screen Height | 7       |
| Color Depth   | 5       |
| Pixel Ratio   | 5       |
| Timezone      |15       |
| CPU Cores     |10       |
| Touch Points  | 5       |
| Language      |10       |
| User-Agent    |20       |
| DNT           | 5       |
| **Total**     | **100** |

Matching signals:

```text
10 + 5 + 5 + 10 = 30
```

**Result: 30% similarity**

The Kali VM and Ubuntu host shared some characteristics, but several high-weight signals differed.

## Experiment 4: Network Metadata

The network layer was tested alongside the browser fingerprint.

### Network Comparison

```json
{
  "forwardedFor": {
    "match": false,
    "value_a": null,
    "value_b": null,
    "weight": 5
  },
  "ipAddress": {
    "match": true,
    "value_a": "127.0.0.1",
    "value_b": "127.0.0.1",
    "weight": 15
  },
  "scheme": {
    "match": true,
    "value_a": "http",
    "value_b": "http",
    "weight": 2
  }
}
```

| Signal          | Weight |
| --------------- |:------:|
| IP Address      |15      |
| X-Forwarded-For |5       |
| Scheme          |2       |
| **Total**       |**22**  |

Matching network signals:

```text
15 + 2 = 17
```

**Network similarity: 17/22**

The application saw both requests as coming from `127.0.0.1`.

This was expected because the test was performed locally.

`127.0.0.1` is the IPv4 loopback address and does not represent a public Internet IP.

## Overall Results

| Experiment | Comparison             | Result |
| ---------- | ---------------------- |:------:|
| 1          | Same Firefox           |100%    |
| 2          | Firefox vs Opera       |75%     |
| 3          | Kali VM vs Ubuntu Host |30%     |
| 4          | Network Metadata       |17/22   |

## Findings

The experiments showed that browser fingerprints can change between browsers and virtual machines even when some underlying characteristics are similar.

Network metadata adds another layer of correlation, but an IP address should not be treated as a unique device identifier.

The results support the main principle of the project:

```text
Browser fingerprint ≠ Device identity
Device identity ≠ Network identity
```

All tests were performed in a controlled local home lab.



Two captures from the same Firefox environment produced matching browser signals.

**Browser similarity: 100%**

This demonstrated that repeated sessions from the same browser configuration can produce very similar fingerprints.

### Test 2: Firefox vs Opera

Firefox and Opera were tested on the same Linux environment.

Most system characteristics matched, but the User-Agent and some browser/display settings differed.

**Browser similarity: 75%**

This showed that different browsers can produce different fingerprints even when running on the same computer.

### Test 3: Kali VM vs Ubuntu Host

A Kali Linux VM was compared with the Ubuntu host.

Several characteristics differed, including:

* CPU cores
* Screen dimensions
* Pixel ratio
* Timezone
* User-Agent
* Do Not Track

**Browser similarity: 30%**

This shows that a virtual machine can produce a substantially different browser fingerprint from its host.

## Network Result

One comparison produced:

```text
IP Address:       127.0.0.1
Forwarded-For:    None
Scheme:           HTTP
```

The matching `127.0.0.1` address shows that both requests reached the application locally.

This doesn't prove that the browsers belong to the same physical device.

## Key Takeaway

An IP address is not a device identifier.

Multiple devices can share an IP through NAT, while one device can use different IP addresses when changing networks or using a VPN.
Likewise, two browsers on the same computer can produce different fingerprints.
The project therefore treats browser and network information as correlation signals, not proof of device identity.

## Lab

```text
Ubuntu Host:
  1. Flask: 5000
  2. Virtual Network
  3. Kali Linux VM
```

The Flask server listens on:

```python
app.run(
    host="0.0.0.0",
    port=5000,
    debug=True
)
```

Check the listening socket with:

```bash
ss -ltnp | grep 5000
```

Test connectivity from another lab machine:

```bash
curl http://<host-ip>:5000/health
```

## Stack

Python, Flask, SQLite, JavaScript, HTML, CSS, Linux and Virtual Machine Manager.

The similarity score is based on manually selected signals and doesn't prove that two sessions came from the same physical device XD

## Setup

### Requirements

* Python 3
* Git
* Modern web browser

### Install

```bash
git clone https://github.com/Stacyy-Were/Device_Fingerprint.git
cd Device_Fingerprint

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### Run

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

### Network Testing

To test from another machine or VM, make sure Flask uses:

```python
app.run(host="0.0.0.0", port=5000, debug=True)
```

Find the host IP:

```bash
ip route get 1.1.1.1
```

Then access:

```text
http://host_IP:5000
```

