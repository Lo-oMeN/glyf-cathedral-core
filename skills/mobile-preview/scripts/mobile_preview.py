#!/usr/bin/env python3
"""
Mobile Preview - Device Emulation and Cross-Platform Testing
Uses Playwright for mobile device emulation
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Optional, List
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

# Preset device profiles combining Playwright devices with custom additions
DEVICE_PROFILES = {
    # iOS Devices
    "iPhone SE": {"width": 375, "height": 667, "device_scale_factor": 2, "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1", "is_mobile": True, "has_touch": True},
    "iPhone 12 mini": {"width": 375, "height": 812, "device_scale_factor": 3, "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1", "is_mobile": True, "has_touch": True},
    "iPhone 12/13/14": {"width": 390, "height": 844, "device_scale_factor": 3, "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1", "is_mobile": True, "has_touch": True},
    "iPhone 14 Pro": {"width": 393, "height": 852, "device_scale_factor": 3, "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1", "is_mobile": True, "has_touch": True},
    "iPhone 14 Pro Max": {"width": 430, "height": 932, "device_scale_factor": 3, "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1", "is_mobile": True, "has_touch": True},
    "iPhone 15": {"width": 393, "height": 852, "device_scale_factor": 3, "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1", "is_mobile": True, "has_touch": True},
    "iPhone 15 Pro Max": {"width": 430, "height": 932, "device_scale_factor": 3, "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1", "is_mobile": True, "has_touch": True},
    
    # Android Devices
    "Pixel 5": {"width": 393, "height": 851, "device_scale_factor": 2.75, "user_agent": "Mozilla/5.0 (Linux; Android 13; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", "is_mobile": True, "has_touch": True},
    "Pixel 7": {"width": 412, "height": 915, "device_scale_factor": 2.625, "user_agent": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", "is_mobile": True, "has_touch": True},
    "Pixel 7 Pro": {"width": 412, "height": 892, "device_scale_factor": 3.5, "user_agent": "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", "is_mobile": True, "has_touch": True},
    "Samsung Galaxy S21": {"width": 384, "height": 854, "device_scale_factor": 2.8125, "user_agent": "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", "is_mobile": True, "has_touch": True},
    "Samsung Galaxy S23": {"width": 384, "height": 854, "device_scale_factor": 3, "user_agent": "Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", "is_mobile": True, "has_touch": True},
    
    # Tablets
    "iPad Mini": {"width": 768, "height": 1024, "device_scale_factor": 2, "user_agent": "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1", "is_mobile": True, "has_touch": True},
    "iPad": {"width": 810, "height": 1080, "device_scale_factor": 2, "user_agent": "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1", "is_mobile": True, "has_touch": True},
    "iPad Air": {"width": 820, "height": 1180, "device_scale_factor": 2, "user_agent": "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1", "is_mobile": True, "has_touch": True},
    "iPad Pro 11": {"width": 834, "height": 1194, "device_scale_factor": 2, "user_agent": "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1", "is_mobile": True, "has_touch": True},
    "iPad Pro 12.9": {"width": 1024, "height": 1366, "device_scale_factor": 2, "user_agent": "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1", "is_mobile": True, "has_touch": True},
    "Samsung Galaxy Tab S8": {"width": 800, "height": 1280, "device_scale_factor": 2, "user_agent": "Mozilla/5.0 (Linux; Android 12; SM-X700) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36", "is_mobile": True, "has_touch": True},
}

# Network throttling profiles
NETWORK_PROFILES = {
    "offline": {"offline": True, "download_throughput": 0, "upload_throughput": 0, "latency": 0},
    "3g": {"offline": False, "download_throughput": 750 * 1024 // 8, "upload_throughput": 250 * 1024 // 8, "latency": 100},
    "3g-fast": {"offline": False, "download_throughput": 1.5 * 1024 * 1024 // 8, "upload_throughput": 750 * 1024 // 8, "latency": 40},
    "4g": {"offline": False, "download_throughput": 4 * 1024 * 1024 // 8, "upload_throughput": 3 * 1024 * 1024 // 8, "latency": 20},
    "4g-lte": {"offline": False, "download_throughput": 12 * 1024 * 1024 // 8, "upload_throughput": 6 * 1024 * 1024 // 8, "latency": 10},
    "wifi": {"offline": False, "download_throughput": 30 * 1024 * 1024 // 8, "upload_throughput": 15 * 1024 * 1024 // 8, "latency": 2},
    "cable": {"offline": False, "download_throughput": 100 * 1024 * 1024 // 8, "upload_throughput": 50 * 1024 * 1024 // 8, "latency": 2},
}


def get_device_profile(device_name: str) -> dict:
    """Get device profile with fuzzy matching"""
    device_name = device_name.strip()
    
    # Direct match
    if device_name in DEVICE_PROFILES:
        return DEVICE_PROFILES[device_name]
    
    # Case-insensitive match
    for name, profile in DEVICE_PROFILES.items():
        if name.lower() == device_name.lower():
            return profile
    
    # Partial match
    device_lower = device_name.lower()
    for name, profile in DEVICE_PROFILES.items():
        if device_lower in name.lower() or any(part.lower() in device_lower for part in name.split()):
            return profile
    
    raise ValueError(f"Unknown device: {device_name}. Use 'list' command to see available devices.")


def list_devices():
    """List all available device profiles"""
    print("Available Device Profiles:\n")
    
    categories = {
        "iOS Devices": [k for k in DEVICE_PROFILES.keys() if "iPhone" in k or "iPad" in k and "Samsung" not in k and "Galaxy" not in k],
        "Android Devices": [k for k in DEVICE_PROFILES.keys() if "Pixel" in k or "Samsung" in k or "Galaxy" in k],
        "Tablets": [k for k in DEVICE_PROFILES.keys() if "iPad" in k or "Tab" in k],
    }
    
    for category, devices in categories.items():
        print(f"\n{category}:")
        print("-" * 40)
        for device in sorted(set(devices)):
            profile = DEVICE_PROFILES[device]
            print(f"  • {device}: {profile['width']}x{profile['height']} @ {profile['device_scale_factor']}x")
    
    print("\n")


async def emulate_device(url: str, device_name: str, output_path: Optional[str] = None, 
                         orientation: str = "portrait", network_profile: Optional[str] = None,
                         full_page: bool = True, wait_time: int = 3) -> str:
    """Emulate a device and capture screenshot"""
    
    device = get_device_profile(device_name)
    
    # Handle orientation
    width = device["width"]
    height = device["height"]
    if orientation.lower() == "landscape":
        width, height = height, width
    
    if not output_path:
        safe_device = device_name.replace("/", "_").replace(" ", "_")
        output_path = f"screenshot_{safe_device}_{orientation}.png"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport={"width": width, "height": height},
            device_scale_factor=device["device_scale_factor"],
            user_agent=device["user_agent"],
            is_mobile=device["is_mobile"],
            has_touch=device["has_touch"],
        )
        
        page = await context.new_page()
        
        # Apply network throttling if specified
        if network_profile:
            if network_profile not in NETWORK_PROFILES:
                raise ValueError(f"Unknown network profile: {network_profile}")
            profile = NETWORK_PROFILES[network_profile]
            cdp_session = await page.context.new_cdp_session(page)
            await cdp_session.send("Network.emulateNetworkConditions", {
                "offline": profile["offline"],
                "downloadThroughput": profile["download_throughput"],
                "uploadThroughput": profile["upload_throughput"],
                "latency": profile["latency"]
            })
        
        try:
            await page.goto(url, wait_until="networkidle")
            await asyncio.sleep(wait_time)  # Additional wait for dynamic content
        except Exception as e:
            print(f"Warning: Error loading page: {e}")
        
        await page.screenshot(path=output_path, full_page=full_page)
        await browser.close()
    
    return output_path


def emulate_device_sync(url: str, device_name: str, output_path: Optional[str] = None,
                        orientation: str = "portrait", network_profile: Optional[str] = None,
                        full_page: bool = True, wait_time: int = 3) -> str:
    """Synchronous wrapper for emulate_device"""
    return asyncio.run(emulate_device(url, device_name, output_path, orientation, 
                                      network_profile, full_page, wait_time))


def rotate_screenshot(url: str, device_name: str, orientation: str = "landscape", 
                      output_path: Optional[str] = None) -> str:
    """Rotate device orientation and capture screenshot"""
    return emulate_device_sync(url, device_name, output_path, orientation)


def throttle_network(url: str, device_name: str, profile: str = "3g",
                     output_path: Optional[str] = None) -> str:
    """Simulate network throttling and capture screenshot"""
    return emulate_device_sync(url, device_name, output_path, network_profile=profile)


def compare_devices(url: str, devices: List[str], output_dir: str = "./comparisons") -> List[str]:
    """Capture screenshots of multiple devices for side-by-side comparison"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    screenshots = []
    for device_name in devices:
        try:
            safe_name = device_name.replace("/", "_").replace(" ", "_")
            output_path = f"{output_dir}/comparison_{safe_name}.png"
            path = emulate_device_sync(url, device_name, output_path)
            screenshots.append(path)
            print(f"✓ Captured: {device_name} -> {path}")
        except Exception as e:
            print(f"✗ Failed: {device_name} - {e}")
    
    return screenshots


