import os
import sys
import pkg_resources
from app.core.config import settings

def check_dependencies():
    print("--- Production Readiness Audit ---")
    required = [
        "fastapi", "uvicorn", "ortools", "networkx", 
        "sqlalchemy", "redis", "cryptography", "python-dotenv", 
        "pydantic-settings", "sentence-transformers", "transformers", "torch", "playwright"
    ]
    missing = []
    for pkg in required:
        try:
            pkg_resources.require(pkg)
        except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
            missing.append(pkg)
    
    if missing:
        print(f"❌ Missing Dependencies: {missing}")
        return False
    print("✅ All dependencies installed.")
    return True

def check_env_vars():
    required_vars = [
        "OPENWEATHERMAP_API_KEY", "GOOGLE_MAPS_API_KEY", 
        "FOURSQUARE_API_KEY", "ANTHROPIC_API_KEY"
    ]
    missing_vars = [v for v in required_vars if not os.getenv(v)]
    if missing_vars:
        print(f"⚠️  Missing API Keys in .env: {missing_vars}")
        print("Note: System will run in 'Mock Mode' until these are provided.")
    else:
        print("✅ All production API keys present.")
    return True

def main():
    dep_ok = check_dependencies()
    env_ok = check_env_vars()
    
    if dep_ok and env_ok:
        print("\n🚀 SYSTEM READY FOR PRODUCTION RUN")
    else:
        print("\n⚠️  System is partially ready. Please check the logs above.")

if __name__ == "__main__":
    main()
