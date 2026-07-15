#!/usr/bin/env python3
"""Monthly egg-price feed: BLS average price (Grade A large, per dozen, US city avg)
via FRED public CSV (no API key). Writes data/eggs.json for the egg-prices shortcode."""
import csv, io, json, urllib.request

CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=APU0000708111"
raw = urllib.request.urlopen(CSV_URL, timeout=30).read().decode()
rows = [r for r in csv.reader(io.StringIO(raw))][1:]
series = [(d[:7], float(v)) for d, v in rows if v not in ("", ".")]
recent = series[-14:]
out = []
for i, (month, price) in enumerate(recent):
    mom = price - recent[i - 1][1] if i > 0 else None
    prior = dict(series).get(f"{int(month[:4]) - 1}{month[4:]}")
    out.append({"month": month, "price": round(price, 2),
                "mom": round(mom, 2) if mom is not None else None,
                "yoy_pct": round((price - prior) / prior * 100, 1) if prior else None})
data = {"as_of": recent[-1][0],
        "unit": "USD per dozen, Grade A large, U.S. city average",
        "source": "U.S. Bureau of Labor Statistics via FRED (series APU0000708111)",
        "series": out[1:]}
json.dump(data, open("data/eggs.json", "w", encoding="utf-8"), indent=1)
print(f"eggs.json: {len(out)-1} months, latest {data['as_of']} = ${recent[-1][1]:.2f}")
