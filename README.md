# Yara Scan Service
![Logo](https://riskmitigation.ch/yara-scan/images/yara_scan.png "Yara Scan Logo")

Repository for scripts and tips for my "Yara Scan Service"

The service is currently in **beta** phase and allows any user to upload a Yara rule, have it scanned against sorted collection of malicious files (mostly based on MalwareBazaar).
> Did it happen to you that you wanted to quickly test a Yara rule your created, but you are missing a large enough data set to test your rule against? This is exactly where Yara Scan is designed for. You submit your Yara rule to the service and a short while later you will receive an email with the results of Yara scan over our large collection of malicious samples. And the best part? Most files are identified by a signature, making it easier to identify if your rule matches for the right malware samples.

## Give it a try ##
https://riskmitigation.ch/yara-scan/

## API Key ##
Please reach out to me if you are interested in getting an API key for easier submission of Yara rules

## Results ##
Each Yara scan task has a JSON file as a result, which includes all the file hits and some additional information, like file type, links to MalwareBazaar and VirusTotal
```
{
    "rule": "injectable_dll_x64",
    "malware": "CobaltStrike",
    "sha256": "8b551d934c77bb89d63071b22d33596b6655f4f2d4b4efaee5482112ba6868fa",
    "mime_type": "application/x-msdownload",
    "virustotal_link": "https://www.virustotal.com/gui/file/8b551d934c77bb89d63071b22d33596b6655f4f2d4b4efaee5482112ba6868fa/detection",
    "malwarebazaar_link": "https://bazaar.abuse.ch/sample/8b551d934c77bb89d63071b22d33596b6655f4f2d4b4efaee5482112ba6868fa/",
    "tags": []
}
```