def test_responsive(url: str, widths: List[int] = None, 
                    output_dir: str = "./responsive") -> List[str]:
    """Test responsive breakpoints at specified widths"""
    if widths is None:
        widths = [375, 768, 1024, 1440]
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    screenshots = []
    for width in widths:
        output_path = f"{output_dir}/responsive_{width}px.png"
        
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context(viewport={"width": width, "height": 900})
            page = context.new_page()
            
            try:
                page.goto(url, wait_until="networkidle")
                page.wait_for_timeout(3000)
            except Exception as e:
                print(f"Warning: Error loading page at {width}px: {e}")
            
            page.screenshot(path=output_path, full_page=True)
            browser.close()
        
        screenshots.append(output_path)
        print(f"✓ Captured: {width}px -> {output_path}")
    
    return screenshots


def create_comparison_html(url: str, screenshots: List[str], devices: List[str], 
                           output_path: str = "comparison.html"):
    """Create an HTML file for side-by-side comparison"""
    
    rows = ""
    for screenshot, device in zip(screenshots, devices):
        rows += f'''
        <div class="device-comparison">
            <h3>{device}</h3>
            <img src="{screenshot}" alt="{device}" loading="lazy">
        </div>
        '''
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Device Comparison - {url}</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #1a1a2e; color: #eee; padding: 20px; }}
        h1 {{ text-align: center; margin-bottom: 10px; }}
        .url {{ text-align: center; color: #888; margin-bottom: 30px; word-break: break-all; }}
        .comparison-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; }}
        .device-comparison {{ background: #16213e; border-radius: 12px; padding: 20px; }}
        .device-comparison h3 {{ margin-bottom: 15px; color: #e94560; font-size: 16px; }}
        .device-comparison img {{ width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }}
        @media (max-width: 768px) {{ .comparison-grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <h1>📱 Device Comparison</h1>
    <div class="url">{url}</div>
    <div class="comparison-grid">
        {rows}
    </div>
</body>
</html>'''
    
    with open(output_path, "w") as f:
        f.write(html_content)
    
    print(f"Comparison HTML created: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Mobile Preview - Device Emulation Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # list command
    subparsers.add_parser("list", help="List available device profiles")
    
    # emulate command
    emulate_parser = subparsers.add_parser("emulate", help="Emulate a device and capture screenshot")
    emulate_parser.add_argument("url", help="URL to capture")
    emulate_parser.add_argument("--device", "-d", default="iPhone 14", help="Device name (default: iPhone 14)")
    emulate_parser.add_argument("--output", "-o", help="Output path for screenshot")
    emulate_parser.add_argument("--orientation", choices=["portrait", "landscape"], default="portrait", help="Device orientation")
    emulate_parser.add_argument("--network", "-n", choices=list(NETWORK_PROFILES.keys()), help="Network throttling profile")
    emulate_parser.add_argument("--wait", "-w", type=int, default=3, help="Wait time in seconds after page load")
    emulate_parser.add_argument("--no-full-page", action="store_true", help="Capture viewport only instead of full page")
    
    # rotate command
    rotate_parser = subparsers.add_parser("rotate", help="Rotate device orientation")
    rotate_parser.add_argument("url", help="URL to capture")
    rotate_parser.add_argument("--device", "-d", default="iPhone 14", help="Device name")
    rotate_parser.add_argument("--orientation", choices=["portrait", "landscape"], default="landscape", help="Orientation")
    rotate_parser.add_argument("--output", "-o", help="Output path")
    
    # throttle command
    throttle_parser = subparsers.add_parser("throttle", help="Simulate network throttling")
    throttle_parser.add_argument("url", help="URL to capture")
    throttle_parser.add_argument("--device", "-d", default="iPhone 14", help="Device name")
    throttle_parser.add_argument("--profile", "-p", choices=list(NETWORK_PROFILES.keys()), default="3g", help="Network profile")
    throttle_parser.add_argument("--output", "-o", help="Output path")
    
    # compare command
    compare_parser = subparsers.add_parser("compare", help="Compare multiple devices side-by-side")
    compare_parser.add_argument("url", help="URL to capture")
    compare_parser.add_argument("--devices", "-d", nargs="+", default=["iPhone 14", "Pixel 7", "iPad"],
                               help="List of devices to compare")
    compare_parser.add_argument("--output-dir", "-o", default="./comparisons", help="Output directory")
    compare_parser.add_argument("--html", action="store_true", help="Generate HTML comparison view")
    
    # responsive command
    responsive_parser = subparsers.add_parser("responsive", help="Test responsive breakpoints")
    responsive_parser.add_argument("url", help="URL to capture")
    responsive_parser.add_argument("--widths", "-w", type=int, nargs="+", default=[375, 768, 1024, 1440],
                                  help="Breakpoint widths to test")
    responsive_parser.add_argument("--output-dir", "-o", default="./responsive", help="Output directory")
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_devices()
    
    elif args.command == "emulate":
        print(f"Emulating {args.device} at {args.url}...")
        path = emulate_device_sync(args.url, args.device, args.output, args.orientation, 
                                   args.network, not args.no_full_page, args.wait)
        print(f"Screenshot saved: {path}")
    
    elif args.command == "rotate":
        print(f"Rotating {args.device} to {args.orientation}...")
        path = rotate_screenshot(args.url, args.device, args.orientation, args.output)
        print(f"Screenshot saved: {path}")
    
    elif args.command == "throttle":
        print(f"Simulating {args.profile} network on {args.device}...")
        path = throttle_network(args.url, args.device, args.profile, args.output)
        print(f"Screenshot saved: {path}")
    
    elif args.command == "compare":
        print(f"Comparing devices for {args.url}...")
        screenshots = compare_devices(args.url, args.devices, args.output_dir)
        print(f"\nCaptured {len(screenshots)} screenshots")
        if args.html:
            create_comparison_html(args.url, screenshots, args.devices, 
                                 f"{args.output_dir}/comparison.html")
    
    elif args.command == "responsive":
        print(f"Testing responsive breakpoints for {args.url}...")
        screenshots = test_responsive(args.url, args.widths, args.output_dir)
        print(f"\nCaptured {len(screenshots)} breakpoints")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
