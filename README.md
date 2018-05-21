# cefp
ArcSight CEF Parser

# Usage

## As module
```
>>> import cefp
>>> cefp.parse(r'CEF:0|security|threatmanager|1.0|100|detected \\, \| and = in message|10|src=10.0.0.1 act=blocked \\, | and \= dst=1.1.1.1')
{'device': {'event_class_id': '100',
  'product': 'threatmanager',
  'vendor': 'security',
  'version': '1.0'},
 'extension': {'act': 'blocked \\, | and =',
  'dst': '1.1.1.1',
  'src': '10.0.0.1'},
 'name': 'detected \\, | and = in message',
 'severity': '10',
 'version': '0'}
```

## As command
```
$ cefp 'CEF:0|security|threatmanager|1.0|100|detected \\, \| and = in message|10|src=10.0.0.1 act=blocked \\, | and \= dst=1.1.1.1' | jq .
{
  "version": "0",
  "device": {
    "vendor": "security",
    "product": "threatmanager",
    "version": "1.0",
    "event_class_id": "100"
  },
  "name": "detected \\, | and = in message",
  "severity": "10",
  "extension": {
    "src": "10.0.0.1",
    "act": "blocked \\, | and =",
    "dst": "1.1.1.1"
  }
}
```
