# CloakBrowser Pro - Fingerprint Injector
# 指纹注入引擎：通过 CDP DevTools Protocol 配置浏览器指纹
# 使用方式: python fingerprint_injector.py --profile amazon-seller --ws ws://localhost:9222

import json, sys, argparse, time
from pathlib import Path

class FingerprintInjector:
    def __init__(self, ws_url=None):
        self.ws_url = ws_url
        self.profiles_dir = Path(__file__).parent / "profiles"
    
    def load_profile(self, name):
        path = self.profiles_dir / f"{name}.json"
        if not path.exists():
            print(f"[ERROR] Profile '{name}' not found at {path}")
            print(f"Available profiles: {[p.stem for p in self.profiles_dir.glob('*.json')]}")
            sys.exit(1)
        with open(path) as f:
            return json.load(f)
    
    def inject(self, profile):
        """Print CDP commands to configure fingerprint"""
        print(f"\n{'='*50}")
        print(f"[PRO] Applying profile: {profile.get('name', 'unknown')}")
        print(f"{'='*50}")
        
        cdp = profile.get("cdp_commands", {})
        
        # WebGL vendor/renderer
        if "webgl" in cdp:
            print(f"\n[CDP] WebGL override:")
            print(f"  Page.addScriptToEvaluateOnNewDocument:")
            print(f"    WebGL vendor: {cdp['webgl'].get('vendor')}")
            print(f"    WebGL renderer: {cdp['webgl'].get('renderer')}")
        
        # Navigator overrides
        if "navigator" in cdp:
            print(f"\n[CDP] Navigator override:")
            for k, v in cdp["navigator"].items():
                print(f"  navigator.{k} = {v}")
        
        # Timezone
        if "timezone" in cdp:
            print(f"\n[CDP] Timezone: {cdp['timezone']}")
            print(f"  Emulation.setTimezoneOverride: {cdp['timezone']}")
        
        # Geolocation
        if "geolocation" in cdp:
            geo = cdp["geolocation"]
            print(f"\n[CDP] Geolocation: {geo['latitude']}, {geo['longitude']}")
            print(f"  Emulation.setGeolocationOverride")
        
        # User-Agent
        if "user_agent" in cdp:
            print(f"\n[CDP] User-Agent: {cdp['user_agent']}")
            print(f"  Network.setUserAgentOverride")
        
        # Screen
        if "screen" in cdp:
            s = cdp["screen"]
            print(f"\n[CDP] Screen: {s['width']}x{s['height']}")
            print(f"  Emulation.setDeviceMetricsOverride")
        
        # Languages
        if "languages" in cdp:
            print(f"\n[CDP] Languages: {cdp['languages']}")
        
        # Audio
        if "audio" in cdp:
            print(f"\n[CDP] AudioContext: {cdp['audio']}")
        
        print(f"\n{'='*50}")
        print(f"[PRO] To apply: connect via CDP ws://localhost:9222")
        print(f"[PRO] Run: python fingerprint_injector.py --apply --profile {profile.get('id','unknown')} --ws ws://localhost:9222")
        print(f"{'='*50}")
    
    def apply(self, profile_name, ws_url):
        """Actually connect to CloakBrowser via CDP and apply fingerprint"""
        try:
            import websockets
            import asyncio
        except ImportError:
            print("[ERROR] Need websockets: pip install websockets")
            sys.exit(1)
        
        profile = self.load_profile(profile_name)
        cdp = profile.get("cdp_commands", {})
        
        async def do_apply():
            async with websockets.connect(ws_url) as ws:
                # Get page targets
                await ws.send(json.dumps({"id": 1, "method": "Target.getTargets"}))
                result = await ws.recv()
                targets = json.loads(result)
                
                # Apply overrides
                cmds = []
                
                if "user_agent" in cdp:
                    cmds.append({
                        "id": 2, "method": "Network.setUserAgentOverride",
                        "params": {"userAgent": cdp["user_agent"]}
                    })
                
                if "timezone" in cdp:
                    cmds.append({
                        "id": 3, "method": "Emulation.setTimezoneOverride",
                        "params": {"timezoneId": cdp["timezone"]}
                    })
                
                if "geolocation" in cdp:
                    cmds.append({
                        "id": 4, "method": "Emulation.setGeolocationOverride",
                        "params": cdp["geolocation"]
                    })
                
                if "screen" in cdp:
                    cmds.append({
                        "id": 5, "method": "Emulation.setDeviceMetricsOverride",
                        "params": {
                            "width": cdp["screen"]["width"],
                            "height": cdp["screen"]["height"],
                            "deviceScaleFactor": cdp["screen"].get("scale", 1),
                            "mobile": False
                        }
                    })
                
                for cmd in cmds:
                    await ws.send(json.dumps(cmd))
                    resp = await ws.recv()
                
                print(f"[PRO] Applied {len(cmds)} CDP commands for profile: {profile_name}")
        
        asyncio.run(do_apply())

    def list_profiles(self):
        profiles = sorted(self.profiles_dir.glob("*.json"))
        print(f"\nAvailable profiles ({len(profiles)}):")
        for p in profiles:
            with open(p) as f:
                data = json.load(f)
            print(f"  [{data.get('id','?')}] {data.get('name','?')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CloakBrowser Pro Fingerprint Injector")
    parser.add_argument("--profile", help="Profile name")
    parser.add_argument("--ws", default="ws://localhost:9222", help="CloakBrowser CDP URL")
    parser.add_argument("--list", action="store_true", help="List profiles")
    parser.add_argument("--apply", action="store_true", help="Actually apply via CDP")
    
    args = parser.parse_args()
    
    injector = FingerprintInjector()
    
    if args.list:
        injector.list_profiles()
    elif args.profile and args.apply:
        injector.apply(args.profile, args.ws)
    elif args.profile:
        profile = injector.load_profile(args.profile)
        injector.inject(profile)
    else:
        parser.print_help()
