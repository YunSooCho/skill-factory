#!/usr/bin/env python3
import os

repo_path = "/Users/clks001/.openclaw/workspace/github/skill-factory/repo"

all_services = {
    "13_계약체결_Contracts": ["signable", "signtime", "wan-sign", "xodo-sign", "yousign", "zapsign", "zoho_sign"],
    "14_수발주재고관리_Inventory": ["booqable", "detrack", "dextre", "easyship", "kura-bugyo", "logiless", "maintainx", "next-engine", "openlogi", "order_desk", "pca-cloud-konkan", "sendcloud", "sendle", "sos_inventory", "tookan", "weclapp", "zaico", "zoho-inventory"],
    "15_웹사이트제작_WebDev": ["adalo", "agora", "bubble", "cloudflare", "contentful"]
}

print("Service Status Check:")
print("="*80)

total_services = 0
existing_services = 0
missing_services = 0

for category, services in all_services.items():
    print(f"\n{category}:")
    for service in services:
        total_services += 1
        service_path = os.path.join(repo_path, service)
        exists = os.path.exists(service_path)
        if exists:
            existing_services += 1
            status = "✓ EXISTS"
        else:
            missing_services += 1
            status = "✗ MISSING"
        print(f"  {service}: {status}")

print("\n" + "="*80)
print(f"Total services: {total_services}")
print(f"Existing: {existing_services}")
print(f"Missing: {missing_services}")
print(f"Need to create: {missing_services}")